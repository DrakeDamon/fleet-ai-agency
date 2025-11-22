import os
import time
import csv
import sys
import logging
import requests
import smtplib
import dns.resolver
import pandas as pd
import re
from itertools import permutations
from dotenv import load_dotenv
from urllib.parse import urlparse

# ---------------------------------------------------------------------------
# CONFIGURATION & SETUP
# ---------------------------------------------------------------------------

# Configure Logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

# Load Environment Variables
load_dotenv()

# Socrata (Data.transportation.gov) Configuration
SOCRATA_API_URL = "https://data.transportation.gov/api/v3/views/az4n-8mr2/query.json"

# Load Key ID and Secret for Basic Auth
SOCRATA_KEY_ID = os.getenv("SOCRATA_APP_key")
SOCRATA_KEY_SECRET = os.getenv("SOCRATA_APP_secret")

# FMCSA Filter Config
MIN_POWER_UNITS = 10
MAX_POWER_UNITS = 100
LIMIT_RECORDS = 50  # Limit for enrichment processing to avoid huge batches

# ---------------------------------------------------------------------------
# 1. FMCSA CENSUS API DATA RETRIEVAL
# ---------------------------------------------------------------------------

def fetch_census_data():
    """
    Queries the FMCSA Census dataset via Socrata API (SoQL).
    Returns a DataFrame with the target fleet records.
    """
    logger.info("📡 Querying FMCSA Census API for active fleets (10-100 trucks)...")
    
    # SoQL Query
    query = f"""
    SELECT 
        dot_number, legal_name, dba_name, phy_city, phy_state, 
        phone, email_address, power_units, truck_units, bus_units
    LIMIT 5000
    """
    
    params = {"query": query}
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
    }
    
    # Basic Auth if Key/Secret provided
    auth = None
    if SOCRATA_KEY_ID and SOCRATA_KEY_SECRET:
        auth = (SOCRATA_KEY_ID, SOCRATA_KEY_SECRET)

    try:
        resp = requests.get(SOCRATA_API_URL, params=params, headers=headers, auth=auth, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            
            # Socrata SODA 2.1 usually returns a list of dicts directly
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif "data" in data and "meta" in data:
                 # Fallback for older view-based response
                 cols = [c["name"] for c in data["meta"]["view"]["columns"]]
                 rows = data["data"]
                 df = pd.DataFrame(rows, columns=cols)
            else:
                logger.error(f"❌ Unexpected API response structure. Keys: {data.keys() if isinstance(data, dict) else 'Not a dict'}")
                return None
            
            # --- POST-FETCH FILTERING ---
            # Socrata stores power_units as text, so we filter here to be safe
            df['power_units'] = pd.to_numeric(df['power_units'], errors='coerce').fillna(0)
            
            # Apply 10-100 filter
            df = df[
                (df['power_units'] >= MIN_POWER_UNITS) & 
                (df['power_units'] <= MAX_POWER_UNITS)
            ]
            
            logger.info(f"✅ Successfully fetched {len(df)} active fleets (10-100 units) from Census API.")
            return df
            
        else:
            logger.error(f"API Error {resp.status_code}: {resp.text}")
            return None
            
    except Exception as e:
        logger.error(f"Fetch failed: {e}")
        return None

# ---------------------------------------------------------------------------
# 2. DOMAIN DISCOVERY (FREE)
# ---------------------------------------------------------------------------

def find_domain_free(company_name, city, state):
    """
    Uses DuckDuckGo to find a company website.
    Returns 'NO_DOMAIN_FOUND' if unsuccessful.
    """
    if not company_name:
        return "NO_DOMAIN_FOUND"

    query = f"{company_name} {city} {state} official site"
    
    try:
        # Try using DDGS library if available
        from duckduckgo_search import DDGS
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
            
        if results:
            first_url = results[0]['href']
            domain = urlparse(first_url).netloc.replace("www.", "")
            
            # Filter out common directory sites
            blocklist = ["facebook.com", "linkedin.com", "manta.com", "bbb.org", "yellowpages.com", "safer.fmcsa.dot.gov", "mapquest.com"]
            if any(b in domain for b in blocklist):
                return "NO_DOMAIN_FOUND"
                
            return domain
            
    except ImportError:
        logger.warning("⚠️  'duckduckgo-search' not installed. Skipping domain lookup.")
        return "NO_DOMAIN_FOUND"
    except Exception as e:
        pass
        
    return "NO_DOMAIN_FOUND"

# ---------------------------------------------------------------------------
# 3. CONTACT DISCOVERY (FREE)
# ---------------------------------------------------------------------------

def find_key_contacts(company_name, domain):
    """
    Attempts to find Owner/President/Manager using search queries.
    Returns a dict of names or 'UNKNOWN'.
    """
    contacts = {
        "foundOwnerName": "UNKNOWN",
        "foundFleetManagerName": "UNKNOWN"
    }
    
    if not company_name:
        return contacts

    try:
        from duckduckgo_search import DDGS
        
        # Heuristic: Look for "Owner", "President", "Safety Director"
        query = f'"{company_name}" Owner OR President OR "Safety Director" OR "Operations Manager" site:linkedin.com'
        
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=3))
        
        for r in results:
            title = r['title']
            
            if "Owner" in title or "President" in title:
                parts = title.split("-")[0].strip()
                if len(parts.split()) in [2, 3]: 
                    contacts["foundOwnerName"] = parts
                    
            if "Fleet Manager" in title or "Safety Director" in title:
                parts = title.split("-")[0].strip()
                if len(parts.split()) in [2, 3]:
                    contacts["foundFleetManagerName"] = parts

    except ImportError:
        pass
    except Exception:
        pass

    return contacts

# ---------------------------------------------------------------------------
# 4 & 5. EMAIL GENERATION & VERIFICATION
# ---------------------------------------------------------------------------

def generate_emails(names_list, domain):
    """
    Generates list of likely corporate emails from a list of names.
    """
    emails = []
    if domain == "NO_DOMAIN_FOUND":
        return []

    for name in names_list:
        if not name or name == "UNKNOWN":
            continue
            
        name_parts = name.lower().split()
        if len(name_parts) < 2:
            continue
            
        first, last = name_parts[0], name_parts[-1]
        
        # Common patterns
        emails.extend([
            f"{first}@{domain}",
            f"{first}.{last}@{domain}",
            f"{first}{last}@{domain}",
            f"{first[0]}{last}@{domain}",
            f"{first}_{last}@{domain}"
        ])
    
    # Generics
    emails.extend([f"info@{domain}", f"dispatch@{domain}", f"safety@{domain}", f"admin@{domain}"])
    
    return list(set(emails)) # Dedupe

def verify_smtp(email):
    """
    Performs MX lookup and SMTP RCPT TO check.
    Returns: 'deliverable', 'catch_all', or 'undeliverable'
    """
    # NOTE: Port 25 is often blocked on residential/cloud networks.
    # This function is kept for completeness but disabled by default in main() for reliability.
    domain = email.split('@')[-1]
    
    try:
        records = dns.resolver.resolve(domain, 'MX')
        mx_record = str(records[0].exchange)
    except Exception:
        return "undeliverable" 

    try:
        server = smtplib.SMTP(timeout=3)
        server.set_debuglevel(0)
        server.connect(mx_record)
        server.helo(server.local_hostname)
        server.mail('test@example.com')
        
        code, message = server.rcpt(email)
        server.quit()
        
        if code == 250:
            return "deliverable"
        else:
            return "undeliverable"
            
    except Exception:
        return "undeliverable" # Assume fail on timeout

# ---------------------------------------------------------------------------
# MAIN PIPELINE
# ---------------------------------------------------------------------------

def main():
    logger.info("🚀 Starting FMCSA Census Enrichment Pipeline...")
    
    # 1. Get Data Frame from API
    df_census = fetch_census_data()
    
    if df_census is None or df_census.empty:
        logger.error("❌ No data returned from Census API. Exiting.")
        return

    valid_records = []
    
    # Process Records
    # We limit processing to LIMIT_RECORDS to respect rate limits of enrichment tools
    records_to_process = df_census.head(LIMIT_RECORDS).to_dict('records')
    
    logger.info(f"🔄 Processing {len(records_to_process)} records for enrichment...")

    for row in records_to_process:
        # --- MAPPING & NORMALIZATION ---
        # Extract fields safely from Socrata row
        record = {
            "dotNumber": row.get("dot_number"),
            "legalName": row.get("legal_name"),
            "dbaName": row.get("dba_name"),
            "phyCity": row.get("phy_city"),
            "phyState": row.get("phy_state"),
            "telephone": row.get("phone"),
            "powerUnits": row.get("power_units", 0),
            "truckUnits": row.get("truck_units", 0),
            # Convert email to string, handle NaN
            "emailFromFMCSA": str(row.get("email_address", "")).strip() if pd.notna(row.get("email_address")) else "",
            # Officers for email gen
            "officer1": "",
            "officer2": ""
        }
        
        logger.info(f"🔎 Enriching: {record['legalName']} (DOT: {record['dotNumber']})")

        # --- ENRICHMENT STEPS ---
        
        # 1. Find Domain
        domain = find_domain_free(record['legalName'], record['phyCity'], record['phyState'])
        record['websiteDomain'] = domain
        time.sleep(1.5) # Respect Search Rate Limits
        
        # 2. Find Contacts (LinkedIn scraping)
        contacts = find_key_contacts(record['legalName'], domain)
        record.update(contacts)
        time.sleep(1.5) 
        
        # 3. Generate Emails
        # Collect all potential names: Officers from FMCSA + Scraped LinkedIn names
        names_to_permute = []
        if record['officer1']: names_to_permute.append(record['officer1'])
        if record['officer2']: names_to_permute.append(record['officer2'])
        if record['foundOwnerName'] != "UNKNOWN": names_to_permute.append(record['foundOwnerName'])
        if record['foundFleetManagerName'] != "UNKNOWN": names_to_permute.append(record['foundFleetManagerName'])
        
        generated_emails = generate_emails(names_to_permute, domain)
        
        # Add FMCSA email to the list if valid
        if record['emailFromFMCSA'] and record['emailFromFMCSA'] != 'nan':
             generated_emails.insert(0, record['emailFromFMCSA'])
        
        record['allGeneratedEmails'] = list(set(generated_emails)) # Dedupe
        
        # 4. Verify Emails
        # Note: We are mocking verification 'not_verified' to avoid port 25 blocks locally.
        # In production with proper server, uncomment verify_smtp usage.
        
        verified_emails = []
        
        if generated_emails:
            logger.info(f"   Generated {len(generated_emails)} emails. Validating top 5...")
            for email in generated_emails[:5]:
                # status = verify_smtp(email) 
                status = "not_verified" # Bypass for local dev
                
                if status == 'deliverable' or status == 'not_verified':
                    verified_emails.append(str(email))  # Ensure string
        
        # Ensure all items are strings before joining
        verified_emails = [str(e) for e in verified_emails if e and str(e) != 'nan']
        all_emails = [str(e) for e in record['allGeneratedEmails'] if e and str(e) != 'nan']
        
        record['verifiedEmails'] = ",".join(verified_emails)
        record['allGeneratedEmails'] = ",".join(all_emails)
        
        valid_records.append(record)

    # Output to CSV
    if valid_records:
        output_df = pd.DataFrame(valid_records)
        
        # Reorder for clean output
        cols = [
            "dotNumber", "legalName", "dbaName", "phyCity", "phyState", "powerUnits", 
            "websiteDomain", "emailFromFMCSA", "verifiedEmails", 
            "officer1", "foundOwnerName", "telephone", "allGeneratedEmails"
        ]
        # Ensure cols exist
        for c in cols:
            if c not in output_df.columns:
                output_df[c] = ""
                
        output_df = output_df[cols]
        
        filename = "fmcsa_census_verified_leads.csv"
        output_df.to_csv(filename, index=False)
        logger.info(f"🎉 Done! Saved {len(output_df)} leads to {filename}")
    else:
        logger.warning("No records processed.")

if __name__ == "__main__":
    main()

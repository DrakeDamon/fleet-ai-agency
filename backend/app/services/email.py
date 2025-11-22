import httpx
import json
import os
import time
from sqlmodel import Session, select
from app.models import Lead
from app.config import settings

# Hunter.io Cache File
HUNTER_CACHE_FILE = "hunter_cache.json"

# ---------------------------------------------------------------------------
# HUNTER.IO HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def load_hunter_cache():
    if os.path.exists(HUNTER_CACHE_FILE):
        try:
            with open(HUNTER_CACHE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Failed to load Hunter cache: {e}")
    return {}

def save_hunter_cache(cache):
    try:
        with open(HUNTER_CACHE_FILE, 'w') as f:
            json.dump(cache, f, indent=2)
    except Exception as e:
        print(f"Failed to save Hunter cache: {e}")

def hunter_domain_search(domain, cache):
    """
    Search for emails associated with a domain using Hunter.io.
    Returns domain search data including primary email and pattern.
    """
    if not settings.HUNTER_API_KEY or not domain or domain == "NO_DOMAIN_FOUND":
        return None
    
    cache_key = f"domain:{domain}"
    if cache_key in cache:
        return cache[cache_key]
    
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={settings.HUNTER_API_KEY}"
    try:
        import requests
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            cache[cache_key] = data
            save_hunter_cache(cache)
            time.sleep(0.5)  # Rate limit niceness
            return data
    except Exception as e:
        print(f"Hunter Domain Search error: {e}")
    
    return None

def hunter_verify_email(email, cache):
    """
    Verify an email address using Hunter.io.
    Handles 202 (Processing) status with retries.
    Filters out gibberish and disposable emails.
    """
    if not settings.HUNTER_API_KEY or not email:
        return None
        
    cache_key = f"email:{email}"
    if cache_key in cache:
        return cache[cache_key]
        
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.HUNTER_API_KEY}"
    
    # Retry loop for 202 status (Processing)
    max_retries = 5
    for attempt in range(max_retries):
        try:
            import requests
            resp = requests.get(url, timeout=20)
            
            if resp.status_code == 200:
                data = resp.json()
                cache[cache_key] = data
                save_hunter_cache(cache)
                time.sleep(0.5)
                return data
            elif resp.status_code == 202:
                # Verification in progress, wait and retry
                print(f"⏳ Verification for {email} in progress (202). Retrying {attempt+1}/{max_retries}...")
                time.sleep(2)  # Wait before polling
                continue
            else:
                return None
                
        except Exception as e:
            print(f"Hunter Verify error: {e}")
            return None
            
    return None

# ---------------------------------------------------------------------------
# BACKGROUND TASKS
# ---------------------------------------------------------------------------

async def verify_email_background(lead_id: int, email: str, session: Session):
    """
    Background task to verify email using Hunter.io and update the DB.
    """
    if not settings.HUNTER_API_KEY:
        print(f"Skipping verification for {email}: No API Key found.")
        return

    # Load cache
    cache = load_hunter_cache()
    
    # Verify email
    result = hunter_verify_email(email, cache)
    
    if result:
        # Extract verification status
        verification_data = result.get("data", {})
        result_status = verification_data.get("result")  # valid, invalid, accept_all, unknown
        
        # Check for quality flags
        is_gibberish = verification_data.get("gibberish", False)
        is_disposable = verification_data.get("disposable", False)
        
        # Filter out low-quality emails
        if is_gibberish or is_disposable:
            result_status = "invalid"
        
        # Update DB
        lead = session.get(Lead, lead_id)
        if lead:
            lead.verified_status = result_status
            session.add(lead)
            session.commit()
            print(f"Verified {email}: {result_status}")
    else:
        print(f"Could not verify {email}")

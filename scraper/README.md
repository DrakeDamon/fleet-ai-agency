# FMCSA Lead Generator

Automated pipeline to discover and enrich FMCSA carrier data with domains, contacts, and email addresses.

## Overview

This script:
1. **Queries FMCSA Census API** (via Socrata) for active fleets (10-100 power units)
2. **Finds company domains** using DuckDuckGo search
3. **Discovers key contacts** (Owner, Safety Director, Operations Manager) via LinkedIn search
4. **Generates email permutations** based on common patterns
5. **Exports enriched leads** to CSV

## Setup

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure Environment:**
   Create a `.env` file in the scraper directory:
   ```
   SOCRATA_APP_key=your_key_here
   SOCRATA_APP_secret=your_secret_here
   ```

3. **Run:**
   ```bash
   python fmcsa_lead_generator.py
   ```

## Output

Creates `fmcsa_census_verified_leads.csv` with columns:
- `dotNumber` - USDOT number
- `legalName` - Company legal name
- `websiteDomain` - Discovered domain
- `verifiedEmails` - Generated email addresses
- `foundOwnerName` - LinkedIn-discovered owner name
- And more...

## Notes

- Email verification is currently disabled (marked "not_verified") to avoid port 25 blocks locally
- For production, use external verification services (NeverBounce, MailTester, etc.)
- Rate limiting is built-in (1.5s delays between searches)


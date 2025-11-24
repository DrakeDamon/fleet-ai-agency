import os
import resend

# Initialize Resend
# Initialize Resend
# Initialize Resend
api_key = os.environ.get("RESEND_API_KEY") or os.environ.get("RESEND_API")
if api_key:
    resend.api_key = api_key.strip()
    print(f"📧 Resend API Key Loaded: {resend.api_key[:5]}...{resend.api_key[-4:]}")
else:
    print("❌ Resend API Key NOT FOUND in environment variables.")

def send_report_email(to_email: str, first_name: str, pdf_bytes: bytes, dot_number: str):
    """
    Sends the Risk Snapshot PDF via email.
    """
    try:
        # Convert bytes to list of integers for Resend attachment if needed, 
        # but the python SDK usually handles bytes or we might need to encode.
        # Checking resend docs pattern, usually attachments are list of dicts.
        # For simple bytes, we might need to convert to list of ints or base64.
        # However, the user request just said "Pass pdf_bytes". 
        # The Resend Python SDK expects 'content' as a list of integers for buffers.
        
        attachment_content = list(pdf_bytes)
        
        params = {
            "from": f"Fleet Clarity Audit Team <{os.environ.get('SENDER_EMAIL', 'audit@fleetclarity.io')}>",
            "to": [to_email],
            "subject": f"Your Fleet Data Snapshot (DOT #{dot_number})",
            "html": f"""
                <p>Hi {first_name},</p>
                <p>Your risk analysis is attached. We detected critical flags.</p>
                <p>Please review the financial projections immediately.</p>
                <br>
                <p>Best,</p>
                <p>Fleet AI Agency</p>
            """,
            "attachments": [
                {
                    "filename": f"Risk_Report_{dot_number}.pdf",
                    "content": attachment_content
                }
            ]
        }
        
        email = resend.Emails.send(params)
        print(f"Email sent to {to_email}: {email}")
        return email
        
    except Exception as e:
        print(f"Failed to send email: {e}")
        return None

def subscribe_to_newsletter(email: str, first_name: str, last_name: str = ""):
    """
    Adds the lead to the marketing list.
    """
    audience_id = os.environ.get("RESEND_AUDIENCE_ID")
    if not audience_id:
        print("RESEND_AUDIENCE_ID not set, skipping subscription.")
        return

    try:
        params = {
            "email": email,
            "first_name": first_name,
            "last_name": last_name,
            "unsubscribed": False,
            "audience_id": audience_id,
        }
        
        contact = resend.Contacts.create(params)
        print(f"Subscribed {email}: {contact}")
        return contact
        
    except Exception as e:
        print(f"Failed to subscribe contact: {e}")
        return None

# ---------------------------------------------------------------------------
# EMAIL VERIFICATION (Hunter.io) - LEGACY FUNCTION
# ---------------------------------------------------------------------------

import httpx
import json
import time
from sqlmodel import Session
from app.models import Lead
from app.config import settings

# Hunter.io Cache File
HUNTER_CACHE_FILE = "hunter_cache.json"

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

def hunter_verify_email(email, cache):
    """
    Verify an email address using Hunter.io.
    """
    if not settings.HUNTER_API_KEY or not email:
        return None
        
    cache_key = f"email:{email}"
    if cache_key in cache:
        return cache[cache_key]
        
    url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={settings.HUNTER_API_KEY}"
    
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
                print(f"⏳ Verification for {email} in progress (202). Retrying {attempt+1}/{max_retries}...")
                time.sleep(2)
                continue
            else:
                return None
                
        except Exception as e:
            print(f"Hunter Verify error: {e}")
            return None
            
    return None

async def verify_email_background(lead_id: int, email: str, session: Session):
    """
    Background task to verify email using Hunter.io and update the DB.
    """
    if not settings.HUNTER_API_KEY:
        print(f"Skipping verification for {email}: No API Key found.")
        return

    cache = load_hunter_cache()
    result = hunter_verify_email(email, cache)
    
    if result:
        verification_data = result.get("data", {})
        result_status = verification_data.get("result")
        
        is_gibberish = verification_data.get("gibberish", False)
        is_disposable = verification_data.get("disposable", False)
        
        if is_gibberish or is_disposable:
            result_status = "invalid"
        
        lead = session.get(Lead, lead_id)
        if lead:
            lead.verified_status = result_status
            session.add(lead)
            session.commit()
            print(f"Verified {email}: {result_status}")
    else:
        print(f"Could not verify {email}")


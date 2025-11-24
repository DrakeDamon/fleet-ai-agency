import os
import resend
import httpx
import json
import time
from sqlmodel import Session
from app.models import Lead
from app.config import settings

# --- CONFIGURATION ---
# Initialize Resend API Key
api_key = os.environ.get("RESEND_API")
if api_key:
    resend.api_key = api_key.strip()
else:
    print("❌ Resend API Key (RESEND_API) NOT FOUND in environment variables.")

# Official Calendly Link (from environment variable)
# Official Calendly Link (from environment variable)
CALENDLY_URL = os.environ.get("CALENDLY_URL")


def send_report_email(to_email: str, first_name: str, pdf_bytes: bytes, dot_number: str):
    """
    Sends the Risk Snapshot PDF via email with the 'Forward to Boss' conversion script.
    """
    try:
        # Convert bytes to list of integers for Resend API
        attachment_content = list(pdf_bytes)
        
        # 1. Sender Identity (Use your verified alias)
        sender_email = os.environ.get("SENDER_EMAIL")
        from_address = f"Fleet Clarity Audit Team <{sender_email}>"

        # 2. The High-Conversion HTML Body
        # Includes 'Strategic Recommendation' box and Backup Calendly Link
        html_content = f"""
        <div style="font-family: sans-serif; color: #333; line-height: 1.6;">
            <p>Hi {first_name},</p>
            
            <p>Your <strong>Data Risk Snapshot</strong> (DOT #{dot_number}) is attached below.</p>
            
            <div style="background-color: #fef2f2; border-left: 4px solid #ef4444; padding: 15px; margin: 20px 0;">
                <p style="margin: 0; font-weight: bold; color: #991b1b;">STRATEGIC RECOMMENDATION:</p>
                <p style="margin: 5px 0 0 0; color: #7f1d1d;">
                    Forward this PDF to your Owner or Safety Director immediately. 
                    The financial projections on Page 2 are critical for Q4 budget planning.
                </p>
            </div>

            <p><em>(Copy/Paste this text when forwarding):</em></p>
            <p style="font-style: italic; color: #555; border: 1px dashed #ccc; padding: 10px; background-color: #f9fafb;">
                "Boss, I found a compliance tool that flagged our OOS rate. 
                Take a look at Page 2—we might be overpaying on insurance due to these specific violations."
            </p>
            
            <br>
            <p>If you want to review these findings with a Senior Analyst, I have kept a slot open:</p>
            <p>
                <a href="{CALENDLY_URL}" style="background-color: #0F172A; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">
                    Book Priority Review &raquo;
                </a>
            </p>

            <br>
            <p>Best,<br><strong>The Fleet Clarity Team</strong></p>
        </div>
        """

        params = {
            "from": from_address,
            "to": [to_email],
            # "Fear of Loss" Subject Line (High Open Rate)
            "subject": f"ACTION REQUIRED: Your Fleet Risk Snapshot (DOT #{dot_number})",
            "html": html_content,
            "attachments": [
                {
                    "filename": f"Risk_Snapshot_{dot_number}.pdf",
                    "content": attachment_content
                }
            ]
        }
        
        email_resp = resend.Emails.send(params)
        print(f"✅ Email sent to {to_email}: {email_resp}")
        return email_resp
        
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
        return None


def subscribe_to_newsletter(email: str, first_name: str, last_name: str = ""):
    """
    Adds the lead to the Resend 'Leads' Audience for the Nurture Sequence.
    """
    audience_id = os.environ.get("RESEND_AUDIENCE_ID")
    if not audience_id:
        print("⚠️ RESEND_AUDIENCE_ID not set. Skipping subscription.")
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
        print(f"✅ Subscribed {email} to Audience")
        return contact
        
    except Exception as e:
        print(f"❌ Failed to subscribe contact: {e}")
        return None


# ---------------------------------------------------------------------------
# EMAIL VERIFICATION (Hunter.io) - LEGACY / OPTIONAL
# ---------------------------------------------------------------------------
# Kept for future verification needs if you buy a Hunter subscription later.

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
    if not settings.HUNTER_API_KEY or not email:
        return None
    cache_key = f"email:{email}"
    if cache_key in cache:
        return cache[cache_key]
    
    # Logic preserved but inactive unless API Key is present
    return None
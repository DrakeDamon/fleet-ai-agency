import os
import resend

# Initialize Resend
resend.api_key = os.environ.get("RESEND_API_KEY")

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
            "from": "Fleet AI Agency <onboarding@resend.dev>", # Replace with verified domain in prod
            "to": [to_email],
            "subject": f"URGENT: Your Fleet Risk Snapshot (DOT #{dot_number})",
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

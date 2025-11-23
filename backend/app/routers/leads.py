from fastapi import APIRouter, Depends, BackgroundTasks, Request
from sqlmodel import Session
from app.db import get_session
from app.models import Lead, LeadCreate, LeadRead, FleetData
from app.services import verify_email_background
from app.limiter import limiter

from app.services.fmcsa import fetch_carrier_risk

router = APIRouter(prefix="/api/v1/leads", tags=["Leads"])

@router.get("/audit/preview/{dot_number}")
@limiter.limit("5/minute")
async def get_audit_preview(
    request: Request,
    dot_number: str,
):
    """
    Step 1 of the Funnel: Takes DOT#, returns the 'Teaser' Risk Score.
    """
    data = await fetch_carrier_risk(dot_number)
    return data

@router.post("/", response_model=LeadRead)
@limiter.limit("5/minute") # SECURITY: Max 5 leads per IP per minute
async def create_lead(
    request: Request, 
    lead: LeadCreate, 
    session: Session = Depends(get_session),
    background_tasks: BackgroundTasks = None
):
    # 1. Create DB Object
    db_lead = Lead.from_orm(lead)
    
    # 2. THE BRAIN: Cross-Reference FMCSA Data
    if db_lead.dot_number:
        clean_dot = db_lead.dot_number.strip()
        fleet_data = session.get(FleetData, clean_dot)
        
        if fleet_data:
            units = fleet_data.total_power_units
            # Grading Logic
            if 10 <= units <= 100:
                db_lead.qualification_status = f"Qualified ({units} Units)"
            elif units > 100:
                db_lead.qualification_status = f"Enterprise ({units} Units)"
            else:
                db_lead.qualification_status = f"Too Small ({units} Units)"
        else:
            db_lead.qualification_status = "Unknown DOT"
            
    # 3. Save to DB
    session.add(db_lead)
    session.commit()
    session.refresh(db_lead)
    
    # 4. Automation (Enrichment + PDF + Email)
    background_tasks.add_task(handle_lead_automation, db_lead, session)
    
    return db_lead

async def handle_lead_automation(lead: Lead, session: Session):
    """
    Background task to handle all post-submission logic:
    1. Verify Email (Hunter.io)
    2. Fetch Risk Data
    3. Generate PDF
    4. Send Email
    5. Subscribe to Newsletter
    """
    # 1. Enrichment
    await verify_email_background(lead.id, lead.work_email, session)
    
    # 2. PDF & Email Fulfillment
    if lead.dot_number:
        try:
            print(f"🚀 Starting Automation for Lead {lead.id} (DOT: {lead.dot_number})")
            
            # Re-fetch fresh data for the PDF (Async)
            print("   - Fetching FMCSA data...")
            fmcsa_data = await fetch_carrier_risk(lead.dot_number)
            
            # Generate PDF (Sync)
            print("   - Generating PDF...")
            from app.services.pdf import generate_risk_report
            from app.services.email import send_report_email, subscribe_to_newsletter
            
            pdf_bytes = generate_risk_report(lead, fmcsa_data)
            print(f"   - PDF Generated ({len(pdf_bytes)} bytes)")
            
            # Extract Name for Personalization
            name_parts = lead.full_name.split(" ")
            first_name = name_parts[0]
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
            
            # Send Email (Sync)
            print(f"   - Sending Email to {lead.work_email}...")
            email_result = send_report_email(lead.work_email, first_name, pdf_bytes, lead.dot_number)
            if email_result:
                print(f"   ✅ Email Sent! ID: {email_result.get('id')}")
            else:
                print("   ❌ Email Failed to Send (Check Resend Logs)")
            
            # Subscribe (Sync)
            print(f"   - Subscribing to Newsletter...")
            sub_result = subscribe_to_newsletter(lead.work_email, first_name, last_name)
            if sub_result:
                print(f"   ✅ Subscribed! ID: {sub_result.get('id')}")
            else:
                print("   ⚠️ Subscription Failed (Check Resend Logs)")
            
        except Exception as e:
            print(f"❌ Automation Error for Lead {lead.id}: {e}")
            import traceback
            traceback.print_exc()

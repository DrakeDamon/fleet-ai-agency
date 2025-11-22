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
    
    # 4. Enrichment (Hunter.io)
    background_tasks.add_task(verify_email_background, db_lead.id, db_lead.work_email, session)
    
    return db_lead

import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Header, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from app.db import get_session
from app.models import Lead, FleetData
from app.config import settings

router = APIRouter(prefix="/api/v1/admin", tags=["Admin"])

def verify_admin_token(x_admin_token: str = Header(...)):
    if x_admin_token != settings.ADMIN_SECRET:
        raise HTTPException(status_code=401, detail="Invalid Admin Token")

# --- SMARTLEAD EXPORT ---
@router.get("/export_csv")
def export_leads(
    token: str = Depends(verify_admin_token),
    session: Session = Depends(get_session)
):
    leads = session.exec(select(Lead)).all()
    
    stream = io.StringIO()
    csv_writer = csv.writer(stream)
    
    # Headers formatted for SmartLead Import
    headers = [
        "Email", "FirstName", "LastName", "CompanyName", "Website", 
        "Phone", "CustomField:FleetSize", "CustomField:Role", 
        "CustomField:PainPoints", "CustomField:Qualified", "Date"
    ]
    csv_writer.writerow(headers)
    
    for lead in leads:
        # Split Name safely
        names = lead.full_name.split(" ", 1)
        first_name = names[0]
        last_name = names[1] if len(names) > 1 else ""
        
        csv_writer.writerow([
            lead.work_email,
            first_name,
            last_name,
            lead.company_name,
            "", # Website placeholder
            lead.phone or "",
            lead.fleet_size,
            lead.role,
            lead.pain_points or "",
            lead.qualification_status,
            lead.created_at.strftime("%Y-%m-%d")
        ])
    
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=smartlead_export.csv"
    return response

# --- FMCSA DATA IMPORT ---
@router.post("/import_fmcsa")
async def import_fmcsa_data(
    file: UploadFile = File(...),
    token: str = Depends(verify_admin_token),
    session: Session = Depends(get_session)
):
    """
    Uploads a CSV with headers: dot_number, company_name, total_power_units, safety_rating
    """
    content = await file.read()
    decoded = content.decode("utf-8")
    csv_reader = csv.DictReader(io.StringIO(decoded))
    
    count = 0
    for row in csv_reader:
        try:
            fleet = FleetData(
                dot_number=str(row["dot_number"]).strip(),
                company_name=row.get("company_name", ""),
                total_power_units=int(row.get("total_power_units", 0)),
                safety_rating=row.get("safety_rating", None)
            )
            session.merge(fleet)
            count += 1
        except Exception as e:
            print(f"Skipping row: {e}")
            continue
            
    session.commit()
    return {"status": "success", "imported_rows": count}

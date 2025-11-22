from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field
from enum import Enum

# --- Enums ---
class FleetSize(str, Enum):
    SMALL = "10-20"
    MEDIUM = "21-50"
    LARGE = "51-100"
    ENTERPRISE = "100+"

class Role(str, Enum):
    OWNER = "Owner"
    MANAGER = "Fleet Manager"
    OPS = "Operations"
    FINANCE = "Finance"
    OTHER = "Other"

# --- THE BRAIN: FMCSA Data Model ---
class FleetData(SQLModel, table=True):
    dot_number: str = Field(primary_key=True)
    company_name: Optional[str] = None
    total_power_units: int = 0
    safety_rating: Optional[str] = None

# --- Lead Models ---
class LeadBase(SQLModel):
    full_name: str
    work_email: str = Field(index=True)
    company_name: str
    phone: Optional[str] = None
    dot_number: Optional[str] = None
    fleet_size: FleetSize
    role: Role
    pain_points: Optional[str] = None 
    tech_stack: Optional[str] = None
    
    # Marketing/Tracking
    source: Optional[str] = "direct"
    utm_campaign: Optional[str] = None
    landing_page_path: Optional[str] = "/"
    consent_audit: bool = False

class Lead(LeadBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Enrichment & Qualification
    verified_status: Optional[str] = "pending"
    origin: str = "inbound"
    
    # NEW: Result of the FMCSA Cross-Check
    qualification_status: str = "Unchecked"

class LeadCreate(LeadBase):
    pass

class LeadRead(LeadBase):
    id: int
    created_at: datetime
    verified_status: str
    qualification_status: str

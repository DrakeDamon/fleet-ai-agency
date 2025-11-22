export enum FleetSize {
  SMALL = "10-20",
  MEDIUM = "21-50",
  LARGE = "51-100",
  ENTERPRISE = "100+"
}

export enum Role {
  OWNER = "Owner",
  MANAGER = "Fleet Manager",
  OPS = "Operations",
  FINANCE = "Finance",
  OTHER = "Other"
}

export interface LeadFormData {
  full_name: string;
  work_email: string;
  company_name: string;
  phone?: string;
  dot_number?: string; // Optional, but we will encourage it in UX
  fleet_size: FleetSize;
  role: Role;
  pain_points?: string;
  
  // Hidden / Auto-captured
  tech_stack?: string;
  source?: string;
  utm_campaign?: string;
  landing_page_path?: string;
  consent_audit: boolean;
}

export interface ApiError {
  detail: string | { loc: string[]; msg: string; type: string }[];
}

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

export enum PainPoint {
  BROKER_FRAUD = "Broker Fraud / Double Brokering",
  INSURANCE = "Insurance Premium Spikes",
  DOWNTIME = "Unplanned Breakdowns / Downtime",
  FUEL_THEFT = "Fuel Theft / High Fuel Costs",
  OTHER = "Other / Not Sure"
}

export interface LeadFormData {
  full_name: string;
  work_email: string;
  company_name: string;
  phone?: string;
  dot_number?: string; // Optional, but we will encourage it in UX
  fleet_size: FleetSize;
  role: Role;
  pain_points?: PainPoint | string; // Allow string for backward compatibility or custom input if needed, but primarily PainPoint
  
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

export interface RiskData {
  risk_level: "LOW" | "HIGH" | "CRITICAL";
  risk_flags: string[];
  vehicle_oos_rate: number;
  driver_oos_rate: number;
  crash_rate: number;
  company_name: string;
  dot_number: string;
  safety_rating?: string;
  rating?: string;
  total_crashes: number;
  fleet_size?: number;
}

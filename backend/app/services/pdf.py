import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from app.models import Lead

def generate_risk_report(lead: Lead, fmcsa_data: dict) -> bytes:
    """
    Generates a 2-Page Executive Valuation Brief.
    Page 1: Cover Sheet (Navy Blue Background)
    Page 2: The Dashboard (Scorecard + Financial Narrative)
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- DATA PREP ---
    risk_level = fmcsa_data.get('risk_level', 'UNKNOWN')
    unit_count = fmcsa_data.get('unit_count', 1)
    driver_count = fmcsa_data.get('driver_count', 0)
    vehicle_oos = float(fmcsa_data.get('vehicle_oos_rate', 0))
    driver_oos = float(fmcsa_data.get('driver_oos_rate', 0))
    total_crashes = fmcsa_data.get('total_crashes', 0)
    
    # Calculations
    # Bleed: Units * $6,000 (Fuel) * 5% (Fraud)
    monthly_bleed = unit_count * 6000 * 0.05
    
    # Churn: Drivers / Units
    churn_ratio = driver_count / unit_count if unit_count > 0 else 0
    
    # ==========================================
    # PAGE 1: COVER SHEET
    # ==========================================
    
    # Full Navy Blue Background
    c.setFillColorRGB(0.06, 0.09, 0.16) # #0F172A (Navy Blue)
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    # Centered Content
    c.setFillColor(colors.white)
    
    # Logo Placeholder (Text for now)
    c.setFont("Helvetica-Bold", 30)
    c.drawCentredString(width / 2, height - 3*inch, "FLEET AI AGENCY")
    
    # Report Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height / 2 + 20, "CONFIDENTIAL")
    c.drawCentredString(width / 2, height / 2 - 20, "VALUATION DEFENSE REPORT")
    
    # Client Details
    c.setFont("Helvetica", 16)
    y = height / 2 - 1.5*inch
    c.drawCentredString(width / 2, y, f"Prepared For: {lead.company_name}")
    c.drawCentredString(width / 2, y - 30, f"DOT #: {lead.dot_number}")
    
    c.showPage()

    # ==========================================
    # PAGE 2: THE DASHBOARD
    # ==========================================
    
    # Header
    c.setFillColorRGB(0.06, 0.09, 0.16) # Navy Blue Header
    c.rect(0, height - 1*inch, width, 1*inch, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 18)
    c.drawString(0.5*inch, height - 0.65*inch, "EXECUTIVE VALUATION BRIEF")
    
    # Layout Config
    left_col_x = 0.5*inch
    right_col_x = 3.0*inch # Start of right column (approx 1/3 split)
    y_start = height - 1.5*inch
    
    # --- LEFT COLUMN: SCORECARD (1/3) ---
    y = y_start
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_col_x, y, "FLEET SCORECARD")
    y -= 20
    
    # Safety Rating Badge
    status_color = colors.red if risk_level in ["HIGH", "CRITICAL"] else colors.green
    status_text = "CONDITIONAL" if risk_level in ["HIGH", "CRITICAL"] else "SATISFACTORY"
    
    c.setFillColor(status_color)
    c.roundRect(left_col_x, y - 30, 150, 30, 4, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(left_col_x + 75, y - 20, status_text)
    
    y -= 50
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(left_col_x, y, "Safety Rating Status")
    
    # OOS Metrics
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_col_x, y, f"Vehicle OOS: {vehicle_oos}%")
    c.setFont("Helvetica", 9)
    c.drawString(left_col_x, y - 12, "(Natl Avg: 20.7%)")
    
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_col_x, y, f"Driver OOS: {driver_oos}%")
    c.setFont("Helvetica", 9)
    c.drawString(left_col_x, y - 12, "(Natl Avg: 5.5%)")
    
    y -= 40
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_col_x, y, f"Crashes: {total_crashes}")
    c.setFont("Helvetica", 9)
    c.drawString(left_col_x, y - 12, "(Last 24 Months)")

    # --- RIGHT COLUMN: FINANCIAL NARRATIVE (2/3) ---
    y = y_start
    
    # 1. Financial Bleed (The Anchor)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(right_col_x, y, "FINANCIAL EXPOSURE ANALYSIS")
    y -= 30
    
    # Bleed Box
    c.setFillColor(colors.HexColor("#FEF2F2")) # Light Red
    c.setStrokeColor(colors.red)
    c.rect(right_col_x, y - 50, 350, 60, fill=True, stroke=True)
    
    c.setFillColor(colors.red)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(right_col_x + 175, y - 25, f"Est. Monthly Revenue Leakage: ${monthly_bleed:,.0f}")
    c.setFont("Helvetica", 10)
    c.setFillColor(colors.black)
    c.drawCentredString(right_col_x + 175, y - 42, "Based on unverified fuel & maintenance transaction models")
    
    y -= 80
    
    # 2. Driver Churn Risk
    c.setFont("Helvetica-Bold", 12)
    c.drawString(right_col_x, y, "Operational Risk Assessment:")
    y -= 20
    
    c.setFont("Helvetica", 11)
    if churn_ratio > 1.5:
        risk_text = "• High Theft Risk (Slip-Seating): Driver/Unit ratio > 1.5 indicates low accountability."
        c.setFillColor(colors.red)
    elif churn_ratio < 1.0:
        risk_text = "• Utilization Risk (Idle Assets): Trucks are sitting without drivers generating revenue."
        c.setFillColor(colors.orange)
    else:
        risk_text = "• Utilization: Healthy Driver/Unit ratio."
        c.setFillColor(colors.green)
        
    c.drawString(right_col_x, y, risk_text)
    
    # 3. Liability Gap
    y -= 40
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(right_col_x, y, "Liability Gap Assessment:")
    y -= 20
    
    # Visual Bar
    c.setFillColor(colors.lightgrey)
    c.rect(right_col_x, y - 15, 300, 15, fill=True, stroke=False) # Benchmark Bar
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawString(right_col_x + 305, y - 10, "$27.5M (Avg Nuclear Verdict)")
    
    # Client Coverage (Assume $1M for visual if unknown, or use placeholder)
    c.setFillColor(colors.blue)
    c.rect(right_col_x, y - 15, 300 * (1/27.5), 15, fill=True, stroke=False) # Tiny bar for $1M
    c.drawString(right_col_x, y - 25, "Your Coverage ($1M Est)")
    
    # Footer: Decision Maker Box
    footer_y = 1.5*inch
    c.setFillColor(colors.HexColor("#F3F4F6"))
    c.setStrokeColor(colors.darkgrey)
    c.rect(0.5*inch, footer_y, width - 1*inch, 0.8*inch, fill=True, stroke=True)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(width/2, footer_y + 0.5*inch, "PERFORMANCE GUARANTEE")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width/2, footer_y + 0.25*inch, "We will identify $20,000 in recoverable savings or refund the audit fee. (Valid for fleets with 20+ units).")
    
    # Metadata Footer
    c.setFont("Helvetica", 8)
    c.setFillColor(colors.grey)
    c.drawCentredString(width/2, 0.5*inch, "© 2024 Fleet AI Agency | Operation Type: Interstate | Confidential")

    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()

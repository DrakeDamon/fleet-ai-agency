import io
import os
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
    
    # Safety: Convert to float and handle potential string/null inputs safely
    try:
        vehicle_oos = float(fmcsa_data.get('vehicle_oos_rate', 0))
    except (ValueError, TypeError):
        vehicle_oos = 0.0
        
    try:
        driver_oos = float(fmcsa_data.get('driver_oos_rate', 0))
    except (ValueError, TypeError):
        driver_oos = 0.0
        
    total_crashes = fmcsa_data.get('total_crashes', 0)
    
    # Calculations
    # Bleed: Units * $6,000 (Avg Monthly Fuel Spend) * 5% (Fraud Rate)
    monthly_bleed = unit_count * 6000 * 0.05
    
    # Churn: Drivers / Units
    churn_ratio = driver_count / unit_count if unit_count > 0 else 0
    
    # ==========================================
    # PAGE 1: COVER SHEET
    # ==========================================
    
    # Full Navy Blue Background (#0F172A)
    c.setFillColorRGB(0.06, 0.09, 0.16) 
    c.rect(0, 0, width, height, fill=True, stroke=False)
    
    # Centered Content
    c.setFillColor(colors.white)
    
    # Logo Logic: Check if logo file exists, else use text
    logo_path = "public/logo.png"  # Update this path if your logo is elsewhere
    if os.path.exists(logo_path):
        # Draw Logo Image (Centered, approx 2.5 inches wide)
        # Adjust aspect ratio preservation as needed
        c.drawImage(logo_path, (width/2) - 1.25*inch, height - 3.5*inch, width=2.5*inch, preserveAspectRatio=True, mask='auto')
    else:
        # Fallback Text
        c.setFont("Helvetica-Bold", 30)
        c.drawCentredString(width / 2, height - 3*inch, "FLEET CLARITY")
    
    # Report Title
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height / 2 + 40, "CONFIDENTIAL")
    c.setFont("Helvetica", 18)
    c.drawCentredString(width / 2, height / 2, "VALUATION DEFENSE REPORT")
    
    # Divider Line
    c.setStrokeColor(colors.white)
    c.setLineWidth(1)
    c.line((width/2) - 1.5*inch, height/2 - 20, (width/2) + 1.5*inch, height/2 - 20)
    
    # Client Details
    c.setFont("Helvetica", 14)
    y = height / 2 - 1.5*inch
    c.drawCentredString(width / 2, y, f"Prepared For: {lead.company_name}")
    c.drawCentredString(width / 2, y - 25, f"DOT #: {lead.dot_number}")
    c.drawCentredString(width / 2, y - 50, f"Date: {lead.created_at.strftime('%Y-%m-%d') if lead.created_at else 'N/A'}")
    
    c.showPage()

    # ==========================================
    # PAGE 2: THE DASHBOARD
    # ==========================================
    
    # Header Bar
    c.setFillColorRGB(0.06, 0.09, 0.16) # Navy Blue
    c.rect(0, height - 1*inch, width, 1*inch, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(0.5*inch, height - 0.65*inch, "EXECUTIVE VALUATION BRIEF")
    
    # Layout Config
    left_col_x = 0.5*inch
    right_col_x = 3.2*inch # Gave right column slightly more space
    y_start = height - 1.5*inch
    
    # --- LEFT COLUMN: SCORECARD (Visual Indicators) ---
    y = y_start
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(left_col_x, y, "FLEET SCORECARD")
    y -= 25
    
    # Safety Rating Badge
    if risk_level in ["HIGH", "CRITICAL", "Conditional"]:
        status_color = colors.HexColor("#EF4444") # Red
        status_text = "CONDITIONAL"
    else:
        status_color = colors.HexColor("#10B981") # Green
        status_text = "SATISFACTORY"
    
    # Draw Badge Pill
    c.setFillColor(status_color)
    c.roundRect(left_col_x, y - 25, 140, 30, 6, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 11)
    c.drawCentredString(left_col_x + 70, y - 16, status_text)
    
    y -= 45
    c.setFillColor(colors.grey)
    c.setFont("Helvetica", 9)
    c.drawString(left_col_x, y, "Safety Rating Status")
    
    # Divider
    y -= 20
    c.setStrokeColor(colors.lightgrey)
    c.line(left_col_x, y, left_col_x + 140, y)
    y -= 20
    
    # Metric 1: Vehicle OOS
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    # Format to 1 decimal place
    c.drawString(left_col_x, y, f"{vehicle_oos:.1f}%")
    
    c.setFont("Helvetica", 10)
    c.drawString(left_col_x + 50, y, "Vehicle OOS")
    
    y -= 15
    c.setFillColor(colors.grey)
    c.setFont("Helvetica", 8)
    c.drawString(left_col_x, y, "(National Avg: 20.7%)")
    
    # Metric 2: Driver OOS
    y -= 35
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_col_x, y, f"{driver_oos:.1f}%")
    
    c.setFont("Helvetica", 10)
    c.drawString(left_col_x + 50, y, "Driver OOS")
    
    y -= 15
    c.setFillColor(colors.grey)
    c.setFont("Helvetica", 8)
    c.drawString(left_col_x, y, "(National Avg: 5.5%)")
    
    # Metric 3: Crashes
    y -= 35
    crash_color = colors.red if total_crashes > 0 else colors.black
    c.setFillColor(crash_color)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(left_col_x, y, f"{total_crashes}")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(left_col_x + 50, y, "Reportable Crashes")
    
    y -= 15
    c.setFillColor(colors.grey)
    c.setFont("Helvetica", 8)
    c.drawString(left_col_x, y, "(Last 24 Months)")

    # --- RIGHT COLUMN: FINANCIAL NARRATIVE ---
    y = y_start
    
    # 1. Financial Bleed Box
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(right_col_x, y, "FINANCIAL EXPOSURE ANALYSIS")
    y -= 30
    
    # Box Background
    c.setFillColor(colors.HexColor("#FEF2F2")) # Light Red BG
    c.setStrokeColor(colors.HexColor("#EF4444")) # Red Border
    c.setLineWidth(1.5)
    c.roundRect(right_col_x, y - 55, 380, 60, 6, fill=True, stroke=True)
    
    # Inside the Box
    c.setFillColor(colors.HexColor("#991B1B")) # Dark Red Text
    c.setFont("Helvetica-Bold", 15)
    c.drawCentredString(right_col_x + 190, y - 25, f"Est. Monthly Revenue Leakage: ${monthly_bleed:,.0f}")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 9)
    c.drawCentredString(right_col_x + 190, y - 45, "Based on unverified fuel & maintenance transaction models")
    
    y -= 90 # Move down past the box
    
    # 2. Operational Risk (Bullet Points)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(right_col_x, y, "Operational Risk Assessment:")
    y -= 20
    
    c.setFont("Helvetica", 10)
    if churn_ratio > 1.5:
        c.setFillColor(colors.HexColor("#B91C1C")) # Red
        c.drawString(right_col_x, y, "• High Theft Risk (Slip-Seating): Driver/Unit ratio > 1.5")
        y -= 15
        c.setFillColor(colors.black)
        c.drawString(right_col_x + 10, y, "  Indicates low accountability for fuel card usage.")
    elif churn_ratio < 1.0:
        c.setFillColor(colors.HexColor("#C2410C")) # Orange
        c.drawString(right_col_x, y, "• Utilization Risk (Idle Assets): Driver/Unit ratio < 1.0")
        y -= 15
        c.setFillColor(colors.black)
        c.drawString(right_col_x + 10, y, "  Trucks are sitting idle, generating zero revenue.")
    else:
        c.setFillColor(colors.HexColor("#047857")) # Green
        c.drawString(right_col_x, y, "• Optimal Utilization: Healthy Driver/Unit ratio detected.")
    
    y -= 30
    
    # 3. Liability Gap (Visual Bar)
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(right_col_x, y, "Liability Gap Assessment:")
    y -= 25
    
    # Background Bar (The Threat)
    c.setFillColor(colors.lightgrey)
    c.roundRect(right_col_x, y, 350, 12, 3, fill=True, stroke=False)
    
    # Client Coverage Bar (The Reality) - Assume $1M or use 4% width as visual
    c.setFillColor(colors.HexColor("#1D4ED8")) # Blue
    c.roundRect(right_col_x, y, 40, 12, 3, fill=True, stroke=False) # Small bar represents $1M
    
    # Labels
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 8)
    c.drawString(right_col_x, y - 12, "Your Coverage ($1M)")
    c.drawRightString(right_col_x + 350, y - 12, "$27.5M (Avg Nuclear Verdict)")
    
    # --- FOOTER: GUARANTEE ---
    footer_y = 1.0*inch
    c.setStrokeColor(colors.HexColor("#E5E7EB"))
    c.setLineWidth(1)
    c.line(0.5*inch, footer_y + 0.6*inch, width - 0.5*inch, footer_y + 0.6*inch)
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 10)
    c.drawCentredString(width/2, footer_y + 0.35*inch, "PERFORMANCE GUARANTEE")
    c.setFont("Helvetica", 9)
    c.drawCentredString(width/2, footer_y + 0.15*inch, "We will identify $20,000 in recoverable savings or refund the audit fee. (Valid for fleets with 20+ units).")
    
    # Metadata
    c.setFillColor(colors.grey)
    c.setFont("Helvetica", 7)
    c.drawCentredString(width/2, 0.5*inch, "© 2025 Fleet Clarity | Confidential | Generated via fleetclarity.io")

    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()

import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from app.models import Lead

def generate_risk_report(lead: Lead, fmcsa_data: dict) -> bytes:
    """
    Generates a High-End PDF Risk Snapshot in memory.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # --- 1. BRANDED HEADER (Dark Blue Background) ---
    c.setFillColorRGB(0.1, 0.15, 0.3) # Navy Blue
    c.rect(0, height - 1.5*inch, width, 1.5*inch, fill=True, stroke=False)
    
    c.setFillColor(colors.white)
    c.setFont("Helvetica-Bold", 24)
    c.drawCentredString(width / 2, height - 0.9*inch, "FLEET DATA RISK SNAPSHOT")
    c.setFont("Helvetica", 10)
    c.drawCentredString(width / 2, height - 1.2*inch, "CONFIDENTIAL DIAGNOSTIC REPORT")

    # --- 2. CLIENT PROFILE BOX ---
    y = height - 2.5*inch
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.5*inch, y, "1. FLEET PROFILE")
    
    y -= 20
    c.setFont("Helvetica", 12)
    # Handle potential None values gracefully
    name = lead.full_name if hasattr(lead, 'full_name') else "Valued Client"
    c.drawString(0.5*inch, y, f"Fleet: {lead.company_name}")
    c.drawString(4.5*inch, y, f"DOT #: {lead.dot_number}")
    
    y -= 20
    c.drawString(0.5*inch, y, f"Contact: {name}")
    c.drawString(4.5*inch, y, f"Est. Size: {lead.fleet_size}")
    
    # Draw a line separator
    c.setStrokeColor(colors.lightgrey)
    c.line(0.5*inch, y - 15, width - 0.5*inch, y - 15)

    # --- 3. RISK ANALYSIS (The Scorecard) ---
    y -= 60
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.5*inch, y, "2. FMCSA RISK ANALYSIS")
    
    # Extract Data
    risk_level = fmcsa_data.get('risk_level', 'UNKNOWN')
    vehicle_oos = float(fmcsa_data.get('vehicle_oos_rate', 0))
    natl_avg = 22.0
    
    # Visual Badge Logic
    y -= 40
    if risk_level in ["HIGH", "CRITICAL"]:
        badge_color = colors.red
        text_color = colors.white
    elif risk_level == "MODERATE":
        badge_color = colors.orange
        text_color = colors.white
    else:
        badge_color = colors.green
        text_color = colors.white
        
    # Draw Badge
    c.setFillColor(badge_color)
    c.roundRect(0.5*inch, y - 10, 200, 30, 4, fill=True, stroke=False)
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(0.5*inch + 100, y, f"RISK LEVEL: {risk_level}")
    
    # --- 4. DATA VISUALIZATION (The Bar Chart) ---
    # Draw a simple bar chart comparing their OOS vs National Avg
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 10)
    c.drawString(4.5*inch, y + 20, "Vehicle Out-of-Service Rate")
    
    chart_base_y = y - 10
    # National Bar (Grey)
    c.setFillColor(colors.lightgrey)
    c.rect(4.5*inch, chart_base_y, 150 * (natl_avg/100), 15, fill=True, stroke=False)
    c.setFillColor(colors.black)
    c.drawString(4.5*inch + 5, chart_base_y + 4, f"Natl Avg: {natl_avg}%")
    
    # Client Bar (Red if high)
    client_color = colors.red if vehicle_oos > natl_avg else colors.green
    c.setFillColor(client_color)
    c.rect(4.5*inch, chart_base_y - 20, 150 * (vehicle_oos/100), 15, fill=True, stroke=False)
    c.setFillColor(colors.white)
    c.drawString(4.5*inch + 5, chart_base_y - 16, f"Your Fleet: {vehicle_oos}%")

    # --- 5. FINANCIAL IMPACT (The Pain) ---
    y -= 80
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    c.drawString(0.5*inch, y, "3. PROJECTED FINANCIAL BLEED")
    
    # Dynamic Math
    # Estimate 100 gallons per truck per week * $3.50/gal * 4 weeks
    # 5% Fraud/Waste Rate
    truck_count_map = {"10-20": 15, "21-50": 35, "51-100": 75, "100+": 120}
    # Handle case where fleet_size might be enum or string
    est_trucks = truck_count_map.get(str(lead.fleet_size), 20)
    monthly_fuel_spend = est_trucks * 400 * 3.50 
    est_fraud_loss = monthly_fuel_spend * 0.05 # 5% Loss
    
    # Draw "Alert Box"
    y -= 60
    c.setFillColor(colors.lightyellow)
    c.setStrokeColor(colors.orange)
    c.rect(0.5*inch, y - 40, width - 1*inch, 80, fill=True, stroke=True)
    
    c.setFillColor(colors.red)
    c.setFont("Helvetica-Bold", 12)
    c.drawString(0.7*inch, y + 20, "⚠ CRITICAL PROFIT LEAKS DETECTED")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    
    # Line 1: Insurance
    if risk_level in ["HIGH", "CRITICAL"]:
        c.drawString(0.7*inch, y, f"• Est. Insurance Premium Surcharge: $25,000+ / Year (Due to {risk_level} rating)")
    else:
        c.drawString(0.7*inch, y, f"• Est. Compliance Risk: Moderate (Audit probability increasing)")
        
    # Line 2: Fuel Fraud
    y -= 20
    c.drawString(0.7*inch, y, f"• Est. Unverified Fuel Spend (Fraud/Waste): ${est_fraud_loss:,.0f} / Month")
    
    # --- 6. CALL TO ACTION (Footer) ---
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(width/2, 100, "STOP THE BLEED. FIX YOUR DATA.")
    
    c.setFillColor(colors.blue)
    c.setFont("Helvetica-Oblique", 10)
    c.drawCentredString(width/2, 80, "Book your full audit review: https://fleet-ai-agency.com/booking")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()

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

    # --- 1. BRANDED HEADER (Conditional) ---
    risk_level = fmcsa_data.get('risk_level', 'UNKNOWN')
    
    if risk_level == "LOW":
        # SAFE PATH: Profit Optimization
        c.setFillColorRGB(0.1, 0.15, 0.3) # Navy Blue
        c.rect(0, height - 1.5*inch, width, 1.5*inch, fill=True, stroke=False)
        
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 24)
        c.drawCentredString(width / 2, height - 0.9*inch, "PROFIT OPTIMIZATION SNAPSHOT")
        c.setFont("Helvetica", 10)
        c.drawCentredString(width / 2, height - 1.2*inch, "CONFIDENTIAL EFFICIENCY REPORT")
    else:
        # RISK PATH: Remediation
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
    vehicle_oos = float(fmcsa_data.get('vehicle_oos_rate', 0))
    natl_avg = 22.0
    
    # Visual Badge Logic
    y -= 40
    if risk_level in ["HIGH", "CRITICAL"]:
        badge_color = colors.red
        text_color = colors.white
        badge_text = f"RISK LEVEL: {risk_level}"
    elif risk_level == "MODERATE":
        badge_color = colors.orange
        text_color = colors.white
        badge_text = f"RISK LEVEL: {risk_level}"
    else:
        badge_color = colors.green
        text_color = colors.white
        badge_text = "SAFETY STATUS: STRONG"
        
    # Draw Badge
    c.setFillColor(badge_color)
    c.roundRect(0.5*inch, y - 10, 200, 30, 4, fill=True, stroke=False)
    c.setFillColor(text_color)
    c.setFont("Helvetica-Bold", 12)
    c.drawCentredString(0.5*inch + 100, y, badge_text)
    
    # --- 4. DATA VISUALIZATION (Conditional) ---
    if risk_level == "LOW":
        # SAFE PATH: Show "Checkmark" / Positive Reinforcement
        c.setFillColor(colors.black)
        c.setFont("Helvetica", 10)
        c.drawString(4.5*inch, y + 20, "Compliance Status")
        
        c.setFillColor(colors.green)
        c.setFont("Helvetica-Bold", 14)
        c.drawString(4.5*inch, y, "✓ BEATING NATIONAL AVERAGE")
        c.setFont("Helvetica", 10)
        c.setFillColor(colors.black)
        c.drawString(4.5*inch, y - 15, f"Your OOS: {vehicle_oos}% (Natl Avg: {natl_avg}%)")
        
    else:
        # RISK PATH: The Bar Chart
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
    
    if risk_level == "LOW":
        c.drawString(0.5*inch, y, "3. HIDDEN PROFIT LEAKS")
    else:
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
    
    if risk_level == "LOW":
        c.drawString(0.7*inch, y + 20, "⚠ UNVERIFIED SPEND DETECTED")
    else:
        c.drawString(0.7*inch, y + 20, "⚠ CRITICAL PROFIT LEAKS DETECTED")
    
    c.setFillColor(colors.black)
    c.setFont("Helvetica", 11)
    
    if risk_level == "LOW":
        # SAFE PATH: Fuel & Maintenance
        c.drawString(0.7*inch, y, f"• Est. Unverified Fuel Spend: ${est_fraud_loss:,.0f} / Month (5% Industry Avg)")
        y -= 20
        c.drawString(0.7*inch, y, "• Est. Maintenance Over-Spend: 12% (Due to early replacement cycles)")
    else:
        # RISK PATH: Insurance & Fuel
        if risk_level in ["HIGH", "CRITICAL"]:
            c.drawString(0.7*inch, y, f"• Est. Insurance Premium Surcharge: $25,000+ / Year (Due to {risk_level} rating)")
        else:
            c.drawString(0.7*inch, y, f"• Est. Compliance Risk: Moderate (Audit probability increasing)")
            
        y -= 20
        c.drawString(0.7*inch, y, f"• Est. Unverified Fuel Spend (Fraud/Waste): ${est_fraud_loss:,.0f} / Month")
    
    # --- 6. DECISION MAKER BLOCK (The "Trojan Horse" CTA) ---
    y -= 100
    
    # Draw the Decision Maker Box
    c.setFillColor(colors.HexColor("#F3F4F6"))  # Light Grey
    c.setStrokeColor(colors.darkgrey)
    c.rect(0.5*inch, y - 80, width - 1*inch, 100, fill=True, stroke=True)
    
    # Header
    c.setFillColor(colors.black)
    c.setFont("Helvetica-Bold", 14)
    
    if risk_level == "LOW":
        c.drawCentredString(width/2, y - 10, "FINAL ACTION: STOP THE SILENT BLEED")
    else:
        c.drawCentredString(width/2, y - 10, "FINAL ACTION REQUIRED: SECURE YOUR PROFIT PROTECTION")
    
    # Body Text
    c.setFont("Helvetica", 10)
    y -= 35
    
    if risk_level == "LOW":
        body_text = "To The Owner: Your safety is strong, but your efficiency is unverified."
        c.drawCentredString(width/2, y, body_text)
        y -= 15
        c.drawCentredString(width/2, y, "Unlock your Profit Audit to recover these lost dollars.")
    else:
        body_text = "To The Owner: This report identifies potential savings that trigger our $20,000 Performance Guarantee."
        c.drawCentredString(width/2, y, body_text)
        y -= 15
        c.drawCentredString(width/2, y, "We found the leaks. Do not delegate this fix.")
    
    # CTA Button/Link
    y -= 30
    c.setFillColor(colors.blue)
    c.setFont("Helvetica-Bold", 11)
    
    if risk_level == "LOW":
         c.drawCentredString(width/2, y, "CLICK HERE: Unlock Your Profit Audit")
    else:
        c.drawCentredString(width/2, y, "CLICK HERE: Book Your Guaranteed Profit Briefing")
        
    c.setFont("Helvetica", 9)
    c.setFillColor(colors.darkblue)
    y -= 12
    c.drawCentredString(width/2, y, "https://fleet-ai-agency.com/booking")
    
    # --- 7. COPYRIGHT FOOTER ---
    c.setFillColor(colors.grey)
    c.setFont("Helvetica", 8)
    c.drawCentredString(width/2, 40, "© 2024 Fleet AI Agency. Confidential & Proprietary.")
    
    c.showPage()
    c.save()
    
    buffer.seek(0)
    return buffer.getvalue()

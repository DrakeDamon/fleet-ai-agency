import os
import sys
from dotenv import load_dotenv

load_dotenv()

from app.services.email import send_report_email
from app.services.pdf import generate_risk_report
from app.models import Lead

# Mock Data
lead = Lead(
    first_name="David",
    last_name="Damon",
    company_name="Damon Logistics",
    dot_number="1234567",
    fleet_size="21-50",
    work_email="dddamon06@gmail.com"
)

fmcsa_data = {
    "risk_level": "HIGH",
    "vehicle_oos_rate": 35.5,
    "risk_flags": ["Vehicle OOS > 22%"]
}

print("Generating PDF...")
pdf_bytes = generate_risk_report(lead, fmcsa_data)

# Save locally to verify
with open("test_output.pdf", "wb") as f:
    f.write(pdf_bytes)
print("✅ Saved test_output.pdf locally. Please check if it opens.")

# Test Data
to_email = "dddamon06@gmail.com"
first_name = "David"
dot_number = "1234567"

print(f"Sending test email to {to_email}...")
result = send_report_email(to_email, first_name, pdf_bytes, dot_number)

if result:
    print("✅ Email sent successfully!")
    print(result)
else:
    print("❌ Email failed to send.")

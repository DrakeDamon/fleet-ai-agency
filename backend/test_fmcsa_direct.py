import asyncio
import os
from dotenv import load_dotenv
from app.services.fmcsa import fetch_carrier_risk

# Force load .env from backend directory
load_dotenv(".env")

async def main():
    dot_number = "2377196"
    print(f"Testing FMCSA API for DOT: {dot_number}")
    
    # Check if key is present in env
    key = os.getenv("FMCSA_WEBKEY")
    if key:
        print(f"FMCSA_WEBKEY found: {key[:4]}...{key[-4:]}")
    else:
        print("❌ FMCSA_WEBKEY not found in environment!")

    try:
        result = await fetch_carrier_risk(dot_number)
        print("\n✅ Success! Result:")
        print(result)
    except Exception as e:
        print(f"\n❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())

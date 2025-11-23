import os
import httpx
from fastapi import HTTPException
from app.config import settings

FMCSA_BASE_URL = "https://mobile.fmcsa.dot.gov/qc/services"

async def fetch_carrier_risk(dot_number: str):
    webkey = settings.FMCSA_WEBKEY
    
    if not webkey:
        print("⚠️ No FMCSA_WEBKEY found.")
        raise HTTPException(status_code=500, detail="Server configuration error: FMCSA_WEBKEY missing")

    async with httpx.AsyncClient() as client:
        try:
            # Official QCMobile Endpoint
            response = await client.get(
                f"{FMCSA_BASE_URL}/carriers/{dot_number}",
                params={"webKey": webkey}
            )
            
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="DOT Number not found")

            data = response.json()
            
            # Handle different response structures
            # Sometimes content is a list, sometimes a dict
            content = data.get("content", {})
            
            if isinstance(content, list):
                if not content:
                    raise HTTPException(status_code=404, detail="DOT Number not found")
                carrier = content[0].get("carrier", {})
            else:
                # content is a dict
                carrier = content.get("carrier", {})
            
            if not carrier:
                 raise HTTPException(status_code=404, detail="DOT Number not found")
            
            # Extract Key Metrics
            # The API might return these as strings or numbers, so we safely convert
            vehicle_oos = float(carrier.get("vehicleOosRate", 0))
            driver_oos = float(carrier.get("driverOosRate", 0))
            rating = carrier.get("safetyRating", "None")
            
            # NEW: Crash Data Extraction
            crashes = carrier.get("crashes", {})
            fatal = int(crashes.get("fatal", 0))
            injury = int(crashes.get("injury", 0))
            tow = int(crashes.get("tow", 0))
            total_crashes = fatal + injury + tow

            # LOGIC: The "Risk" Calculation
            risk_level = "LOW"
            flags = []
            
            if vehicle_oos > 22.0:
                risk_level = "HIGH"
                flags.append(f"Vehicle OOS is {vehicle_oos}% (Natl Avg: 22%)")
            
            if rating == "Conditional":
                risk_level = "CRITICAL"
                flags.append("Safety Rating is CONDITIONAL (Insurance Risk)")

            if total_crashes > 0:
                flags.append(f"{total_crashes} Reportable Crashes (Potential Ghost Downtime)")

            return {
                "company_name": carrier.get("legalName"),
                "vehicle_oos_rate": vehicle_oos,
                "driver_oos_rate": driver_oos,
                "rating": rating,
                "risk_level": risk_level,
                "risk_flags": flags,
                "total_crashes": total_crashes
            }

        except HTTPException as he:
            raise he
        except Exception as e:
            print(f"FMCSA API Error: {e}")
            raise HTTPException(status_code=500, detail="Failed to fetch FMCSA data")

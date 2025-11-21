from fastapi import APIRouter, Response
from fastapi.responses import JSONResponse

router = APIRouter(tags=["SEO"])

@router.get("/sitemap.xml")
def get_sitemap():
    base_url = "https://www.your-agency-domain.com"
    routes = ["/", "/audit-offer", "/privacy"]
    
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    for route in routes:
        xml_content += f'  <url>\n    <loc>{base_url}{route}</loc>\n    <changefreq>weekly</changefreq>\n  </url>\n'
    
    xml_content += '</urlset>'
    return Response(content=xml_content, media_type="application/xml")

@router.get("/api/v1/seo/schema")
def get_json_ld():
    schema = {
        "@context": "https://schema.org",
        "@type": "ProfessionalService",
        "name": "Data & AI Clarity Agency",
        "description": "Data engineering and AI readiness audits for mid-sized trucking fleets.",
        "priceRange": "$$$"
    }
    return JSONResponse(content=schema)

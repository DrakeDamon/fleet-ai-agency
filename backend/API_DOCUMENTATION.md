# Backend API Documentation
**Fleet AI Agency Lead Capture Backend**

This document provides complete API documentation for frontend integration.

---

## 🔧 Server Configuration

**Base URL (Local)**: `http://127.0.0.1:8000`  
**Base URL (Production)**: `https://your-backend.onrender.com`

**CORS**: Enabled for all origins during development (`allow_origins=["*"]`)

**Rate Limiting**: 5 requests per minute per IP on lead submission endpoint

---

## 📋 API Endpoints

### 1. Health Check
Check if the backend is running.

```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "database": "connected"
}
```

---

### 2. Create Lead
Submit a new lead with optional DOT number for automatic qualification.

```http
POST /api/v1/leads/
Content-Type: application/json
```

**Rate Limit**: 5 requests/minute per IP

**Request Body:**
```json
{
  "full_name": "John Doe",
  "work_email": "john@example.com",
  "company_name": "Example Trucking LLC",
  "phone": "555-1234",
  "dot_number": "123456",
  "fleet_size": "21-50",
  "role": "Owner",
  "pain_points": "Need better route optimization",
  "tech_stack": "Excel, Google Sheets",
  "source": "direct",
  "utm_campaign": "google_ads_q4",
  "landing_page_path": "/",
  "consent_audit": true
}
```

**Field Constraints:**
| Field | Type | Required | Enum Values |
|-------|------|----------|-------------|
| `full_name` | string | ✅ | - |
| `work_email` | string (email) | ✅ | - |
| `company_name` | string | ✅ | - |
| `phone` | string | ❌ | - |
| `dot_number` | string | ❌ | - |
| `fleet_size` | string | ✅ | `"10-20"`, `"21-50"`, `"51-100"`, `"100+"` |
| `role` | string | ✅ | `"Owner"`, `"Fleet Manager"`, `"Operations"`, `"Finance"`, `"Other"` |
| `pain_points` | string | ❌ | - |
| `tech_stack` | string | ❌ | - |
| `source` | string | ❌ (default: `"direct"`) | - |
| `utm_campaign` | string | ❌ | - |
| `landing_page_path` | string | ❌ (default: `"/"`) | - |
| `consent_audit` | boolean | ❌ (default: `false`) | - |

**Response (201 Created):**
```json
{
  "id": 1,
  "full_name": "John Doe",
  "work_email": "john@example.com",
  "company_name": "Example Trucking LLC",
  "phone": "555-1234",
  "dot_number": "123456",
  "fleet_size": "21-50",
  "role": "Owner",
  "pain_points": "Need better route optimization",
  "tech_stack": "Excel, Google Sheets",
  "source": "direct",
  "utm_campaign": "google_ads_q4",
  "landing_page_path": "/",
  "consent_audit": true,
  "created_at": "2025-11-21T02:26:48.502109",
  "verified_status": "pending",
  "qualification_status": "Qualified (45 Units)"
}
```

**Qualification Status Values:**
- `"Qualified (X Units)"` - Fleet has 10-100 power units
- `"Enterprise (X Units)"` - Fleet has 100+ power units
- `"Too Small (X Units)"` - Fleet has <10 power units
- `"Unknown DOT"` - DOT number not found in database
- `"Unchecked"` - No DOT number provided

**Error Responses:**
```json
// 429 Too Many Requests (Rate Limit Exceeded)
{
  "error": "Rate limit exceeded: 5 per minute"
}

// 422 Validation Error
{
  "detail": [
    {
      "type": "string_type",
      "loc": ["body", "work_email"],
      "msg": "Input should be a valid string",
      "input": null
    }
  ]
}
```

---

### 3. Export Leads (Admin)
Download all leads as SmartLead-compatible CSV.

```http
GET /api/v1/admin/export_csv
x-admin-token: <ADMIN_SECRET>
```

**Headers:**
```
x-admin-token: ybyrlZ9VOisbkly3bL2Khqzpg0F6BKMlxMevxtDUzF17vM9JPgx5uoU2etu6seDH
```

**Response:**
```csv
Email,FirstName,LastName,CompanyName,Website,Phone,CustomField:FleetSize,CustomField:Role,CustomField:PainPoints,CustomField:Qualified,Date
john@example.com,John,Doe,Example Trucking LLC,,555-1234,21-50,Owner,Need better route optimization,Qualified (45 Units),2025-11-21
```

**Error Response (401):**
```json
{
  "detail": "Invalid Admin Token"
}
```

---

### 4. Import FMCSA Data (Admin)
Upload FMCSA fleet data for lead qualification.

```http
POST /api/v1/admin/import_fmcsa
x-admin-token: <ADMIN_SECRET>
Content-Type: multipart/form-data
```

**Request:**
```
file: <CSV file>
```

**CSV Format:**
```csv
dot_number,company_name,total_power_units,safety_rating
123456,Test Trucking LLC,45,Satisfactory
999999,Small Time Carriers,3,None
888888,Big Fleet Inc,150,Satisfactory
```

**Response (200):**
```json
{
  "status": "success",
  "imported_rows": 3
}
```

---

### 5. SEO Sitemap
Generate XML sitemap for search engines.

```http
GET /sitemap.xml
```

**Response:**
```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://yoursite.com/</loc>
    <lastmod>2025-11-21</lastmod>
    <changefreq>weekly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>
```

---

### 6. JSON-LD Schema
Get structured data for homepage SEO.

```http
GET /api/v1/seo/schema
```

**Response:**
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Fleet AI Agency",
  "description": "Leading provider of AI solutions for fleet management",
  "url": "https://yoursite.com",
  "contactPoint": {
    "@type": "ContactPoint",
    "contactType": "Sales",
    "email": "hello@fleetaiagency.com"
  }
}
```

---

## 🔐 Authentication

**Admin Endpoints** require the `x-admin-token` header:
- `/api/v1/admin/export_csv`
- `/api/v1/admin/import_fmcsa`

**Token Location**: Set in `.env` as `ADMIN_SECRET`

**Example:**
```bash
curl -H "x-admin-token: your_secret_token" \
  http://localhost:8000/api/v1/admin/export_csv
```

---

## 🗄️ Database Models

### Lead Table Schema
```python
{
  "id": int,                          # Auto-generated
  "full_name": str,                   # Stored as single field; split into FirstName/LastName in CSV export
  "work_email": str,                  # Indexed
  "company_name": str,
  "phone": str | null,
  "dot_number": str | null,
  "fleet_size": str,                  # Enum: "10-20", "21-50", "51-100", "100+"
  "role": str,                        # Enum: "Owner", "Fleet Manager", etc.
  "pain_points": str | null,
  "tech_stack": str | null,
  "source": str,                      # Default: "direct"
  "utm_campaign": str | null,
  "landing_page_path": str,           # Default: "/"
  "consent_audit": bool,              # Default: false
  "created_at": datetime,             # Auto-generated
  "updated_at": datetime,             # Auto-generated
  "verified_status": str,             # "pending", "valid", "invalid", "accept_all", "unknown"
  "origin": str,                      # Default: "inbound"
  "qualification_status": str         # See qualification values above
}
```

> **Note on CSV Export**: The `full_name` field in the database is dynamically split into `FirstName` and `LastName` during CSV export using the logic: `name.split(" ", 1)` to separate first name from the rest. This ensures SmartLead compatibility while maintaining a single name field in the database.

### FleetData Table Schema
```python
{
  "dot_number": str,                  # Primary key
  "company_name": str | null,
  "total_power_units": int,
  "safety_rating": str | null
}
```

---

## 🚀 Frontend Integration Example

### React/Next.js Example

```typescript
// types.ts
export interface LeadFormData {
  full_name: string;
  work_email: string;
  company_name: string;
  phone?: string;
  dot_number?: string;
  fleet_size: "10-20" | "21-50" | "51-100" | "100+";
  role: "Owner" | "Fleet Manager" | "Operations" | "Finance" | "Other";
  pain_points?: string;
  tech_stack?: string;
  utm_campaign?: string;
  consent_audit?: boolean;
}

// api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function submitLead(data: LeadFormData) {
  const response = await fetch(`${API_BASE}/api/v1/leads/`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    if (response.status === 429) {
      throw new Error("Too many submissions. Please wait a minute.");
    }
    throw new Error("Failed to submit lead");
  }

  return response.json();
}

// LeadForm.tsx
import { useState } from 'react';
import { submitLead } from './api';

export default function LeadForm() {
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setStatus('loading');

    const formData = new FormData(e.currentTarget);
    const data = {
      full_name: formData.get('full_name') as string,
      work_email: formData.get('work_email') as string,
      company_name: formData.get('company_name') as string,
      phone: formData.get('phone') as string,
      dot_number: formData.get('dot_number') as string,
      fleet_size: formData.get('fleet_size') as any,
      role: formData.get('role') as any,
      pain_points: formData.get('pain_points') as string,
      consent_audit: true,
    };

    try {
      await submitLead(data);
      setStatus('success');
    } catch (error) {
      setStatus('error');
      console.error(error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {/* Form fields */}
      <input name="full_name" required />
      <input name="work_email" type="email" required />
      <select name="fleet_size" required>
        <option value="10-20">10-20 Trucks</option>
        <option value="21-50">21-50 Trucks</option>
        <option value="51-100">51-100 Trucks</option>
        <option value="100+">100+ Trucks</option>
      </select>
      <button type="submit" disabled={status === 'loading'}>
        {status === 'loading' ? 'Submitting...' : 'Submit'}
      </button>
    </form>
  );
}
```

---

## 🌐 Environment Variables

Create a `.env` file in your frontend:

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
# For production:
# NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

---

## 🛡️ Security Features

1. **Rate Limiting**: 5 requests/minute per IP on lead endpoint
2. **CORS**: Configurable origins (currently `*` for development)
3. **Email Validation**: Server-side validation via `email-validator`
4. **Admin Authentication**: Token-based auth for sensitive endpoints
5. **Hunter.io Verification**: Background email verification with spam filtering

---

## 📊 Background Tasks

### Email Verification Flow
1. Lead created with `verified_status: "pending"`
2. Background task triggers Hunter.io API call
3. API checks for:
   - Deliverability
   - Gibberish detection
   - Disposable email detection
4. Status updated to: `valid`, `invalid`, `accept_all`, or `unknown`
5. Result cached in `hunter_cache.json` for 30 days

---

## 🧪 Testing

### Test Lead Submission
```bash
curl -X POST "http://localhost:8000/api/v1/leads/" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Test User",
    "work_email": "test@example.com",
    "company_name": "Test Co",
    "fleet_size": "21-50",
    "role": "Owner"
  }'
```

### Test Rate Limiting
Run the above command 6 times quickly to trigger rate limit.

### Test FMCSA Qualification
```bash
curl -X POST "http://localhost:8000/api/v1/leads/" \
  -H "Content-Type: application/json" \
  -d '{
    "full_name": "Qualified Lead",
    "work_email": "lead@qualified.com",
    "company_name": "Qualified Trucking",
    "dot_number": "123456",
    "fleet_size": "21-50",
    "role": "Owner"
  }'
```

Check `qualification_status` in response - should show fleet size if DOT exists in database.

---

## 📝 Interactive API Documentation

Visit `http://localhost:8000/docs` for Swagger UI with:
- Interactive API testing
- Schema validation
- Request/Response examples
- Try out all endpoints with sample data

---

## 🚨 Common Errors

| Status | Error | Solution |
|--------|-------|----------|
| 422 | Validation error | Check field types and enum values |
| 429 | Rate limit exceeded | Wait 1 minute between submissions |
| 401 | Invalid admin token | Verify `x-admin-token` header |
| 500 | Server error | Check server logs for details |

---

## 📞 Support

For backend issues or questions:
- Check logs: `./venv/bin/uvicorn app.main:app --reload`
- View API docs: `http://localhost:8000/docs`
- Verify database: Check Supabase dashboard

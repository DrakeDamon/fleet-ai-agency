# Fleet AI Agency

**Lead Capture & Enrichment Platform for Fleet Management Services**

---

## 🚀 Project Structure

```
fleet-ai-agency/
├── backend/          # FastAPI backend (Python)
└── frontend/         # [Coming Soon] React/Next.js frontend
```

---

## 📦 Backend

FastAPI-based lead capture and enrichment system with:

- **The Brain**: FMCSA data cross-referencing for automatic lead qualification
- **Hunter.io Integration**: Email verification with quality filtering
- **Rate Limiting**: 5 requests/minute per IP for security
- **SmartLead Export**: CSV export optimized for SmartLead CRM
- **Admin Dashboard**: Protected endpoints for data management

### Quick Start

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env      # Configure your environment variables
uvicorn app.main:app --reload
```

Server runs on `http://localhost:8000`

**API Docs**: `http://localhost:8000/docs`

### Environment Variables

Create a `.env` file:

```bash
DATABASE_URL=postgresql://user:pass@host:port/db
ADMIN_SECRET=your_secret_token
HUNTER_API_KEY=your_hunter_api_key
```

### Key Features

- ✅ Lead capture with validation
- ✅ FMCSA DOT number qualification
- ✅ Background email verification
- ✅ Rate limiting & analytics
- ✅ SmartLead-compatible export
- ✅ SEO endpoints (sitemap, JSON-LD)

### API Documentation

See [API_DOCUMENTATION.md](./backend/API_DOCUMENTATION.md) for complete endpoint reference and frontend integration examples.

---

## 🔜 Frontend

Coming soon! The frontend will be built with React/Next.js and integrated with the backend API.

---

## 🛠️ Tech Stack

**Backend:**
- FastAPI (Python)
- SQLModel + PostgreSQL (Supabase)
- Hunter.io API
- SlowAPI (rate limiting)

**Frontend (Planned):**
- Next.js 14+
- TypeScript
- TailwindCSS

---

## 📝 Development Workflow

### Branches

- `main` - Production-ready backend code
- `frontend` - Frontend development (TBD)
- `dev` - Active development

### Deployment

**Backend**: Deploy to Render, Railway, or similar platforms using the included `Dockerfile`.

**Database**: Supabase (PostgreSQL)

---

## 🤝 Contributing

This is a private project. Contact the repository owner for access.

---

## 📄 License

Proprietary - All rights reserved

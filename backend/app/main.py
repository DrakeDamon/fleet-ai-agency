from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.db import create_db_and_tables
from app.routers import leads, seo, admin
from app.limiter import limiter

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Fleet AI Agency Backend",
    lifespan=lifespan
)

# 1. SETUP RATE LIMITER (Security)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# 2. SETUP CORS
origins = [
    "http://localhost:3000",
    "https://data-clarity-agency.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Change to 'origins' variable for Production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. ANALYTICS MIDDLEWARE
@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    
    # Filter noise (health checks, favicon)
    if request.method == "GET" and "/health" not in request.url.path and "favicon" not in request.url.path:
        print(f"📊 ANALYTICS: Path={request.url.path} | Status={response.status_code} | IP={request.client.host}")
        
    return response

# Mount Routers
app.include_router(leads.router)
app.include_router(seo.router)
app.include_router(admin.router)

@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected"}

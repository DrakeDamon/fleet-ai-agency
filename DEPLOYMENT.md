# Deployment Guide - Render

This document outlines how to deploy the FMCSA backend to Render.

## Prerequisites

1. **Render Account**: Sign up at https://render.com
2. **GitHub Repository**: Connect your GitHub repo to Render
3. **Environment Variables**: Set up in Render Dashboard

## Render Deployment Setup

### 1. Connect Repository

1. Go to https://dashboard.render.com
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select the `fmcsa` repository

### 2. Configure Service (Using render.yaml)

The `render.yaml` file in the root directory will auto-configure:
- **Service Type**: Docker Web Service
- **Dockerfile**: `./backend/Dockerfile`
- **Docker Context**: `./backend`

Alternatively, manually configure:
- **Name**: `fmcsa-backend`
- **Environment**: `Docker`
- **Region**: `Oregon (US West)`
- **Branch**: `main` (or your default branch)
- **Root Directory**: Leave empty (or `backend` if deploying from subdirectory)
- **Dockerfile Path**: `./backend/Dockerfile`
- **Docker Context**: `./backend`

### 3. Environment Variables

Set these in Render Dashboard → Environment:

```bash
DATABASE_URL=postgresql://...  # Your Supabase PostgreSQL URL
ADMIN_SECRET=your_secret_here
HUNTER_API_KEY=your_hunter_key
FMCSA_WEBKEY=your_fmcsa_key
```

**Note**: PORT is automatically set by Render (don't set manually)

### 4. Deploy

Once configured, Render will:
1. Build the Docker image from `backend/Dockerfile`
2. Start the FastAPI server on the PORT Render provides
3. Your backend will be available at: `https://fmcsa-backend.onrender.com`

### 5. Update Frontend

After deployment, update the frontend `.env.local`:

```bash
NEXT_PUBLIC_API_URL=https://fmcsa-backend.onrender.com
```

Or update `frontend/lib/api.ts` if you want it hardcoded.

### 6. Update CORS (if needed)

If your frontend is on a different domain, update `backend/app/main.py`:

```python
origins = [
    "http://localhost:3000",
    "https://data-clarity-agency.vercel.app",
    "https://your-render-url.onrender.com",  # Add if needed
]
```

## Health Check

After deployment, verify:
```bash
curl https://fmcsa-backend.onrender.com/health
```

Should return:
```json
{"status":"ok","database":"connected"}
```

## Troubleshooting

### Build Fails
- Check Dockerfile path is correct
- Verify all dependencies in `requirements.txt`
- Check Render build logs for errors

### Database Connection Issues
- Verify `DATABASE_URL` is correct
- Ensure PostgreSQL database is accessible from Render's IPs
- Check if Supabase requires IP whitelisting

### CORS Errors
- Update CORS origins in `backend/app/main.py`
- Ensure frontend URL is in the allowed origins list

## Auto-Deploy

Render will auto-deploy on every push to your main branch. You can disable this in Render Dashboard → Settings → Manual Deploys Only.


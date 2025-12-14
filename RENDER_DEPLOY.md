# Render Deployment Guide - Frontend + Backend

## Setup Steps

### 1. Local Testing (Optional)
```bash
# Build frontend
cd frontend
npm install
npm run build
cd ..

# Collect static files
python manage.py collectstatic --no-input

# Run server
python manage.py runserver
```

Visit: http://localhost:8000

### 2. Push to GitHub
```bash
git add .
git commit -m "Configure frontend + backend deployment"
git push origin main
```

### 3. Render Dashboard Setup

#### Create PostgreSQL Database
1. Go to Render Dashboard
2. Click "New +" → "PostgreSQL"
3. Name: `insightstream-db`
4. Click "Create Database"
5. Copy the "Internal Database URL"

#### Create Web Service
1. Click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure:
   - **Name**: `insightstream`
   - **Environment**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn insightstream.wsgi:application`

#### Add Environment Variables
```
DATABASE_URL = [paste Internal Database URL]
SECRET_KEY = [generate random string]
DEBUG = False
ALLOWED_HOSTS = .onrender.com
CORS_ALLOWED_ORIGINS = https://your-app.onrender.com

# API Keys
GEMINI_API_KEY_1 = your_key
GEMINI_API_KEY_2 = your_key
GEMINI_API_KEY_3 = your_key
YOUTUBE_API_KEY_1 = your_key
YOUTUBE_API_KEY_2 = your_key
YOUTUBE_API_KEY_3 = your_key
REPLICATE_API_TOKEN = your_token
IMAGEKIT_PUBLIC_KEY = your_key
IMAGEKIT_PRIVATE_KEY = your_key
IMAGEKIT_URL_ENDPOINT = your_endpoint

# Redis (Optional)
REDIS_URL = redis://...

# Admin
ADMIN_USERNAME = admin
ADMIN_PASSWORD = your_secure_password
```

### 4. Deploy
Click "Create Web Service" - Render will:
1. Install Python dependencies
2. Build frontend (npm install + build)
3. Collect static files
4. Run migrations
5. Start Gunicorn server

### 5. Verify Deployment
- Frontend: `https://your-app.onrender.com/`
- API Root: `https://your-app.onrender.com/api/`
- Admin: `https://your-app.onrender.com/admin/`

## How It Works

1. **Build Process** (`build.sh`):
   - Installs Python packages
   - Builds React frontend → `frontend/dist/`
   - Collects all static files → `staticfiles/`
   - Runs database migrations

2. **Static Files**:
   - WhiteNoise serves static files
   - Frontend assets from `frontend/dist/assets/`
   - Django static files from `staticfiles/`

3. **Routing**:
   - `/api/*` → Django REST API
   - `/admin/` → Django Admin
   - All other routes → React frontend (index.html)

## Troubleshooting

### Blank Page Issue
- Check Render logs: "Logs" tab in dashboard
- Verify frontend built: Look for "Frontend built successfully!" in logs
- Check static files: Look for "X static files copied"

### Build Fails
```bash
# Test locally first
chmod +x build.sh
./build.sh
```

### Frontend Not Loading
- Ensure `frontend/dist/index.html` exists after build
- Check TEMPLATES DIRS in settings.py
- Verify STATICFILES_DIRS includes frontend/dist/assets

### API Not Working
- Check CORS settings
- Verify DATABASE_URL is set
- Check API keys are configured

## Update Deployment
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render auto-deploys on push!

## Local Development

**Option 1: Separate (Recommended)**
```bash
# Terminal 1 - Backend
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Option 2: Together**
```bash
cd frontend && npm run build && cd ..
python manage.py collectstatic --no-input
python manage.py runserver
```

## Production URLs
- **Frontend**: https://insightstream-cyoz.onrender.com
- **API**: https://insightstream-cyoz.onrender.com/api/
- **Admin**: https://insightstream-cyoz.onrender.com/admin/

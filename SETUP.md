# InsightStream Django Setup Guide

## Prerequisites

- Python 3.10+
- PostgreSQL (or Neon account)
- Redis server

## Installation Steps

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Required variables:
- `DATABASE_URL` - PostgreSQL connection string
- `REDIS_URL` - Redis connection string
- `SECRET_KEY` - Django secret key
- `GEMINI_API_KEY_1`, `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3` - Google Gemini API keys
- `REPLICATE_API_TOKEN` - Replicate API token
- `YOUTUBE_API_KEY_1`, `YOUTUBE_API_KEY_2`, `YOUTUBE_API_KEY_3` - YouTube Data API keys
- `IMAGEKIT_PUBLIC_KEY`, `IMAGEKIT_PRIVATE_KEY`, `IMAGEKIT_URL_ENDPOINT` - ImageKit credentials
- `ADMIN_USERNAME`, `ADMIN_PASSWORD` - Admin dashboard credentials

### 3. Database Setup

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

### 5. Run Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### 6. Start Celery Worker (Optional)

For background tasks:

```bash
celery -A insightstream worker -l info
```

## Testing the API

### 1. Register a User

```bash
curl -X POST http://localhost:8000/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "username": "testuser", "password": "testpass123"}'
```

### 2. Login

```bash
curl -X POST http://localhost:8000/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpass123"}'
```

Save the `access` token from the response.

### 3. Generate Thumbnail

```bash
curl -X POST http://localhost:8000/api/thumbnails/generate/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"user_input": "A futuristic city at sunset"}'
```

### 4. Generate Content

```bash
curl -X POST http://localhost:8000/api/content/generate/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"topic": "Python programming tutorials"}'
```

### 5. Research Keywords

```bash
curl -X POST http://localhost:8000/api/keywords/research/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"topic": "Web development"}'
```

### 6. Generate Hashtags

```bash
curl -X POST http://localhost:8000/api/hashtags/generate/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN" \
  -d '{"topic": "Gaming"}'
```

### 7. Search Thumbnails

```bash
curl -X GET "http://localhost:8000/api/analytics/thumbnail-search/?query=python+tutorial" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 8. Detect Outliers

```bash
curl -X GET "http://localhost:8000/api/analytics/outlier/?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

### 9. Analyze Upload Streak

```bash
curl -X GET "http://localhost:8000/api/analytics/upload-streak/?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

## Admin Dashboard

Access the Django admin at `http://localhost:8000/admin/`

Use the admin API:

```bash
# Login
curl -X POST http://localhost:8000/api/admin-dashboard/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "your_admin_password"}'

# Get Stats (requires session cookie from login)
curl -X GET http://localhost:8000/api/admin-dashboard/stats/ \
  --cookie "sessionid=YOUR_SESSION_ID"
```

## Project Structure

```
insightstream/
├── apps/
│   ├── users/          # User authentication
│   ├── thumbnails/     # AI thumbnail generation
│   ├── content/        # AI content generation
│   ├── keywords/       # Keyword research
│   ├── hashtags/       # Trending hashtags
│   ├── analytics/      # Analytics features
│   └── admin_dashboard/ # Admin panel
├── core/
│   ├── clients/        # External API clients
│   └── utils/          # Utility functions
└── insightstream/      # Django settings
```

## Features Implemented

✅ User authentication (JWT)
✅ AI thumbnail generation (FLUX + Pollinations fallback)
✅ AI content generation (3 concepts with SEO scores)
✅ Keyword research (AI + YouTube trending data)
✅ Trending hashtags (real + AI-generated)
✅ Thumbnail search (text + image similarity)
✅ Outlier detection (IQR + SmartScore algorithm)
✅ Upload streak analyzer (algorithm score 0-100)
✅ Admin dashboard (stats + user management)
✅ API key rotation and retry logic
✅ Comprehensive error handling
✅ Caching for performance

## Next Steps

1. Set up production environment variables
2. Configure CORS for your frontend domain
3. Set up SSL/TLS certificates
4. Configure production database (PostgreSQL)
5. Set up Redis for production
6. Deploy to your hosting platform
7. Monitor API usage and rate limits
8. Set up logging and monitoring

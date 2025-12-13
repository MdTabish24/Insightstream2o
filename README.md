# InsightStream Django Backend

A comprehensive YouTube analytics and content creation platform built with Django. Provides AI-powered tools for thumbnail generation, content optimization, keyword research, and advanced analytics.

## 🚀 Features

- **User Authentication**: JWT-based authentication with token refresh
- **AI Thumbnail Generator**: Generate professional thumbnails using FLUX AI with Pollinations fallback
- **AI Content Generator**: Create 3 unique video concepts with SEO scores
- **Keyword Research**: Combine AI and real YouTube trending data
- **Trending Hashtags**: Extract real hashtags and generate AI suggestions
- **Thumbnail Search**: Text-based and image similarity search
- **Outlier Detection**: Identify best/worst performing videos using IQR method
- **Upload Streak Analyzer**: Calculate algorithm score (0-100) and get recommendations
- **Admin Dashboard**: Platform statistics and user management

## 🛠️ Tech Stack

- **Framework**: Django 5.0 + Django REST Framework
- **Database**: PostgreSQL (Neon)
- **Cache**: Redis
- **Authentication**: JWT (SimpleJWT)
- **AI Services**: Google Gemini, Replicate FLUX, Pollinations
- **External APIs**: YouTube Data API v3, ImageKit CDN
- **Background Tasks**: Celery
- **Production Server**: Gunicorn

## 📋 Prerequisites

- Python 3.10+
- PostgreSQL
- Redis
- API Keys:
  - Google Gemini API
  - Replicate API
  - YouTube Data API v3
  - ImageKit CDN

## 🔧 Installation

### 1. Clone Repository

```bash
git clone https://github.com/RainaMishra1/InsightStream2o.git
cd InsightStream2o
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Setup

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Required variables:
- `DATABASE_URL` - PostgreSQL connection
- `REDIS_URL` - Redis connection
- `SECRET_KEY` - Django secret key
- `GEMINI_API_KEY_1`, `GEMINI_API_KEY_2`, `GEMINI_API_KEY_3`
- `YOUTUBE_API_KEY_1`, `YOUTUBE_API_KEY_2`, `YOUTUBE_API_KEY_3`
- `REPLICATE_API_TOKEN`
- `IMAGEKIT_PUBLIC_KEY`, `IMAGEKIT_PRIVATE_KEY`, `IMAGEKIT_URL_ENDPOINT`
- `ADMIN_USERNAME`, `ADMIN_PASSWORD`

### 4. Database Setup

```bash
python manage.py migrate
```

### 5. Run Development Server

```bash
python manage.py runserver
```

API available at: `http://localhost:8000`

## 📚 API Documentation

See [API_ENDPOINTS.md](API_ENDPOINTS.md) for complete API documentation.

### Quick Examples

**Register User:**
```bash
POST /api/users/register/
{
  "email": "user@example.com",
  "username": "username",
  "password": "password123"
}
```

**Generate Thumbnail:**
```bash
POST /api/thumbnails/generate/
Authorization: Bearer <token>
{
  "user_input": "A futuristic city at sunset"
}
```

**Generate Content:**
```bash
POST /api/content/generate/
Authorization: Bearer <token>
{
  "topic": "Python programming"
}
```

**Detect Outliers:**
```bash
GET /api/analytics/outlier/?channel_id=UC_x5XG1OV2P6uZZ5FSM9Ttw
Authorization: Bearer <token>
```

## 🚀 Deployment

### Deploy to Render

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

Quick steps:
1. Push to GitHub
2. Create PostgreSQL database on Render
3. Create Web Service on Render
4. Add environment variables
5. Deploy!

Your API will be live at: `https://your-app.onrender.com`

## 📁 Project Structure

```
insightstream/
├── apps/
│   ├── users/              # User authentication
│   ├── thumbnails/         # AI thumbnail generation
│   ├── content/            # AI content generation
│   ├── keywords/           # Keyword research
│   ├── hashtags/           # Trending hashtags
│   ├── analytics/          # Analytics features
│   └── admin_dashboard/    # Admin panel
├── core/
│   ├── clients/            # External API clients
│   │   ├── gemini.py       # Google Gemini AI
│   │   ├── replicate.py    # Replicate FLUX
│   │   ├── pollinations.py # Pollinations AI
│   │   ├── youtube.py      # YouTube Data API
│   │   └── imagekit.py     # ImageKit CDN
│   └── utils/              # Utility functions
│       ├── api_key_manager.py  # API key rotation
│       └── retry.py        # Retry logic
└── insightstream/          # Django settings
```

## 🔐 Security Features

- JWT authentication with token blacklist
- API key rotation for rate limit handling
- HTTPS enforcement in production
- CORS configuration
- Input validation on all endpoints
- Secure password hashing
- Environment-based configuration

## 🎯 Key Features Explained

### SmartScore Algorithm
Combines multiple metrics for video performance:
- 50% Views (normalized)
- 30% Velocity (views per day)
- 20% Engagement (likes + comments)

### Outlier Detection
Uses IQR (Interquartile Range) method:
- High outliers: Score > Q3 + 1.5×IQR
- Low outliers: Score < Q1 - 1.5×IQR

### Algorithm Score (0-100)
Upload consistency analysis:
- 40% Consistency score
- 30% Frequency score
- 30% Engagement score

### API Key Rotation
Automatic rotation when rate limits hit:
- Multiple keys per service
- Automatic failover
- Exhaustion detection

## 🧪 Testing

```bash
# Run tests
python manage.py test

# Run specific app tests
python manage.py test apps.users
```

## 📊 Monitoring

- Check logs in Render dashboard
- Monitor API usage and rate limits
- Track database performance
- Review error logs

## 🤝 Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open Pull Request

## 📝 License

This project is licensed under the MIT License.

## 👥 Authors

- Raina Mishra - [GitHub](https://github.com/RainaMishra1)

## 🙏 Acknowledgments

- Google Gemini AI for content generation
- Replicate for FLUX image generation
- YouTube Data API for video analytics
- ImageKit for CDN services

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
- Review [API_ENDPOINTS.md](API_ENDPOINTS.md) for API documentation

## 🔄 Updates

To update your deployment:
```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render will automatically deploy the updates!

---

**Live API**: `https://insightstream-api.onrender.com`

**Status**: ✅ Production Ready

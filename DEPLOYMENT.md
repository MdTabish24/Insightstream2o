# InsightStream Django - GitHub & Render Deployment Guide

## Part 1: Push to GitHub

### Step 1: Initialize Git Repository (if not already done)

```bash
git init
```

### Step 2: Add Remote Repository

```bash
git remote add origin https://github.com/RainaMishra1/InsightStream2o.git
```

### Step 3: Add All Files

```bash
git add .
```

### Step 4: Commit Changes

```bash
git commit -m "Initial commit: Complete InsightStream Django backend"
```

### Step 5: Push to GitHub

```bash
git branch -M main
git push -u origin main
```

If you get authentication errors, you may need to:
- Use a Personal Access Token (PAT) instead of password
- Or use SSH keys

**To create a PAT:**
1. Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Generate new token with `repo` scope
3. Use the token as your password when pushing

---

## Part 2: Deploy on Render

### Step 1: Create Render Account

1. Go to [render.com](https://render.com)
2. Sign up or log in
3. Connect your GitHub account

### Step 2: Create PostgreSQL Database

1. Click **"New +"** → **"PostgreSQL"**
2. Configure:
   - **Name**: `insightstream-db`
   - **Database**: `insightstream`
   - **User**: `insightstream`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for production)
3. Click **"Create Database"**
4. Wait for database to be created
5. **Save the Internal Database URL** (you'll need this)

### Step 3: Create Redis Instance (Optional but Recommended)

1. Click **"New +"** → **"Redis"**
2. Configure:
   - **Name**: `insightstream-redis`
   - **Region**: Same as database
   - **Plan**: Free (or paid)
3. Click **"Create Redis"**
4. **Save the Internal Redis URL**

### Step 4: Create Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `RainaMishra1/InsightStream2o`
3. Configure:
   - **Name**: `insightstream-api`
   - **Region**: Same as database
   - **Branch**: `main`
   - **Root Directory**: Leave empty
   - **Runtime**: `Python 3`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn insightstream.wsgi:application`
   - **Plan**: Free (or paid for production)

### Step 5: Add Environment Variables

In the **Environment** section, add these variables:

#### Required Variables:

```
SECRET_KEY=<generate-a-random-secret-key>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<your-postgres-internal-url>
REDIS_URL=<your-redis-internal-url>

# Admin Credentials
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<your-secure-admin-password>

# API Keys - Gemini
GEMINI_API_KEY_1=<your-gemini-key-1>
GEMINI_API_KEY_2=<your-gemini-key-2>
GEMINI_API_KEY_3=<your-gemini-key-3>

# API Keys - YouTube
YOUTUBE_API_KEY_1=<your-youtube-key-1>
YOUTUBE_API_KEY_2=<your-youtube-key-2>
YOUTUBE_API_KEY_3=<your-youtube-key-3>

# API Keys - Replicate
REPLICATE_API_TOKEN=<your-replicate-token>

# API Keys - ImageKit
IMAGEKIT_PUBLIC_KEY=<your-imagekit-public-key>
IMAGEKIT_PRIVATE_KEY=<your-imagekit-private-key>
IMAGEKIT_URL_ENDPOINT=<your-imagekit-url-endpoint>

# CORS (add your frontend domain)
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com,http://localhost:3000
```

**To generate SECRET_KEY:**
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 6: Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Clone your repository
   - Install dependencies
   - Run migrations
   - Collect static files
   - Start the server

### Step 7: Monitor Deployment

1. Watch the **Logs** tab for any errors
2. Wait for "Build successful" and "Deploy live" messages
3. Your API will be available at: `https://insightstream-api.onrender.com`

---

## Part 3: Post-Deployment Setup

### Step 1: Test the API

```bash
# Health check
curl https://insightstream-api.onrender.com/api/users/register/

# Register a user
curl -X POST https://insightstream-api.onrender.com/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "username": "testuser", "password": "testpass123"}'
```

### Step 2: Create Superuser (Optional)

1. Go to Render Dashboard → Your Web Service
2. Click **"Shell"** tab
3. Run:
```bash
python manage.py createsuperuser
```

### Step 3: Access Admin Panel

Visit: `https://insightstream-api.onrender.com/admin/`

---

## Part 4: Continuous Deployment

Render automatically deploys when you push to GitHub:

```bash
# Make changes to your code
git add .
git commit -m "Your commit message"
git push origin main
```

Render will automatically:
1. Detect the push
2. Build the new version
3. Run migrations
4. Deploy the update

---

## Part 5: Environment-Specific Settings

### For Development (.env file):
```
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=postgresql://user:password@localhost:5432/insightstream
REDIS_URL=redis://localhost:6379/0
```

### For Production (Render Environment Variables):
```
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<render-postgres-url>
REDIS_URL=<render-redis-url>
```

---

## Part 6: Troubleshooting

### Build Fails

**Check logs for:**
- Missing dependencies → Update `requirements.txt`
- Python version issues → Specify in `render.yaml`
- Build script errors → Check `build.sh` permissions

**Fix build.sh permissions:**
```bash
chmod +x build.sh
git add build.sh
git commit -m "Fix build.sh permissions"
git push
```

### Database Connection Issues

1. Verify `DATABASE_URL` is set correctly
2. Check database is in same region as web service
3. Use **Internal Database URL** (not external)

### Static Files Not Loading

1. Check `STATIC_ROOT` in settings.py
2. Verify `whitenoise` is in `MIDDLEWARE`
3. Run `python manage.py collectstatic` in build script

### API Keys Not Working

1. Verify all API keys are set in Environment Variables
2. Check for typos in variable names
3. Ensure keys have proper permissions/quotas

### CORS Errors

Add your frontend domain to `CORS_ALLOWED_ORIGINS`:
```
CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000
```

---

## Part 7: Scaling & Performance

### Free Tier Limitations

- Web service spins down after 15 minutes of inactivity
- First request after spin-down takes ~30 seconds
- 750 hours/month free

### Upgrade to Paid Plan for:

- Always-on service (no spin-down)
- More CPU and RAM
- Custom domains
- Better performance

### Performance Tips

1. **Enable Caching**: Redis is already configured
2. **Database Indexing**: Add indexes to frequently queried fields
3. **API Rate Limiting**: Implement rate limiting for public endpoints
4. **CDN**: Use ImageKit CDN for images (already configured)
5. **Background Tasks**: Use Celery for long-running tasks

---

## Part 8: Monitoring & Maintenance

### Monitor Logs

```bash
# View recent logs
render logs --tail

# Follow logs in real-time
render logs --follow
```

### Database Backups

Render automatically backs up PostgreSQL databases:
- Free tier: 7 days retention
- Paid tiers: 30+ days retention

### Update Dependencies

```bash
pip install --upgrade <package-name>
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

## Part 9: API Documentation

Your API will be available at:
- **Base URL**: `https://insightstream-api.onrender.com`
- **Admin Panel**: `https://insightstream-api.onrender.com/admin/`
- **API Endpoints**: See `API_ENDPOINTS.md`

### Example Frontend Integration

```javascript
const API_BASE_URL = 'https://insightstream-api.onrender.com';

// Register user
const response = await fetch(`${API_BASE_URL}/api/users/register/`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    username: 'username',
    password: 'password123'
  })
});

const data = await response.json();
const accessToken = data.access;

// Use token for authenticated requests
const thumbnailResponse = await fetch(`${API_BASE_URL}/api/thumbnails/generate/`, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${accessToken}`
  },
  body: JSON.stringify({
    user_input: 'A futuristic city'
  })
});
```

---

## Part 10: Security Checklist

- ✅ `DEBUG=False` in production
- ✅ Strong `SECRET_KEY`
- ✅ HTTPS enabled (automatic on Render)
- ✅ CORS configured for your frontend only
- ✅ Environment variables for sensitive data
- ✅ Database credentials secured
- ✅ API keys rotated regularly
- ✅ Admin password is strong
- ✅ Rate limiting implemented
- ✅ Input validation on all endpoints

---

## Support

If you encounter issues:
1. Check Render logs
2. Review Django error messages
3. Verify environment variables
4. Check API key quotas
5. Review CORS settings

For Render-specific issues: [Render Documentation](https://render.com/docs)

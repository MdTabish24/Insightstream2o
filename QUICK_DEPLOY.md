# Quick Deployment Commands

## 1. Push to GitHub

```bash
# Initialize git (if needed)
git init

# Add remote
git remote add origin https://github.com/RainaMishra1/InsightStream2o.git

# Add all files
git add .

# Commit
git commit -m "Initial commit: Complete InsightStream Django backend"

# Push to GitHub
git branch -M main
git push -u origin main
```

## 2. Make build.sh Executable

```bash
chmod +x build.sh
git add build.sh
git commit -m "Make build.sh executable"
git push
```

## 3. Render Setup (Manual Steps)

### A. Create PostgreSQL Database
1. Go to render.com → New + → PostgreSQL
2. Name: `insightstream-db`
3. Copy Internal Database URL

### B. Create Redis (Optional)
1. Go to render.com → New + → Redis
2. Name: `insightstream-redis`
3. Copy Internal Redis URL

### C. Create Web Service
1. Go to render.com → New + → Web Service
2. Connect GitHub repo: `RainaMishra1/InsightStream2o`
3. Settings:
   - **Name**: `insightstream-api`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn insightstream.wsgi:application`

### D. Add Environment Variables

**Required:**
```
SECRET_KEY=<generate-random-key>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<postgres-internal-url>
REDIS_URL=<redis-internal-url>
ADMIN_USERNAME=admin
ADMIN_PASSWORD=<secure-password>
```

**API Keys:**
```
GEMINI_API_KEY_1=<key>
GEMINI_API_KEY_2=<key>
GEMINI_API_KEY_3=<key>
YOUTUBE_API_KEY_1=<key>
YOUTUBE_API_KEY_2=<key>
YOUTUBE_API_KEY_3=<key>
REPLICATE_API_TOKEN=<token>
IMAGEKIT_PUBLIC_KEY=<key>
IMAGEKIT_PRIVATE_KEY=<key>
IMAGEKIT_URL_ENDPOINT=<endpoint>
```

**CORS (add your frontend):**
```
CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000
```

### E. Deploy
Click "Create Web Service" and wait for deployment.

## 4. Generate SECRET_KEY

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

## 5. Test Deployment

```bash
# Test registration
curl -X POST https://insightstream-api.onrender.com/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "username": "testuser", "password": "testpass123"}'
```

## 6. Future Updates

```bash
# Make changes
git add .
git commit -m "Your changes"
git push origin main
# Render auto-deploys!
```

## Your API URL
`https://insightstream-api.onrender.com`

## Admin Panel
`https://insightstream-api.onrender.com/admin/`

## Common Issues

**Build fails?**
```bash
chmod +x build.sh
git add build.sh
git commit -m "Fix permissions"
git push
```

**Database connection fails?**
- Use Internal Database URL (not external)
- Check DATABASE_URL environment variable

**CORS errors?**
- Add your frontend domain to CORS_ALLOWED_ORIGINS

**API keys not working?**
- Verify all keys are set in Render environment variables
- Check for typos in variable names

# InsightStream Django - Deployment Guide (हिंदी में)

## 📱 GitHub पर Push करने के Steps

### Step 1: Git Initialize करें (अगर पहले से नहीं है)

```bash
git init
```

### Step 2: GitHub Repository Add करें

```bash
git remote add origin https://github.com/RainaMishra1/InsightStream2o.git
```

### Step 3: सभी Files Add करें

```bash
git add .
```

### Step 4: Commit करें

```bash
git commit -m "Complete InsightStream Django backend"
```

### Step 5: GitHub पर Push करें

```bash
git branch -M main
git push -u origin main
```

**Note**: अगर password मांगे तो GitHub Personal Access Token use करें।

---

## 🚀 Render पर Deploy करने के Steps

### Step 1: Render Account बनाएं

1. [render.com](https://render.com) पर जाएं
2. Sign up करें या Login करें
3. GitHub account connect करें

### Step 2: PostgreSQL Database बनाएं

1. **"New +"** → **"PostgreSQL"** पर click करें
2. Settings:
   - **Name**: `insightstream-db`
   - **Database**: `insightstream`
   - **Region**: अपने location के पास वाला select करें
   - **Plan**: Free (या paid)
3. **"Create Database"** पर click करें
4. **Internal Database URL** को copy करके save कर लें

### Step 3: Redis बनाएं (Optional)

1. **"New +"** → **"Redis"** पर click करें
2. Settings:
   - **Name**: `insightstream-redis`
   - **Region**: Database जैसा ही
   - **Plan**: Free
3. **"Create Redis"** पर click करें
4. **Internal Redis URL** copy करें

### Step 4: Web Service बनाएं

1. **"New +"** → **"Web Service"** पर click करें
2. अपनी GitHub repository select करें: `RainaMishra1/InsightStream2o`
3. Settings:
   - **Name**: `insightstream-api`
   - **Region**: Database जैसा ही
   - **Branch**: `main`
   - **Build Command**: `./build.sh`
   - **Start Command**: `gunicorn insightstream.wsgi:application`
   - **Plan**: Free (या paid)

### Step 5: Environment Variables Add करें

**Environment** section में ये variables add करें:

```
SECRET_KEY=<random-secret-key-generate-karein>
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=<postgres-internal-url>
REDIS_URL=<redis-internal-url>

ADMIN_USERNAME=admin
ADMIN_PASSWORD=<strong-password>

GEMINI_API_KEY_1=<your-key>
GEMINI_API_KEY_2=<your-key>
GEMINI_API_KEY_3=<your-key>

YOUTUBE_API_KEY_1=<your-key>
YOUTUBE_API_KEY_2=<your-key>
YOUTUBE_API_KEY_3=<your-key>

REPLICATE_API_TOKEN=<your-token>

IMAGEKIT_PUBLIC_KEY=<your-key>
IMAGEKIT_PRIVATE_KEY=<your-key>
IMAGEKIT_URL_ENDPOINT=<your-endpoint>

CORS_ALLOWED_ORIGINS=https://your-frontend.com,http://localhost:3000
```

**SECRET_KEY generate करने के लिए:**
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Step 6: Deploy करें

1. **"Create Web Service"** पर click करें
2. Logs देखें - build होने में 5-10 minutes लगेंगे
3. "Deploy live" message आने का wait करें
4. आपका API live हो जाएगा: `https://insightstream-api.onrender.com`

---

## ✅ Test करें

### Registration Test:

```bash
curl -X POST https://insightstream-api.onrender.com/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "username": "test", "password": "test123"}'
```

### Login Test:

```bash
curl -X POST https://insightstream-api.onrender.com/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'
```

---

## 🔄 Future Updates के लिए

जब भी code में changes करें:

```bash
git add .
git commit -m "Your changes"
git push origin main
```

Render automatically deploy कर देगा! 🎉

---

## 📱 Quick Commands (Copy-Paste करें)

### 1. GitHub पर Push करने के लिए:

```bash
git init
git remote add origin https://github.com/RainaMishra1/InsightStream2o.git
chmod +x build.sh
git add .
git commit -m "Complete InsightStream Django backend"
git branch -M main
git push -u origin main
```

### 2. SECRET_KEY Generate करने के लिए:

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 🎯 Important URLs

- **GitHub Repo**: https://github.com/RainaMishra1/InsightStream2o
- **Render Dashboard**: https://dashboard.render.com
- **Your API** (deploy के बाद): https://insightstream-api.onrender.com
- **Admin Panel**: https://insightstream-api.onrender.com/admin/

---

## ❓ Common Problems और Solutions

### Problem 1: Build fail हो रहा है

**Solution:**
```bash
chmod +x build.sh
git add build.sh
git commit -m "Fix build.sh permissions"
git push
```

### Problem 2: Database connect नहीं हो रहा

**Solution:**
- Internal Database URL use करें (External नहीं)
- DATABASE_URL environment variable check करें
- Database और Web Service same region में हों

### Problem 3: CORS error आ रहा है

**Solution:**
- CORS_ALLOWED_ORIGINS में अपना frontend domain add करें
- Example: `CORS_ALLOWED_ORIGINS=https://myapp.com,http://localhost:3000`

### Problem 4: API keys काम नहीं कर रहे

**Solution:**
- सभी API keys Render environment variables में add करें
- Variable names में typo check करें
- API keys की quota/limit check करें

---

## 📚 Documentation Files

- **README.md** - Project overview
- **DEPLOYMENT.md** - Detailed deployment guide (English)
- **QUICK_DEPLOY.md** - Quick reference
- **DEPLOYMENT_CHECKLIST.md** - Step-by-step checklist
- **API_ENDPOINTS.md** - All API endpoints
- **SETUP.md** - Local setup guide

---

## 🎉 Success!

अगर सब कुछ सही हो गया तो:
- ✅ आपका API live है
- ✅ सभी endpoints काम कर रहे हैं
- ✅ Frontend से connect हो सकता है
- ✅ Admin panel accessible है

---

## 💡 Tips

1. **Free Tier पर**: Service 15 minutes inactivity के बाद sleep हो जाती है
2. **First request**: Sleep के बाद पहली request में 30 seconds लग सकते हैं
3. **Paid Plan**: Always-on service के लिए paid plan upgrade करें
4. **Logs**: Render dashboard में logs check करते रहें
5. **Backups**: Database automatically backup होता है

---

## 📞 Help चाहिए?

1. Render logs check करें
2. DEPLOYMENT.md पढ़ें
3. GitHub पर issue create करें
4. Render documentation देखें: [render.com/docs](https://render.com/docs)

---

**Happy Deploying! 🚀**

अगर कोई problem आए तो documentation files check करें या GitHub पर issue create करें।

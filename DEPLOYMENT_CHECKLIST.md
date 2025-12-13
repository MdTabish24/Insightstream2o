# Deployment Checklist ✅

## Pre-Deployment

- [ ] All code is committed and tested locally
- [ ] `.env` file is NOT committed (in `.gitignore`)
- [ ] `requirements.txt` is up to date
- [ ] `build.sh` has execute permissions (`chmod +x build.sh`)
- [ ] All API keys are ready
- [ ] Database backup created (if migrating)

## GitHub Setup

- [ ] Repository created: `https://github.com/RainaMishra1/InsightStream2o.git`
- [ ] Git initialized: `git init`
- [ ] Remote added: `git remote add origin <url>`
- [ ] All files added: `git add .`
- [ ] Initial commit: `git commit -m "Initial commit"`
- [ ] Pushed to GitHub: `git push -u origin main`

## Render - Database Setup

- [ ] PostgreSQL database created
- [ ] Database name: `insightstream-db`
- [ ] Internal Database URL copied
- [ ] Database is in correct region

## Render - Redis Setup (Optional)

- [ ] Redis instance created
- [ ] Redis name: `insightstream-redis`
- [ ] Internal Redis URL copied
- [ ] Redis is in same region as database

## Render - Web Service Setup

- [ ] Web service created
- [ ] GitHub repository connected
- [ ] Service name: `insightstream-api`
- [ ] Build command: `./build.sh`
- [ ] Start command: `gunicorn insightstream.wsgi:application`
- [ ] Python 3 runtime selected
- [ ] Same region as database

## Environment Variables

### Core Settings
- [ ] `SECRET_KEY` (generated)
- [ ] `DEBUG=False`
- [ ] `ALLOWED_HOSTS=.onrender.com`
- [ ] `DATABASE_URL` (from Render PostgreSQL)
- [ ] `REDIS_URL` (from Render Redis)

### Admin
- [ ] `ADMIN_USERNAME`
- [ ] `ADMIN_PASSWORD`

### Gemini API
- [ ] `GEMINI_API_KEY_1`
- [ ] `GEMINI_API_KEY_2`
- [ ] `GEMINI_API_KEY_3`

### YouTube API
- [ ] `YOUTUBE_API_KEY_1`
- [ ] `YOUTUBE_API_KEY_2`
- [ ] `YOUTUBE_API_KEY_3`

### Replicate
- [ ] `REPLICATE_API_TOKEN`

### ImageKit
- [ ] `IMAGEKIT_PUBLIC_KEY`
- [ ] `IMAGEKIT_PRIVATE_KEY`
- [ ] `IMAGEKIT_URL_ENDPOINT`

### CORS
- [ ] `CORS_ALLOWED_ORIGINS` (add your frontend domain)

## Deployment

- [ ] "Create Web Service" clicked
- [ ] Build logs monitored
- [ ] Build successful
- [ ] Migrations ran successfully
- [ ] Static files collected
- [ ] Service is live

## Post-Deployment Testing

### Basic Tests
- [ ] API is accessible: `https://your-app.onrender.com`
- [ ] Health check works
- [ ] Admin panel accessible: `https://your-app.onrender.com/admin/`

### User Authentication
- [ ] User registration works
- [ ] User login works
- [ ] JWT tokens are issued
- [ ] Protected endpoints require authentication

### AI Features
- [ ] Thumbnail generation works
- [ ] Content generation works
- [ ] Keyword research works
- [ ] Hashtag generation works

### Analytics
- [ ] Thumbnail search works
- [ ] Outlier detection works
- [ ] Upload streak analysis works

### Admin
- [ ] Admin login works
- [ ] Admin stats endpoint works

## Security Verification

- [ ] `DEBUG=False` in production
- [ ] HTTPS is enforced
- [ ] CORS is configured correctly
- [ ] API keys are not exposed in code
- [ ] Strong admin password set
- [ ] Database credentials secured

## Performance Optimization

- [ ] Redis caching enabled
- [ ] Static files served via WhiteNoise
- [ ] Database indexes added (if needed)
- [ ] API rate limiting configured

## Monitoring Setup

- [ ] Render logs accessible
- [ ] Error tracking configured
- [ ] Database backups enabled
- [ ] Uptime monitoring (optional)

## Documentation

- [ ] README.md updated
- [ ] API_ENDPOINTS.md available
- [ ] DEPLOYMENT.md available
- [ ] Environment variables documented

## Frontend Integration

- [ ] Frontend has correct API URL
- [ ] CORS allows frontend domain
- [ ] Authentication flow tested
- [ ] All API endpoints tested from frontend

## Continuous Deployment

- [ ] Auto-deploy on push enabled
- [ ] Build notifications configured
- [ ] Deployment process documented

## Backup & Recovery

- [ ] Database backup strategy in place
- [ ] Environment variables backed up securely
- [ ] Recovery procedure documented

## Final Checks

- [ ] All features working in production
- [ ] No errors in logs
- [ ] Performance is acceptable
- [ ] API response times are good
- [ ] All team members have access

---

## Quick Test Commands

```bash
# Test registration
curl -X POST https://your-app.onrender.com/api/users/register/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "username": "test", "password": "test123"}'

# Test login
curl -X POST https://your-app.onrender.com/api/users/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "test123"}'

# Test protected endpoint (use token from login)
curl -X GET https://your-app.onrender.com/api/users/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

---

## If Something Goes Wrong

### Build Fails
1. Check build logs in Render
2. Verify `build.sh` has execute permissions
3. Check `requirements.txt` for errors
4. Verify Python version compatibility

### Database Connection Fails
1. Verify `DATABASE_URL` is correct
2. Use Internal Database URL (not external)
3. Check database is in same region
4. Verify database is running

### API Keys Not Working
1. Check environment variables are set
2. Verify no typos in variable names
3. Check API key quotas/limits
4. Test keys locally first

### CORS Errors
1. Add frontend domain to `CORS_ALLOWED_ORIGINS`
2. Include protocol (https://)
3. Restart service after changes

---

## Success Criteria

✅ API is live and accessible
✅ All endpoints return expected responses
✅ Authentication works correctly
✅ AI features generate content
✅ Analytics provide insights
✅ Admin panel is functional
✅ No errors in production logs
✅ Frontend can connect successfully

---

## Next Steps After Deployment

1. Monitor logs for first 24 hours
2. Test all features thoroughly
3. Set up monitoring/alerting
4. Document any issues
5. Plan for scaling if needed
6. Set up staging environment
7. Configure custom domain (optional)
8. Set up SSL certificate (automatic on Render)

---

**Deployment Date**: _____________

**Deployed By**: _____________

**Production URL**: https://insightstream-api.onrender.com

**Status**: ⬜ Not Started | ⬜ In Progress | ⬜ Complete

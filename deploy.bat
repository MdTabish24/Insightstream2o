@echo off
echo 🚀 Deploying InsightStream to Render...

echo 📝 Adding changes to git...
git add .

echo 💾 Committing changes...
set /p message="Enter commit message (or press Enter for default): "
if "%message%"=="" set message=Update deployment

git commit -m "%message%"

echo 📤 Pushing to GitHub...
git push origin main

echo ✅ Deployment triggered! Check Render dashboard for progress.
echo 🌐 Your API will be live at: https://insightstream-api.onrender.com

pause
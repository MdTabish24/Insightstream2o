@echo off
echo ========================================
echo   InsightStream - Deploy to Render
echo ========================================
echo.

echo [1/4] Building frontend...
cd frontend
call npm install
call npm run build
cd ..
echo ✓ Frontend built successfully!
echo.

echo [2/4] Collecting static files...
python manage.py collectstatic --no-input
echo ✓ Static files collected!
echo.

echo [3/4] Committing changes...
git add .
set /p commit_msg="Enter commit message: "
git commit -m "%commit_msg%"
echo ✓ Changes committed!
echo.

echo [4/4] Pushing to GitHub...
git push origin main
echo ✓ Pushed to GitHub!
echo.

echo ========================================
echo   Deployment initiated!
echo   Check Render dashboard for progress
echo ========================================
pause

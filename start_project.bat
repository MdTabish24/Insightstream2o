@echo off
echo ========================================
echo   InsightStream - Starting Project
echo ========================================
echo.

echo [1/3] Clearing cache and resetting API keys...
python clear_cache.py
echo.

echo [2/3] Starting Django Backend on http://localhost:8000
start "Django Backend" cmd /k "python manage.py runserver"
timeout /t 3 /nobreak >nul
echo.

echo [3/3] Starting React Frontend on http://localhost:5173
start "React Frontend" cmd /k "cd frontend && npm run dev"
echo.

echo ========================================
echo   Both servers are starting!
echo   Backend:  http://localhost:8000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
echo Press any key to exit this window...
pause >nul

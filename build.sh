#!/usr/bin/env bash
# exit on error
set -o errexit

echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "🎨 Building frontend..."
if [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
    cd frontend
    npm install
    npm run build
    cd ..
    echo "✅ Frontend built successfully!"
else
    echo "⚠️  No frontend found, skipping..."
fi

echo "🎨 Collecting static files..."
python manage.py collectstatic --no-input

echo "🗄️ Running database migrations..."
python manage.py migrate

echo "✅ Build complete!"

#!/bin/bash

# InsightStream Django - Quick Deploy Script
# This script will push your code to GitHub

echo "🚀 InsightStream Django Deployment Script"
echo "=========================================="
echo ""

# Check if git is initialized
if [ ! -d .git ]; then
    echo "📦 Initializing Git repository..."
    git init
fi

# Make build.sh executable
echo "🔧 Making build.sh executable..."
chmod +x build.sh

# Check if remote exists
if ! git remote | grep -q origin; then
    echo "🔗 Adding GitHub remote..."
    git remote add origin https://github.com/RainaMishra1/InsightStream2o.git
else
    echo "✅ GitHub remote already exists"
fi

# Add all files
echo "📝 Adding all files..."
git add .

# Commit
echo "💾 Committing changes..."
git commit -m "Deploy: Complete InsightStream Django backend with all features"

# Push to GitHub
echo "⬆️  Pushing to GitHub..."
git branch -M main
git push -u origin main

echo ""
echo "✅ Code pushed to GitHub successfully!"
echo ""
echo "📋 Next Steps:"
echo "1. Go to https://render.com"
echo "2. Create PostgreSQL database (name: insightstream-db)"
echo "3. Create Redis instance (name: insightstream-redis)"
echo "4. Create Web Service:"
echo "   - Connect GitHub repo: RainaMishra1/InsightStream2o"
echo "   - Build Command: ./build.sh"
echo "   - Start Command: gunicorn insightstream.wsgi:application"
echo "5. Add environment variables (see DEPLOYMENT.md)"
echo "6. Deploy!"
echo ""
echo "📚 Documentation:"
echo "   - Full guide: DEPLOYMENT.md"
echo "   - Quick guide: QUICK_DEPLOY.md"
echo "   - Checklist: DEPLOYMENT_CHECKLIST.md"
echo ""
echo "🎉 Happy deploying!"

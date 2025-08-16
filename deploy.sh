#!/bin/bash

echo "🚀 Starting Railway deployment..."

# Check if we're in the right directory
if [ ! -f "requirements-simple.txt" ]; then
    echo "❌ Error: requirements-simple.txt not found. Please run this from the project root."
    exit 1
fi

# Check if Dockerfile exists
if [ ! -f "Dockerfile" ]; then
    echo "❌ Error: Dockerfile not found."
    exit 1
fi

echo "✅ Files check passed"

# Create downloads directory if it doesn't exist
mkdir -p downloads

echo "📁 Created downloads directory"

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found. Please create one from sample.env"
    echo "   cp sample.env .env"
    echo "   Then edit .env with your actual values"
fi

echo "🔧 Environment check completed"

echo "✅ Ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Push your code to GitHub"
echo "2. Deploy to Railway from your GitHub repository"
echo "3. Set environment variables in Railway dashboard"
echo "4. Monitor the deployment logs"
echo ""
echo "🎵 Good luck with your Audify Music Bot deployment!"

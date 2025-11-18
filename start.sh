#!/bin/bash
# Quick start script for Agriculture Extension Chatbot

echo "🌾 Agriculture Extension Chatbot - Quick Start"
echo "=============================================="
echo ""

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose first."
    exit 1
fi

echo "✅ Docker and Docker Compose found"
echo ""

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo "📝 Creating .env file from template..."
    cp backend/.env.example backend/.env
    echo ""
    echo "⚠️  Please update backend/.env with your API keys:"
    echo "   - OPENAI_API_KEY"
    echo "   - AFRICAS_TALKING_API_KEY"
    echo "   - AFRICAS_TALKING_USERNAME"
    echo "   - WEATHER_API_KEY"
    echo ""
    echo "Edit the file and run this script again:"
    echo "  nano backend/.env"
    exit 1
fi

# Check if API keys are set
if grep -q "your_" backend/.env; then
    echo "⚠️  Some API keys are still not configured!"
    echo "Please update backend/.env with real API keys:"
    echo "  nano backend/.env"
    exit 1
fi

echo "✅ Environment configured"
echo ""

# Pull latest images
echo "📥 Pulling Docker images..."
docker-compose pull
echo ""

# Build and start services
echo "🚀 Starting services..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 10

# Check services
echo ""
echo "📊 Service Status:"
docker-compose ps

# Check backend health
echo ""
echo "🏥 Checking backend health..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Backend is healthy"
else
    echo "⏳ Backend still starting, checking logs..."
    docker-compose logs backend | tail -20
fi

echo ""
echo "=============================================="
echo "✅ Startup Complete!"
echo ""
echo "🌐 Access the application:"
echo "   Frontend:  http://localhost:3000"
echo "   Backend:   http://localhost:8000"
echo "   API Docs:  http://localhost:8000/docs"
echo ""
echo "📚 Documentation:"
echo "   Setup Guide:    docs/SETUP.md"
echo "   API Reference:  docs/API.md"
echo "   Deployment:     docs/DEPLOYMENT.md"
echo ""
echo "📋 Useful Commands:"
echo "   View logs:      docker-compose logs -f"
echo "   Stop services:  docker-compose down"
echo "   Reset database: docker-compose down -v"
echo ""
echo "🚀 Next steps:"
echo "   1. Open http://localhost:3000 in browser"
echo "   2. Test chat with the bot"
echo "   3. Configure Africa's Talking for SMS/USSD"
echo "   4. Add farmers and market prices via admin panel"
echo ""

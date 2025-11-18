@echo off
REM Quick start script for Windows
REM Agriculture Extension Chatbot

echo.
echo 🌾 Agriculture Extension Chatbot - Quick Start
echo =============================================
echo.

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ Docker not found. Please install Docker first.
    exit /b 1
)

echo ✅ Docker found
echo.

REM Check if .env exists
if not exist "backend\.env" (
    echo 📝 Creating .env file from template...
    copy backend\.env.example backend\.env
    echo.
    echo ⚠️  Please update backend\.env with your API keys:
    echo    - OPENAI_API_KEY
    echo    - AFRICAS_TALKING_API_KEY
    echo    - AFRICAS_TALKING_USERNAME
    echo    - WEATHER_API_KEY
    echo.
    echo Edit the file and run this script again:
    echo   notepad backend\.env
    exit /b 1
)

echo ✅ Environment configured
echo.

REM Start services
echo 🚀 Starting services...
docker-compose up -d

REM Wait for services
echo ⏳ Waiting for services to be ready...
timeout /t 10

REM Check services
echo.
echo 📊 Service Status:
docker-compose ps

echo.
echo =============================================
echo ✅ Startup Complete!
echo.
echo 🌐 Access the application:
echo    Frontend:  http://localhost:3000
echo    Backend:   http://localhost:8000
echo    API Docs:  http://localhost:8000/docs
echo.
echo 📚 Documentation:
echo    Setup Guide:    docs/SETUP.md
echo    API Reference:  docs/API.md
echo    Deployment:     docs/DEPLOYMENT.md
echo.
echo 📋 Useful Commands:
echo    View logs:      docker-compose logs -f
echo    Stop services:  docker-compose down
echo    Reset database: docker-compose down -v
echo.
echo 🚀 Next steps:
echo    1. Open http://localhost:3000 in browser
echo    2. Test chat with the bot
echo    3. Configure Africa's Talking for SMS/USSD
echo    4. Add farmers and market prices via admin panel
echo.

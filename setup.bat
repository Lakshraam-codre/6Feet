@echo off
REM Agriculture Extension Chatbot - Windows Setup Script
REM This script helps you configure your environment for local development

echo.
echo ========================================
echo Agriculture Extension Chatbot Setup
echo ========================================
echo.

REM Check if Docker is installed
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker is not installed!
    echo Please install Docker from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo [✓] Docker found: %errorlevel%

REM Check if Docker Compose is installed
docker-compose --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Docker Compose is not installed!
    echo Please install Docker Compose or update Docker Desktop
    pause
    exit /b 1
)
echo [✓] Docker Compose found

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Node.js is not installed!
    echo Please install from: https://nodejs.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('node --version') do set NODE_VERSION=%%i
echo [✓] Node.js found: %NODE_VERSION%

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [!] Python is not installed!
    echo Please install from: https://www.python.org/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo [✓] Python found: %PYTHON_VERSION%

echo.
echo ========================================
echo Step 1: Configuring Backend Environment
echo ========================================
echo.

REM Navigate to backend
cd backend

REM Check if .env exists
if exist .env (
    echo [!] .env already exists. Do you want to overwrite it? (Y/N)
    set /p overwrite=
    if /i not "%overwrite%"=="Y" (
        echo [✓] Keeping existing .env file
        goto skip_env
    )
)

REM Copy .env.example to .env
if exist .env.example (
    copy .env.example .env >nul
    echo [✓] Created .env from template
) else (
    echo [!] .env.example not found!
    exit /b 1
)

echo.
echo ========================================
echo Step 2: Adding API Keys to .env
echo ========================================
echo.
echo You need to add your API keys to backend\.env
echo.
echo Please get your keys from:
echo  1. OpenAI: https://platform.openai.com/api-keys
echo  2. Africa's Talking: https://africastalking.com/app/settings/apikeys
echo  3. Weather API: https://openweathermap.org/api_keys
echo.
echo Open backend\.env in a text editor and fill in:
echo  - OPENAI_API_KEY=sk-your_key_here
echo  - AFRICAS_TALKING_API_KEY=sandbox_your_key_here
echo  - AFRICAS_TALKING_USERNAME=your_username
echo  - WEATHER_API_KEY=your_key_here
echo.
pause

REM Check if user filled in keys
findstr /i "your_key_here" .env >nul
if %errorlevel% equ 0 (
    echo [!] Please update the API keys in .env before proceeding!
    echo Edit: backend\.env
    pause
    exit /b 1
)
echo [✓] API keys configured

:skip_env

echo.
echo ========================================
echo Step 3: Installing Python Dependencies
echo ========================================
echo.

pip install --upgrade pip
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo [!] Failed to install Python dependencies
    pause
    exit /b 1
)
echo [✓] Python dependencies installed

REM Go back to root
cd ..

echo.
echo ========================================
echo Step 4: Installing Frontend Dependencies
echo ========================================
echo.

cd frontend

REM Check if npm packages need installing
if not exist node_modules (
    echo Installing npm packages...
    call npm install
    if %errorlevel% neq 0 (
        echo [!] Failed to install npm packages
        pause
        exit /b 1
    )
    echo [✓] npm packages installed
) else (
    echo [✓] npm packages already installed
)

cd ..

echo.
echo ========================================
echo Step 5: Database Setup
echo ========================================
echo.

echo Starting PostgreSQL container...
docker-compose up -d postgres

echo Waiting for database to start...
timeout /t 10 /nobreak

echo [✓] Database started

echo.
echo ========================================
echo Setup Complete! ✓
echo ========================================
echo.
echo Next steps:
echo 1. Review backend\.env for any additional configuration
echo 2. Run: docker-compose up
echo 3. Open: http://localhost:3000 for the chatbot
echo 4. Open: http://localhost:8000/docs for API documentation
echo.
echo For detailed instructions, see:
echo - DEPLOYMENT_STEPS.md (deployment options)
echo - GET_API_KEYS.md (getting API keys)
echo - QUICK_COMMANDS.md (useful commands)
echo.

pause

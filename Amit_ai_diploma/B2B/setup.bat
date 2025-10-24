@echo off
REM Quick Start Script for Test Automation Framework
REM سكريبت التشغيل السريع لإطار عمل اختبار الأتمتة

echo ========================================
echo Test Automation Framework - Etisalat
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or later
    pause
    exit /b 1
)

echo Python is installed
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo Error: pip is not available
    echo Please install pip
    pause
    exit /b 1
)

echo pip is available
echo.

REM Install requirements
echo Installing required packages...
pip install -r requirements.txt
if errorlevel 1 (
    echo Error: Failed to install requirements
    pause
    exit /b 1
)

echo Requirements installed successfully
echo.

REM Install Playwright browsers
echo Installing Playwright browsers...
playwright install chromium
if errorlevel 1 (
    echo Error: Failed to install Playwright browsers
    pause
    exit /b 1
)

echo Playwright browsers installed successfully
echo.

REM Create necessary directories
echo Creating necessary directories...
if not exist "reports" mkdir reports
if not exist "reports\screenshots" mkdir reports\screenshots
if not exist "reports\allure-results" mkdir reports\allure-results
if not exist "logs" mkdir logs

echo Directories created successfully
echo.

REM Copy environment file if it doesn't exist
if not exist ".env" (
    echo Creating .env file from template...
    copy ".env.example" ".env" >nul 2>&1
    echo Please edit .env file with your test credentials
    echo.
)

echo ========================================
echo Setup completed successfully!
echo ========================================
echo.
echo To run tests:
echo   pytest main.py --alluredir=reports/allure-results
echo.
echo To view Allure report:
echo   allure serve reports/allure-results
echo.
echo To run specific tests:
echo   pytest main.py -m login
echo   pytest main.py -m registration
echo   pytest main.py -m smoke
echo.
pause

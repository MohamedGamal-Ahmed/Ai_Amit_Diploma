@echo off
REM Test Runner Script
REM سكريبت تشغيل الاختبارات

echo ========================================
echo Running Test Automation Framework
echo ========================================
echo.

REM Check if .env file exists
if not exist ".env" (
    echo Warning: .env file not found
    echo Please create .env file with your test credentials
    echo.
)

REM Run tests with Allure reporting
echo Running tests with Allure reporting...
pytest main.py --alluredir=reports/allure-results -v

if errorlevel 1 (
    echo.
    echo Tests completed with some failures
    echo Check the reports for details
) else (
    echo.
    echo All tests passed successfully!
)

echo.
echo ========================================
echo Test execution completed
echo ========================================
echo.
echo Reports generated in:
echo   - Allure: reports/allure-results/
echo   - Screenshots: reports/screenshots/
echo   - Logs: logs/
echo.
echo To view Allure report:
echo   allure serve reports/allure-results
echo.
pause

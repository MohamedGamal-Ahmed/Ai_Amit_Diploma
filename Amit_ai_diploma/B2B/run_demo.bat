@echo off
REM Simple Test Runner for Windows
echo ========================================
echo Test Automation Framework - Demo
echo ========================================
echo.

REM Run the demo test
echo Running demo test...
python -m pytest demo_test.py -v

echo.
echo ========================================
echo Demo completed!
echo ========================================
pause

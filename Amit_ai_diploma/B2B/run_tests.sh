#!/bin/bash
# Test Runner Script
# سكريبت تشغيل الاختبارات

echo "========================================"
echo "Running Test Automation Framework"
echo "========================================"
echo

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "Warning: .env file not found"
    echo "Please create .env file with your test credentials"
    echo
fi

# Run tests with Allure reporting
echo "Running tests with Allure reporting..."
pytest main.py --alluredir=reports/allure-results -v

if [ $? -ne 0 ]; then
    echo
    echo "Tests completed with some failures"
    echo "Check the reports for details"
else
    echo
    echo "All tests passed successfully!"
fi

echo
echo "========================================"
echo "Test execution completed"
echo "========================================"
echo
echo "Reports generated in:"
echo "  - Allure: reports/allure-results/"
echo "  - Screenshots: reports/screenshots/"
echo "  - Logs: logs/"
echo
echo "To view Allure report:"
echo "  allure serve reports/allure-results"
echo

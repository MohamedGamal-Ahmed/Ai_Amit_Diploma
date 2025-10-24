#!/bin/bash
# Quick Start Script for Test Automation Framework
# سكريبت التشغيل السريع لإطار عمل اختبار الأتمتة

echo "========================================"
echo "Test Automation Framework - Etisalat"
echo "========================================"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    echo "Please install Python 3.8 or later"
    exit 1
fi

echo "Python is installed: $(python3 --version)"
echo

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not available"
    echo "Please install pip3"
    exit 1
fi

echo "pip3 is available: $(pip3 --version)"
echo

# Install requirements
echo "Installing required packages..."
pip3 install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "Error: Failed to install requirements"
    exit 1
fi

echo "Requirements installed successfully"
echo

# Install Playwright browsers
echo "Installing Playwright browsers..."
playwright install chromium
if [ $? -ne 0 ]; then
    echo "Error: Failed to install Playwright browsers"
    exit 1
fi

echo "Playwright browsers installed successfully"
echo

# Create necessary directories
echo "Creating necessary directories..."
mkdir -p reports/screenshots
mkdir -p reports/allure-results
mkdir -p logs

echo "Directories created successfully"
echo

# Copy environment file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp ".env.example" ".env" 2>/dev/null || echo "Please create .env file manually"
    echo "Please edit .env file with your test credentials"
    echo
fi

echo "========================================"
echo "Setup completed successfully!"
echo "========================================"
echo
echo "To run tests:"
echo "  pytest main.py --alluredir=reports/allure-results"
echo
echo "To view Allure report:"
echo "  allure serve reports/allure-results"
echo
echo "To run specific tests:"
echo "  pytest main.py -m login"
echo "  pytest main.py -m registration"
echo "  pytest main.py -m smoke"
echo

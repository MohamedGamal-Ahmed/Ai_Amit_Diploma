"""
Simple Test Demo - اختبار بسيط للتأكد من عمل الإطار
"""

import pytest
from playwright.sync_api import sync_playwright
from config.config import Config


def test_simple_demo():
    """اختبار بسيط للتأكد من عمل Playwright"""
    config = Config()
    
    with sync_playwright() as p:
        # تشغيل المتصفح
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # الانتقال إلى موقع Google للاختبار
        page.goto("https://www.google.com")
        
        # التحقق من تحميل الصفحة
        assert "Google" in page.title()
        
        # أخذ لقطة شاشة
        page.screenshot(path="reports/screenshots/demo_test.png")
        
        browser.close()
        
        print("Test passed successfully!")


if __name__ == "__main__":
    test_simple_demo()

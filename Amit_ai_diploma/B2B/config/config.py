"""
ملف الإعدادات الرئيسي للـ Test Automation Framework
يحتوي على جميع الإعدادات المطلوبة لتشغيل الاختبارات
"""

import os
from typing import Dict, Any
from dotenv import load_dotenv

# تحميل متغيرات البيئة من ملف .env
load_dotenv()


class Config:
    """كلاس الإعدادات الرئيسي"""
    
    # إعدادات الموقع الأساسية
    BASE_URL: str = os.getenv("BASE_URL", "https://www.etisalat.eg")
    LOGIN_URL: str = f"{BASE_URL}/login"
    REGISTRATION_URL: str = f"{BASE_URL}/register"
    
    # إعدادات المتصفح
    BROWSER_CONFIG: Dict[str, Any] = {
        "browser": "chromium",  # استخدام Chrome/Chromium فقط
        "headless": os.getenv("HEADLESS", "false").lower() == "true",
        "viewport": {"width": 1920, "height": 1080},
        "timeout": 30000,  # 30 ثانية
        "slow_mo": 0,  # سرعة التنفيذ (0 = عادي)
        "args": [
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu",
            "--disable-web-security",
            "--disable-features=VizDisplayCompositor"
        ]
    }
    
    # إعدادات الاختبار
    TEST_CONFIG: Dict[str, Any] = {
        "implicit_wait": 10,  # انتظار ضمني بالثواني
        "explicit_wait": 20,  # انتظار صريح بالثواني
        "page_load_timeout": 30,  # انتظار تحميل الصفحة
        "retry_count": 3,  # عدد المحاولات عند الفشل
        "parallel_workers": 2  # عدد العمال المتوازيين
    }
    
    # بيانات تسجيل الدخول للاختبار
    TEST_CREDENTIALS: Dict[str, str] = {
        "valid_username": os.getenv("TEST_USERNAME", "test_user@etisalat.eg"),
        "valid_password": os.getenv("TEST_PASSWORD", "Test123456"),
        "invalid_username": "invalid@test.com",
        "invalid_password": "wrongpassword"
    }
    
    # إعدادات التقارير والسكرينشوت
    REPORT_CONFIG: Dict[str, Any] = {
        "screenshots_dir": "reports/screenshots",
        "allure_results_dir": "reports/allure-results",
        "html_report_dir": "reports",
        "screenshot_on_pass": True,
        "screenshot_on_fail": True,
        "video_recording": False,
        "trace_recording": True
    }
    
    # إعدادات Allure Report
    ALLURE_CONFIG: Dict[str, Any] = {
        "environment": "Test Environment",
        "project_name": "Etisalat Test Automation",
        "build_name": "Build 1.0",
        "severity_levels": ["blocker", "critical", "normal", "minor", "trivial"],
        "feature_tags": ["login", "registration", "smoke", "regression"]
    }
    
    # إعدادات قاعدة البيانات (إذا لزم الأمر)
    DATABASE_CONFIG: Dict[str, Any] = {
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "5432")),
        "username": os.getenv("DB_USERNAME", "test_user"),
        "password": os.getenv("DB_PASSWORD", "test_password"),
        "database": os.getenv("DB_NAME", "test_db")
    }
    
    # إعدادات API (إذا لزم الأمر)
    API_CONFIG: Dict[str, Any] = {
        "base_url": os.getenv("API_BASE_URL", "https://api.etisalat.eg"),
        "timeout": 30,
        "headers": {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
    }
    
    # إعدادات اللوجينج
    LOGGING_CONFIG: Dict[str, Any] = {
        "level": "INFO",
        "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        "file_path": "logs/test_execution.log",
        "max_file_size": 10485760,  # 10 MB
        "backup_count": 5
    }
    
    # إعدادات خاصة بموقع اتصالات
    ETISALAT_CONFIG: Dict[str, Any] = {
        "phone_number_length": 8,  # طول رقم الهاتف المصري
        "supported_languages": ["ar", "en"],
        "default_language": "ar",
        "max_file_upload_size": 5242880,  # 5 MB
        "supported_file_types": [".jpg", ".jpeg", ".png", ".pdf"]
    }
    
    @classmethod
    def get_browser_config(cls) -> Dict[str, Any]:
        """إرجاع إعدادات المتصفح"""
        return cls.BROWSER_CONFIG
    
    @classmethod
    def get_test_config(cls) -> Dict[str, Any]:
        """إرجاع إعدادات الاختبار"""
        return cls.TEST_CONFIG
    
    @classmethod
    def get_report_config(cls) -> Dict[str, Any]:
        """إرجاع إعدادات التقارير"""
        return cls.REPORT_CONFIG
    
    @classmethod
    def get_allure_config(cls) -> Dict[str, Any]:
        """إرجاع إعدادات Allure"""
        return cls.ALLURE_CONFIG


# إنشاء مجلدات التقارير إذا لم تكن موجودة
def create_report_directories():
    """إنشاء مجلدات التقارير والسكرينشوت"""
    directories = [
        Config.REPORT_CONFIG["screenshots_dir"],
        Config.REPORT_CONFIG["allure_results_dir"],
        Config.REPORT_CONFIG["html_report_dir"],
        "logs"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


# استدعاء الدالة لإنشاء المجلدات عند استيراد الملف
create_report_directories()

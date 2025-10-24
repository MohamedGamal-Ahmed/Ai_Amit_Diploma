"""
Helper Functions - الدوال المساعدة
يحتوي على دوال مفيدة للسكرينشوت والتقارير واللوجينج
"""

import os
import logging
import allure
import json
from datetime import datetime
from typing import Optional, Dict, Any, List
from playwright.sync_api import Page
from config.config import Config


class ScreenshotHelper:
    """مساعد السكرينشوت"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
    
    def take_screenshot(self, page: Page, test_name: str, step_name: str = "", 
                       status: str = "info") -> str:
        """
        أخذ لقطة شاشة مع إضافة للـ Allure report
        
        Args:
            page: كائن Playwright Page
            test_name: اسم الاختبار
            step_name: اسم الخطوة (اختياري)
            status: حالة اللقطة (info, pass, fail)
            
        Returns:
            str: مسار الملف المحفوظ
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{step_name}_{status}_{timestamp}.png"
            screenshot_path = os.path.join(
                self.config.REPORT_CONFIG["screenshots_dir"], 
                filename
            )
            
            # أخذ اللقطة
            page.screenshot(path=screenshot_path, full_page=True)
            
            # إضافة للـ Allure report
            with open(screenshot_path, "rb") as f:
                screenshot_data = f.read()
            
            if status == "fail":
                allure.attach(
                    screenshot_data, 
                    name=f"Screenshot - {step_name} (FAILED)",
                    attachment_type=allure.attachment_type.PNG
                )
            elif status == "pass":
                allure.attach(
                    screenshot_data, 
                    name=f"Screenshot - {step_name} (PASSED)",
                    attachment_type=allure.attachment_type.PNG
                )
            else:
                allure.attach(
                    screenshot_data, 
                    name=f"Screenshot - {step_name}",
                    attachment_type=allure.attachment_type.PNG
                )
            
            self.logger.info(f"تم أخذ لقطة شاشة: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            self.logger.error(f"خطأ في أخذ لقطة الشاشة: {str(e)}")
            raise
    
    def take_element_screenshot(self, page: Page, selector: str, 
                               test_name: str, step_name: str = "") -> str:
        """
        أخذ لقطة شاشة لعنصر معين
        
        Args:
            page: كائن Playwright Page
            selector: محدد العنصر
            test_name: اسم الاختبار
            step_name: اسم الخطوة
            
        Returns:
            str: مسار الملف المحفوظ
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{test_name}_{step_name}_element_{timestamp}.png"
            screenshot_path = os.path.join(
                self.config.REPORT_CONFIG["screenshots_dir"], 
                filename
            )
            
            # أخذ لقطة للعنصر
            element = page.locator(selector)
            element.screenshot(path=screenshot_path)
            
            # إضافة للـ Allure report
            with open(screenshot_path, "rb") as f:
                screenshot_data = f.read()
            
            allure.attach(
                screenshot_data, 
                name=f"Element Screenshot - {step_name}",
                attachment_type=allure.attachment_type.PNG
            )
            
            self.logger.info(f"تم أخذ لقطة للعنصر: {screenshot_path}")
            return screenshot_path
            
        except Exception as e:
            self.logger.error(f"خطأ في أخذ لقطة العنصر: {str(e)}")
            raise


class AllureHelper:
    """مساعد Allure Reports"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def add_test_step(self, step_name: str, step_description: str = ""):
        """
        إضافة خطوة للاختبار في Allure
        
        Args:
            step_name: اسم الخطوة
            step_description: وصف الخطوة
        """
        try:
            with allure.step(step_name):
                if step_description:
                    allure.attach(
                        step_description,
                        name="Step Description",
                        attachment_type=allure.attachment_type.TEXT
                    )
                self.logger.info(f"تم إضافة خطوة: {step_name}")
        except Exception as e:
            self.logger.error(f"خطأ في إضافة الخطوة: {str(e)}")
    
    def add_test_data(self, data: Dict[str, Any], data_name: str = "Test Data"):
        """
        إضافة بيانات الاختبار للـ Allure report
        
        Args:
            data: بيانات الاختبار
            data_name: اسم البيانات
        """
        try:
            json_data = json.dumps(data, indent=2, ensure_ascii=False)
            allure.attach(
                json_data,
                name=data_name,
                attachment_type=allure.attachment_type.JSON
            )
            self.logger.info(f"تم إضافة بيانات الاختبار: {data_name}")
        except Exception as e:
            self.logger.error(f"خطأ في إضافة بيانات الاختبار: {str(e)}")
    
    def add_error_details(self, error_message: str, error_traceback: str = ""):
        """
        إضافة تفاصيل الخطأ للـ Allure report
        
        Args:
            error_message: رسالة الخطأ
            error_traceback: تفاصيل الخطأ (اختياري)
        """
        try:
            error_details = f"Error Message: {error_message}\n"
            if error_traceback:
                error_details += f"Traceback:\n{error_traceback}"
            
            allure.attach(
                error_details,
                name="Error Details",
                attachment_type=allure.attachment_type.TEXT
            )
            self.logger.info("تم إضافة تفاصيل الخطأ")
        except Exception as e:
            self.logger.error(f"خطأ في إضافة تفاصيل الخطأ: {str(e)}")
    
    def add_page_source(self, page_source: str, page_name: str = "Page Source"):
        """
        إضافة كود HTML للصفحة للـ Allure report
        
        Args:
            page_source: كود HTML للصفحة
            page_name: اسم الصفحة
        """
        try:
            allure.attach(
                page_source,
                name=page_name,
                attachment_type=allure.attachment_type.HTML
            )
            self.logger.info(f"تم إضافة كود الصفحة: {page_name}")
        except Exception as e:
            self.logger.error(f"خطأ في إضافة كود الصفحة: {str(e)}")
    
    def add_environment_info(self, environment_data: Dict[str, Any]):
        """
        إضافة معلومات البيئة للـ Allure report
        
        Args:
            environment_data: بيانات البيئة
        """
        try:
            env_text = ""
            for key, value in environment_data.items():
                env_text += f"{key}: {value}\n"
            
            allure.attach(
                env_text,
                name="Environment Information",
                attachment_type=allure.attachment_type.TEXT
            )
            self.logger.info("تم إضافة معلومات البيئة")
        except Exception as e:
            self.logger.error(f"خطأ في إضافة معلومات البيئة: {str(e)}")


class LoggingHelper:
    """مساعد اللوجينج"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
    
    def _setup_logging(self):
        """إعداد نظام اللوجينج"""
        try:
            # إنشاء مجلد اللوجز إذا لم يكن موجود
            log_dir = os.path.dirname(self.config.LOGGING_CONFIG["file_path"])
            os.makedirs(log_dir, exist_ok=True)
            
            # إعداد اللوجر
            logging.basicConfig(
                level=getattr(logging, self.config.LOGGING_CONFIG["level"]),
                format=self.config.LOGGING_CONFIG["format"],
                handlers=[
                    logging.FileHandler(
                        self.config.LOGGING_CONFIG["file_path"],
                        encoding='utf-8'
                    ),
                    logging.StreamHandler()
                ]
            )
            
            self.logger.info("تم إعداد نظام اللوجينج")
        except Exception as e:
            print(f"خطأ في إعداد اللوجينج: {str(e)}")
    
    def log_test_start(self, test_name: str, test_data: Dict[str, Any] = None):
        """
        تسجيل بداية الاختبار
        
        Args:
            test_name: اسم الاختبار
            test_data: بيانات الاختبار (اختياري)
        """
        try:
            self.logger.info(f"بداية الاختبار: {test_name}")
            if test_data:
                self.logger.info(f"بيانات الاختبار: {test_data}")
        except Exception as e:
            self.logger.error(f"خطأ في تسجيل بداية الاختبار: {str(e)}")
    
    def log_test_end(self, test_name: str, status: str, duration: float = 0):
        """
        تسجيل نهاية الاختبار
        
        Args:
            test_name: اسم الاختبار
            status: حالة الاختبار (PASS/FAIL)
            duration: مدة الاختبار بالثواني
        """
        try:
            self.logger.info(f"نهاية الاختبار: {test_name}")
            self.logger.info(f"حالة الاختبار: {status}")
            self.logger.info(f"مدة الاختبار: {duration:.2f} ثانية")
        except Exception as e:
            self.logger.error(f"خطأ في تسجيل نهاية الاختبار: {str(e)}")
    
    def log_step(self, step_name: str, step_details: str = ""):
        """
        تسجيل خطوة في الاختبار
        
        Args:
            step_name: اسم الخطوة
            step_details: تفاصيل الخطوة
        """
        try:
            self.logger.info(f"الخطوة: {step_name}")
            if step_details:
                self.logger.info(f"التفاصيل: {step_details}")
        except Exception as e:
            self.logger.error(f"خطأ في تسجيل الخطوة: {str(e)}")
    
    def log_error(self, error_message: str, error_details: str = ""):
        """
        تسجيل خطأ
        
        Args:
            error_message: رسالة الخطأ
            error_details: تفاصيل الخطأ
        """
        try:
            self.logger.error(f"خطأ: {error_message}")
            if error_details:
                self.logger.error(f"التفاصيل: {error_details}")
        except Exception as e:
            self.logger.error(f"خطأ في تسجيل الخطأ: {str(e)}")


class DataHelper:
    """مساعد البيانات"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def load_test_cases(self, file_path: str) -> Dict[str, Any]:
        """
        تحميل حالات الاختبار من ملف JSON
        
        Args:
            file_path: مسار ملف JSON
            
        Returns:
            Dict: حالات الاختبار
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                test_cases = json.load(f)
            self.logger.info(f"تم تحميل حالات الاختبار من: {file_path}")
            return test_cases
        except Exception as e:
            self.logger.error(f"خطأ في تحميل حالات الاختبار: {str(e)}")
            raise
    
    def save_test_results(self, results: Dict[str, Any], file_path: str):
        """
        حفظ نتائج الاختبارات
        
        Args:
            results: نتائج الاختبارات
            file_path: مسار الملف
        """
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            self.logger.info(f"تم حفظ النتائج في: {file_path}")
        except Exception as e:
            self.logger.error(f"خطأ في حفظ النتائج: {str(e)}")
            raise
    
    def validate_test_data(self, test_data: Dict[str, Any], required_fields: List[str]) -> bool:
        """
        التحقق من صحة بيانات الاختبار
        
        Args:
            test_data: بيانات الاختبار
            required_fields: الحقول المطلوبة
            
        Returns:
            bool: True إذا كانت البيانات صحيحة
        """
        try:
            for field in required_fields:
                if field not in test_data:
                    self.logger.error(f"الحقل المطلوب مفقود: {field}")
                    return False
            self.logger.info("تم التحقق من صحة البيانات")
            return True
        except Exception as e:
            self.logger.error(f"خطأ في التحقق من البيانات: {str(e)}")
            return False


class UtilityHelper:
    """مساعد الأدوات العامة"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def wait_for_condition(self, condition_func, timeout: int = 30, 
                          interval: float = 0.5) -> bool:
        """
        انتظار تحقق شرط معين
        
        Args:
            condition_func: دالة الشرط
            timeout: وقت الانتظار بالثواني
            interval: فترة التحقق بالثواني
            
        Returns:
            bool: True إذا تحقق الشرط
        """
        try:
            import time
            start_time = time.time()
            
            while time.time() - start_time < timeout:
                if condition_func():
                    return True
                time.sleep(interval)
            
            self.logger.warning(f"انتهى وقت الانتظار للشرط")
            return False
        except Exception as e:
            self.logger.error(f"خطأ في انتظار الشرط: {str(e)}")
            return False
    
    def generate_test_id(self, prefix: str = "TC") -> str:
        """
        توليد معرف فريد للاختبار
        
        Args:
            prefix: البادئة
            
        Returns:
            str: معرف الاختبار
        """
        try:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            test_id = f"{prefix}_{timestamp}"
            self.logger.info(f"تم توليد معرف الاختبار: {test_id}")
            return test_id
        except Exception as e:
            self.logger.error(f"خطأ في توليد معرف الاختبار: {str(e)}")
            return f"{prefix}_UNKNOWN"
    
    def clean_old_files(self, directory: str, days_old: int = 7):
        """
        حذف الملفات القديمة
        
        Args:
            directory: المجلد
            days_old: عدد الأيام
        """
        try:
            import time
            import glob
            
            current_time = time.time()
            cutoff_time = current_time - (days_old * 24 * 60 * 60)
            
            pattern = os.path.join(directory, "*")
            files = glob.glob(pattern)
            
            deleted_count = 0
            for file_path in files:
                if os.path.isfile(file_path):
                    file_time = os.path.getmtime(file_path)
                    if file_time < cutoff_time:
                        os.remove(file_path)
                        deleted_count += 1
            
            self.logger.info(f"تم حذف {deleted_count} ملف قديم من {directory}")
        except Exception as e:
            self.logger.error(f"خطأ في حذف الملفات القديمة: {str(e)}")


# إنشاء مثيلات عامة للمساعدين
screenshot_helper = ScreenshotHelper()
allure_helper = AllureHelper()
logging_helper = LoggingHelper()
data_helper = DataHelper()
utility_helper = UtilityHelper()

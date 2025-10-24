"""
Base Page Class - الكلاس الأساسي لجميع الصفحات
يحتوي على الدوال المشتركة والمفيدة لجميع الصفحات
"""

import logging
import time
from typing import Optional, List, Any, Union
from playwright.sync_api import Page, Locator, expect
from config.config import Config


class BasePage:
    """الكلاس الأساسي لجميع الصفحات"""
    
    def __init__(self, page: Page):
        """
        تهيئة الكلاس الأساسي
        
        Args:
            page: كائن Playwright Page
        """
        self.page = page
        self.config = Config()
        self.logger = logging.getLogger(self.__class__.__name__)
        
        # إعدادات الانتظار
        self.implicit_wait = self.config.TEST_CONFIG["implicit_wait"]
        self.explicit_wait = self.config.TEST_CONFIG["explicit_wait"]
        self.page_load_timeout = self.config.TEST_CONFIG["page_load_timeout"]
    
    def navigate_to(self, url: str) -> None:
        """
        الانتقال إلى رابط معين
        
        Args:
            url: الرابط المطلوب الانتقال إليه
        """
        try:
            self.logger.info(f"الانتقال إلى: {url}")
            self.page.goto(url, timeout=self.page_load_timeout * 1000)
            self.wait_for_page_load()
            self.logger.info("تم الانتقال بنجاح")
        except Exception as e:
            self.logger.error(f"خطأ في الانتقال إلى {url}: {str(e)}")
            raise
    
    def wait_for_page_load(self) -> None:
        """انتظار تحميل الصفحة بالكامل"""
        try:
            self.page.wait_for_load_state("networkidle", timeout=self.page_load_timeout * 1000)
        except Exception as e:
            self.logger.warning(f"لم يتم تحميل الصفحة بالكامل: {str(e)}")
    
    def get_element(self, selector: str) -> Locator:
        """
        الحصول على عنصر من الصفحة
        
        Args:
            selector: محدد العنصر
            
        Returns:
            Locator: كائن العنصر
        """
        try:
            return self.page.locator(selector)
        except Exception as e:
            self.logger.error(f"خطأ في العثور على العنصر {selector}: {str(e)}")
            raise
    
    def click(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        النقر على عنصر
        
        Args:
            selector: محدد العنصر
            timeout: وقت الانتظار (اختياري)
        """
        try:
            timeout = timeout or self.explicit_wait * 1000
            element = self.get_element(selector)
            element.click(timeout=timeout)
            self.logger.info(f"تم النقر على العنصر: {selector}")
        except Exception as e:
            self.logger.error(f"خطأ في النقر على العنصر {selector}: {str(e)}")
            raise
    
    def fill(self, selector: str, text: str, timeout: Optional[int] = None) -> None:
        """
        ملء حقل نصي
        
        Args:
            selector: محدد العنصر
            text: النص المراد إدخاله
            timeout: وقت الانتظار (اختياري)
        """
        try:
            timeout = timeout or self.explicit_wait * 1000
            element = self.get_element(selector)
            element.clear()
            element.fill(text)
            self.logger.info(f"تم ملء الحقل {selector} بالنص: {text}")
        except Exception as e:
            self.logger.error(f"خطأ في ملء الحقل {selector}: {str(e)}")
            raise
    
    def get_text(self, selector: str, timeout: Optional[int] = None) -> str:
        """
        الحصول على نص العنصر
        
        Args:
            selector: محدد العنصر
            timeout: وقت الانتظار (اختياري)
            
        Returns:
            str: نص العنصر
        """
        try:
            timeout = timeout or self.explicit_wait * 1000
            element = self.get_element(selector)
            text = element.text_content(timeout=timeout)
            self.logger.info(f"تم الحصول على النص من {selector}: {text}")
            return text or ""
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على النص من {selector}: {str(e)}")
            raise
    
    def get_attribute(self, selector: str, attribute: str, timeout: Optional[int] = None) -> Optional[str]:
        """
        الحصول على خاصية العنصر
        
        Args:
            selector: محدد العنصر
            attribute: اسم الخاصية
            timeout: وقت الانتظار (اختياري)
            
        Returns:
            str: قيمة الخاصية
        """
        try:
            timeout = timeout or self.explicit_wait * 1000
            element = self.get_element(selector)
            value = element.get_attribute(attribute, timeout=timeout)
            self.logger.info(f"تم الحصول على الخاصية {attribute} من {selector}: {value}")
            return value
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على الخاصية {attribute} من {selector}: {str(e)}")
            raise
    
    def is_visible(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        التحقق من ظهور العنصر
        
        Args:
            selector: محدد العنصر
            timeout: وقت الانتظار (اختياري)
            
        Returns:
            bool: True إذا كان العنصر ظاهر
        """
        try:
            timeout = timeout or self.explicit_wait * 1000
            element = self.get_element(selector)
            is_visible = element.is_visible(timeout=timeout)
            self.logger.info(f"العنصر {selector} ظاهر: {is_visible}")
            return is_visible
        except Exception as e:
            self.logger.warning(f"خطأ في التحقق من ظهور العنصر {selector}: {str(e)}")
            return False
    
    def is_enabled(self, selector: str, timeout: Optional[int] = None) -> bool:
        """
        التحقق من تفعيل العنصر
        
        Args:
            selector: محدد العنصر
            timeout: وقت الانتظار (اختياري)
            
        Returns:
            bool: True إذا كان العنصر مفعل
        """
        try:
            timeout = timeout or self.explicit_wait * 1000
            element = self.get_element(selector)
            is_enabled = element.is_enabled(timeout=timeout)
            self.logger.info(f"العنصر {selector} مفعل: {is_enabled}")
            return is_enabled
        except Exception as e:
            self.logger.warning(f"خطأ في التحقق من تفعيل العنصر {selector}: {str(e)}")
            return False
    
    def wait_for_element(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        انتظار ظهور العنصر
        
        Args:
            selector: محدد العنصر
            timeout: وقت الانتظار (اختياري)
        """
        try:
            timeout = timeout or self.explicit_wait * 1000
            element = self.get_element(selector)
            element.wait_for(state="visible", timeout=timeout)
            self.logger.info(f"تم انتظار ظهور العنصر: {selector}")
        except Exception as e:
            self.logger.error(f"خطأ في انتظار العنصر {selector}: {str(e)}")
            raise
    
    def wait_for_element_to_disappear(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        انتظار اختفاء العنصر
        
        Args:
            selector: محدد العنصر
            timeout: وقت الانتظار (اختياري)
        """
        try:
            timeout = timeout or self.explicit_wait * 1000
            element = self.get_element(selector)
            element.wait_for(state="hidden", timeout=timeout)
            self.logger.info(f"تم انتظار اختفاء العنصر: {selector}")
        except Exception as e:
            self.logger.error(f"خطأ في انتظار اختفاء العنصر {selector}: {str(e)}")
            raise
    
    def select_option(self, selector: str, value: str, timeout: Optional[int] = None) -> None:
        """
        اختيار خيار من قائمة منسدلة
        
        Args:
            selector: محدد العنصر
            value: القيمة المطلوب اختيارها
            timeout: وقت الانتظار (اختياري)
        """
        try:
            timeout = timeout or self.explicit_wait * 1000
            element = self.get_element(selector)
            element.select_option(value, timeout=timeout)
            self.logger.info(f"تم اختيار الخيار {value} من {selector}")
        except Exception as e:
            self.logger.error(f"خطأ في اختيار الخيار من {selector}: {str(e)}")
            raise
    
    def hover(self, selector: str, timeout: Optional[int] = None) -> None:
        """
        تمرير الماوس فوق العنصر
        
        Args:
            selector: محدد العنصر
            timeout: وقت الانتظار (اختياري)
        """
        try:
            timeout = timeout or self.explicit_wait * 1000
            element = self.get_element(selector)
            element.hover(timeout=timeout)
            self.logger.info(f"تم تمرير الماوس فوق العنصر: {selector}")
        except Exception as e:
            self.logger.error(f"خطأ في تمرير الماوس فوق العنصر {selector}: {str(e)}")
            raise
    
    def scroll_to_element(self, selector: str) -> None:
        """
        التمرير إلى العنصر
        
        Args:
            selector: محدد العنصر
        """
        try:
            element = self.get_element(selector)
            element.scroll_into_view_if_needed()
            self.logger.info(f"تم التمرير إلى العنصر: {selector}")
        except Exception as e:
            self.logger.error(f"خطأ في التمرير إلى العنصر {selector}: {str(e)}")
            raise
    
    def take_screenshot(self, filename: str, full_page: bool = True) -> str:
        """
        أخذ لقطة شاشة
        
        Args:
            filename: اسم الملف
            full_page: أخذ لقطة للصفحة كاملة
            
        Returns:
            str: مسار الملف المحفوظ
        """
        try:
            timestamp = int(time.time())
            screenshot_path = f"{self.config.REPORT_CONFIG['screenshots_dir']}/{filename}_{timestamp}.png"
            self.page.screenshot(path=screenshot_path, full_page=full_page)
            self.logger.info(f"تم أخذ لقطة شاشة: {screenshot_path}")
            return screenshot_path
        except Exception as e:
            self.logger.error(f"خطأ في أخذ لقطة الشاشة: {str(e)}")
            raise
    
    def get_page_title(self) -> str:
        """
        الحصول على عنوان الصفحة
        
        Returns:
            str: عنوان الصفحة
        """
        try:
            title = self.page.title()
            self.logger.info(f"عنوان الصفحة: {title}")
            return title
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على عنوان الصفحة: {str(e)}")
            raise
    
    def get_current_url(self) -> str:
        """
        الحصول على الرابط الحالي
        
        Returns:
            str: الرابط الحالي
        """
        try:
            url = self.page.url
            self.logger.info(f"الرابط الحالي: {url}")
            return url
        except Exception as e:
            self.logger.error(f"خطأ في الحصول على الرابط الحالي: {str(e)}")
            raise
    
    def refresh_page(self) -> None:
        """تحديث الصفحة"""
        try:
            self.page.reload()
            self.wait_for_page_load()
            self.logger.info("تم تحديث الصفحة")
        except Exception as e:
            self.logger.error(f"خطأ في تحديث الصفحة: {str(e)}")
            raise
    
    def go_back(self) -> None:
        """العودة للصفحة السابقة"""
        try:
            self.page.go_back()
            self.wait_for_page_load()
            self.logger.info("تم العودة للصفحة السابقة")
        except Exception as e:
            self.logger.error(f"خطأ في العودة للصفحة السابقة: {str(e)}")
            raise
    
    def go_forward(self) -> None:
        """التقدم للصفحة التالية"""
        try:
            self.page.go_forward()
            self.wait_for_page_load()
            self.logger.info("تم التقدم للصفحة التالية")
        except Exception as e:
            self.logger.error(f"خطأ في التقدم للصفحة التالية: {str(e)}")
            raise
    
    def assert_element_visible(self, selector: str, message: str = "") -> None:
        """
        التحقق من ظهور العنصر مع رسالة خطأ مخصصة
        
        Args:
            selector: محدد العنصر
            message: رسالة الخطأ المخصصة
        """
        try:
            element = self.get_element(selector)
            expect(element).to_be_visible()
            self.logger.info(f"تم التحقق من ظهور العنصر: {selector}")
        except Exception as e:
            error_msg = message or f"العنصر {selector} غير ظاهر"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
    
    def assert_text_equals(self, selector: str, expected_text: str, message: str = "") -> None:
        """
        التحقق من تطابق النص
        
        Args:
            selector: محدد العنصر
            expected_text: النص المتوقع
            message: رسالة الخطأ المخصصة
        """
        try:
            element = self.get_element(selector)
            expect(element).to_have_text(expected_text)
            self.logger.info(f"تم التحقق من النص في {selector}: {expected_text}")
        except Exception as e:
            error_msg = message or f"النص في {selector} لا يطابق المتوقع: {expected_text}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)
    
    def assert_url_contains(self, expected_url_part: str, message: str = "") -> None:
        """
        التحقق من احتواء الرابط على جزء معين
        
        Args:
            expected_url_part: الجزء المتوقع في الرابط
            message: رسالة الخطأ المخصصة
        """
        try:
            current_url = self.get_current_url()
            assert expected_url_part in current_url, f"الرابط الحالي {current_url} لا يحتوي على {expected_url_part}"
            self.logger.info(f"تم التحقق من الرابط: يحتوي على {expected_url_part}")
        except Exception as e:
            error_msg = message or f"الرابط لا يحتوي على {expected_url_part}"
            self.logger.error(error_msg)
            raise AssertionError(error_msg)

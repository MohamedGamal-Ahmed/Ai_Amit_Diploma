"""
Login Page Object - صفحة تسجيل الدخول
يحتوي على جميع العمليات المتعلقة بصفحة تسجيل الدخول
"""

from typing import Optional, Dict, Any
from playwright.sync_api import Page
from utils.base_page import BasePage
from locators.all_locators import LoginPageLocators
from utils.helpers import screenshot_helper, allure_helper, logging_helper


class LoginPage(BasePage):
    """صفحة تسجيل الدخول"""
    
    def __init__(self, page: Page):
        """
        تهيئة صفحة تسجيل الدخول
        
        Args:
            page: كائن Playwright Page
        """
        super().__init__(page)
        self.locators = LoginPageLocators()
        self.page_url = self.config.LOGIN_URL
    
    def navigate_to_login_page(self) -> None:
        """الانتقال إلى صفحة تسجيل الدخول"""
        try:
            logging_helper.log_step("الانتقال إلى صفحة تسجيل الدخول")
            self.navigate_to(self.page_url)
            self.wait_for_page_load()
            
            # التحقق من تحميل الصفحة
            self.assert_element_visible(
                self.locators.LOGIN_FORM,
                "صفحة تسجيل الدخول لم يتم تحميلها بشكل صحيح"
            )
            
            # أخذ لقطة شاشة للصفحة المحملة
            screenshot_helper.take_screenshot(
                self.page, 
                "login_page_loaded", 
                "صفحة تسجيل الدخول محملة"
            )
            
            logging_helper.log_step("تم تحميل صفحة تسجيل الدخول بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في تحميل صفحة تسجيل الدخول: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "login_page_error", 
                "خطأ في تحميل صفحة تسجيل الدخول",
                "fail"
            )
            raise
    
    def enter_username(self, username: str) -> None:
        """
        إدخال اسم المستخدم
        
        Args:
            username: اسم المستخدم
        """
        try:
            logging_helper.log_step(f"إدخال اسم المستخدم: {username}")
            
            # انتظار ظهور حقل اسم المستخدم
            self.wait_for_element(self.locators.USERNAME_INPUT)
            
            # ملء الحقل
            self.fill(self.locators.USERNAME_INPUT, username)
            
            # التحقق من إدخال البيانات
            entered_value = self.get_attribute(self.locators.USERNAME_INPUT, "value")
            assert entered_value == username, f"لم يتم إدخال اسم المستخدم بشكل صحيح: {entered_value}"
            
            logging_helper.log_step("تم إدخال اسم المستخدم بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في إدخال اسم المستخدم: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "username_input_error", 
                "خطأ في إدخال اسم المستخدم",
                "fail"
            )
            raise
    
    def enter_password(self, password: str) -> None:
        """
        إدخال كلمة المرور
        
        Args:
            password: كلمة المرور
        """
        try:
            logging_helper.log_step("إدخال كلمة المرور")
            
            # انتظار ظهور حقل كلمة المرور
            self.wait_for_element(self.locators.PASSWORD_INPUT)
            
            # ملء الحقل
            self.fill(self.locators.PASSWORD_INPUT, password)
            
            # التحقق من إدخال البيانات (كلمة المرور قد لا تظهر في القيمة)
            logging_helper.log_step("تم إدخال كلمة المرور بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في إدخال كلمة المرور: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "password_input_error", 
                "خطأ في إدخال كلمة المرور",
                "fail"
            )
            raise
    
    def click_login_button(self) -> None:
        """النقر على زر تسجيل الدخول"""
        try:
            logging_helper.log_step("النقر على زر تسجيل الدخول")
            
            # انتظار ظهور الزر
            self.wait_for_element(self.locators.LOGIN_BUTTON)
            
            # التحقق من تفعيل الزر
            assert self.is_enabled(self.locators.LOGIN_BUTTON), "زر تسجيل الدخول غير مفعل"
            
            # النقر على الزر
            self.click(self.locators.LOGIN_BUTTON)
            
            logging_helper.log_step("تم النقر على زر تسجيل الدخول")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في النقر على زر تسجيل الدخول: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "login_button_error", 
                "خطأ في النقر على زر تسجيل الدخول",
                "fail"
            )
            raise
    
    def check_remember_me(self, check: bool = True) -> None:
        """
        تفعيل أو إلغاء تفعيل خيار تذكرني
        
        Args:
            check: True لتفعيل، False لإلغاء التفعيل
        """
        try:
            action = "تفعيل" if check else "إلغاء تفعيل"
            logging_helper.log_step(f"{action} خيار تذكرني")
            
            # التحقق من وجود خيار تذكرني
            if self.is_visible(self.locators.REMEMBER_ME_CHECKBOX):
                current_state = self.get_attribute(self.locators.REMEMBER_ME_CHECKBOX, "checked")
                
                # إذا كانت الحالة الحالية مختلفة عن المطلوبة، انقر على الخيار
                if (current_state == "true") != check:
                    self.click(self.locators.REMEMBER_ME_CHECKBOX)
                
                logging_helper.log_step(f"تم {action} خيار تذكرني")
            else:
                logging_helper.log_step("خيار تذكرني غير موجود في الصفحة")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في {action} خيار تذكرني: {str(e)}")
            raise
    
    def perform_login(self, username: str, password: str, remember_me: bool = False) -> None:
        """
        تنفيذ عملية تسجيل الدخول الكاملة
        
        Args:
            username: اسم المستخدم
            password: كلمة المرور
            remember_me: تفعيل تذكرني (اختياري)
        """
        try:
            logging_helper.log_step("بدء عملية تسجيل الدخول")
            
            # إدخال البيانات
            self.enter_username(username)
            self.enter_password(password)
            
            # تفعيل تذكرني إذا طُلب
            if remember_me:
                self.check_remember_me(True)
            
            # النقر على زر تسجيل الدخول
            self.click_login_button()
            
            logging_helper.log_step("تم تنفيذ عملية تسجيل الدخول")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في تنفيذ عملية تسجيل الدخول: {str(e)}")
            raise
    
    def get_error_message(self) -> str:
        """
        الحصول على رسالة الخطأ
        
        Returns:
            str: رسالة الخطأ
        """
        try:
            if self.is_visible(self.locators.ERROR_MESSAGE):
                error_text = self.get_text(self.locators.ERROR_MESSAGE)
                logging_helper.log_step(f"رسالة الخطأ: {error_text}")
                return error_text
            return ""
        except Exception as e:
            logging_helper.log_error(f"خطأ في الحصول على رسالة الخطأ: {str(e)}")
            return ""
    
    def get_success_message(self) -> str:
        """
        الحصول على رسالة النجاح
        
        Returns:
            str: رسالة النجاح
        """
        try:
            if self.is_visible(self.locators.SUCCESS_MESSAGE):
                success_text = self.get_text(self.locators.SUCCESS_MESSAGE)
                logging_helper.log_step(f"رسالة النجاح: {success_text}")
                return success_text
            return ""
        except Exception as e:
            logging_helper.log_error(f"خطأ في الحصول على رسالة النجاح: {str(e)}")
            return ""
    
    def is_login_successful(self) -> bool:
        """
        التحقق من نجاح تسجيل الدخول
        
        Returns:
            bool: True إذا نجح تسجيل الدخول
        """
        try:
            # انتظار قليل للتحقق من النتيجة
            self.page.wait_for_timeout(2000)
            
            # التحقق من تغيير الرابط (انتقال إلى لوحة التحكم)
            current_url = self.get_current_url()
            is_dashboard = "dashboard" in current_url.lower() or "home" in current_url.lower()
            
            # التحقق من عدم وجود رسائل خطأ
            has_error = self.is_visible(self.locators.ERROR_MESSAGE)
            
            success = is_dashboard and not has_error
            
            logging_helper.log_step(f"نتيجة تسجيل الدخول: {'نجح' if success else 'فشل'}")
            
            return success
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في التحقق من نجاح تسجيل الدخول: {str(e)}")
            return False
    
    def click_forgot_password_link(self) -> None:
        """النقر على رابط نسيت كلمة المرور"""
        try:
            logging_helper.log_step("النقر على رابط نسيت كلمة المرور")
            
            if self.is_visible(self.locators.FORGOT_PASSWORD_LINK):
                self.click(self.locators.FORGOT_PASSWORD_LINK)
                logging_helper.log_step("تم النقر على رابط نسيت كلمة المرور")
            else:
                logging_helper.log_step("رابط نسيت كلمة المرور غير موجود")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في النقر على رابط نسيت كلمة المرور: {str(e)}")
            raise
    
    def click_register_link(self) -> None:
        """النقر على رابط إنشاء حساب"""
        try:
            logging_helper.log_step("النقر على رابط إنشاء حساب")
            
            if self.is_visible(self.locators.REGISTER_LINK):
                self.click(self.locators.REGISTER_LINK)
                logging_helper.log_step("تم النقر على رابط إنشاء حساب")
            else:
                logging_helper.log_step("رابط إنشاء حساب غير موجود")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في النقر على رابط إنشاء حساب: {str(e)}")
            raise
    
    def verify_page_elements(self) -> bool:
        """
        التحقق من وجود جميع عناصر الصفحة المطلوبة
        
        Returns:
            bool: True إذا كانت جميع العناصر موجودة
        """
        try:
            logging_helper.log_step("التحقق من عناصر صفحة تسجيل الدخول")
            
            required_elements = [
                (self.locators.USERNAME_INPUT, "حقل اسم المستخدم"),
                (self.locators.PASSWORD_INPUT, "حقل كلمة المرور"),
                (self.locators.LOGIN_BUTTON, "زر تسجيل الدخول")
            ]
            
            all_present = True
            for selector, element_name in required_elements:
                if not self.is_visible(selector):
                    logging_helper.log_error(f"العنصر غير موجود: {element_name}")
                    all_present = False
            
            logging_helper.log_step(f"نتيجة التحقق من العناصر: {'نجح' if all_present else 'فشل'}")
            return all_present
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في التحقق من عناصر الصفحة: {str(e)}")
            return False
    
    def clear_form(self) -> None:
        """مسح جميع حقول النموذج"""
        try:
            logging_helper.log_step("مسح حقول النموذج")
            
            # مسح حقل اسم المستخدم
            if self.is_visible(self.locators.USERNAME_INPUT):
                self.fill(self.locators.USERNAME_INPUT, "")
            
            # مسح حقل كلمة المرور
            if self.is_visible(self.locators.PASSWORD_INPUT):
                self.fill(self.locators.PASSWORD_INPUT, "")
            
            # إلغاء تفعيل تذكرني
            if self.is_visible(self.locators.REMEMBER_ME_CHECKBOX):
                self.check_remember_me(False)
            
            logging_helper.log_step("تم مسح حقول النموذج")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في مسح حقول النموذج: {str(e)}")
            raise

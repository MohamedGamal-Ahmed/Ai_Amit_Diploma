"""
Registration Page Object - صفحة التسجيل
يحتوي على جميع العمليات المتعلقة بصفحة التسجيل
"""

from typing import Optional, Dict, Any
from playwright.sync_api import Page
from utils.base_page import BasePage
from locators.all_locators import RegistrationPageLocators
from utils.helpers import screenshot_helper, allure_helper, logging_helper


class RegistrationPage(BasePage):
    """صفحة التسجيل"""
    
    def __init__(self, page: Page):
        """
        تهيئة صفحة التسجيل
        
        Args:
            page: كائن Playwright Page
        """
        super().__init__(page)
        self.locators = RegistrationPageLocators()
        self.page_url = self.config.REGISTRATION_URL
    
    def navigate_to_registration_page(self) -> None:
        """الانتقال إلى صفحة التسجيل"""
        try:
            logging_helper.log_step("الانتقال إلى صفحة التسجيل")
            self.navigate_to(self.page_url)
            self.wait_for_page_load()
            
            # التحقق من تحميل الصفحة
            self.assert_element_visible(
                self.locators.REGISTRATION_FORM,
                "صفحة التسجيل لم يتم تحميلها بشكل صحيح"
            )
            
            # أخذ لقطة شاشة للصفحة المحملة
            screenshot_helper.take_screenshot(
                self.page, 
                "registration_page_loaded", 
                "صفحة التسجيل محملة"
            )
            
            logging_helper.log_step("تم تحميل صفحة التسجيل بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في تحميل صفحة التسجيل: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "registration_page_error", 
                "خطأ في تحميل صفحة التسجيل",
                "fail"
            )
            raise
    
    def enter_first_name(self, first_name: str) -> None:
        """
        إدخال الاسم الأول
        
        Args:
            first_name: الاسم الأول
        """
        try:
            logging_helper.log_step(f"إدخال الاسم الأول: {first_name}")
            
            # انتظار ظهور الحقل
            self.wait_for_element(self.locators.FIRST_NAME_INPUT)
            
            # ملء الحقل
            self.fill(self.locators.FIRST_NAME_INPUT, first_name)
            
            # التحقق من إدخال البيانات
            entered_value = self.get_attribute(self.locators.FIRST_NAME_INPUT, "value")
            assert entered_value == first_name, f"لم يتم إدخال الاسم الأول بشكل صحيح: {entered_value}"
            
            logging_helper.log_step("تم إدخال الاسم الأول بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في إدخال الاسم الأول: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "first_name_input_error", 
                "خطأ في إدخال الاسم الأول",
                "fail"
            )
            raise
    
    def enter_last_name(self, last_name: str) -> None:
        """
        إدخال الاسم الأخير
        
        Args:
            last_name: الاسم الأخير
        """
        try:
            logging_helper.log_step(f"إدخال الاسم الأخير: {last_name}")
            
            # انتظار ظهور الحقل
            self.wait_for_element(self.locators.LAST_NAME_INPUT)
            
            # ملء الحقل
            self.fill(self.locators.LAST_NAME_INPUT, last_name)
            
            # التحقق من إدخال البيانات
            entered_value = self.get_attribute(self.locators.LAST_NAME_INPUT, "value")
            assert entered_value == last_name, f"لم يتم إدخال الاسم الأخير بشكل صحيح: {entered_value}"
            
            logging_helper.log_step("تم إدخال الاسم الأخير بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في إدخال الاسم الأخير: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "last_name_input_error", 
                "خطأ في إدخال الاسم الأخير",
                "fail"
            )
            raise
    
    def enter_email(self, email: str) -> None:
        """
        إدخال البريد الإلكتروني
        
        Args:
            email: البريد الإلكتروني
        """
        try:
            logging_helper.log_step(f"إدخال البريد الإلكتروني: {email}")
            
            # انتظار ظهور الحقل
            self.wait_for_element(self.locators.EMAIL_INPUT)
            
            # ملء الحقل
            self.fill(self.locators.EMAIL_INPUT, email)
            
            # التحقق من إدخال البيانات
            entered_value = self.get_attribute(self.locators.EMAIL_INPUT, "value")
            assert entered_value == email, f"لم يتم إدخال البريد الإلكتروني بشكل صحيح: {entered_value}"
            
            logging_helper.log_step("تم إدخال البريد الإلكتروني بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في إدخال البريد الإلكتروني: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "email_input_error", 
                "خطأ في إدخال البريد الإلكتروني",
                "fail"
            )
            raise
    
    def enter_phone(self, phone: str) -> None:
        """
        إدخال رقم الهاتف
        
        Args:
            phone: رقم الهاتف
        """
        try:
            logging_helper.log_step(f"إدخال رقم الهاتف: {phone}")
            
            # انتظار ظهور الحقل
            self.wait_for_element(self.locators.PHONE_INPUT)
            
            # ملء الحقل
            self.fill(self.locators.PHONE_INPUT, phone)
            
            # التحقق من إدخال البيانات
            entered_value = self.get_attribute(self.locators.PHONE_INPUT, "value")
            assert entered_value == phone, f"لم يتم إدخال رقم الهاتف بشكل صحيح: {entered_value}"
            
            logging_helper.log_step("تم إدخال رقم الهاتف بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في إدخال رقم الهاتف: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "phone_input_error", 
                "خطأ في إدخال رقم الهاتف",
                "fail"
            )
            raise
    
    def enter_address(self, address: str) -> None:
        """
        إدخال العنوان
        
        Args:
            address: العنوان
        """
        try:
            logging_helper.log_step(f"إدخال العنوان: {address}")
            
            # انتظار ظهور الحقل
            self.wait_for_element(self.locators.ADDRESS_INPUT)
            
            # ملء الحقل
            self.fill(self.locators.ADDRESS_INPUT, address)
            
            # التحقق من إدخال البيانات
            entered_value = self.get_attribute(self.locators.ADDRESS_INPUT, "value")
            assert entered_value == address, f"لم يتم إدخال العنوان بشكل صحيح: {entered_value}"
            
            logging_helper.log_step("تم إدخال العنوان بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في إدخال العنوان: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "address_input_error", 
                "خطأ في إدخال العنوان",
                "fail"
            )
            raise
    
    def select_city(self, city: str) -> None:
        """
        اختيار المدينة
        
        Args:
            city: المدينة
        """
        try:
            logging_helper.log_step(f"اختيار المدينة: {city}")
            
            # انتظار ظهور القائمة المنسدلة
            self.wait_for_element(self.locators.CITY_SELECT)
            
            # اختيار المدينة
            self.select_option(self.locators.CITY_SELECT, city)
            
            logging_helper.log_step("تم اختيار المدينة بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في اختيار المدينة: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "city_select_error", 
                "خطأ في اختيار المدينة",
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
            
            # انتظار ظهور الحقل
            self.wait_for_element(self.locators.PASSWORD_INPUT)
            
            # ملء الحقل
            self.fill(self.locators.PASSWORD_INPUT, password)
            
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
    
    def enter_confirm_password(self, confirm_password: str) -> None:
        """
        إدخال تأكيد كلمة المرور
        
        Args:
            confirm_password: تأكيد كلمة المرور
        """
        try:
            logging_helper.log_step("إدخال تأكيد كلمة المرور")
            
            # انتظار ظهور الحقل
            self.wait_for_element(self.locators.CONFIRM_PASSWORD_INPUT)
            
            # ملء الحقل
            self.fill(self.locators.CONFIRM_PASSWORD_INPUT, confirm_password)
            
            logging_helper.log_step("تم إدخال تأكيد كلمة المرور بنجاح")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في إدخال تأكيد كلمة المرور: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "confirm_password_input_error", 
                "خطأ في إدخال تأكيد كلمة المرور",
                "fail"
            )
            raise
    
    def accept_terms(self, accept: bool = True) -> None:
        """
        الموافقة على الشروط والأحكام
        
        Args:
            accept: True للموافقة، False لرفض الموافقة
        """
        try:
            action = "الموافقة على" if accept else "رفض"
            logging_helper.log_step(f"{action} الشروط والأحكام")
            
            # التحقق من وجود خيار الشروط
            if self.is_visible(self.locators.TERMS_CHECKBOX):
                current_state = self.get_attribute(self.locators.TERMS_CHECKBOX, "checked")
                
                # إذا كانت الحالة الحالية مختلفة عن المطلوبة، انقر على الخيار
                if (current_state == "true") != accept:
                    self.click(self.locators.TERMS_CHECKBOX)
                
                logging_helper.log_step(f"تم {action} الشروط والأحكام")
            else:
                logging_helper.log_step("خيار الشروط والأحكام غير موجود في الصفحة")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في {action} الشروط والأحكام: {str(e)}")
            raise
    
    def accept_privacy(self, accept: bool = True) -> None:
        """
        الموافقة على سياسة الخصوصية
        
        Args:
            accept: True للموافقة، False لرفض الموافقة
        """
        try:
            action = "الموافقة على" if accept else "رفض"
            logging_helper.log_step(f"{action} سياسة الخصوصية")
            
            # التحقق من وجود خيار الخصوصية
            if self.is_visible(self.locators.PRIVACY_CHECKBOX):
                current_state = self.get_attribute(self.locators.PRIVACY_CHECKBOX, "checked")
                
                # إذا كانت الحالة الحالية مختلفة عن المطلوبة، انقر على الخيار
                if (current_state == "true") != accept:
                    self.click(self.locators.PRIVACY_CHECKBOX)
                
                logging_helper.log_step(f"تم {action} سياسة الخصوصية")
            else:
                logging_helper.log_step("خيار سياسة الخصوصية غير موجود في الصفحة")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في {action} سياسة الخصوصية: {str(e)}")
            raise
    
    def subscribe_to_newsletter(self, subscribe: bool = True) -> None:
        """
        الاشتراك في النشرة الإخبارية
        
        Args:
            subscribe: True للاشتراك، False لإلغاء الاشتراك
        """
        try:
            action = "الاشتراك في" if subscribe else "إلغاء الاشتراك من"
            logging_helper.log_step(f"{action} النشرة الإخبارية")
            
            # التحقق من وجود خيار النشرة الإخبارية
            if self.is_visible(self.locators.NEWSLETTER_CHECKBOX):
                current_state = self.get_attribute(self.locators.NEWSLETTER_CHECKBOX, "checked")
                
                # إذا كانت الحالة الحالية مختلفة عن المطلوبة، انقر على الخيار
                if (current_state == "true") != subscribe:
                    self.click(self.locators.NEWSLETTER_CHECKBOX)
                
                logging_helper.log_step(f"تم {action} النشرة الإخبارية")
            else:
                logging_helper.log_step("خيار النشرة الإخبارية غير موجود في الصفحة")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في {action} النشرة الإخبارية: {str(e)}")
            raise
    
    def click_register_button(self) -> None:
        """النقر على زر إنشاء الحساب"""
        try:
            logging_helper.log_step("النقر على زر إنشاء الحساب")
            
            # انتظار ظهور الزر
            self.wait_for_element(self.locators.REGISTER_BUTTON)
            
            # التحقق من تفعيل الزر
            assert self.is_enabled(self.locators.REGISTER_BUTTON), "زر إنشاء الحساب غير مفعل"
            
            # النقر على الزر
            self.click(self.locators.REGISTER_BUTTON)
            
            logging_helper.log_step("تم النقر على زر إنشاء الحساب")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في النقر على زر إنشاء الحساب: {str(e)}")
            screenshot_helper.take_screenshot(
                self.page, 
                "register_button_error", 
                "خطأ في النقر على زر إنشاء الحساب",
                "fail"
            )
            raise
    
    def perform_registration(self, registration_data: Dict[str, Any]) -> None:
        """
        تنفيذ عملية التسجيل الكاملة
        
        Args:
            registration_data: بيانات التسجيل
        """
        try:
            logging_helper.log_step("بدء عملية التسجيل")
            
            # إدخال البيانات الشخصية
            self.enter_first_name(registration_data.get("first_name", ""))
            self.enter_last_name(registration_data.get("last_name", ""))
            self.enter_email(registration_data.get("email", ""))
            self.enter_phone(registration_data.get("phone", ""))
            self.enter_address(registration_data.get("address", ""))
            
            # اختيار المدينة إذا كانت متوفرة
            if registration_data.get("city"):
                self.select_city(registration_data["city"])
            
            # إدخال كلمات المرور
            self.enter_password(registration_data.get("password", ""))
            self.enter_confirm_password(registration_data.get("confirm_password", ""))
            
            # الموافقة على الشروط والأحكام
            if registration_data.get("terms_accepted", False):
                self.accept_terms(True)
            
            # الموافقة على سياسة الخصوصية
            if registration_data.get("privacy_accepted", False):
                self.accept_privacy(True)
            
            # الاشتراك في النشرة الإخبارية
            if registration_data.get("newsletter_subscription", False):
                self.subscribe_to_newsletter(True)
            
            # النقر على زر إنشاء الحساب
            self.click_register_button()
            
            logging_helper.log_step("تم تنفيذ عملية التسجيل")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في تنفيذ عملية التسجيل: {str(e)}")
            raise
    
    def get_error_message(self, error_type: str = "general") -> str:
        """
        الحصول على رسالة الخطأ
        
        Args:
            error_type: نوع الخطأ (general, email, phone, password)
            
        Returns:
            str: رسالة الخطأ
        """
        try:
            error_selectors = {
                "general": self.locators.GENERAL_ERROR,
                "email": self.locators.EMAIL_ERROR,
                "phone": self.locators.PHONE_ERROR,
                "password": self.locators.PASSWORD_ERROR
            }
            
            selector = error_selectors.get(error_type, self.locators.GENERAL_ERROR)
            
            if self.is_visible(selector):
                error_text = self.get_text(selector)
                logging_helper.log_step(f"رسالة الخطأ ({error_type}): {error_text}")
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
    
    def is_registration_successful(self) -> bool:
        """
        التحقق من نجاح التسجيل
        
        Returns:
            bool: True إذا نجح التسجيل
        """
        try:
            # انتظار قليل للتحقق من النتيجة
            self.page.wait_for_timeout(3000)
            
            # التحقق من تغيير الرابط أو ظهور رسالة نجاح
            current_url = self.get_current_url()
            has_success_message = self.is_visible(self.locators.SUCCESS_MESSAGE)
            has_error_message = self.is_visible(self.locators.GENERAL_ERROR)
            
            success = has_success_message and not has_error_message
            
            logging_helper.log_step(f"نتيجة التسجيل: {'نجح' if success else 'فشل'}")
            
            return success
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في التحقق من نجاح التسجيل: {str(e)}")
            return False
    
    def click_cancel_button(self) -> None:
        """النقر على زر إلغاء"""
        try:
            logging_helper.log_step("النقر على زر إلغاء")
            
            if self.is_visible(self.locators.CANCEL_BUTTON):
                self.click(self.locators.CANCEL_BUTTON)
                logging_helper.log_step("تم النقر على زر إلغاء")
            else:
                logging_helper.log_step("زر إلغاء غير موجود")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في النقر على زر إلغاء: {str(e)}")
            raise
    
    def verify_page_elements(self) -> bool:
        """
        التحقق من وجود جميع عناصر الصفحة المطلوبة
        
        Returns:
            bool: True إذا كانت جميع العناصر موجودة
        """
        try:
            logging_helper.log_step("التحقق من عناصر صفحة التسجيل")
            
            required_elements = [
                (self.locators.FIRST_NAME_INPUT, "حقل الاسم الأول"),
                (self.locators.LAST_NAME_INPUT, "حقل الاسم الأخير"),
                (self.locators.EMAIL_INPUT, "حقل البريد الإلكتروني"),
                (self.locators.PHONE_INPUT, "حقل رقم الهاتف"),
                (self.locators.ADDRESS_INPUT, "حقل العنوان"),
                (self.locators.PASSWORD_INPUT, "حقل كلمة المرور"),
                (self.locators.CONFIRM_PASSWORD_INPUT, "حقل تأكيد كلمة المرور"),
                (self.locators.REGISTER_BUTTON, "زر إنشاء الحساب")
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
            logging_helper.log_step("مسح حقول نموذج التسجيل")
            
            # مسح جميع الحقول النصية
            text_fields = [
                self.locators.FIRST_NAME_INPUT,
                self.locators.LAST_NAME_INPUT,
                self.locators.EMAIL_INPUT,
                self.locators.PHONE_INPUT,
                self.locators.ADDRESS_INPUT,
                self.locators.PASSWORD_INPUT,
                self.locators.CONFIRM_PASSWORD_INPUT
            ]
            
            for field in text_fields:
                if self.is_visible(field):
                    self.fill(field, "")
            
            # إلغاء تفعيل جميع الخيارات
            checkboxes = [
                self.locators.TERMS_CHECKBOX,
                self.locators.PRIVACY_CHECKBOX,
                self.locators.NEWSLETTER_CHECKBOX
            ]
            
            for checkbox in checkboxes:
                if self.is_visible(checkbox):
                    self.accept_terms(False)
                    self.accept_privacy(False)
                    self.subscribe_to_newsletter(False)
            
            logging_helper.log_step("تم مسح حقول نموذج التسجيل")
            
        except Exception as e:
            logging_helper.log_error(f"خطأ في مسح حقول النموذج: {str(e)}")
            raise

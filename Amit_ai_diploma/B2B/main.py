"""
Main Test Execution File - ملف التنفيذ الرئيسي للاختبارات
يقرأ test_cases.json وينفذ الاختبارات باستخدام pytest
"""

import json
import pytest
import allure
import logging
import time
from typing import Dict, Any, List
from playwright.sync_api import sync_playwright
from config.config import Config
from pages.login_page import LoginPage
from pages.registration_page import RegistrationPage
from test_data.login_data import get_login_data, get_all_login_scenarios
from test_data.registration_data import get_registration_data
from utils.helpers import (
    screenshot_helper, 
    allure_helper, 
    logging_helper, 
    data_helper,
    utility_helper
)


class TestExecutor:
    """منفذ الاختبارات الرئيسي"""
    
    def __init__(self):
        self.config = Config()
        self.logger = logging.getLogger(__name__)
        self.test_cases = None
        self.browser = None
        self.context = None
        self.page = None
        
        # تحميل حالات الاختبار
        self.load_test_cases()
    
    def load_test_cases(self) -> None:
        """تحميل حالات الاختبار من ملف JSON"""
        try:
            self.test_cases = data_helper.load_test_cases("test_data/test_cases.json")
            self.logger.info("تم تحميل حالات الاختبار بنجاح")
        except Exception as e:
            self.logger.error(f"خطأ في تحميل حالات الاختبار: {str(e)}")
            raise
    
    def setup_browser(self) -> None:
        """إعداد المتصفح"""
        try:
            self.logger.info("إعداد المتصفح")
            
            playwright = sync_playwright().start()
            browser_config = self.config.get_browser_config()
            
            # تشغيل المتصفح
            self.browser = playwright.chromium.launch(
                headless=browser_config["headless"],
                slow_mo=browser_config["slow_mo"],
                args=browser_config["args"]
            )
            
            # إنشاء السياق
            self.context = self.browser.new_context(
                viewport=browser_config["viewport"],
                timeout=browser_config["timeout"]
            )
            
            # إنشاء الصفحة
            self.page = self.context.new_page()
            
            self.logger.info("تم إعداد المتصفح بنجاح")
            
        except Exception as e:
            self.logger.error(f"خطأ في إعداد المتصفح: {str(e)}")
            raise
    
    def teardown_browser(self) -> None:
        """إغلاق المتصفح"""
        try:
            if self.page:
                self.page.close()
            if self.context:
                self.context.close()
            if self.browser:
                self.browser.close()
            self.logger.info("تم إغلاق المتصفح")
        except Exception as e:
            self.logger.error(f"خطأ في إغلاق المتصفح: {str(e)}")
    
    def execute_login_tests(self) -> None:
        """تنفيذ اختبارات تسجيل الدخول"""
        try:
            self.logger.info("بدء تنفيذ اختبارات تسجيل الدخول")
            
            login_page = LoginPage(self.page)
            
            # الحصول على اختبارات تسجيل الدخول
            login_tests = self.test_cases.get("LoginPage", {}).get("Login_Feature", {})
            
            # تنفيذ الاختبارات الإيجابية
            positive_tests = login_tests.get("positive", [])
            for test_case in positive_tests:
                self.execute_login_test_case(test_case, login_page, "positive")
            
            # تنفيذ الاختبارات السلبية
            negative_tests = login_tests.get("negative", [])
            for test_case in negative_tests:
                self.execute_login_test_case(test_case, login_page, "negative")
            
            self.logger.info("تم الانتهاء من اختبارات تسجيل الدخول")
            
        except Exception as e:
            self.logger.error(f"خطأ في تنفيذ اختبارات تسجيل الدخول: {str(e)}")
            raise
    
    def execute_login_test_case(self, test_case: Dict[str, Any], 
                               login_page: LoginPage, test_type: str) -> None:
        """
        تنفيذ حالة اختبار تسجيل الدخول
        
        Args:
            test_case: حالة الاختبار
            login_page: صفحة تسجيل الدخول
            test_type: نوع الاختبار (positive/negative)
        """
        test_id = test_case.get("test_id", "UNKNOWN")
        description = test_case.get("description", "")
        
        try:
            with allure.step(f"تنفيذ {test_id}: {description}"):
                # إضافة تفاصيل الاختبار للـ Allure
                allure_helper.add_test_data(test_case, f"Test Case Data - {test_id}")
                
                # بدء تسجيل الاختبار
                logging_helper.log_test_start(test_id, test_case)
                
                # الانتقال إلى صفحة تسجيل الدخول
                login_page.navigate_to_login_page()
                
                # الحصول على بيانات الاختبار
                test_data = test_case.get("test_data", {})
                username = test_data.get("username", "")
                password = test_data.get("password", "")
                remember_me = test_data.get("remember_me", False)
                
                # تنفيذ تسجيل الدخول
                login_page.perform_login(username, password, remember_me)
                
                # التحقق من النتيجة المتوقعة
                expected_result = test_case.get("expected_result", "")
                
                if test_type == "positive":
                    # للاختبارات الإيجابية، نتوقع النجاح
                    success = login_page.is_login_successful()
                    
                    if success:
                        screenshot_helper.take_screenshot(
                            self.page, 
                            f"{test_id}_success", 
                            f"نجح الاختبار: {description}",
                            "pass"
                        )
                        logging_helper.log_test_end(test_id, "PASS")
                    else:
                        error_msg = login_page.get_error_message()
                        screenshot_helper.take_screenshot(
                            self.page, 
                            f"{test_id}_fail", 
                            f"فشل الاختبار: {description}",
                            "fail"
                        )
                        allure_helper.add_error_details(f"Expected success but got error: {error_msg}")
                        logging_helper.log_test_end(test_id, "FAIL")
                        pytest.fail(f"Expected login success but failed: {error_msg}")
                
                else:  # negative tests
                    # للاختبارات السلبية، نتوقع الفشل
                    success = login_page.is_login_successful()
                    
                    if not success:
                        error_msg = login_page.get_error_message()
                        screenshot_helper.take_screenshot(
                            self.page, 
                            f"{test_id}_success", 
                            f"نجح الاختبار السالب: {description}",
                            "pass"
                        )
                        logging_helper.log_test_end(test_id, "PASS")
                    else:
                        screenshot_helper.take_screenshot(
                            self.page, 
                            f"{test_id}_fail", 
                            f"فشل الاختبار السالب: {description}",
                            "fail"
                        )
                        allure_helper.add_error_details("Expected login failure but succeeded")
                        logging_helper.log_test_end(test_id, "FAIL")
                        pytest.fail("Expected login failure but succeeded")
                
        except Exception as e:
            # في حالة حدوث خطأ غير متوقع
            screenshot_helper.take_screenshot(
                self.page, 
                f"{test_id}_error", 
                f"خطأ في الاختبار: {description}",
                "fail"
            )
            allure_helper.add_error_details(f"Unexpected error: {str(e)}")
            logging_helper.log_test_end(test_id, "FAIL")
            raise
    
    def execute_registration_tests(self) -> None:
        """تنفيذ اختبارات التسجيل"""
        try:
            self.logger.info("بدء تنفيذ اختبارات التسجيل")
            
            registration_page = RegistrationPage(self.page)
            
            # الحصول على اختبارات التسجيل
            registration_tests = self.test_cases.get("RegistrationPage", {}).get("Registration_Feature", {})
            
            # تنفيذ الاختبارات الإيجابية
            positive_tests = registration_tests.get("positive", [])
            for test_case in positive_tests:
                self.execute_registration_test_case(test_case, registration_page, "positive")
            
            # تنفيذ الاختبارات السلبية
            negative_tests = registration_tests.get("negative", [])
            for test_case in negative_tests:
                self.execute_registration_test_case(test_case, registration_page, "negative")
            
            self.logger.info("تم الانتهاء من اختبارات التسجيل")
            
        except Exception as e:
            self.logger.error(f"خطأ في تنفيذ اختبارات التسجيل: {str(e)}")
            raise
    
    def execute_registration_test_case(self, test_case: Dict[str, Any], 
                                     registration_page: RegistrationPage, test_type: str) -> None:
        """
        تنفيذ حالة اختبار التسجيل
        
        Args:
            test_case: حالة الاختبار
            registration_page: صفحة التسجيل
            test_type: نوع الاختبار (positive/negative)
        """
        test_id = test_case.get("test_id", "UNKNOWN")
        description = test_case.get("description", "")
        
        try:
            with allure.step(f"تنفيذ {test_id}: {description}"):
                # إضافة تفاصيل الاختبار للـ Allure
                allure_helper.add_test_data(test_case, f"Test Case Data - {test_id}")
                
                # بدء تسجيل الاختبار
                logging_helper.log_test_start(test_id, test_case)
                
                # الانتقال إلى صفحة التسجيل
                registration_page.navigate_to_registration_page()
                
                # الحصول على بيانات الاختبار
                test_data = test_case.get("test_data", {})
                
                # توليد البيانات إذا كانت مطلوبة
                if test_data.get("first_name") == "generated":
                    registration_data = get_registration_data("valid")
                else:
                    registration_data = test_data
                
                # تنفيذ التسجيل
                registration_page.perform_registration(registration_data)
                
                # التحقق من النتيجة المتوقعة
                expected_result = test_case.get("expected_result", "")
                
                if test_type == "positive":
                    # للاختبارات الإيجابية، نتوقع النجاح
                    success = registration_page.is_registration_successful()
                    
                    if success:
                        screenshot_helper.take_screenshot(
                            self.page, 
                            f"{test_id}_success", 
                            f"نجح الاختبار: {description}",
                            "pass"
                        )
                        logging_helper.log_test_end(test_id, "PASS")
                    else:
                        error_msg = registration_page.get_error_message()
                        screenshot_helper.take_screenshot(
                            self.page, 
                            f"{test_id}_fail", 
                            f"فشل الاختبار: {description}",
                            "fail"
                        )
                        allure_helper.add_error_details(f"Expected success but got error: {error_msg}")
                        logging_helper.log_test_end(test_id, "FAIL")
                        pytest.fail(f"Expected registration success but failed: {error_msg}")
                
                else:  # negative tests
                    # للاختبارات السلبية، نتوقع الفشل
                    success = registration_page.is_registration_successful()
                    
                    if not success:
                        error_msg = registration_page.get_error_message()
                        screenshot_helper.take_screenshot(
                            self.page, 
                            f"{test_id}_success", 
                            f"نجح الاختبار السالب: {description}",
                            "pass"
                        )
                        logging_helper.log_test_end(test_id, "PASS")
                    else:
                        screenshot_helper.take_screenshot(
                            self.page, 
                            f"{test_id}_fail", 
                            f"فشل الاختبار السالب: {description}",
                            "fail"
                        )
                        allure_helper.add_error_details("Expected registration failure but succeeded")
                        logging_helper.log_test_end(test_id, "FAIL")
                        pytest.fail("Expected registration failure but succeeded")
                
        except Exception as e:
            # في حالة حدوث خطأ غير متوقع
            screenshot_helper.take_screenshot(
                self.page, 
                f"{test_id}_error", 
                f"خطأ في الاختبار: {description}",
                "fail"
            )
            allure_helper.add_error_details(f"Unexpected error: {str(e)}")
            logging_helper.log_test_end(test_id, "FAIL")
            raise
    
    def execute_home_page_tests(self) -> None:
        """تنفيذ اختبارات الصفحة الرئيسية"""
        try:
            self.logger.info("بدء تنفيذ اختبارات الصفحة الرئيسية")
            
            # الحصول على اختبارات الصفحة الرئيسية
            home_tests = self.test_cases.get("HomePage", {}).get("Navigation_Feature", {})
            
            # تنفيذ الاختبارات الإيجابية
            positive_tests = home_tests.get("positive", [])
            for test_case in positive_tests:
                self.execute_home_page_test_case(test_case)
            
            self.logger.info("تم الانتهاء من اختبارات الصفحة الرئيسية")
            
        except Exception as e:
            self.logger.error(f"خطأ في تنفيذ اختبارات الصفحة الرئيسية: {str(e)}")
            raise
    
    def execute_home_page_test_case(self, test_case: Dict[str, Any]) -> None:
        """
        تنفيذ حالة اختبار الصفحة الرئيسية
        
        Args:
            test_case: حالة الاختبار
        """
        test_id = test_case.get("test_id", "UNKNOWN")
        description = test_case.get("description", "")
        
        try:
            with allure.step(f"تنفيذ {test_id}: {description}"):
                # إضافة تفاصيل الاختبار للـ Allure
                allure_helper.add_test_data(test_case, f"Test Case Data - {test_id}")
                
                # بدء تسجيل الاختبار
                logging_helper.log_test_start(test_id, test_case)
                
                # الانتقال إلى الصفحة الرئيسية
                self.page.goto(self.config.BASE_URL)
                self.page.wait_for_load_state("networkidle")
                
                # التحقق من تحميل الصفحة
                page_title = self.page.title()
                assert page_title, "الصفحة الرئيسية لم يتم تحميلها"
                
                screenshot_helper.take_screenshot(
                    self.page, 
                    f"{test_id}_success", 
                    f"نجح الاختبار: {description}",
                    "pass"
                )
                
                logging_helper.log_test_end(test_id, "PASS")
                
        except Exception as e:
            screenshot_helper.take_screenshot(
                self.page, 
                f"{test_id}_error", 
                f"خطأ في الاختبار: {description}",
                "fail"
            )
            allure_helper.add_error_details(f"Unexpected error: {str(e)}")
            logging_helper.log_test_end(test_id, "FAIL")
            raise
    
    def run_all_tests(self) -> None:
        """تشغيل جميع الاختبارات"""
        try:
            self.logger.info("بدء تشغيل جميع الاختبارات")
            
            # إعداد المتصفح
            self.setup_browser()
            
            # تنفيذ الاختبارات
            self.execute_home_page_tests()
            self.execute_login_tests()
            self.execute_registration_tests()
            
            self.logger.info("تم الانتهاء من جميع الاختبارات")
            
        except Exception as e:
            self.logger.error(f"خطأ في تشغيل الاختبارات: {str(e)}")
            raise
        finally:
            # إغلاق المتصفح
            self.teardown_browser()


# دوال الاختبار لـ pytest
@pytest.fixture(scope="session")
def test_executor():
    """Fixture لإنشاء منفذ الاختبارات"""
    executor = TestExecutor()
    executor.setup_browser()
    yield executor
    executor.teardown_browser()


@pytest.mark.smoke
@pytest.mark.login
def test_login_feature(test_executor):
    """اختبار ميزة تسجيل الدخول"""
    with allure.step("تنفيذ اختبارات تسجيل الدخول"):
        test_executor.execute_login_tests()


@pytest.mark.regression
@pytest.mark.registration
def test_registration_feature(test_executor):
    """اختبار ميزة التسجيل"""
    with allure.step("تنفيذ اختبارات التسجيل"):
        test_executor.execute_registration_tests()


@pytest.mark.smoke
@pytest.mark.home
def test_home_page_feature(test_executor):
    """اختبار ميزة الصفحة الرئيسية"""
    with allure.step("تنفيذ اختبارات الصفحة الرئيسية"):
        test_executor.execute_home_page_tests()


# تشغيل الاختبارات إذا تم تنفيذ الملف مباشرة
if __name__ == "__main__":
    # إعداد Allure
    allure.dynamic.description("Test Automation Framework for Etisalat Website")
    allure.dynamic.severity(allure.severity_level.CRITICAL)
    allure.dynamic.tag("etisalat", "automation", "playwright")
    
    # تشغيل الاختبارات
    executor = TestExecutor()
    executor.run_all_tests()

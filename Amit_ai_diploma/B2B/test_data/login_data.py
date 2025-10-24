"""
Login Data - بيانات تسجيل الدخول
يحتوي على بيانات الاختبار لتسجيل الدخول
"""

from typing import Dict, Any, List
from config.config import Config


class LoginTestData:
    """بيانات اختبار تسجيل الدخول"""
    
    def __init__(self):
        self.config = Config()
    
    def get_valid_credentials(self) -> Dict[str, str]:
        """
        الحصول على بيانات تسجيل دخول صحيحة
        
        Returns:
            Dict: بيانات تسجيل الدخول الصحيحة
        """
        return {
            "username": self.config.TEST_CREDENTIALS["valid_username"],
            "password": self.config.TEST_CREDENTIALS["valid_password"],
            "remember_me": False
        }
    
    def get_invalid_credentials(self) -> Dict[str, str]:
        """
        الحصول على بيانات تسجيل دخول غير صحيحة
        
        Returns:
            Dict: بيانات تسجيل الدخول غير الصحيحة
        """
        return {
            "username": self.config.TEST_CREDENTIALS["invalid_username"],
            "password": self.config.TEST_CREDENTIALS["invalid_password"],
            "remember_me": False
        }
    
    def get_empty_credentials(self) -> Dict[str, str]:
        """
        الحصول على بيانات تسجيل دخول فارغة
        
        Returns:
            Dict: بيانات تسجيل الدخول الفارغة
        """
        return {
            "username": "",
            "password": "",
            "remember_me": False
        }
    
    def get_wrong_password_credentials(self) -> Dict[str, str]:
        """
        الحصول على بيانات تسجيل دخول بكلمة مرور خاطئة
        
        Returns:
            Dict: بيانات تسجيل الدخول بكلمة مرور خاطئة
        """
        return {
            "username": self.config.TEST_CREDENTIALS["valid_username"],
            "password": self.config.TEST_CREDENTIALS["invalid_password"],
            "remember_me": False
        }
    
    def get_wrong_username_credentials(self) -> Dict[str, str]:
        """
        الحصول على بيانات تسجيل دخول باسم مستخدم خاطئ
        
        Returns:
            Dict: بيانات تسجيل الدخول باسم مستخدم خاطئ
        """
        return {
            "username": self.config.TEST_CREDENTIALS["invalid_username"],
            "password": self.config.TEST_CREDENTIALS["valid_password"],
            "remember_me": False
        }
    
    def get_credentials_with_remember_me(self) -> Dict[str, Any]:
        """
        الحصول على بيانات تسجيل دخول مع تفعيل تذكرني
        
        Returns:
            Dict: بيانات تسجيل الدخول مع تذكرني
        """
        return {
            "username": self.config.TEST_CREDENTIALS["valid_username"],
            "password": self.config.TEST_CREDENTIALS["valid_password"],
            "remember_me": True
        }
    
    def get_test_scenarios(self) -> List[Dict[str, Any]]:
        """
        الحصول على جميع سيناريوهات الاختبار
        
        Returns:
            List: قائمة بجميع سيناريوهات الاختبار
        """
        return [
            {
                "scenario_name": "valid_login",
                "description": "تسجيل دخول صحيح",
                "data": self.get_valid_credentials(),
                "expected_result": "success",
                "severity": "critical"
            },
            {
                "scenario_name": "invalid_login",
                "description": "تسجيل دخول ببيانات خاطئة",
                "data": self.get_invalid_credentials(),
                "expected_result": "error",
                "severity": "critical"
            },
            {
                "scenario_name": "empty_fields",
                "description": "تسجيل دخول بحقول فارغة",
                "data": self.get_empty_credentials(),
                "expected_result": "validation_error",
                "severity": "normal"
            },
            {
                "scenario_name": "wrong_password",
                "description": "تسجيل دخول بكلمة مرور خاطئة",
                "data": self.get_wrong_password_credentials(),
                "expected_result": "error",
                "severity": "critical"
            },
            {
                "scenario_name": "wrong_username",
                "description": "تسجيل دخول باسم مستخدم خاطئ",
                "data": self.get_wrong_username_credentials(),
                "expected_result": "error",
                "severity": "normal"
            },
            {
                "scenario_name": "remember_me_enabled",
                "description": "تسجيل دخول مع تفعيل تذكرني",
                "data": self.get_credentials_with_remember_me(),
                "expected_result": "success",
                "severity": "normal"
            }
        ]
    
    def get_credentials_by_scenario(self, scenario_name: str) -> Dict[str, Any]:
        """
        الحصول على بيانات تسجيل الدخول حسب اسم السيناريو
        
        Args:
            scenario_name: اسم السيناريو
            
        Returns:
            Dict: بيانات تسجيل الدخول
        """
        scenarios = {
            "valid_login": self.get_valid_credentials(),
            "invalid_login": self.get_invalid_credentials(),
            "empty_fields": self.get_empty_credentials(),
            "wrong_password": self.get_wrong_password_credentials(),
            "wrong_username": self.get_wrong_username_credentials(),
            "remember_me_enabled": self.get_credentials_with_remember_me()
        }
        
        return scenarios.get(scenario_name, self.get_valid_credentials())
    
    def get_edge_case_credentials(self) -> List[Dict[str, Any]]:
        """
        الحصول على بيانات الحالات الحدية
        
        Returns:
            List: قائمة ببيانات الحالات الحدية
        """
        return [
            {
                "scenario_name": "sql_injection_username",
                "description": "محاولة حقن SQL في اسم المستخدم",
                "data": {
                    "username": "admin'; DROP TABLE users; --",
                    "password": "password",
                    "remember_me": False
                },
                "expected_result": "error"
            },
            {
                "scenario_name": "xss_username",
                "description": "محاولة حقن XSS في اسم المستخدم",
                "data": {
                    "username": "<script>alert('XSS')</script>",
                    "password": "password",
                    "remember_me": False
                },
                "expected_result": "error"
            },
            {
                "scenario_name": "very_long_username",
                "description": "اسم مستخدم طويل جداً",
                "data": {
                    "username": "a" * 1000,
                    "password": "password",
                    "remember_me": False
                },
                "expected_result": "validation_error"
            },
            {
                "scenario_name": "very_long_password",
                "description": "كلمة مرور طويلة جداً",
                "data": {
                    "username": "testuser",
                    "password": "a" * 1000,
                    "remember_me": False
                },
                "expected_result": "validation_error"
            },
            {
                "scenario_name": "special_characters",
                "description": "أحرف خاصة في البيانات",
                "data": {
                    "username": "test@#$%^&*()",
                    "password": "pass!@#$%^&*()",
                    "remember_me": False
                },
                "expected_result": "error"
            }
        ]


# إنشاء مثيل عام للبيانات
login_test_data = LoginTestData()


def get_login_data(scenario: str = "valid_login") -> Dict[str, Any]:
    """
    دالة مساعدة للحصول على بيانات تسجيل الدخول
    
    Args:
        scenario: اسم السيناريو
        
    Returns:
        Dict: بيانات تسجيل الدخول
    """
    return login_test_data.get_credentials_by_scenario(scenario)


def get_all_login_scenarios() -> List[Dict[str, Any]]:
    """
    دالة مساعدة للحصول على جميع سيناريوهات تسجيل الدخول
    
    Returns:
        List: قائمة بجميع السيناريوهات
    """
    return login_test_data.get_test_scenarios()


def get_edge_case_scenarios() -> List[Dict[str, Any]]:
    """
    دالة مساعدة للحصول على سيناريوهات الحالات الحدية
    
    Returns:
        List: قائمة بسيناريوهات الحالات الحدية
    """
    return login_test_data.get_edge_case_credentials()

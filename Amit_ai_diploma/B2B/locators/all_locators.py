"""
ملف Locators الرئيسي
يحتوي على جميع العناصر (locators) لكل الصفحات في الموقع
"""

from typing import Dict, Any


class LoginPageLocators:
    """عناصر صفحة تسجيل الدخول"""
    
    # حقول الإدخال
    USERNAME_INPUT = "input[name='username'], input[id='username'], input[type='email']"
    PASSWORD_INPUT = "input[name='password'], input[id='password'], input[type='password']"
    
    # الأزرار
    LOGIN_BUTTON = "button[type='submit'], input[type='submit'], button:has-text('تسجيل الدخول'), button:has-text('Login')"
    FORGOT_PASSWORD_LINK = "a:has-text('نسيت كلمة المرور'), a:has-text('Forgot Password')"
    REGISTER_LINK = "a:has-text('إنشاء حساب'), a:has-text('Register')"
    
    # رسائل الخطأ والنجاح
    ERROR_MESSAGE = ".error-message, .alert-danger, .invalid-feedback"
    SUCCESS_MESSAGE = ".success-message, .alert-success"
    
    # عناصر إضافية
    REMEMBER_ME_CHECKBOX = "input[type='checkbox'][name='remember'], input[id='remember']"
    CAPTCHA_IMAGE = ".captcha-image, img[alt*='captcha']"
    CAPTCHA_INPUT = "input[name='captcha'], input[id='captcha']"
    
    # عناصر التحقق من الصفحة
    PAGE_TITLE = "h1:has-text('تسجيل الدخول'), h1:has-text('Login')"
    LOGIN_FORM = "form[action*='login'], .login-form"


class RegistrationPageLocators:
    """عناصر صفحة التسجيل"""
    
    # حقول البيانات الشخصية
    FIRST_NAME_INPUT = "input[name='first_name'], input[id='first_name']"
    LAST_NAME_INPUT = "input[name='last_name'], input[id='last_name']"
    EMAIL_INPUT = "input[name='email'], input[id='email'], input[type='email']"
    PHONE_INPUT = "input[name='phone'], input[id='phone'], input[type='tel']"
    
    # حقول العنوان
    ADDRESS_INPUT = "textarea[name='address'], input[name='address']"
    CITY_SELECT = "select[name='city'], select[id='city']"
    COUNTRY_SELECT = "select[name='country'], select[id='country']"
    
    # حقول كلمة المرور
    PASSWORD_INPUT = "input[name='password'], input[id='password'], input[type='password']"
    CONFIRM_PASSWORD_INPUT = "input[name='confirm_password'], input[id='confirm_password']"
    
    # الأزرار
    REGISTER_BUTTON = "button[type='submit'], input[type='submit'], button:has-text('إنشاء حساب'), button:has-text('Register')"
    CANCEL_BUTTON = "button:has-text('إلغاء'), button:has-text('Cancel')"
    
    # رسائل التحقق
    EMAIL_ERROR = ".email-error, .invalid-feedback"
    PHONE_ERROR = ".phone-error, .invalid-feedback"
    PASSWORD_ERROR = ".password-error, .invalid-feedback"
    GENERAL_ERROR = ".error-message, .alert-danger"
    SUCCESS_MESSAGE = ".success-message, .alert-success"
    
    # عناصر إضافية
    TERMS_CHECKBOX = "input[type='checkbox'][name='terms'], input[id='terms']"
    PRIVACY_CHECKBOX = "input[type='checkbox'][name='privacy'], input[id='privacy']"
    NEWSLETTER_CHECKBOX = "input[type='checkbox'][name='newsletter'], input[id='newsletter']"
    
    # عناصر التحقق من الصفحة
    PAGE_TITLE = "h1:has-text('إنشاء حساب'), h1:has-text('Register')"
    REGISTRATION_FORM = "form[action*='register'], .registration-form"


class HomePageLocators:
    """عناصر الصفحة الرئيسية"""
    
    # القائمة الرئيسية
    MAIN_MENU = ".main-menu, .navbar-nav"
    LOGIN_LINK = "a:has-text('تسجيل الدخول'), a:has-text('Login')"
    REGISTER_LINK = "a:has-text('إنشاء حساب'), a:has-text('Register')"
    
    # عناصر الصفحة الرئيسية
    HERO_SECTION = ".hero-section, .banner"
    SERVICES_SECTION = ".services-section"
    ABOUT_SECTION = ".about-section"
    
    # الروابط السريعة
    QUICK_LINKS = ".quick-links, .footer-links"
    CONTACT_INFO = ".contact-info"
    
    # عناصر التحقق من الصفحة
    PAGE_TITLE = "title"
    LOGO = ".logo, img[alt*='logo']"


class DashboardPageLocators:
    """عناصر صفحة لوحة التحكم"""
    
    # القائمة الجانبية
    SIDEBAR_MENU = ".sidebar-menu, .nav-sidebar"
    PROFILE_LINK = "a:has-text('الملف الشخصي'), a:has-text('Profile')"
    SETTINGS_LINK = "a:has-text('الإعدادات'), a:has-text('Settings')"
    LOGOUT_LINK = "a:has-text('تسجيل الخروج'), a:has-text('Logout')"
    
    # محتوى الصفحة
    DASHBOARD_CONTENT = ".dashboard-content"
    USER_INFO = ".user-info"
    STATISTICS_CARDS = ".stats-cards"
    
    # عناصر التحقق من الصفحة
    PAGE_TITLE = "h1:has-text('لوحة التحكم'), h1:has-text('Dashboard')"
    WELCOME_MESSAGE = ".welcome-message"


class CommonLocators:
    """عناصر مشتركة في جميع الصفحات"""
    
    # عناصر التنقل العامة
    HEADER = "header, .header"
    FOOTER = "footer, .footer"
    NAVIGATION = "nav, .navigation"
    
    # عناصر التحميل والانتظار
    LOADING_SPINNER = ".loading, .spinner, .loader"
    LOADING_OVERLAY = ".loading-overlay, .modal-backdrop"
    
    # رسائل النظام
    NOTIFICATION = ".notification, .toast, .alert"
    MODAL_DIALOG = ".modal, .dialog"
    MODAL_CLOSE_BUTTON = ".modal-close, .close-button"
    
    # عناصر البحث
    SEARCH_INPUT = "input[type='search'], input[name='search']"
    SEARCH_BUTTON = "button[type='submit'], .search-button"
    
    # عناصر اللغة
    LANGUAGE_SELECTOR = ".language-selector, select[name='language']"
    ARABIC_LANGUAGE = "option[value='ar'], a:has-text('العربية')"
    ENGLISH_LANGUAGE = "option[value='en'], a:has-text('English')"


class LocatorManager:
    """مدير Locators للوصول السهل للعناصر"""
    
    @staticmethod
    def get_login_locators() -> LoginPageLocators:
        """إرجاع locators صفحة تسجيل الدخول"""
        return LoginPageLocators()
    
    @staticmethod
    def get_registration_locators() -> RegistrationPageLocators:
        """إرجاع locators صفحة التسجيل"""
        return RegistrationPageLocators()
    
    @staticmethod
    def get_home_locators() -> HomePageLocators:
        """إرجاع locators الصفحة الرئيسية"""
        return HomePageLocators()
    
    @staticmethod
    def get_dashboard_locators() -> DashboardPageLocators:
        """إرجاع locators صفحة لوحة التحكم"""
        return DashboardPageLocators()
    
    @staticmethod
    def get_common_locators() -> CommonLocators:
        """إرجاع locators العناصر المشتركة"""
        return CommonLocators()
    
    @staticmethod
    def get_all_locators() -> Dict[str, Any]:
        """إرجاع جميع locators في قاموس"""
        return {
            "login": LoginPageLocators(),
            "registration": RegistrationPageLocators(),
            "home": HomePageLocators(),
            "dashboard": DashboardPageLocators(),
            "common": CommonLocators()
        }

"""
Registration Data Generator - مولد بيانات التسجيل
يستخدم مكتبة Faker لتوليد بيانات وهمية للتسجيل
"""

from faker import Faker
from typing import Dict, Any
import random


class RegistrationDataGenerator:
    """مولد بيانات التسجيل"""
    
    def __init__(self, locale: str = "ar_EG"):
        """
        تهيئة مولد البيانات
        
        Args:
            locale: اللغة المطلوبة (ar_EG للعربية المصرية)
        """
        self.fake = Faker(locale)
        self.fake_en = Faker("en_US")  # للبيانات الإنجليزية
        
        # قائمة المدن المصرية
        self.egyptian_cities = [
            "القاهرة", "الإسكندرية", "الجيزة", "المنصورة", "طنطا",
            "أسيوط", "الأقصر", "أسوان", "بورسعيد", "السويس",
            "الإسماعيلية", "دمياط", "كفر الشيخ", "الغربية", "المنيا",
            "قنا", "البحر الأحمر", "الوادي الجديد", "مطروح", "شمال سيناء",
            "جنوب سيناء", "الفيوم", "بني سويف", "الشرقية", "الدقهلية"
        ]
        
        # قائمة أرقام الهواتف المصرية
        self.egyptian_phone_prefixes = ["010", "011", "012", "015"]
    
    def generate_full_registration_data(self) -> Dict[str, Any]:
        """
        توليد بيانات تسجيل كاملة
        
        Returns:
            Dict: بيانات التسجيل الكاملة
        """
        return {
            "first_name": self.generate_first_name(),
            "last_name": self.generate_last_name(),
            "email": self.generate_email(),
            "phone": self.generate_phone_number(),
            "address": self.generate_address(),
            "city": self.generate_city(),
            "password": self.generate_password(),
            "confirm_password": None,  # سيتم تعيينه لاحقاً
            "terms_accepted": True,
            "privacy_accepted": True,
            "newsletter_subscription": random.choice([True, False])
        }
    
    def generate_first_name(self) -> str:
        """
        توليد اسم أول
        
        Returns:
            str: اسم أول عربي
        """
        try:
            return self.fake.first_name()
        except:
            # في حالة عدم دعم العربية، استخدم أسماء عربية ثابتة
            arabic_names = [
                "أحمد", "محمد", "علي", "حسن", "حسين", "محمود", "عبدالله",
                "عبدالرحمن", "يوسف", "إبراهيم", "عمر", "خالد", "سعد",
                "طارق", "مصطفى", "عبدالعزيز", "فاروق", "نور", "كريم"
            ]
            return random.choice(arabic_names)
    
    def generate_last_name(self) -> str:
        """
        توليد اسم أخير
        
        Returns:
            str: اسم أخير عربي
        """
        try:
            return self.fake.last_name()
        except:
            # في حالة عدم دعم العربية، استخدم أسماء عربية ثابتة
            arabic_last_names = [
                "محمد", "أحمد", "علي", "حسن", "حسين", "محمود", "عبدالله",
                "عبدالرحمن", "يوسف", "إبراهيم", "عمر", "خالد", "سعد",
                "طارق", "مصطفى", "عبدالعزيز", "فاروق", "نور", "كريم"
            ]
            return random.choice(arabic_last_names)
    
    def generate_email(self) -> str:
        """
        توليد بريد إلكتروني
        
        Returns:
            str: بريد إلكتروني صحيح
        """
        # استخدام أسماء إنجليزية للبريد الإلكتروني لضمان التوافق
        first_name = self.fake_en.first_name().lower()
        last_name = self.fake_en.last_name().lower()
        domain = random.choice(["gmail.com", "yahoo.com", "hotmail.com", "outlook.com"])
        
        return f"{first_name}.{last_name}@{domain}"
    
    def generate_phone_number(self) -> str:
        """
        توليد رقم هاتف مصري صحيح
        
        Returns:
            str: رقم هاتف مصري
        """
        prefix = random.choice(self.egyptian_phone_prefixes)
        # توليد 7 أرقام إضافية (المجموع 10 أرقام)
        remaining_digits = ''.join([str(random.randint(0, 9)) for _ in range(7)])
        return f"{prefix}{remaining_digits}"
    
    def generate_address(self) -> str:
        """
        توليد عنوان
        
        Returns:
            str: عنوان مصري
        """
        try:
            # محاولة توليد عنوان عربي
            street = self.fake.street_name()
            building_number = random.randint(1, 999)
            return f"{street}، رقم {building_number}"
        except:
            # في حالة عدم دعم العربية، استخدم عناوين ثابتة
            streets = [
                "شارع التحرير", "شارع رمسيس", "شارع الهرم", "شارع المعادي",
                "شارع مصر الجديدة", "شارع النزهة", "شارع الدقي", "شارع المهندسين"
            ]
            street = random.choice(streets)
            building_number = random.randint(1, 999)
            return f"{street}، رقم {building_number}"
    
    def generate_city(self) -> str:
        """
        توليد مدينة مصرية
        
        Returns:
            str: مدينة مصرية
        """
        return random.choice(self.egyptian_cities)
    
    def generate_password(self, length: int = 8) -> str:
        """
        توليد كلمة مرور قوية
        
        Args:
            length: طول كلمة المرور
            
        Returns:
            str: كلمة مرور قوية
        """
        # كلمة مرور تحتوي على أحرف كبيرة وصغيرة وأرقام ورموز
        import string
        
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        symbols = "!@#$%^&*"
        
        # ضمان وجود كل نوع من الأحرف
        password = [
            random.choice(lowercase),
            random.choice(uppercase),
            random.choice(digits),
            random.choice(symbols)
        ]
        
        # إضافة باقي الأحرف عشوائياً
        all_chars = lowercase + uppercase + digits + symbols
        for _ in range(length - 4):
            password.append(random.choice(all_chars))
        
        # خلط الأحرف
        random.shuffle(password)
        return ''.join(password)
    
    def generate_invalid_email(self) -> str:
        """
        توليد بريد إلكتروني غير صحيح للاختبارات السلبية
        
        Returns:
            str: بريد إلكتروني غير صحيح
        """
        invalid_formats = [
            "invalid_email",
            "test@",
            "@gmail.com",
            "test..test@gmail.com",
            "test@.com",
            "test@com",
            "test@.com..",
            "test@.com.."
        ]
        return random.choice(invalid_formats)
    
    def generate_invalid_phone(self) -> str:
        """
        توليد رقم هاتف غير صحيح للاختبارات السلبية
        
        Returns:
            str: رقم هاتف غير صحيح
        """
        invalid_phones = [
            "123",  # قصير جداً
            "123456789012345",  # طويل جداً
            "abc1234567",  # يحتوي على أحرف
            "0000000000",  # كل الأرقام صفر
            "1111111111",  # كل الأرقام متشابهة
            "1234567890"  # لا يبدأ ببادئة مصرية صحيحة
        ]
        return random.choice(invalid_phones)
    
    def generate_weak_password(self) -> str:
        """
        توليد كلمة مرور ضعيفة للاختبارات السلبية
        
        Returns:
            str: كلمة مرور ضعيفة
        """
        weak_passwords = [
            "123",  # قصيرة جداً
            "password",  # كلمة شائعة
            "12345678",  # أرقام فقط
            "abcdefgh",  # أحرف صغيرة فقط
            "ABCDEFGH",  # أحرف كبيرة فقط
            "1234567890",  # أرقام متتالية
            "qwertyui",  # لوحة مفاتيح متتالية
            "aaaaaaaa"  # نفس الحرف
        ]
        return random.choice(weak_passwords)
    
    def generate_test_data_for_scenario(self, scenario_type: str) -> Dict[str, Any]:
        """
        توليد بيانات اختبار حسب نوع السيناريو
        
        Args:
            scenario_type: نوع السيناريو (valid, invalid_email, invalid_phone, weak_password)
            
        Returns:
            Dict: بيانات الاختبار
        """
        base_data = self.generate_full_registration_data()
        
        if scenario_type == "valid":
            # بيانات صحيحة
            base_data["confirm_password"] = base_data["password"]
            return base_data
            
        elif scenario_type == "invalid_email":
            # بريد إلكتروني غير صحيح
            base_data["email"] = self.generate_invalid_email()
            base_data["confirm_password"] = base_data["password"]
            return base_data
            
        elif scenario_type == "invalid_phone":
            # رقم هاتف غير صحيح
            base_data["phone"] = self.generate_invalid_phone()
            base_data["confirm_password"] = base_data["password"]
            return base_data
            
        elif scenario_type == "weak_password":
            # كلمة مرور ضعيفة
            base_data["password"] = self.generate_weak_password()
            base_data["confirm_password"] = base_data["password"]
            return base_data
            
        elif scenario_type == "mismatched_passwords":
            # كلمات مرور غير متطابقة
            base_data["confirm_password"] = self.generate_password()
            return base_data
            
        elif scenario_type == "no_terms":
            # عدم الموافقة على الشروط
            base_data["terms_accepted"] = False
            base_data["confirm_password"] = base_data["password"]
            return base_data
            
        else:
            # بيانات صحيحة افتراضياً
            base_data["confirm_password"] = base_data["password"]
            return base_data


# إنشاء مثيل عام للمولد
registration_data_generator = RegistrationDataGenerator()


def get_registration_data(scenario_type: str = "valid") -> Dict[str, Any]:
    """
    دالة مساعدة للحصول على بيانات التسجيل
    
    Args:
        scenario_type: نوع السيناريو
        
    Returns:
        Dict: بيانات التسجيل
    """
    return registration_data_generator.generate_test_data_for_scenario(scenario_type)


def get_multiple_registration_data(count: int = 5) -> list:
    """
    الحصول على عدة مجموعات من بيانات التسجيل
    
    Args:
        count: عدد المجموعات المطلوبة
        
    Returns:
        list: قائمة ببيانات التسجيل
    """
    return [registration_data_generator.generate_full_registration_data() for _ in range(count)]

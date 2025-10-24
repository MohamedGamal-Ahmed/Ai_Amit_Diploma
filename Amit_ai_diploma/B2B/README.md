# Test Automation Framework - Etisalat Website

## 📋 نظرة عامة
إطار عمل شامل لاختبار الأتمتة باستخدام Python و Playwright لموقع اتصالات مصر. يوفر هذا الإطار بنية منظمة وقابلة للتوسع لتنفيذ اختبارات الويب الشاملة.

## 🏗️ هيكل المشروع

```
project_root/
│
├── pages/                          # فولدر يحتوي على كل الصفحات
│   ├── __init__.py
│   ├── login_page.py
│   └── registration_page.py
│
├── locators/                       # فولدر الـ Locators
│   ├── __init__.py
│   └── all_locators.py            # ملف واحد يحتوي على locators لكل الصفحات
│
├── test_data/                      # فولدر الـ Test Data
│   ├── __init__.py
│   ├── test_cases.json            # ملف JSON يحتوي على كل الـ test cases
│   ├── login_data.py              # بيانات Login
│   └── registration_data.py       # بيانات Registration باستخدام Faker
│
├── config/                         # فولدر الإعدادات
│   ├── __init__.py
│   └── config.py                  # ملف Config يحتوي على URLs والإعدادات
│
├── reports/                        # فولدر التقارير والسكرينشوت
│   ├── screenshots/               # مجلد السكرينشوت
│   └── allure-results/            # نتائج Allure
│
├── utils/                          # فولدر الـ Utilities
│   ├── __init__.py
│   ├── base_page.py               # Base Page Class
│   └── helpers.py                 # Helper functions للسكرينشوت والتقارير
│
├── main.py                         # ملف التنفيذ الرئيسي
├── requirements.txt                # المكتبات المطلوبة
├── pytest.ini                      # إعدادات pytest
└── README.md                       # هذا الملف
```

## 🚀 التثبيت والإعداد

### 1. متطلبات النظام
- Python 3.8 أو أحدث
- Windows/Linux/macOS
- متصفح Chrome أو Chromium

### 2. تثبيت المكتبات (الطريقة المبسطة)
```bash
# تثبيت المكتبات الأساسية
pip install playwright pytest allure-pytest faker python-dotenv

# تثبيت متصفحات Playwright
python -m playwright install chromium
```

### 3. إعداد متغيرات البيئة
```bash
# نسخ ملف البيئة
copy env.example .env
```

ثم عدّل ملف `.env`:
```env
BASE_URL=https://www.etisalat.eg
TEST_USERNAME=your_test_username
TEST_PASSWORD=your_test_password
HEADLESS=false
```

### 4. اختبار التثبيت
```bash
# تشغيل اختبار تجريبي
python demo_test.py

# أو باستخدام pytest
python -m pytest demo_test.py -v
```

## 🧪 تشغيل الاختبارات

### اختبار تجريبي (للبداية)
```bash
# تشغيل اختبار تجريبي بسيط
python demo_test.py

# أو باستخدام pytest
python -m pytest demo_test.py -v
```

### تشغيل جميع الاختبارات
```bash
# تشغيل جميع الاختبارات مع Allure
python -m pytest main.py --alluredir=reports/allure-results

# تشغيل الاختبارات مع تقرير HTML
python -m pytest main.py --html=reports/report.html --self-contained-html
```

### تشغيل اختبارات محددة
```bash
# تشغيل اختبارات تسجيل الدخول فقط
python -m pytest main.py -m login

# تشغيل اختبارات التسجيل فقط
python -m pytest main.py -m registration

# تشغيل اختبارات التدخين فقط
python -m pytest main.py -m smoke
```

### تشغيل اختبارات متوازية
```bash
# تشغيل الاختبارات على عدة عمال (يتطلب pytest-xdist)
python -m pytest main.py -n 2
```

## 📊 التقارير

### Allure Reports
```bash
# تشغيل الاختبارات مع Allure
python -m pytest main.py --alluredir=reports/allure-results

# عرض تقرير Allure (يتطلب تثبيت Allure)
allure serve reports/allure-results
```

### HTML Reports
```bash
# تشغيل الاختبارات مع تقرير HTML (يتطلب pytest-html)
python -m pytest main.py --html=reports/report.html --self-contained-html
```

## 🔧 الإعدادات

### إعدادات المتصفح (config/config.py)
```python
BROWSER_CONFIG = {
    "browser": "chromium",
    "headless": False,
    "viewport": {"width": 1920, "height": 1080},
    "timeout": 30000,
    "slow_mo": 0
}
```

### إعدادات الاختبار
```python
TEST_CONFIG = {
    "implicit_wait": 10,
    "explicit_wait": 20,
    "page_load_timeout": 30,
    "retry_count": 3,
    "parallel_workers": 2
}
```

## 📝 إضافة اختبارات جديدة

### 1. إضافة صفحة جديدة
```python
# pages/new_page.py
from utils.base_page import BasePage
from locators.all_locators import NewPageLocators

class NewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.locators = NewPageLocators()
    
    def perform_action(self):
        # تنفيذ العمليات المطلوبة
        pass
```

### 2. إضافة Locators جديدة
```python
# locators/all_locators.py
class NewPageLocators:
    ELEMENT_SELECTOR = "selector"
    BUTTON_SELECTOR = "button"
```

### 3. إضافة حالات اختبار جديدة
```json
{
  "NewPage": {
    "New_Feature": {
      "positive": [
        {
          "test_id": "TC_NEW_001",
          "description": "وصف الاختبار",
          "steps": ["خطوة 1", "خطوة 2"],
          "expected_result": "النتيجة المتوقعة"
        }
      ]
    }
  }
}
```

## 🎯 الميزات الرئيسية

### ✅ Page Object Model
- فصل منطق الاختبار عن تفاصيل التنفيذ
- إعادة استخدام الكود
- سهولة الصيانة

### ✅ Data-Driven Testing
- اختبارات مدفوعة بالبيانات من JSON
- توليد بيانات وهمية باستخدام Faker
- دعم الاختبارات الإيجابية والسلبية

### ✅ Comprehensive Reporting
- تقارير Allure تفصيلية
- لقطات شاشة تلقائية
- تسجيل مفصل للعمليات

### ✅ Error Handling
- معالجة شاملة للأخطاء
- رسائل خطأ واضحة
- استرداد من الأخطاء

### ✅ Parallel Execution
- تشغيل الاختبارات بشكل متوازي
- تحسين وقت التنفيذ
- دعم CI/CD

## 🔍 استكشاف الأخطاء

### مشاكل شائعة وحلولها

#### 1. خطأ في تثبيت Playwright
```bash
# إعادة تثبيت المتصفحات
playwright install --force chromium
```

#### 2. خطأ في الاتصال بالموقع
- تحقق من صحة BASE_URL
- تحقق من الاتصال بالإنترنت
- تحقق من إعدادات البروكسي

#### 3. خطأ في Locators
- تحقق من صحة محددات العناصر
- استخدم أدوات المطور للتحقق من العناصر
- أضف انتظارات إضافية إذا لزم الأمر

## 📈 أفضل الممارسات

### 1. كتابة الاختبارات
- استخدم أسماء وصفية للاختبارات
- اكتب اختبارات مستقلة
- تجنب الاعتماد على ترتيب التنفيذ

### 2. إدارة البيانات
- استخدم بيانات وهمية للاختبارات
- لا تعتمد على بيانات الإنتاج
- نظف البيانات بعد كل اختبار

### 3. الصيانة
- راجع Locators بانتظام
- حدث البيانات الوهمية
- احتفظ بالتقارير القديمة

## 🤝 المساهمة

1. Fork المشروع
2. إنشاء فرع للميزة الجديدة
3. Commit التغييرات
4. Push إلى الفرع
5. إنشاء Pull Request

## 📄 الترخيص

هذا المشروع مرخص تحت رخصة MIT - راجع ملف LICENSE للتفاصيل.

## 📞 الدعم

للحصول على الدعم أو الإبلاغ عن مشاكل:
- إنشاء Issue في GitHub
- التواصل عبر البريد الإلكتروني
- مراجعة الوثائق

---

**ملاحظة**: تأكد من تحديث بيانات الاختبار والـ Locators حسب الموقع الفعلي قبل التشغيل.

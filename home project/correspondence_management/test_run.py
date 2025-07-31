#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف اختبار سريع للبرنامج
Quick Test Run
"""

import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    print("🚀 بدء تشغيل نظام إدارة المراسلات...")
    print("=" * 50)
    
    # استيراد التطبيق
    from main import CorrespondenceApp
    
    # تشغيل التطبيق
    app = CorrespondenceApp()
    print("✅ تم تحميل التطبيق بنجاح")
    print("📋 بيانات تسجيل الدخول الافتراضية:")
    print("   اسم المستخدم: admin")
    print("   كلمة المرور: admin123")
    print("=" * 50)
    
    app.run()
    
except Exception as e:
    print(f"❌ خطأ في تشغيل البرنامج: {e}")
    print("\n🔧 تأكد من:")
    print("1. تثبيت المكتبات المطلوبة: pip install matplotlib numpy Pillow")
    print("2. وجود جميع ملفات البرنامج")
    print("3. صحة مسار المشروع")
    
    input("\nاضغط Enter للخروج...")
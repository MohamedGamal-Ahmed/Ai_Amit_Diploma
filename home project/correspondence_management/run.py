#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل برنامج إدارة المراسلات
Correspondence Management System Launcher
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox

def check_requirements():
    """التحقق من المتطلبات"""
    missing_modules = []
    
    try:
        import matplotlib
    except ImportError:
        missing_modules.append('matplotlib')
    
    try:
        import numpy
    except ImportError:
        missing_modules.append('numpy')
    
    try:
        from PIL import Image
    except ImportError:
        missing_modules.append('Pillow')
    
    if missing_modules:
        root = tk.Tk()
        root.withdraw()  # إخفاء النافذة الرئيسية
        
        message = "المكتبات التالية مفقودة:\n\n"
        message += "\n".join(f"• {module}" for module in missing_modules)
        message += "\n\nيرجى تثبيتها باستخدام الأمر:\n"
        message += f"pip install {' '.join(missing_modules)}"
        
        messagebox.showerror("مكتبات مفقودة", message)
        return False
    
    return True

def main():
    """الدالة الرئيسية"""
    print("=" * 50)
    print("نظام إدارة المراسلات")
    print("Correspondence Management System")
    print("=" * 50)
    
    # التحقق من المتطلبات
    if not check_requirements():
        print("خطأ: مكتبات مفقودة. يرجى تثبيت المتطلبات أولاً.")
        return
    
    try:
        # استيراد وتشغيل التطبيق
        from main import CorrespondenceApp
        
        print("جاري تشغيل البرنامج...")
        app = CorrespondenceApp()
        app.run()
        
    except ImportError as e:
        print(f"خطأ في الاستيراد: {e}")
        print("تأكد من وجود جميع ملفات البرنامج في المجلد الصحيح")
        
    except Exception as e:
        print(f"خطأ في تشغيل البرنامج: {e}")
        
        # عرض رسالة خطأ للمستخدم
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("خطأ", f"حدث خطأ في تشغيل البرنامج:\n{e}")

if __name__ == "__main__":
    main()
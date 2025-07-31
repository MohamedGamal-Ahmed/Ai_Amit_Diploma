#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
برنامج إدارة المراسلات
Correspondence Management System

المطور: AI Assistant
التاريخ: 2025
"""

import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3    #
import hashlib
from datetime import datetime
import os
import sys

# إضافة مسار المشروع لاستيراد الوحدات
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import DatabaseManager
from auth import AuthManager
from gui.main_window import MainWindow

class CorrespondenceApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("نظام إدارة المراسلات")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # تعيين الخط العربي
        self.setup_fonts()
        
        # إنشاء قاعدة البيانات
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager(self.db_manager)
        
        # إنشاء المستخدم الافتراضي (admin)
        self.create_default_admin()
        
        # بدء تشغيل نافذة تسجيل الدخول
        self.show_login()
        
    def setup_fonts(self):
        """إعداد الخطوط العربية"""
        try:
            # محاولة استخدام خط عربي
            self.arabic_font = ('Arial Unicode MS', 12)
            self.arabic_font_bold = ('Arial Unicode MS', 12, 'bold')
            self.arabic_font_large = ('Arial Unicode MS', 14, 'bold')
        except:
            # في حالة عدم توفر الخط، استخدام الخط الافتراضي
            self.arabic_font = ('Arial', 12)
            self.arabic_font_bold = ('Arial', 12, 'bold')
            self.arabic_font_large = ('Arial', 14, 'bold')
    
    def create_default_admin(self):
        """إنشاء مستخدم المدير الافتراضي"""
        try:
            # التحقق من وجود مستخدم admin
            if not self.auth_manager.user_exists('admin'):
                self.auth_manager.create_user(
                    username='admin',
                    password='admin123',
                    full_name='مدير النظام',
                    role='admin',
                    department='الإدارة'
                )
                print("تم إنشاء مستخدم المدير الافتراضي:")
                print("اسم المستخدم: admin")
                print("كلمة المرور: admin123")
        except Exception as e:
            print(f"خطأ في إنشاء المستخدم الافتراضي: {e}")
    
    def show_login(self):
        """عرض نافذة تسجيل الدخول"""
        from gui.login_window import LoginWindow
        login_window = LoginWindow(self.root, self.auth_manager, self.on_login_success)
        
    def on_login_success(self, user_data):
        """عند نجاح تسجيل الدخول"""
        # إغلاق نافذة تسجيل الدخول
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # فتح النافذة الرئيسية
        self.main_window = MainWindow(
            self.root, 
            self.db_manager, 
            self.auth_manager, 
            user_data
        )
        # رسالة ترحيب فورية
        self.root.after(500, lambda: self.main_window.show_notification(f"مرحبًا {user_data['full_name']}! تم تسجيل الدخول بنجاح.", type_="success", duration=4000))
        
    def run(self):
        """تشغيل التطبيق"""
        # تعيين أيقونة التطبيق (اختيارية)
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
            
        # تشغيل الحلقة الرئيسية
        self.root.mainloop()

if __name__ == "__main__":
    app = CorrespondenceApp()
    app.run()
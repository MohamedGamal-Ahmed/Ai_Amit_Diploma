#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نموذج إضافة/تعديل المستخدمين
User Form
"""

import tkinter as tk
from tkinter import ttk, messagebox

class UserForm:
    def __init__(self, parent, db_manager, auth_manager, user_data, user_id=None, callback=None, notify=None):
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.user_data = user_data
        self.user_id = user_id
        self.callback = callback
        self.notify = notify  # دالة الإشعار الفوري
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        
        # تحميل البيانات للتعديل
        if user_id:
            self.load_data()
    
    def setup_window(self):
        """إعداد النافذة"""
        title = "تعديل مستخدم" if self.user_id else "إضافة مستخدم"
        
        self.window.title(title)
        self.window.geometry("500x400")
        self.window.resizable(False, False)
        
        # توسيط النافذة
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.window.winfo_screenheight() // 2) - (400 // 2)
        self.window.geometry(f"500x400+{x}+{y}")
        
        # جعل النافذة في المقدمة
        self.window.transient(self.window.master)
        self.window.grab_set()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # العنوان
        title_text = "تعديل مستخدم" if self.user_id else "إضافة مستخدم"
        title_label = tk.Label(
            main_frame,
            text=title_text,
            font=('Arial Unicode MS', 14, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # إطار الحقول
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill='both', expand=True)
        
        # اسم المستخدم
        self.create_field(fields_frame, "اسم المستخدم:", 0)
        self.username_var = tk.StringVar()
        self.username_entry = ttk.Entry(
            fields_frame,
            textvariable=self.username_var,
            font=('Arial Unicode MS', 10)
        )
        self.username_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # كلمة المرور (للإضافة فقط)
        if not self.user_id:
            self.create_field(fields_frame, "كلمة المرور:", 1)
            self.password_var = tk.StringVar()
            self.password_entry = ttk.Entry(
                fields_frame,
                textvariable=self.password_var,
                font=('Arial Unicode MS', 10),
                show='*'
            )
            self.password_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
            
            # تأكيد كلمة المرور
            self.create_field(fields_frame, "تأكيد كلمة المرور:", 2)
            self.confirm_password_var = tk.StringVar()
            self.confirm_password_entry = ttk.Entry(
                fields_frame,
                textvariable=self.confirm_password_var,
                font=('Arial Unicode MS', 10),
                show='*'
            )
            self.confirm_password_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
            row_offset = 3
        else:
            row_offset = 1
        
        # الاسم الكامل
        self.create_field(fields_frame, "الاسم الكامل:", row_offset)
        self.full_name_var = tk.StringVar()
        self.full_name_entry = ttk.Entry(
            fields_frame,
            textvariable=self.full_name_var,
            font=('Arial Unicode MS', 10),
            justify='right'
        )
        self.full_name_entry.grid(row=row_offset, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # الصلاحية
        self.create_field(fields_frame, "الصلاحية:", row_offset + 1)
        self.role_var = tk.StringVar(value="employee")
        role_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.role_var,
            values=[("admin", "مدير"), ("employee", "موظف"), ("viewer", "مشاهد")],
            state="readonly",
            font=('Arial Unicode MS', 10)
        )
        role_combo.grid(row=row_offset + 1, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # القسم
        self.create_field(fields_frame, "القسم:", row_offset + 2)
        self.department_var = tk.StringVar()
        self.department_entry = ttk.Entry(
            fields_frame,
            textvariable=self.department_var,
            font=('Arial Unicode MS', 10),
            justify='right'
        )
        self.department_entry.grid(row=row_offset + 2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # الحالة (للتعديل فقط)
        if self.user_id:
            self.create_field(fields_frame, "الحالة:", row_offset + 3)
            self.is_active_var = tk.BooleanVar(value=True)
            active_check = ttk.Checkbutton(
                fields_frame,
                text="نشط",
                variable=self.is_active_var,
                font=('Arial Unicode MS', 10)
            )
            active_check.grid(row=row_offset + 3, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # تكوين الشبكة
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        # زر الحفظ
        save_btn = ttk.Button(
            buttons_frame,
            text="حفظ",
            command=self.save_user
        )
        save_btn.pack(side='right', padx=5)
        
        # زر الإلغاء
        cancel_btn = ttk.Button(
            buttons_frame,
            text="إلغاء",
            command=self.window.destroy
        )
        cancel_btn.pack(side='right', padx=5)
        
        # التركيز على أول حقل
        self.username_entry.focus()
    
    def create_field(self, parent, text, row):
        """إنشاء تسمية حقل"""
        label = ttk.Label(
            parent,
            text=text,
            font=('Arial Unicode MS', 10, 'bold')
        )
        label.grid(row=row, column=0, sticky='e', padx=(0, 10), pady=5)
    
    def load_data(self):
        """تحميل البيانات للتعديل"""
        user_data = self.auth_manager.get_user_by_id(self.user_id)
        
        if user_data:
            self.username_var.set(user_data['username'])
            self.full_name_var.set(user_data['full_name'])
            self.role_var.set(user_data['role'])
            self.department_var.set(user_data['department'] or '')
            
            if hasattr(self, 'is_active_var'):
                self.is_active_var.set(user_data['is_active'])
    
    def save_user(self):
        """حفظ المستخدم"""
        # التحقق من صحة البيانات
        if not self.validate_data():
            return
        
        try:
            if self.user_id:
                # تحديث
                self.update_user()
            else:
                # إضافة جديد
                self.create_user()
            
            if self.notify:
                self.notify("تم حفظ المستخدم بنجاح", type_="success")
            
            # استدعاء callback لتحديث البيانات
            if self.callback:
                self.callback()
            
            self.window.destroy()
            
        except Exception as e:
            if self.notify:
                self.notify(f"فشل في حفظ المستخدم: {e}", type_="error")
            else:
                messagebox.showerror("خطأ", f"فشل في حفظ المستخدم: {e}")
    
    def validate_data(self):
        """التحقق من صحة البيانات"""
        if not self.username_var.get().strip():
            if self.notify:
                self.notify("يرجى إدخال اسم المستخدم", type_="error")
            self.username_entry.focus()
            return False
        
        if not self.full_name_var.get().strip():
            if self.notify:
                self.notify("يرجى إدخال الاسم الكامل", type_="error")
            self.full_name_entry.focus()
            return False
        
        # التحقق من كلمة المرور للإضافة
        if not self.user_id:
            if not self.password_var.get():
                if self.notify:
                    self.notify("يرجى إدخال كلمة المرور", type_="error")
                self.password_entry.focus()
                return False
            
            if len(self.password_var.get()) < 6:
                if self.notify:
                    self.notify("كلمة المرور يجب أن تكون 6 أحرف على الأقل", type_="error")
                self.password_entry.focus()
                return False
            
            if self.password_var.get() != self.confirm_password_var.get():
                if self.notify:
                    self.notify("كلمة المرور وتأكيدها غير متطابقتان", type_="error")
                self.confirm_password_entry.focus()
                return False
        
        # التحقق من عدم تكرار اسم المستخدم
        if not self.user_id or self.username_var.get() != getattr(self, 'original_username', None):
            if self.auth_manager.user_exists(self.username_var.get()):
                if self.notify:
                    self.notify("اسم المستخدم موجود مسبقاً", type_="error")
                self.username_entry.focus()
                return False
        
        return True
    
    def create_user(self):
        """إنشاء مستخدم جديد"""
        result = self.auth_manager.create_user(
            username=self.username_var.get().strip(),
            password=self.password_var.get(),
            full_name=self.full_name_var.get().strip(),
            role=self.role_var.get(),
            department=self.department_var.get().strip() or None
        )
        
        if not result:
            raise Exception("فشل في إنشاء المستخدم")
    
    def update_user(self):
        """تحديث مستخدم موجود"""
        # حفظ اسم المستخدم الأصلي للمقارنة
        original_data = self.auth_manager.get_user_by_id(self.user_id)
        self.original_username = original_data['username'] if original_data else ''
        
        result = self.auth_manager.update_user(
            user_id=self.user_id,
            username=self.username_var.get().strip(),
            full_name=self.full_name_var.get().strip(),
            role=self.role_var.get(),
            department=self.department_var.get().strip() or None,
            is_active=self.is_active_var.get() if hasattr(self, 'is_active_var') else None
        )
        
        if not result:
            raise Exception("فشل في تحديث المستخدم")
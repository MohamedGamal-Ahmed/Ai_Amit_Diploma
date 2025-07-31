#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نافذة تسجيل الدخول المحسنة
Enhanced Login Window
"""

import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow:
    def __init__(self, parent, auth_manager, success_callback):
        self.parent = parent
        self.auth_manager = auth_manager
        self.success_callback = success_callback
        
        # إعداد النافذة
        self.setup_window()
        self.create_widgets()
        
    def setup_window(self):
        """إعداد النافذة الرئيسية"""
        self.parent.title("تسجيل الدخول - نظام إدارة المراسلات")
        self.parent.geometry("450x600")  # زيادة الارتفاع
        self.parent.configure(bg='#f8f9fa')
        
        # توسيط النافذة
        self.parent.update_idletasks()
        x = (self.parent.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.parent.winfo_screenheight() // 2) - (600 // 2)  # تحديث الارتفاع
        self.parent.geometry(f"450x600+{x}+{y}")
        
        # منع تغيير حجم النافذة
        self.parent.resizable(False, False)
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # شعار أو أيقونة
        logo_frame = tk.Frame(main_frame, bg='#f8f9fa')
        logo_frame.pack(pady=(0, 30))
        
        # دائرة ملونة كشعار
        logo_canvas = tk.Canvas(logo_frame, width=80, height=80, bg='#f8f9fa', highlightthickness=0)
        logo_canvas.pack()
        logo_canvas.create_oval(10, 10, 70, 70, fill='#3498db', outline='#2980b9', width=3)
        logo_canvas.create_text(40, 40, text="📧", font=('Arial Unicode MS', 24), fill='white')
        
        # العنوان الرئيسي
        title_label = tk.Label(
            main_frame,
            text="نظام إدارة المراسلات",
            font=('Arial Unicode MS', 18, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        )
        title_label.pack(pady=(0, 10))
        
        # العنوان الفرعي
        subtitle_label = tk.Label(
            main_frame,
            text="تسجيل الدخول",
            font=('Arial Unicode MS', 12),
            fg='#7f8c8d',
            bg='#f8f9fa'
        )
        subtitle_label.pack(pady=(0, 30))
        
        # إطار تسجيل الدخول
        login_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        login_frame.pack(fill='x', pady=(0, 20), padx=20)
        
        # إطار الحقول
        fields_frame = tk.Frame(login_frame, bg='white')
        fields_frame.pack(pady=30, padx=30, fill='x')
        
        # حقل اسم المستخدم
        username_label = tk.Label(
            fields_frame,
            text="اسم المستخدم",
            font=('Arial Unicode MS', 11, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        username_label.pack(anchor='e', pady=(0, 5))
        
        # إطار حقل اسم المستخدم
        username_frame = tk.Frame(fields_frame, bg='white', relief='solid', bd=1)
        username_frame.pack(fill='x', pady=(0, 20))
        
        self.username_entry = tk.Entry(
            username_frame,
            font=('Arial Unicode MS', 11),
            relief='flat',
            bd=0,
            bg='white',
            fg='#2c3e50',
            justify='right'
        )
        self.username_entry.pack(fill='x', padx=10, pady=8)
        self.username_entry.focus()
        
        # حقل كلمة المرور
        password_label = tk.Label(
            fields_frame,
            text="كلمة المرور",
            font=('Arial Unicode MS', 11, 'bold'),
            fg='#2c3e50',
            bg='white'
        )
        password_label.pack(anchor='e', pady=(0, 5))
        
        # إطار حقل كلمة المرور
        password_frame = tk.Frame(fields_frame, bg='white', relief='solid', bd=1)
        password_frame.pack(fill='x', pady=(0, 25))
        
        self.password_entry = tk.Entry(
            password_frame,
            font=('Arial Unicode MS', 11),
            show='●',
            relief='flat',
            bd=0,
            bg='white',
            fg='#2c3e50',
            justify='right'
        )
        self.password_entry.pack(fill='x', padx=10, pady=8)
        
        # التأكد من ظهور حقل كلمة المرور
        password_frame.update_idletasks()
        
        # زر تسجيل الدخول
        self.login_button = tk.Button(
            fields_frame,
            text="تسجيل الدخول",
            font=('Arial Unicode MS', 12, 'bold'),
            bg='#3498db',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.login,
            pady=12
        )
        self.login_button.pack(fill='x', pady=(0, 15))
        
        # تأثيرات hover للزر
        self.setup_button_effects()
        
        # خط فاصل
        separator = tk.Frame(fields_frame, height=1, bg='#ecf0f1')
        separator.pack(fill='x', pady=(10, 15))
        
        # معلومات المستخدم الافتراضي
        info_frame = tk.Frame(main_frame, bg='#e8f4fd', relief='solid', bd=1)
        info_frame.pack(fill='x', padx=20, pady=(10, 0))
        
        info_title = tk.Label(
            info_frame,
            text="بيانات تسجيل الدخول الافتراضية",
            font=('Arial Unicode MS', 10, 'bold'),
            fg='#2980b9',
            bg='#e8f4fd'
        )
        info_title.pack(pady=(15, 5))
        
        info_content = tk.Label(
            info_frame,
            text="اسم المستخدم: admin\nكلمة المرور: admin123",
            font=('Arial Unicode MS', 10),
            fg='#34495e',
            bg='#e8f4fd',
            justify='center'
        )
        info_content.pack(pady=(0, 10))
        
        # زر ملء البيانات التلقائي
        auto_fill_btn = tk.Button(
            info_frame,
            text="ملء البيانات تلقائياً",
            font=('Arial Unicode MS', 9),
            bg='#2980b9',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.auto_fill,
            pady=5
        )
        auto_fill_btn.pack(pady=(0, 15))
        
        # إضافة مساحة إضافية في الأسفل
        spacer = tk.Frame(main_frame, bg='#f8f9fa', height=20)
        spacer.pack()
        
        # ربط Enter بتسجيل الدخول
        self.parent.bind('<Return>', self.on_enter_key)
        
        # تأثيرات التركيز للحقول
        self.setup_entry_effects()
    
    def setup_button_effects(self):
        """إعداد تأثيرات الأزرار"""
        def on_enter(e):
            self.login_button.config(bg='#2980b9')
        
        def on_leave(e):
            self.login_button.config(bg='#3498db')
        
        self.login_button.bind("<Enter>", on_enter)
        self.login_button.bind("<Leave>", on_leave)
    
    def setup_entry_effects(self):
        """إعداد تأثيرات الحقول"""
        def on_username_focus_in(e):
            e.widget.master.config(relief='solid', bd=2, highlightbackground='#3498db')
        
        def on_username_focus_out(e):
            e.widget.master.config(relief='solid', bd=1, highlightbackground='#bdc3c7')
        
        def on_password_focus_in(e):
            e.widget.master.config(relief='solid', bd=2, highlightbackground='#3498db')
        
        def on_password_focus_out(e):
            e.widget.master.config(relief='solid', bd=1, highlightbackground='#bdc3c7')
        
        self.username_entry.bind('<FocusIn>', on_username_focus_in)
        self.username_entry.bind('<FocusOut>', on_username_focus_out)
        self.password_entry.bind('<FocusIn>', on_password_focus_in)
        self.password_entry.bind('<FocusOut>', on_password_focus_out)
    
    def auto_fill(self):
        """ملء البيانات تلقائياً"""
        self.username_entry.delete(0, tk.END)
        self.username_entry.insert(0, "admin")
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, "admin123")
        self.username_entry.focus()
    
    def login(self):
        """تسجيل الدخول"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("خطأ", "يرجى إدخال اسم المستخدم وكلمة المرور")
            return
        
        # تعطيل الزر أثناء المعالجة
        try:
            if hasattr(self, 'login_button') and self.login_button.winfo_exists():
                self.login_button.config(state='disabled', text='جاري التحقق...')
                self.parent.update()
        except tk.TclError:
            pass
        
        try:
            # محاولة تسجيل الدخول
            user_data = self.auth_manager.authenticate(username, password)
            
            if user_data:
                messagebox.showinfo("نجح تسجيل الدخول", f"مرحباً {user_data['full_name']}")
                self.success_callback(user_data)
            else:
                messagebox.showerror("خطأ في تسجيل الدخول", "اسم المستخدم أو كلمة المرور غير صحيحة")
                self.password_entry.delete(0, tk.END)
                self.password_entry.focus()
        
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ أثناء تسجيل الدخول: {e}")
        
        finally:
            # إعادة تفعيل الزر (إذا كانت النافذة ما زالت موجودة)
            try:
                if hasattr(self, 'login_button') and self.login_button.winfo_exists():
                    self.login_button.config(state='normal', text='تسجيل الدخول')
            except tk.TclError:
                # النافذة تم إغلاقها بالفعل
                pass
    
    def on_enter_key(self, event):
        """معالج ضغط مفتاح Enter"""
        self.login()
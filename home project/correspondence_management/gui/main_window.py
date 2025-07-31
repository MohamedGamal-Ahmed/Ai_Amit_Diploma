#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
النافذة الرئيسية للتطبيق
Main Application Window
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import sys
import os

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gui.incoming_tab import IncomingTab
from gui.outgoing_tab import OutgoingTab
from gui.followup_tab import FollowUpTab
from gui.reports_tab import ReportsTab
from gui.users_tab import UsersTab

class MainWindow:
    def __init__(self, parent, db_manager, auth_manager, user_data):
        self.parent = parent
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.user_data = user_data
        
        # إعداد النافذة
        self.setup_window()
        self.create_menu()
        self.create_widgets()
        self.update_status_bar()
        self.check_overdue_alerts()
        
    def setup_window(self):
        """إعداد النافذة الرئيسية"""
        self.parent.title(f"نظام إدارة المراسلات - {self.user_data['full_name']}")
        self.parent.geometry("1400x900")
        self.parent.configure(bg='#f8f9fa')
        
        # توسيط النافذة
        self.parent.update_idletasks()
        x = (self.parent.winfo_screenwidth() // 2) - (1400 // 2)
        y = (self.parent.winfo_screenheight() // 2) - (900 // 2)
        self.parent.geometry(f"1400x900+{x}+{y}")
        
        # تعيين الحد الأدنى لحجم النافذة
        self.parent.minsize(1200, 700)
        
        # إعداد الخطوط
        self.setup_fonts()
    
    def setup_fonts(self):
        """إعداد الخطوط"""
        self.font_normal = ('Arial Unicode MS', 10)
        self.font_bold = ('Arial Unicode MS', 10, 'bold')
        self.font_large = ('Arial Unicode MS', 12, 'bold')
        self.font_title = ('Arial Unicode MS', 14, 'bold')
    
    def create_menu(self):
        """إنشاء شريط القوائم"""
        menubar = tk.Menu(self.parent)
        self.parent.config(menu=menubar)
        
        # قائمة الملف
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="ملف", menu=file_menu)
        file_menu.add_command(label="نسخة احتياطية", command=self.backup_database)
        file_menu.add_command(label="استعادة", command=self.restore_database)
        file_menu.add_separator()
        file_menu.add_command(label="الإعدادات", command=self.show_settings_window)
        file_menu.add_separator()
        file_menu.add_command(label="خروج", command=self.logout)
        
        # قائمة المستخدمين (للمدير فقط)
        if self.auth_manager.has_permission('manage_users'):
            users_menu = tk.Menu(menubar, tearoff=0)
            menubar.add_cascade(label="المستخدمين", menu=users_menu)
            users_menu.add_command(label="إدارة المستخدمين", command=self.show_users_tab)
            users_menu.add_command(label="سجل النشاطات", command=self.show_activity_log)
        
        # قائمة المساعدة
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="مساعدة", menu=help_menu)
        help_menu.add_command(label="حول البرنامج", command=self.show_about)
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.parent, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True)

        # شريط الإشعارات الفورية
        self.notification_bar = tk.Frame(main_frame, bg='#f8d7da', height=0)
        self.notification_bar.pack(fill='x', padx=0, pady=0)
        self.notification_bar.pack_propagate(False)
        self.notification_label = tk.Label(self.notification_bar, text='', font=self.font_bold, bg='#f8d7da', fg='#721c24')
        self.notification_label.pack(side='right', padx=20, pady=2)
        self.notification_bar.pack_forget()

        # شريط العلوي
        self.create_header(main_frame)
        
        # إطار المحتوى
        content_frame = tk.Frame(main_frame, bg='#f8f9fa')
        content_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # إنشاء التبويبات
        self.create_tabs(content_frame)
        
        # شريط الحالة
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """إنشاء الشريط العلوي"""
        header_frame = tk.Frame(parent, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', padx=10, pady=(10, 0))
        header_frame.pack_propagate(False)
        
        # العنوان
        title_label = tk.Label(
            header_frame,
            text="نظام إدارة المراسلات",
            font=self.font_title,
            fg='white',
            bg='#2c3e50'
        )
        title_label.pack(side='right', padx=20, pady=10)
        
        # معلومات المستخدم
        user_frame = tk.Frame(header_frame, bg='#2c3e50')
        user_frame.pack(side='left', padx=20, pady=10)
        
        user_label = tk.Label(
            user_frame,
            text=f"المستخدم: {self.user_data['full_name']}",
            font=self.font_normal,
            fg='#ecf0f1',
            bg='#2c3e50'
        )
        user_label.pack(anchor='w')
        
        role_label = tk.Label(
            user_frame,
            text=f"الصلاحية: {self.get_role_name(self.user_data['role'])}",
            font=self.font_normal,
            fg='#bdc3c7',
            bg='#2c3e50'
        )
        role_label.pack(anchor='w')
        
        # زر تسجيل الخروج
        logout_button = tk.Button(
            header_frame,
            text="تسجيل الخروج",
            font=self.font_normal,
            bg='#e74c3c',
            fg='white',
            relief='flat',
            cursor='hand2',
            command=self.logout,
            padx=20
        )
        logout_button.pack(side='left', padx=(0, 20), pady=20)
    
    def create_tabs(self, parent):
        """إنشاء التبويبات"""
        # إنشاء notebook للتبويبات
        self.notebook = ttk.Notebook(parent)
        self.notebook.pack(fill='both', expand=True)
        
        # تخصيص مظهر التبويبات
        style = ttk.Style()
        style.configure('TNotebook.Tab', padding=[20, 10])
        
        # تبويب المراسلات الواردة
        if self.auth_manager.has_permission('view_incoming'):
            self.incoming_tab = IncomingTab(
                self.notebook, 
                self.db_manager, 
                self.auth_manager, 
                self.user_data
            )
            self.notebook.add(self.incoming_tab.frame, text="المراسلات الواردة")
        
        # تبويب المراسلات الصادرة
        if self.auth_manager.has_permission('view_outgoing'):
            self.outgoing_tab = OutgoingTab(
                self.notebook, 
                self.db_manager, 
                self.auth_manager, 
                self.user_data
            )
            self.notebook.add(self.outgoing_tab.frame, text="المراسلات الصادرة")
        
        # تبويب المتابعة
        if self.auth_manager.has_permission('view_followup'):
            self.followup_tab = FollowUpTab(
                self.notebook, 
                self.db_manager, 
                self.auth_manager, 
                self.user_data
            )
            self.notebook.add(self.followup_tab.frame, text="متابعة الموضوعات")
        
        # تبويب التقارير
        if self.auth_manager.has_permission('view_reports'):
            self.reports_tab = ReportsTab(
                self.notebook, 
                self.db_manager, 
                self.auth_manager, 
                self.user_data
            )
            self.notebook.add(self.reports_tab.frame, text="التقارير")
        
        # تبويب المستخدمين (للمدير فقط)
        if self.auth_manager.has_permission('manage_users'):
            self.users_tab = UsersTab(
                self.notebook, 
                self.db_manager, 
                self.auth_manager, 
                self.user_data
            )
            self.notebook.add(self.users_tab.frame, text="إدارة المستخدمين")
    
    def create_status_bar(self, parent):
        """إنشاء شريط الحالة"""
        self.status_frame = tk.Frame(parent, bg='#34495e', height=30)
        self.status_frame.pack(fill='x', padx=10, pady=(0, 10))
        self.status_frame.pack_propagate(False)
        
        # نص الحالة
        self.status_label = tk.Label(
            self.status_frame,
            text="جاهز",
            font=self.font_normal,
            fg='white',
            bg='#34495e'
        )
        self.status_label.pack(side='right', padx=10, pady=5)
        
        # الوقت والتاريخ
        self.time_label = tk.Label(
            self.status_frame,
            text="",
            font=self.font_normal,
            fg='#bdc3c7',
            bg='#34495e'
        )
        self.time_label.pack(side='left', padx=10, pady=5)
        
        # تحديث الوقت كل ثانية
        self.update_time()
    
    def update_time(self):
        """تحديث الوقت في شريط الحالة"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.parent.after(1000, self.update_time)
    
    def update_status_bar(self, message="جاهز"):
        """تحديث رسالة شريط الحالة"""
        if hasattr(self, 'status_label'):
            self.status_label.config(text=message)
    
    def get_role_name(self, role):
        """الحصول على اسم الصلاحية بالعربية"""
        roles = {
            'admin': 'مدير',
            'employee': 'موظف',
            'viewer': 'مشاهد'
        }
        return roles.get(role, role)
    
    def show_users_tab(self):
        """عرض تبويب المستخدمين"""
        if hasattr(self, 'users_tab'):
            # البحث عن فهرس التبويب
            for i in range(self.notebook.index('end')):
                if self.notebook.tab(i, 'text') == 'إدارة المستخدمين':
                    self.notebook.select(i)
                    break
    
    def show_activity_log(self):
        """عرض سجل النشاطات"""
        from gui.activity_log_window import ActivityLogWindow
        ActivityLogWindow(self.parent, self.db_manager, self.auth_manager)
    
    def backup_database(self):
        """إنشاء نسخة احتياطية"""
        from tkinter import filedialog
        
        filename = filedialog.asksaveasfilename(
            title="حفظ النسخة الاحتياطية",
            defaultextension=".db",
            filetypes=[("قاعدة بيانات", "*.db"), ("جميع الملفات", "*.*")]
        )
        
        if filename:
            if self.db_manager.backup_database(filename):
                messagebox.showinfo("نجح", "تم إنشاء النسخة الاحتياطية بنجاح")
                self.update_status_bar("تم إنشاء النسخة الاحتياطية")
            else:
                messagebox.showerror("خطأ", "فشل في إنشاء النسخة الاحتياطية")
    
    def restore_database(self):
        """استعادة النسخة الاحتياطية"""
        from tkinter import filedialog
        
        result = messagebox.askyesno(
            "تأكيد",
            "هل أنت متأكد من استعادة النسخة الاحتياطية؟\nسيتم استبدال البيانات الحالية."
        )
        
        if result:
            filename = filedialog.askopenfilename(
                title="اختيار النسخة الاحتياطية",
                filetypes=[("قاعدة بيانات", "*.db"), ("جميع الملفات", "*.*")]
            )
            
            if filename:
                if self.db_manager.restore_database(filename):
                    messagebox.showinfo("نجح", "تم استعادة النسخة الاحتياطية بنجاح")
                    self.update_status_bar("تم استعادة النسخة الاحتياطية")
                    # إعادة تحميل البيانات
                    self.refresh_all_tabs()
                else:
                    messagebox.showerror("خطأ", "فشل في استعادة النسخة الاحتياطية")
    
    def refresh_all_tabs(self):
        """تحديث جميع التبويبات"""
        try:
            if hasattr(self, 'incoming_tab'):
                self.incoming_tab.refresh_data()
            if hasattr(self, 'outgoing_tab'):
                self.outgoing_tab.refresh_data()
            if hasattr(self, 'followup_tab'):
                self.followup_tab.refresh_data()
            if hasattr(self, 'reports_tab'):
                self.reports_tab.refresh_data()
            if hasattr(self, 'users_tab'):
                self.users_tab.refresh_data()
        except Exception as e:
            print(f"خطأ في تحديث التبويبات: {e}")
    
    def show_about(self):
        """عرض معلومات البرنامج"""
        about_text = """
نظام إدارة المراسلات
الإصدار 1.0

برنامج شامل لإدارة المراسلات الواردة والصادرة
مع إمكانيات المتابعة والتقارير

المطور: AI Assistant
سنة التطوير: 2025

المميزات:
• إدارة المراسلات الواردة والصادرة
• نظام متابعة الموضوعات
• تقارير شاملة وإحصائيات
• نظام مستخدمين متعدد المستويات
• واجهة عربية حديثة
• نسخ احتياطي واستعادة
        """
        
        messagebox.showinfo("حول البرنامج", about_text)
    
    def show_settings_window(self):
        """عرض نافذة الإعدادات"""
        from gui.settings_window import SettingsWindow
        SettingsWindow(self.parent, self.auth_manager, self.user_data)

    def show_notification(self, message, type_="info", duration=5000):
        """عرض إشعار فوري أعلى الشاشة"""
        colors = {
            "success": ("#d4edda", "#155724"),
            "warning": ("#fff3cd", "#856404"),
            "error": ("#f8d7da", "#721c24"),
            "info": ("#d1ecf1", "#0c5460")
        }
        bg, fg = colors.get(type_, ("#d1ecf1", "#0c5460"))
        self.notification_bar.config(bg=bg, height=36)
        self.notification_label.config(text=message, bg=bg, fg=fg)
        self.notification_bar.pack(fill='x', padx=0, pady=0)
        self.notification_bar.lift()
        self.notification_bar.bind('<Button-1>', lambda e: self.hide_notification())
        self.parent.after(duration, self.hide_notification)

    def hide_notification(self):
        self.notification_bar.pack_forget()

    def check_overdue_alerts(self):
        """فحص الموضوعات المتأخرة والتنبيه عليها"""
        from datetime import datetime, timedelta
        now = datetime.now()
        overdue_msgs = []
        # فحص الوارد
        incoming_query = """
            SELECT reference_number, subject, received_date, status
            FROM incoming_correspondence
            WHERE status != 'مغلق'
        """
        incoming = self.db_manager.execute_query(incoming_query)
        for row in incoming:
            try:
                received = datetime.strptime(row['received_date'], '%Y-%m-%d')
                if (now - received).days > 3:
                    overdue_msgs.append(f"مراسلة واردة رقم {row['reference_number']} بخصوص '{row['subject']}' تجاوزت 3 أيام ولم تغلق.")
            except:
                continue
        # فحص المتابعة
        followup_query = """
            SELECT follow_up_code, action_required, follow_up_date, status
            FROM follow_up
            WHERE status != 'مغلق'
        """
        followups = self.db_manager.execute_query(followup_query)
        for row in followups:
            try:
                follow_date = datetime.strptime(row['follow_up_date'], '%Y-%m-%d')
                if (now - follow_date).days > 3:
                    overdue_msgs.append(f"متابعة '{row['action_required']}' (كود: {row['follow_up_code']}) تجاوزت 3 أيام ولم تغلق.")
            except:
                continue
        if overdue_msgs:
            self.show_notification("\n".join(overdue_msgs), type_="warning", duration=9000)

    def logout(self):
        """تسجيل الخروج"""
        result = messagebox.askyesno("تأكيد", "هل تريد تسجيل الخروج؟")
        if result:
            self.auth_manager.logout()
            self.parent.quit()
            self.parent.destroy()
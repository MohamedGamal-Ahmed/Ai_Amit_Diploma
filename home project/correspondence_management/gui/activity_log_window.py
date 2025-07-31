#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نافذة سجل النشاطات
Activity Log Window
"""

import tkinter as tk
from tkinter import ttk

class ActivityLogWindow:
    def __init__(self, parent, db_manager, auth_manager):
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        self.load_data()
    
    def setup_window(self):
        """إعداد النافذة"""
        self.window.title("سجل النشاطات")
        self.window.geometry("1000x600")
        
        # توسيط النافذة
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (1000 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"1000x600+{x}+{y}")
        
        # جعل النافذة في المقدمة
        self.window.transient(self.window.master)
        self.window.grab_set()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # العنوان
        title_label = tk.Label(
            main_frame,
            text="سجل النشاطات",
            font=('Arial Unicode MS', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # إطار الجدول
        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill='both', expand=True)
        
        # إنشاء الجدول
        columns = ('timestamp', 'username', 'action', 'table_name', 'record_id')
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)

        # تعريف أنماط الألوان
        self.tree.tag_configure('add', background='#e8f8e8')      # أخضر فاتح
        self.tree.tag_configure('edit', background='#e8f4fa')     # أزرق فاتح
        self.tree.tag_configure('delete', background='#fae8e8')   # أحمر فاتح
        self.tree.tag_configure('login', background='#fff6e0')    # برتقالي فاتح
        self.tree.tag_configure('default', background='#f8f8f8')  # رمادي فاتح

        # تعريف عناوين الأعمدة
        self.tree.heading('timestamp', text='التاريخ والوقت')
        self.tree.heading('username', text='المستخدم')
        self.tree.heading('action', text='النشاط')
        self.tree.heading('table_name', text='الجدول')
        self.tree.heading('record_id', text='معرف السجل')
        
        # تعيين عرض الأعمدة
        self.tree.column('timestamp', width=150, anchor='center')
        self.tree.column('username', width=120, anchor='center')
        self.tree.column('action', width=400, anchor='e')
        self.tree.column('table_name', width=150, anchor='center')
        self.tree.column('record_id', width=100, anchor='center')
        
        # إضافة شريط التمرير
        scrollbar_v = ttk.Scrollbar(table_frame, orient='vertical', command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(table_frame, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # تخطيط الجدول وشريط التمرير
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_v.grid(row=0, column=1, sticky='ns')
        scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        # تكوين الشبكة
        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # زر الإغلاق
        close_btn = ttk.Button(
            main_frame,
            text="إغلاق",
            command=self.window.destroy
        )
        close_btn.pack(pady=(20, 0))
    
    def load_data(self):
        """تحميل بيانات سجل النشاطات"""
        # جلب آخر 500 نشاط
        activities = self.auth_manager.get_user_activity_log(limit=500)
        
        # إدراج البيانات في الجدول مع تلوين حسب نوع العملية
        for activity in activities:
            action_text = activity['action'].lower()
            if 'حذف' in action_text or 'delete' in action_text:
                tag = 'delete'
            elif 'تعديل' in action_text or 'edit' in action_text:
                tag = 'edit'
            elif 'إضافة' in action_text or 'add' in action_text or 'إنشاء' in action_text:
                tag = 'add'
            elif 'دخول' in action_text or 'login' in action_text:
                tag = 'login'
            else:
                tag = 'default'
            self.tree.insert('', 'end', values=(
                activity['timestamp'][:16] if activity['timestamp'] else '-',
                activity['username'] or 'غير معروف',
                activity['action'],
                activity['table_name'] or '-',
                activity['record_id'] or '-'
            ), tags=(tag,))
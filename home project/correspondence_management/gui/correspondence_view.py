#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نافذة عرض تفاصيل المراسلة
Correspondence View Window
"""

import tkinter as tk
from tkinter import ttk, messagebox

class CorrespondenceView:
    def __init__(self, parent, db_manager, correspondence_type, correspondence_id):
        self.db_manager = db_manager
        self.correspondence_type = correspondence_type
        self.correspondence_id = correspondence_id
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.load_and_display_data()
    
    def setup_window(self):
        """إعداد النافذة"""
        type_name = "مراسلة واردة" if self.correspondence_type == 'incoming' else "مراسلة صادرة"
        self.window.title(f"عرض {type_name}")
        self.window.geometry("700x600")
        self.window.resizable(False, False)
        
        # توسيط النافذة
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.window.winfo_screenheight() // 2) - (600 // 2)
        self.window.geometry(f"700x600+{x}+{y}")
        
        # جعل النافذة في المقدمة
        self.window.transient(self.window.master)
        self.window.grab_set()
    
    def load_and_display_data(self):
        """تحميل وعرض البيانات"""
        # تحديد الجدول والحقول حسب النوع
        if self.correspondence_type == 'incoming':
            table = 'incoming_correspondence'
            date_field = 'received_date'
            sender_field = 'sender'
            dept_field = 'sender_department'
            date_label = 'تاريخ الاستلام'
            sender_label = 'المرسل'
            dept_label = 'قسم المرسل'
        else:
            table = 'outgoing_correspondence'
            date_field = 'sent_date'
            sender_field = 'recipient'
            dept_field = 'recipient_department'
            date_label = 'تاريخ الإرسال'
            sender_label = 'المرسل إليه'
            dept_label = 'قسم المرسل إليه'
        
        # جلب البيانات
        query = f"SELECT * FROM {table} WHERE id = ?"
        data = self.db_manager.execute_query(query, (self.correspondence_id,))
        
        if not data:
            messagebox.showerror("خطأ", "لم يتم العثور على المراسلة")
            self.window.destroy()
            return
        
        record = dict(data[0])
        
        # إنشاء الواجهة
        self.create_display_widgets(record, date_field, sender_field, dept_field, 
                                  date_label, sender_label, dept_label)
    
    def create_display_widgets(self, record, date_field, sender_field, dept_field,
                             date_label, sender_label, dept_label):
        """إنشاء عناصر العرض"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # العنوان
        type_text = "مراسلة واردة" if self.correspondence_type == 'incoming' else "مراسلة صادرة"
        title_label = tk.Label(
            main_frame,
            text=f"تفاصيل {type_text}",
            font=('Arial Unicode MS', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # إطار التفاصيل
        details_frame = ttk.LabelFrame(main_frame, text="معلومات المراسلة")
        details_frame.pack(fill='x', pady=(0, 10))
        
        # إنشاء الحقول
        fields = [
            ("رقم المراسلة:", record['reference_number']),
            ("الموضوع:", record['subject']),
            (sender_label + ":", record[sender_field]),
            (dept_label + ":", record[dept_field] or '-'),
            (date_label + ":", record[date_field]),
            ("الأولوية:", record['priority']),
            ("الحالة:", record['status']),
        ]
        
        for i, (label, value) in enumerate(fields):
            self.create_info_row(details_frame, label, value, i)
        
        # المحتوى
        if record['content']:
            content_frame = ttk.LabelFrame(main_frame, text="المحتوى")
            content_frame.pack(fill='both', expand=True, pady=(10, 0))
            
            content_text = tk.Text(
                content_frame,
                height=10,
                font=('Arial Unicode MS', 10),
                wrap='word',
                state='disabled',
                bg='#f8f9fa'
            )
            content_text.pack(fill='both', expand=True, padx=10, pady=10)
            
            # إدراج المحتوى
            content_text.config(state='normal')
            content_text.insert('1.0', record['content'])
            content_text.config(state='disabled')
        
        # الملاحظات
        if record['notes']:
            notes_frame = ttk.LabelFrame(main_frame, text="ملاحظات")
            notes_frame.pack(fill='x', pady=(10, 0))
            
            notes_text = tk.Text(
                notes_frame,
                height=4,
                font=('Arial Unicode MS', 10),
                wrap='word',
                state='disabled',
                bg='#f8f9fa'
            )
            notes_text.pack(fill='x', padx=10, pady=10)
            
            # إدراج الملاحظات
            notes_text.config(state='normal')
            notes_text.insert('1.0', record['notes'])
            notes_text.config(state='disabled')
        
        # معلومات إضافية
        info_frame = ttk.LabelFrame(main_frame, text="معلومات إضافية")
        info_frame.pack(fill='x', pady=(10, 0))
        
        additional_fields = [
            ("تاريخ الإنشاء:", record['created_at'][:16] if record['created_at'] else '-'),
            ("آخر تحديث:", record['updated_at'][:16] if record['updated_at'] else '-'),
        ]
        
        for i, (label, value) in enumerate(additional_fields):
            self.create_info_row(info_frame, label, value, i)
        
        # زر الإغلاق
        close_btn = ttk.Button(
            main_frame,
            text="إغلاق",
            command=self.window.destroy
        )
        close_btn.pack(pady=(20, 0))
    
    def create_info_row(self, parent, label_text, value_text, row):
        """إنشاء صف معلومات"""
        # التسمية
        label = ttk.Label(
            parent,
            text=label_text,
            font=('Arial Unicode MS', 10, 'bold')
        )
        label.grid(row=row, column=0, sticky='e', padx=(10, 5), pady=5)
        
        # القيمة
        value = ttk.Label(
            parent,
            text=str(value_text),
            font=('Arial Unicode MS', 10)
        )
        value.grid(row=row, column=1, sticky='w', padx=(5, 10), pady=5)
        
        # تكوين الأعمدة
        parent.grid_columnconfigure(1, weight=1)
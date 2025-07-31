#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نافذة عرض تفاصيل المتابعة
Follow-up View Window
"""

import tkinter as tk
from tkinter import ttk, messagebox

class FollowUpView:
    def __init__(self, parent, db_manager, followup_id):
        self.db_manager = db_manager
        self.followup_id = followup_id
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.load_and_display_data()
    
    def setup_window(self):
        """إعداد النافذة"""
        self.window.title("عرض تفاصيل المتابعة")
        self.window.geometry("600x500")
        self.window.resizable(False, False)
        
        # توسيط النافذة
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (500 // 2)
        self.window.geometry(f"600x500+{x}+{y}")
        
        # جعل النافذة في المقدمة
        self.window.transient(self.window.master)
        self.window.grab_set()
    
    def load_and_display_data(self):
        """تحميل وعرض البيانات"""
        # جلب بيانات المتابعة
        query = '''
            SELECT f.*, 
                   CASE 
                       WHEN f.correspondence_type = 'incoming' THEN ic.reference_number
                       WHEN f.correspondence_type = 'outgoing' THEN oc.reference_number
                   END as correspondence_ref,
                   CASE 
                       WHEN f.correspondence_type = 'incoming' THEN ic.subject
                       WHEN f.correspondence_type = 'outgoing' THEN oc.subject
                   END as correspondence_subject
            FROM follow_up f
            LEFT JOIN incoming_correspondence ic ON f.correspondence_type = 'incoming' AND f.correspondence_id = ic.id
            LEFT JOIN outgoing_correspondence oc ON f.correspondence_type = 'outgoing' AND f.correspondence_id = oc.id
            WHERE f.id = ?
        '''
        
        data = self.db_manager.execute_query(query, (self.followup_id,))
        
        if not data:
            messagebox.showerror("خطأ", "لم يتم العثور على المتابعة")
            self.window.destroy()
            return
        
        record = dict(data[0])
        self.create_display_widgets(record)
    
    def create_display_widgets(self, record):
        """إنشاء عناصر العرض"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # العنوان
        title_label = tk.Label(
            main_frame,
            text="تفاصيل المتابعة",
            font=('Arial Unicode MS', 16, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # إطار التفاصيل
        details_frame = ttk.LabelFrame(main_frame, text="معلومات المتابعة")
        details_frame.pack(fill='x', pady=(0, 10))
        
        # إنشاء الحقول
        type_display = 'واردة' if record['correspondence_type'] == 'incoming' else 'صادرة'
        
        fields = [
            ("رقم المتابعة:", record['id']),
            ("نوع المراسلة:", type_display),
            ("رقم المراسلة:", record['correspondence_ref'] or '-'),
            ("موضوع المراسلة:", record['correspondence_subject'] or '-'),
            ("تاريخ المتابعة:", record['follow_up_date']),
            ("المسؤول:", record['responsible_person'] or '-'),
            ("الحالة:", record['status']),
        ]
        
        for i, (label, value) in enumerate(fields):
            self.create_info_row(details_frame, label, value, i)
        
        # الإجراء المطلوب
        if record['action_required']:
            action_frame = ttk.LabelFrame(main_frame, text="الإجراء المطلوب")
            action_frame.pack(fill='both', expand=True, pady=(10, 0))
            
            action_text = tk.Text(
                action_frame,
                height=6,
                font=('Arial Unicode MS', 10),
                wrap='word',
                state='disabled',
                bg='#f8f9fa'
            )
            action_text.pack(fill='both', expand=True, padx=10, pady=10)
            
            # إدراج النص
            action_text.config(state='normal')
            action_text.insert('1.0', record['action_required'])
            action_text.config(state='disabled')
        
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
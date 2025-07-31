#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نموذج إضافة/تعديل المراسلات
Correspondence Form
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from tkcalendar import DateEntry

class CorrespondenceForm:
    def __init__(self, parent, db_manager, auth_manager, user_data, 
                 correspondence_type='incoming', correspondence_id=None, 
                 related_incoming_id=None, original_data=None, callback=None, notify=None):
        
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.user_data = user_data
        self.correspondence_type = correspondence_type
        self.correspondence_id = correspondence_id
        self.related_incoming_id = related_incoming_id
        self.original_data = original_data
        self.callback = callback
        self.notify = notify  # دالة الإشعار الفوري
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        
        # تحميل البيانات للتعديل
        if correspondence_id:
            self.load_data()
        elif original_data:
            self.load_reply_data()
    
    def setup_window(self):
        """إعداد النافذة"""
        title = "تعديل" if self.correspondence_id else "إضافة"
        type_name = "مراسلة واردة" if self.correspondence_type == 'incoming' else "مراسلة صادرة"
        
        self.window.title(f"{title} {type_name}")
        self.window.geometry("600x700")
        self.window.resizable(False, False)
        
        # توسيط النافذة
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"600x700+{x}+{y}")
        
        # جعل النافذة في المقدمة
        self.window.transient(self.window.master)
        self.window.grab_set()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # العنوان
        title_text = "تعديل" if self.correspondence_id else "إضافة"
        type_text = "مراسلة واردة" if self.correspondence_type == 'incoming' else "مراسلة صادرة"
        
        title_label = tk.Label(
            main_frame,
            text=f"{title_text} {type_text}",
            font=('Arial Unicode MS', 14, 'bold'),
            fg='#2c3e50'
        )
        title_label.pack(pady=(0, 20))
        
        # إطار الحقول
        fields_frame = ttk.Frame(main_frame)
        fields_frame.pack(fill='both', expand=True)
        
        # رقم المراسلة
        self.create_field(fields_frame, "رقم المراسلة:", 0)
        self.reference_var = tk.StringVar()
        self.reference_entry = ttk.Entry(
            fields_frame, 
            textvariable=self.reference_var,
            font=('Arial Unicode MS', 10),
            justify='right'
        )
        self.reference_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # الموضوع
        self.create_field(fields_frame, "الموضوع:", 1)
        self.subject_var = tk.StringVar()
        self.subject_entry = ttk.Entry(
            fields_frame, 
            textvariable=self.subject_var,
            font=('Arial Unicode MS', 10),
            justify='right'
        )
        self.subject_entry.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # المرسل/المرسل إليه
        sender_label = "المرسل:" if self.correspondence_type == 'incoming' else "المرسل إليه:"
        self.create_field(fields_frame, sender_label, 2)
        self.sender_var = tk.StringVar()
        self.sender_entry = ttk.Entry(
            fields_frame, 
            textvariable=self.sender_var,
            font=('Arial Unicode MS', 10),
            justify='right'
        )
        self.sender_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # القسم
        dept_label = "قسم المرسل:" if self.correspondence_type == 'incoming' else "قسم المرسل إليه:"
        self.create_field(fields_frame, dept_label, 3)
        self.department_var = tk.StringVar()
        self.department_entry = ttk.Entry(
            fields_frame, 
            textvariable=self.department_var,
            font=('Arial Unicode MS', 10),
            justify='right'
        )
        self.department_entry.grid(row=3, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # التاريخ
        date_label = "تاريخ الاستلام:" if self.correspondence_type == 'incoming' else "تاريخ الإرسال:"
        self.create_field(fields_frame, date_label, 4)
        
        try:
            self.date_entry = DateEntry(
                fields_frame,
                width=12,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                date_pattern='yyyy-mm-dd',
                font=('Arial Unicode MS', 10)
            )
            self.date_entry.grid(row=4, column=1, sticky='w', padx=(10, 0), pady=5)
        except:
            # في حالة عدم توفر tkcalendar
            self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
            self.date_entry = ttk.Entry(
                fields_frame,
                textvariable=self.date_var,
                font=('Arial Unicode MS', 10),
                width=15
            )
            self.date_entry.grid(row=4, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # الأولوية
        self.create_field(fields_frame, "الأولوية:", 5)
        self.priority_var = tk.StringVar(value="عادي")
        priority_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.priority_var,
            values=["عاجل", "مهم", "عادي"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=15
        )
        priority_combo.grid(row=5, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # الحالة
        self.create_field(fields_frame, "الحالة:", 6)
        self.status_var = tk.StringVar()
        
        if self.correspondence_type == 'incoming':
            status_values = ["جديد", "قيد المراجعة", "تم الرد", "مؤرشف"]
            default_status = "جديد"
        else:
            status_values = ["مسودة", "تم الإرسال", "تم الاستلام", "مؤرشف"]
            default_status = "مسودة"
        
        self.status_var.set(default_status)
        status_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.status_var,
            values=status_values,
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=15
        )
        status_combo.grid(row=6, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # المحتوى
        self.create_field(fields_frame, "المحتوى:", 7)
        content_frame = ttk.Frame(fields_frame)
        content_frame.grid(row=7, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.content_text = tk.Text(
            content_frame,
            height=8,
            width=40,
            font=('Arial Unicode MS', 10),
            wrap='word'
        )
        content_scrollbar = ttk.Scrollbar(content_frame, orient='vertical', command=self.content_text.yview)
        self.content_text.configure(yscrollcommand=content_scrollbar.set)
        
        self.content_text.pack(side='left', fill='both', expand=True)
        content_scrollbar.pack(side='right', fill='y')
        
        # الملاحظات
        self.create_field(fields_frame, "ملاحظات:", 8)
        notes_frame = ttk.Frame(fields_frame)
        notes_frame.grid(row=8, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.notes_text = tk.Text(
            notes_frame,
            height=4,
            width=40,
            font=('Arial Unicode MS', 10),
            wrap='word'
        )
        notes_scrollbar = ttk.Scrollbar(notes_frame, orient='vertical', command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scrollbar.set)
        
        self.notes_text.pack(side='left', fill='both', expand=True)
        notes_scrollbar.pack(side='right', fill='y')
        
        # تكوين الشبكة
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        # زر الحفظ
        save_btn = ttk.Button(
            buttons_frame,
            text="حفظ",
            command=self.save_correspondence
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
        self.reference_entry.focus()
    
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
        if self.correspondence_type == 'incoming':
            table = 'incoming_correspondence'
            date_field = 'received_date'
            sender_field = 'sender'
            dept_field = 'sender_department'
        else:
            table = 'outgoing_correspondence'
            date_field = 'sent_date'
            sender_field = 'recipient'
            dept_field = 'recipient_department'
        
        query = f"SELECT * FROM {table} WHERE id = ?"
        data = self.db_manager.execute_query(query, (self.correspondence_id,))
        
        if data:
            record = dict(data[0])
            
            self.reference_var.set(record['reference_number'])
            self.subject_var.set(record['subject'])
            self.sender_var.set(record[sender_field])
            self.department_var.set(record[dept_field] or '')
            
            # تعيين التاريخ
            try:
                if hasattr(self.date_entry, 'set_date'):
                    date_obj = datetime.strptime(record[date_field], '%Y-%m-%d').date()
                    self.date_entry.set_date(date_obj)
                else:
                    self.date_var.set(record[date_field])
            except:
                pass
            
            self.priority_var.set(record['priority'])
            self.status_var.set(record['status'])
            
            self.content_text.delete('1.0', tk.END)
            self.content_text.insert('1.0', record['content'] or '')
            
            self.notes_text.delete('1.0', tk.END)
            self.notes_text.insert('1.0', record['notes'] or '')
    
    def load_reply_data(self):
        """تحميل بيانات للرد على مراسلة"""
        if self.original_data:
            # تعبئة البيانات من المراسلة الأصلية
            self.subject_var.set(f"رد على: {self.original_data['subject']}")
            self.sender_var.set(self.original_data['sender'])
            self.department_var.set(self.original_data['sender_department'] or '')
            
            # إضافة نص في المحتوى
            reply_content = f"بالإشارة إلى مراسلتكم رقم {self.original_data['reference_number']} "
            reply_content += f"بتاريخ {self.original_data['received_date']} "
            reply_content += f"بخصوص: {self.original_data['subject']}\n\n"
            
            self.content_text.delete('1.0', tk.END)
            self.content_text.insert('1.0', reply_content)
    
    def save_correspondence(self):
        """حفظ المراسلة"""
        # التحقق من صحة البيانات
        if not self.validate_data():
            return
        
        # جمع البيانات
        data = self.collect_data()
        
        try:
            if self.correspondence_id:
                # تحديث
                self.update_correspondence(data)
            else:
                # إضافة جديدة
                self.insert_correspondence(data)
            
            if self.notify:
                self.notify("تم حفظ المراسلة بنجاح", type_="success")
            
            # اس��دعاء callback لتحديث البيانات
            if self.callback:
                self.callback()
            
            self.window.destroy()
            
        except Exception as e:
            if self.notify:
                self.notify(f"فشل في حفظ المراسلة: {e}", type_="error")
            else:
                messagebox.showerror("خطأ", f"فشل في حفظ المراسلة: {e}")
    
    def validate_data(self):
        """التحقق من صحة البيانات"""
        if not self.reference_var.get().strip():
            if self.notify:
                self.notify("يرجى إدخال رقم المراسلة", type_="error")
            self.reference_entry.focus()
            return False
        
        if not self.subject_var.get().strip():
            if self.notify:
                self.notify("يرجى إدخال موضوع المراسلة", type_="error")
            self.subject_entry.focus()
            return False
        
        if not self.sender_var.get().strip():
            sender_label = "المرسل" if self.correspondence_type == 'incoming' else "المرسل إليه"
            if self.notify:
                self.notify(f"يرجى إدخال {sender_label}", type_="error")
            self.sender_entry.focus()
            return False
        
        return True
    
    def collect_data(self):
        """جمع البيانات من النموذج"""
        # الحصول على التاريخ
        try:
            if hasattr(self.date_entry, 'get_date'):
                date_value = self.date_entry.get_date().strftime('%Y-%m-%d')
            else:
                date_value = self.date_var.get()
        except:
            date_value = date.today().strftime('%Y-%m-%d')
        
        data = {
            'reference_number': self.reference_var.get().strip(),
            'subject': self.subject_var.get().strip(),
            'sender': self.sender_var.get().strip(),
            'department': self.department_var.get().strip() or None,
            'date': date_value,
            'priority': self.priority_var.get(),
            'status': self.status_var.get(),
            'content': self.content_text.get('1.0', tk.END).strip() or None,
            'notes': self.notes_text.get('1.0', tk.END).strip() or None
        }
        
        return data
    
    def insert_correspondence(self, data):
        """إدراج مراسلة جديدة"""
        if self.correspondence_type == 'incoming':
            query = '''
                INSERT INTO incoming_correspondence 
                (reference_number, subject, sender, sender_department, received_date, 
                 priority, status, content, notes, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                data['reference_number'], data['subject'], data['sender'],
                data['department'], data['date'], data['priority'],
                data['status'], data['content'], data['notes'],
                self.user_data['id']
            )
        else:
            query = '''
                INSERT INTO outgoing_correspondence 
                (reference_number, subject, recipient, recipient_department, sent_date, 
                 priority, status, content, notes, related_incoming_id, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            params = (
                data['reference_number'], data['subject'], data['sender'],
                data['department'], data['date'], data['priority'],
                data['status'], data['content'], data['notes'],
                self.related_incoming_id, self.user_data['id']
            )
        
        result = self.db_manager.execute_update(query, params)
        
        if result:
            # تسجيل النشاط
            action = f"إضافة مراسلة {'واردة' if self.correspondence_type == 'incoming' else 'صادرة'} رقم {data['reference_number']}"
            table_name = 'incoming_correspondence' if self.correspondence_type == 'incoming' else 'outgoing_correspondence'
            
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=action,
                table_name=table_name,
                record_id=result
            )
    
    def update_correspondence(self, data):
        """تحديث مراسلة موجودة"""
        if self.correspondence_type == 'incoming':
            query = '''
                UPDATE incoming_correspondence 
                SET reference_number=?, subject=?, sender=?, sender_department=?, 
                    received_date=?, priority=?, status=?, content=?, notes=?, 
                    updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            '''
            params = (
                data['reference_number'], data['subject'], data['sender'],
                data['department'], data['date'], data['priority'],
                data['status'], data['content'], data['notes'],
                self.correspondence_id
            )
            table_name = 'incoming_correspondence'
        else:
            query = '''
                UPDATE outgoing_correspondence 
                SET reference_number=?, subject=?, recipient=?, recipient_department=?, 
                    sent_date=?, priority=?, status=?, content=?, notes=?, 
                    updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            '''
            params = (
                data['reference_number'], data['subject'], data['sender'],
                data['department'], data['date'], data['priority'],
                data['status'], data['content'], data['notes'],
                self.correspondence_id
            )
            table_name = 'outgoing_correspondence'
        
        result = self.db_manager.execute_update(query, params)
        
        if result is not None:
            # تسجيل النشاط
            action = f"تحديث مراسلة {'واردة' if self.correspondence_type == 'incoming' else 'صادرة'} رقم {data['reference_number']}"
            
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=action,
                table_name=table_name,
                record_id=self.correspondence_id
            )
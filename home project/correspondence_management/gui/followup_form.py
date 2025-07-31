#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نموذج إضافة/تعديل المتابعة
Follow-up Form
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

class FollowUpForm:
    def __init__(self, parent, db_manager, auth_manager, user_data, 
                 correspondence_type=None, correspondence_id=None, 
                 followup_id=None, callback=None, notify=None):
        
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.user_data = user_data
        self.correspondence_type = correspondence_type
        self.correspondence_id = correspondence_id
        self.followup_id = followup_id
        self.callback = callback
        self.notify = notify  # دالة الإشعار الفوري
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        
        # تحميل البيانات للتعديل
        if followup_id:
            self.load_data()
    
    def setup_window(self):
        """إعداد النافذة"""
        title = "تعديل متابعة" if self.followup_id else "إضافة متابعة"
        
        self.window.title(title)
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
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = ttk.Frame(self.window)
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # العنوان
        title_text = "تعديل متابعة" if self.followup_id else "إضافة متابعة"
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
        
        # نوع المراسلة (إذا لم يكن محدد مسبقاً)
        if not self.correspondence_type:
            self.create_field(fields_frame, "نوع المراسلة:", 0)
            self.type_var = tk.StringVar(value="incoming")
            type_combo = ttk.Combobox(
                fields_frame,
                textvariable=self.type_var,
                values=[("incoming", "واردة"), ("outgoing", "صادرة")],
                state="readonly",
                font=('Arial Unicode MS', 10)
            )
            type_combo.grid(row=0, column=1, sticky='w', padx=(10, 0), pady=5)
            type_combo.bind('<<ComboboxSelected>>', self.on_type_change)
        
        # المراسلة المرتبطة
        row_offset = 0 if self.correspondence_type else 1
        
        self.create_field(fields_frame, "المراسلة المرتبطة:", row_offset)
        self.correspondence_var = tk.StringVar()
        self.correspondence_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.correspondence_var,
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=40
        )
        self.correspondence_combo.grid(row=row_offset, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # تحميل قائمة المراسلات
        self.load_correspondence_list()
        
        # تاريخ المتابعة
        self.create_field(fields_frame, "تاريخ المتابعة:", row_offset + 1)
        
        try:
            from tkcalendar import DateEntry
            self.date_entry = DateEntry(
                fields_frame,
                width=12,
                background='darkblue',
                foreground='white',
                borderwidth=2,
                date_pattern='yyyy-mm-dd',
                font=('Arial Unicode MS', 10)
            )
            self.date_entry.grid(row=row_offset + 1, column=1, sticky='w', padx=(10, 0), pady=5)
        except:
            # في حالة عدم توفر tkcalendar
            self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
            self.date_entry = ttk.Entry(
                fields_frame,
                textvariable=self.date_var,
                font=('Arial Unicode MS', 10),
                width=15
            )
            self.date_entry.grid(row=row_offset + 1, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # الإجراء المطلوب
        self.create_field(fields_frame, "الإجراء المطلوب:", row_offset + 2)
        action_frame = ttk.Frame(fields_frame)
        action_frame.grid(row=row_offset + 2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.action_text = tk.Text(
            action_frame,
            height=4,
            width=40,
            font=('Arial Unicode MS', 10),
            wrap='word'
        )
        action_scrollbar = ttk.Scrollbar(action_frame, orient='vertical', command=self.action_text.yview)
        self.action_text.configure(yscrollcommand=action_scrollbar.set)
        
        self.action_text.pack(side='left', fill='both', expand=True)
        action_scrollbar.pack(side='right', fill='y')
        
        # المسؤول
        self.create_field(fields_frame, "المسؤول:", row_offset + 3)
        self.responsible_var = tk.StringVar()
        self.responsible_entry = ttk.Entry(
            fields_frame,
            textvariable=self.responsible_var,
            font=('Arial Unicode MS', 10),
            justify='right'
        )
        self.responsible_entry.grid(row=row_offset + 3, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # الحالة
        self.create_field(fields_frame, "الحالة:", row_offset + 4)
        self.status_var = tk.StringVar(value="معلق")
        status_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.status_var,
            values=["معلق", "قيد التنفيذ", "مكتمل", "ملغي"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=15
        )
        status_combo.grid(row=row_offset + 4, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # ملاحظات
        self.create_field(fields_frame, "ملاحظات:", row_offset + 5)
        notes_frame = ttk.Frame(fields_frame)
        notes_frame.grid(row=row_offset + 5, column=1, sticky='ew', padx=(10, 0), pady=5)
        
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
            command=self.save_followup
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
        if hasattr(self, 'action_text'):
            self.action_text.focus()
    
    def create_field(self, parent, text, row):
        """إنشاء تسمية حقل"""
        label = ttk.Label(
            parent,
            text=text,
            font=('Arial Unicode MS', 10, 'bold')
        )
        label.grid(row=row, column=0, sticky='e', padx=(0, 10), pady=5)
    
    def load_correspondence_list(self):
        """تحميل قائمة المراسلات"""
        if self.correspondence_type:
            # نوع محدد مسبقاً
            self.load_correspondence_by_type(self.correspondence_type)
        else:
            # تحميل حسب النوع المختار
            self.load_correspondence_by_type('incoming')  # افتراضي
    
    def load_correspondence_by_type(self, corr_type):
        """تحميل المراسلات حسب النوع"""
        if corr_type == 'incoming':
            query = "SELECT id, reference_number, subject FROM incoming_correspondence ORDER BY received_date DESC"
        else:
            query = "SELECT id, reference_number, subject FROM outgoing_correspondence ORDER BY sent_date DESC"
        
        data = self.db_manager.execute_query(query)
        
        # تحديث قائمة الخيارات
        values = []
        for row in data:
            display_text = f"{row['reference_number']} - {row['subject'][:50]}"
            values.append((row['id'], display_text))
        
        self.correspondence_combo['values'] = [item[1] for item in values]
        self.correspondence_data = {item[1]: item[0] for item in values}
        
        # تحديد المراسلة إذا كانت محددة مسبقاً
        if self.correspondence_id:
            for display_text, corr_id in self.correspondence_data.items():
                if corr_id == self.correspondence_id:
                    self.correspondence_var.set(display_text)
                    break
    
    def on_type_change(self, event=None):
        """عند تغيير نوع المراسلة"""
        selected_type = self.type_var.get()
        self.load_correspondence_by_type(selected_type)
    
    def load_data(self):
        """تحميل البيانات للتعديل"""
        query = "SELECT * FROM follow_up WHERE id = ?"
        data = self.db_manager.execute_query(query, (self.followup_id,))
        
        if data:
            record = dict(data[0])
            
            # تعيين نوع المراسلة
            if not self.correspondence_type:
                self.type_var.set(record['correspondence_type'])
                self.load_correspondence_by_type(record['correspondence_type'])
            
            # تعيين المراسلة المرتبطة
            for display_text, corr_id in self.correspondence_data.items():
                if corr_id == record['correspondence_id']:
                    self.correspondence_var.set(display_text)
                    break
            
            # تعيين التاريخ
            try:
                if hasattr(self.date_entry, 'set_date'):
                    date_obj = datetime.strptime(record['follow_up_date'], '%Y-%m-%d').date()
                    self.date_entry.set_date(date_obj)
                else:
                    self.date_var.set(record['follow_up_date'])
            except:
                pass
            
            # تعيين باقي الحقول
            self.action_text.delete('1.0', tk.END)
            self.action_text.insert('1.0', record['action_required'])
            
            self.responsible_var.set(record['responsible_person'] or '')
            self.status_var.set(record['status'])
            
            self.notes_text.delete('1.0', tk.END)
            self.notes_text.insert('1.0', record['notes'] or '')
    
    def save_followup(self):
        """حفظ المتابعة"""
        # التحقق من صحة البيانات
        if not self.validate_data():
            return
        
        # جمع البيانات
        data = self.collect_data()
        
        try:
            if self.followup_id:
                # تحديث
                self.update_followup(data)
            else:
                # إضافة جديدة
                self.insert_followup(data)
            
            if self.notify:
                self.notify("تم حفظ المتابعة بنجاح", type_="success")
            
            # استدعاء callback لتحديث البيانات
            if self.callback:
                self.callback()
            
            self.window.destroy()
            
        except Exception as e:
            if self.notify:
                self.notify(f"فشل في حفظ المتابعة: {e}", type_="error")
            else:
                messagebox.showerror("خطأ", f"فشل في حفظ المتابعة: {e}")
    
    def validate_data(self):
        """التحقق من صحة البيانات"""
        if not self.correspondence_var.get():
            if self.notify:
                self.notify("يرجى اختيار المراسلة المرتبطة", type_="error")
            return False
        
        if not self.action_text.get('1.0', tk.END).strip():
            if self.notify:
                self.notify("يرجى إدخال الإجراء المطلوب", type_="error")
            self.action_text.focus()
            return False
        
        return True
    
    def collect_data(self):
        """جمع البيانات من النموذج"""
        # الحصول على معرف المراسلة
        selected_correspondence = self.correspondence_var.get()
        correspondence_id = self.correspondence_data.get(selected_correspondence)
        
        # تحديد نوع المراسلة
        if self.correspondence_type:
            corr_type = self.correspondence_type
        else:
            corr_type = self.type_var.get()
        
        # الحصول على التاريخ
        try:
            if hasattr(self.date_entry, 'get_date'):
                date_value = self.date_entry.get_date().strftime('%Y-%m-%d')
            else:
                date_value = self.date_var.get()
        except:
            date_value = date.today().strftime('%Y-%m-%d')
        
        data = {
            'correspondence_type': corr_type,
            'correspondence_id': correspondence_id,
            'follow_up_date': date_value,
            'action_required': self.action_text.get('1.0', tk.END).strip(),
            'responsible_person': self.responsible_var.get().strip() or None,
            'status': self.status_var.get(),
            'notes': self.notes_text.get('1.0', tk.END).strip() or None
        }
        
        return data
    
    def insert_followup(self, data):
        """إدراج متابعة جديدة"""
        query = '''
            INSERT INTO follow_up 
            (correspondence_type, correspondence_id, follow_up_date, action_required,
             responsible_person, status, notes, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            data['correspondence_type'], data['correspondence_id'], data['follow_up_date'],
            data['action_required'], data['responsible_person'], data['status'],
            data['notes'], self.user_data['id']
        )
        
        result = self.db_manager.execute_update(query, params)
        
        if result:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"إضافة متابعة للمراسلة {data['correspondence_type']} رقم {data['correspondence_id']}",
                table_name="follow_up",
                record_id=result
            )
    
    def update_followup(self, data):
        """تحديث متابعة موجودة"""
        query = '''
            UPDATE follow_up 
            SET correspondence_type=?, correspondence_id=?, follow_up_date=?, 
                action_required=?, responsible_person=?, status=?, notes=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        '''
        params = (
            data['correspondence_type'], data['correspondence_id'], data['follow_up_date'],
            data['action_required'], data['responsible_person'], data['status'],
            data['notes'], self.followup_id
        )
        
        result = self.db_manager.execute_update(query, params)
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"تحديث متابعة رقم {self.followup_id}",
                table_name="follow_up",
                record_id=self.followup_id
            )
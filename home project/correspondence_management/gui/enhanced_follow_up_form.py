#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نموذج المتابعة المحسن
Enhanced Follow-up Form
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import re

class EnhancedFollowUpForm:
    def __init__(self, parent, db_manager, auth_manager, user_data, 
                 follow_up_id=None, callback=None):
        
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.user_data = user_data
        self.follow_up_id = follow_up_id
        self.callback = callback
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        
        # تحميل البيانات للتعديل
        if follow_up_id:
            self.load_data()
        else:
            # تحديث قائمة المراسلات
            self.refresh_correspondence_list()
    
    def setup_window(self):
        """إعداد النافذة"""
        title = "تعديل متابعة" if self.follow_up_id else "إضافة متابعة جديدة"
        
        self.window.title(title)
        self.window.geometry("700x650")
        self.window.resizable(False, False)
        self.window.configure(bg='#f8f9fa')
        
        # توسيط النافذة
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.window.winfo_screenheight() // 2) - (650 // 2)
        self.window.geometry(f"700x650+{x}+{y}")
        
        # جعل النافذة في المقدمة
        self.window.transient(self.window.master)
        self.window.grab_set()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.window, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # العنوان
        title_text = "تعديل متابعة" if self.follow_up_id else "إضافة متابعة جديدة"
        title_label = tk.Label(
            main_frame,
            text=title_text,
            font=('Arial Unicode MS', 16, 'bold'),
            fg='#2c3e50',
            bg='#f8f9fa'
        )
        title_label.pack(pady=(0, 20))
        
        # إطار النموذج
        form_frame = tk.Frame(main_frame, bg='white', relief='solid', bd=1)
        form_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # إطار الحقول
        fields_frame = tk.Frame(form_frame, bg='white')
        fields_frame.pack(fill='both', expand=True, padx=30, pady=30)
        
        # 1. كود المتابعة (تلقائي)
        self.create_field_label(fields_frame, "كود المتابعة", 0)
        self.follow_up_code_var = tk.StringVar()
        code_frame = tk.Frame(fields_frame, bg='white')
        code_frame.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.code_entry = tk.Entry(
            code_frame,
            textvariable=self.follow_up_code_var,
            font=('Arial Unicode MS', 11),
            state='readonly',
            bg='#f8f9fa',
            fg='#2c3e50',
            justify='center',
            relief='solid',
            bd=1
        )
        self.code_entry.pack(side='left', fill='x', expand=True)
        
        # 2. نوع المراسلة
        self.create_field_label(fields_frame, "نوع المراسلة", 1)
        self.correspondence_type_var = tk.StringVar(value="incoming")
        type_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.correspondence_type_var,
            values=["incoming", "outgoing"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=20
        )
        type_combo.grid(row=1, column=1, sticky='w', padx=(10, 0), pady=5)
        type_combo.bind('<<ComboboxSelected>>', self.on_type_change)
        
        # 3. المراسلة المرتبطة
        self.create_field_label(fields_frame, "المراسلة المرتبطة", 2)
        correspondence_frame = tk.Frame(fields_frame, bg='white')
        correspondence_frame.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.correspondence_var = tk.StringVar()
        self.correspondence_combo = ttk.Combobox(
            correspondence_frame,
            textvariable=self.correspondence_var,
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=50
        )
        self.correspondence_combo.pack(side='left', fill='x', expand=True)
        self.correspondence_combo.bind('<<ComboboxSelected>>', self.on_correspondence_change)
        
        # زر تحديث القائمة
        refresh_btn = tk.Button(
            correspondence_frame,
            text="🔄",
            font=('Arial Unicode MS', 10),
            bg='#3498db',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.refresh_correspondence_list,
            width=3
        )
        refresh_btn.pack(side='right', padx=(5, 0))
        
        # 4. تاريخ المتابعة
        self.create_field_label(fields_frame, "تاريخ المتابعة", 3)
        
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
            self.date_entry.grid(row=3, column=1, sticky='w', padx=(10, 0), pady=5)
        except ImportError:
            self.date_var = tk.StringVar(value=date.today().strftime('%Y-%m-%d'))
            self.date_entry = tk.Entry(
                fields_frame,
                textvariable=self.date_var,
                font=('Arial Unicode MS', 11),
                width=15,
                justify='center',
                relief='solid',
                bd=1
            )
            self.date_entry.grid(row=3, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # 5. الإجراء المطلوب
        self.create_field_label(fields_frame, "الإجراء المطلوب", 4)
        action_frame = tk.Frame(fields_frame, bg='white')
        action_frame.grid(row=4, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.action_text = tk.Text(
            action_frame,
            height=4,
            font=('Arial Unicode MS', 11),
            wrap='word',
            relief='solid',
            bd=1
        )
        action_scrollbar = ttk.Scrollbar(action_frame, orient='vertical', command=self.action_text.yview)
        self.action_text.configure(yscrollcommand=action_scrollbar.set)
        
        self.action_text.pack(side='left', fill='both', expand=True)
        action_scrollbar.pack(side='right', fill='y')
        
        # 6. المسئول
        self.create_field_label(fields_frame, "المسئول", 5)
        self.responsible_var = tk.StringVar()
        self.responsible_entry = tk.Entry(
            fields_frame,
            textvariable=self.responsible_var,
            font=('Arial Unicode MS', 11),
            justify='right',
            relief='solid',
            bd=1
        )
        self.responsible_entry.grid(row=5, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # 7. الحالة
        self.create_field_label(fields_frame, "الحالة", 6)
        self.status_var = tk.StringVar(value="معلق")
        self.status_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.status_var,
            values=["معلق", "جاري", "مغلق"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=15
        )
        self.status_combo.grid(row=6, column=1, sticky='w', padx=(10, 0), pady=5)
        self.status_combo.bind('<<ComboboxSelected>>', self.on_status_change)
        
        # 8. ملاحظات
        self.create_field_label(fields_frame, "ملاحظات", 7)
        notes_frame = tk.Frame(fields_frame, bg='white')
        notes_frame.grid(row=7, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.notes_text = tk.Text(
            notes_frame,
            height=3,
            font=('Arial Unicode MS', 11),
            wrap='word',
            relief='solid',
            bd=1
        )
        notes_scrollbar = ttk.Scrollbar(notes_frame, orient='vertical', command=self.notes_text.yview)
        self.notes_text.configure(yscrollcommand=notes_scrollbar.set)
        
        self.notes_text.pack(side='left', fill='both', expand=True)
        notes_scrollbar.pack(side='right', fill='y')
        
        # تكوين الشبكة
        fields_frame.grid_columnconfigure(1, weight=1)
        
        # أزرار العمليات
        buttons_frame = tk.Frame(main_frame, bg='#f8f9fa')
        buttons_frame.pack(fill='x', pady=(20, 0))
        
        # زر الحفظ
        save_btn = tk.Button(
            buttons_frame,
            text="💾 حفظ المتابعة",
            font=('Arial Unicode MS', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.save_follow_up,
            pady=10
        )
        save_btn.pack(side='right', padx=5)
        
        # زر الإلغاء
        cancel_btn = tk.Button(
            buttons_frame,
            text="❌ إلغاء",
            font=('Arial Unicode MS', 12),
            bg='#e74c3c',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.window.destroy,
            pady=10
        )
        cancel_btn.pack(side='right', padx=5)
    
    def create_field_label(self, parent, text, row):
        """إنشاء تسمية حقل"""
        label = tk.Label(
            parent,
            text=text + ":",
            font=('Arial Unicode MS', 11, 'bold'),
            fg='#2c3e50',
            bg='white',
            anchor='e'
        )
        label.grid(row=row, column=0, sticky='e', padx=(0, 10), pady=5)
    
    def on_type_change(self, event=None):
        """عند تغيير نوع المراسلة"""
        self.refresh_correspondence_list()
    
    def on_correspondence_change(self, event=None):
        """عند تغيير المراسلة المحددة"""
        if not self.follow_up_id:  # فقط للمتابعات الجديدة
            self.generate_follow_up_code()
    
    def on_status_change(self, event=None):
        """عند تغيير الحالة"""
        status = self.status_var.get()
        
        # التحقق من الصلاحيات للحالة "مغلق"
        if status == "مغلق" and not self.auth_manager.has_permission('close_follow_up'):
            messagebox.showerror("خطأ", "ليس لديك صلاحية لإغلاق المتابعات")
            self.status_var.set("معلق")  # إعادة تعيين للحالة السابقة
            return
        
        # تحذير عند الإغلاق
        if status == "مغلق":
            if not messagebox.askyesno("تأكيد", "هل أنت متأكد من إغلاق هذه المتابعة؟\nلن يمكن تعديلها مرة أخرى إلا بصلاحيات خاصة."):
                self.status_var.set("معلق")
                return
    
    def refresh_correspondence_list(self):
        """تحديث قائمة المراسلات (استبعاد المغلقة)"""
        correspondence_type = self.correspondence_type_var.get()
        
        if correspondence_type == "incoming":
            # جلب المراسلات الواردة غير المغلقة
            query = '''
                SELECT ic.id, ic.reference_number, ic.subject_code, ic.subject
                FROM incoming_correspondence ic
                LEFT JOIN follow_up fu ON ic.id = fu.correspondence_id 
                    AND fu.correspondence_type = 'incoming'
                WHERE fu.status IS NULL OR fu.status != 'مغلق'
                ORDER BY ic.received_date DESC
            '''
        else:
            # جلب المراسلات الصادرة غير المغلقة
            query = '''
                SELECT oc.id, oc.reference_number, oc.subject, '' as subject_code
                FROM outgoing_correspondence oc
                LEFT JOIN follow_up fu ON oc.id = fu.correspondence_id 
                    AND fu.correspondence_type = 'outgoing'
                WHERE fu.status IS NULL OR fu.status != 'مغلق'
                ORDER BY oc.sent_date DESC
            '''
        
        try:
            data = self.db_manager.execute_query(query)
            
            # تحديث القائمة المنسدلة
            correspondence_list = []
            self.correspondence_data = {}
            
            for row in data:
                if correspondence_type == "incoming":
                    display_text = f"{row['reference_number']} - {row['subject'][:50]}..."
                    code_part = row['subject_code'] or 'CHR'
                else:
                    display_text = f"{row['reference_number']} - {row['subject'][:50]}..."
                    code_part = 'OUT'
                
                correspondence_list.append(display_text)
                self.correspondence_data[display_text] = {
                    'id': row['id'],
                    'reference_number': row['reference_number'],
                    'subject_code': code_part
                }
            
            self.correspondence_combo['values'] = correspondence_list
            
            if correspondence_list:
                self.correspondence_combo.set('')
            else:
                messagebox.showinfo("تنبيه", "لا توجد مراسلات متاحة للمتابعة")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحديث قائمة المراسلات: {e}")
    
    def generate_follow_up_code(self):
        """توليد كود المتابعة"""
        selected = self.correspondence_var.get()
        if not selected or selected not in self.correspondence_data:
            return
        
        correspondence_info = self.correspondence_data[selected]
        correspondence_type = self.correspondence_type_var.get()
        
        # تحديد بادئة النوع
        type_prefix = "IN" if correspondence_type == "incoming" else "OUT"
        
        # الحصول على كود الموضوع
        subject_code = correspondence_info['subject_code']
        
        # الحصول على رقم المتابعة التالي لهذه المراسلة
        query = '''
            SELECT COUNT(*) as count 
            FROM follow_up 
            WHERE correspondence_id = ? AND correspondence_type = ?
        '''
        result = self.db_manager.execute_query(query, (correspondence_info['id'], correspondence_type))
        
        follow_up_number = (result[0]['count'] + 1) if result else 1
        
        # تكوين الكود النهائي
        follow_up_code = f"{type_prefix}-{subject_code}-{follow_up_number}"
        
        self.follow_up_code_var.set(follow_up_code)
    
    def validate_data(self):
        """التحقق من صحة البيانات"""
        if not self.correspondence_var.get():
            messagebox.showerror("خطأ", "يرجى اختيار المراسلة المرتبطة")
            return False
        
        if not self.action_text.get('1.0', tk.END).strip():
            messagebox.showerror("خطأ", "يرجى إدخال الإجراء المطلوب")
            self.action_text.focus()
            return False
        
        if not self.responsible_var.get().strip():
            messagebox.showerror("خطأ", "يرجى إدخال اسم المسئول")
            self.responsible_entry.focus()
            return False
        
        return True
    
    def check_closed_status(self):
        """التحقق من حالة الإغلاق للمتابعة الحالية"""
        if not self.follow_up_id:
            return True  # متابعة جديدة
        
        query = "SELECT status FROM follow_up WHERE id = ?"
        result = self.db_manager.execute_query(query, (self.follow_up_id,))
        
        if result and result[0]['status'] == 'مغلق':
            # التحقق من الصلاحيات
            if not self.auth_manager.has_permission('edit_closed_follow_up'):
                messagebox.showerror("خطأ", "لا يمكن تعديل متابعة مغلقة")
                return False
            
            # طلب كلمة المرور للتأكيد
            return self.verify_admin_password()
        
        return True
    
    def verify_admin_password(self):
        """التحقق من كلمة مرور المدير"""
        password_window = tk.Toplevel(self.window)
        password_window.title("تأكيد الهوية")
        password_window.geometry("300x150")
        password_window.resizable(False, False)
        password_window.transient(self.window)
        password_window.grab_set()
        
        # توسيط النافذة
        password_window.update_idletasks()
        x = (password_window.winfo_screenwidth() // 2) - (300 // 2)
        y = (password_window.winfo_screenheight() // 2) - (150 // 2)
        password_window.geometry(f"300x150+{x}+{y}")
        
        tk.Label(password_window, text="أدخل كلمة المرور للتأكيد:", 
                font=('Arial Unicode MS', 10)).pack(pady=10)
        
        password_var = tk.StringVar()
        password_entry = tk.Entry(password_window, textvariable=password_var, 
                                show='*', font=('Arial Unicode MS', 10))
        password_entry.pack(pady=5)
        password_entry.focus()
        
        result = {'verified': False}
        
        def verify():
            password = password_var.get()
            user_data = self.auth_manager.authenticate(self.user_data['username'], password)
            
            if user_data and self.auth_manager.has_permission('edit_closed_follow_up'):
                result['verified'] = True
                password_window.destroy()
            else:
                messagebox.showerror("خطأ", "كلمة مرور خاطئة أو ليس لديك صلاحية")
                password_entry.delete(0, tk.END)
        
        tk.Button(password_window, text="تأكيد", command=verify).pack(pady=10)
        
        password_window.wait_window()
        return result['verified']
    
    def save_follow_up(self):
        """حفظ المتابعة"""
        # التحقق من حالة الإغلاق
        if not self.check_closed_status():
            return
        
        # التحقق من صحة البيانات
        if not self.validate_data():
            return
        
        # جمع البيانات
        data = self.collect_data()
        
        try:
            if self.follow_up_id:
                # تحديث
                self.update_follow_up(data)
            else:
                # إضافة جديدة
                self.insert_follow_up(data)
            
            messagebox.showinfo("نجح", "تم حفظ المتابعة بنجاح")
            
            # استدعاء callback لتحديث البيانات
            if self.callback:
                self.callback()
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ المتابعة: {e}")
    
    def collect_data(self):
        """جمع البيانات من النموذج"""
        selected = self.correspondence_var.get()
        correspondence_info = self.correspondence_data[selected]
        
        # الحصول على التاريخ
        try:
            if hasattr(self.date_entry, 'get_date'):
                date_value = self.date_entry.get_date().strftime('%Y-%m-%d')
            else:
                date_value = self.date_var.get()
        except:
            date_value = date.today().strftime('%Y-%m-%d')
        
        data = {
            'follow_up_code': self.follow_up_code_var.get(),
            'correspondence_type': self.correspondence_type_var.get(),
            'correspondence_id': correspondence_info['id'],
            'follow_up_date': date_value,
            'action_required': self.action_text.get('1.0', tk.END).strip(),
            'responsible_person': self.responsible_var.get().strip(),
            'status': self.status_var.get(),
            'notes': self.notes_text.get('1.0', tk.END).strip() or None
        }
        
        return data
    
    def insert_follow_up(self, data):
        """إدراج متابعة جديدة"""
        query = '''
            INSERT INTO follow_up 
            (follow_up_code, correspondence_type, correspondence_id, follow_up_date, 
             action_required, responsible_person, status, notes, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            data['follow_up_code'], data['correspondence_type'], data['correspondence_id'],
            data['follow_up_date'], data['action_required'], data['responsible_person'],
            data['status'], data['notes'], self.user_data['id']
        )
        
        result = self.db_manager.execute_update(query, params)
        
        if result:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"إضافة متابعة {data['follow_up_code']}",
                table_name="follow_up",
                record_id=result
            )
    
    def update_follow_up(self, data):
        """تحديث متابعة موجودة"""
        query = '''
            UPDATE follow_up 
            SET follow_up_code=?, correspondence_type=?, correspondence_id=?, 
                follow_up_date=?, action_required=?, responsible_person=?, 
                status=?, notes=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        '''
        params = (
            data['follow_up_code'], data['correspondence_type'], data['correspondence_id'],
            data['follow_up_date'], data['action_required'], data['responsible_person'],
            data['status'], data['notes'], self.follow_up_id
        )
        
        result = self.db_manager.execute_update(query, params)
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"تحديث متابعة {data['follow_up_code']}",
                table_name="follow_up",
                record_id=self.follow_up_id
            )
    
    def load_data(self):
        """تحميل البيانات للتعديل"""
        query = "SELECT * FROM follow_up WHERE id = ?"
        data = self.db_manager.execute_query(query, (self.follow_up_id,))
        
        if data:
            record = dict(data[0])
            
            # تعيين البيانات
            self.follow_up_code_var.set(record['follow_up_code'] or '')
            self.correspondence_type_var.set(record['correspondence_type'])
            
            # تحديث قائمة المراسلات أولاً
            self.refresh_correspondence_list()
            
            # البحث عن المراسلة المرتبطة وتحديدها
            correspondence_id = record['correspondence_id']
            for display_text, info in self.correspondence_data.items():
                if info['id'] == correspondence_id:
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
            
            # تعيين النصوص
            self.action_text.delete('1.0', tk.END)
            self.action_text.insert('1.0', record['action_required'])
            
            self.responsible_var.set(record['responsible_person'] or '')
            self.status_var.set(record['status'])
            
            self.notes_text.delete('1.0', tk.END)
            if record['notes']:
                self.notes_text.insert('1.0', record['notes'])
            
            # تعطيل التعديل إذا كانت مغلقة وليس لديه صلاحية
            if record['status'] == 'مغلق' and not self.auth_manager.has_permission('edit_closed_follow_up'):
                self.disable_form()
    
    def disable_form(self):
        """تعطيل النموذج للمتابعات المغلقة"""
        widgets_to_disable = [
            self.correspondence_combo, self.action_text, self.responsible_entry,
            self.status_combo, self.notes_text
        ]
        
        for widget in widgets_to_disable:
            if hasattr(widget, 'config'):
                widget.config(state='disabled')
        
        # إضافة تنبيه
        warning_label = tk.Label(
            self.window,
            text="⚠️ هذه المتابعة مغلقة - للتعديل يتطلب صلاحيات خاصة",
            font=('Arial Unicode MS', 10, 'bold'),
            fg='red',
            bg='#f8f9fa'
        )
        warning_label.pack(pady=5)
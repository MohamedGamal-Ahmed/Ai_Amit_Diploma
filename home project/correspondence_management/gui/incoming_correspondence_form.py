#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نموذج إضافة/تعديل المراسلات الواردة المحسن
Enhanced Incoming Correspondence Form
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import re

class IncomingCorrespondenceForm:
    def __init__(self, parent, db_manager, auth_manager, user_data, 
                 correspondence_id=None, callback=None, notify=None):
        
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.user_data = user_data
        self.correspondence_id = correspondence_id
        self.callback = callback
        self.notify = notify  # دالة الإشعار الفوري
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        
        # تحميل البيانات للتعديل
        if correspondence_id:
            self.load_data()
        else:
            # تعيين الرقم التلقائي للمراسلة الجديدة
            self.set_auto_reference_number()
    
    def setup_window(self):
        """إعداد النافذة"""
        title = "تعديل مراسلة واردة" if self.correspondence_id else "إضافة مراسلة واردة"
        
        self.window.title(title)
        self.window.geometry("700x800")
        self.window.resizable(False, False)
        self.window.configure(bg='#f8f9fa')
        
        # توسيط النافذة
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (700 // 2)
        y = (self.window.winfo_screenheight() // 2) - (800 // 2)
        self.window.geometry(f"700x800+{x}+{y}")
        
        # جعل النافذة في المقدمة
        self.window.transient(self.window.master)
        self.window.grab_set()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.window, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # العنوان
        title_text = "تعديل مراسلة واردة" if self.correspondence_id else "إضافة مراسلة واردة"
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
        
        # 1. رقم المراسلة (تلقائي)
        self.create_field_label(fields_frame, "رقم المراسلة", 0)
        self.reference_var = tk.StringVar()
        reference_frame = tk.Frame(fields_frame, bg='white')
        reference_frame.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.reference_entry = tk.Entry(
            reference_frame,
            textvariable=self.reference_var,
            font=('Arial Unicode MS', 11),
            state='readonly',
            bg='#f8f9fa',
            fg='#2c3e50',
            justify='center',
            relief='solid',
            bd=1
        )
        self.reference_entry.pack(side='left', fill='x', expand=True)
        
        # زر تجديد الرقم
        refresh_btn = tk.Button(
            reference_frame,
            text="🔄",
            font=('Arial Unicode MS', 10),
            bg='#3498db',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.set_auto_reference_number,
            width=3
        )
        refresh_btn.pack(side='right', padx=(5, 0))
        
        # 2. كود الموضوع (XX-XXXX)
        self.create_field_label(fields_frame, "كود الموضوع", 1)
        subject_code_frame = tk.Frame(fields_frame, bg='white')
        subject_code_frame.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # الجزء الأول (حرفين)
        self.subject_code_part1_var = tk.StringVar()
        self.subject_code_part1_entry = tk.Entry(
            subject_code_frame,
            textvariable=self.subject_code_part1_var,
            font=('Arial Unicode MS', 11),
            width=5,
            justify='center',
            relief='solid',
            bd=1
        )
        self.subject_code_part1_entry.pack(side='left')
        
        # الشرطة
        dash_label = tk.Label(
            subject_code_frame,
            text="-",
            font=('Arial Unicode MS', 14, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        dash_label.pack(side='left', padx=5)
        
        # الجزء الثاني (4 أحرف)
        self.subject_code_part2_var = tk.StringVar()
        self.subject_code_part2_entry = tk.Entry(
            subject_code_frame,
            textvariable=self.subject_code_part2_var,
            font=('Arial Unicode MS', 11),
            width=8,
            justify='center',
            relief='solid',
            bd=1
        )
        self.subject_code_part2_entry.pack(side='left')
        
        # ربط التحقق من الإدخال
        self.subject_code_part1_var.trace('w', self.validate_subject_code_part1)
        self.subject_code_part2_var.trace('w', self.validate_subject_code_part2)
        
        # 3. وارد من (الجهة)
        self.create_field_label(fields_frame, "وارد من (الجهة)", 2)
        self.sender_organization_var = tk.StringVar()
        self.sender_organization_entry = tk.Entry(
            fields_frame,
            textvariable=self.sender_organization_var,
            font=('Arial Unicode MS', 11),
            justify='right',
            relief='solid',
            bd=1
        )
        self.sender_organization_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # 4. وارد من (مهندس/مهندسة)
        self.create_field_label(fields_frame, "وارد من (مهندس/مهندسة)", 3)
        sender_person_frame = tk.Frame(fields_frame, bg='white')
        sender_person_frame.grid(row=3, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # اختيار النوع
        self.sender_title_var = tk.StringVar(value="مهندس")
        title_combo = ttk.Combobox(
            sender_person_frame,
            textvariable=self.sender_title_var,
            values=["مهندس", "مهندسة"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=8
        )
        title_combo.pack(side='right', padx=(5, 0))
        
        # اسم المهندس
        self.sender_person_var = tk.StringVar()
        self.sender_person_entry = tk.Entry(
            sender_person_frame,
            textvariable=self.sender_person_var,
            font=('Arial Unicode MS', 11),
            justify='right',
            relief='solid',
            bd=1
        )
        self.sender_person_entry.pack(side='left', fill='x', expand=True)
        
        # 5. الموضوع
        self.create_field_label(fields_frame, "الموضوع", 4)
        subject_frame = tk.Frame(fields_frame, bg='white')
        subject_frame.grid(row=4, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.subject_text = tk.Text(
            subject_frame,
            height=4,
            font=('Arial Unicode MS', 11),
            wrap='word',
            relief='solid',
            bd=1
        )
        subject_scrollbar = ttk.Scrollbar(subject_frame, orient='vertical', command=self.subject_text.yview)
        self.subject_text.configure(yscrollcommand=subject_scrollbar.set)
        
        self.subject_text.pack(side='left', fill='both', expand=True)
        subject_scrollbar.pack(side='right', fill='y')
        
        # 6. المهندس/ة المسئول عن العرض
        self.create_field_label(fields_frame, "المهندس/ة المسئول عن العرض", 5)
        responsible_frame = tk.Frame(fields_frame, bg='white')
        responsible_frame.grid(row=5, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # اختيار النوع
        self.responsible_title_var = tk.StringVar(value="مهندس")
        responsible_title_combo = ttk.Combobox(
            responsible_frame,
            textvariable=self.responsible_title_var,
            values=["مهندس", "مهندسة"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=8
        )
        responsible_title_combo.pack(side='right', padx=(5, 0))
        
        # اسم المهندس المسئول
        self.responsible_person_var = tk.StringVar()
        self.responsible_person_entry = tk.Entry(
            responsible_frame,
            textvariable=self.responsible_person_var,
            font=('Arial Unicode MS', 11),
            justify='right',
            relief='solid',
            bd=1
        )
        self.responsible_person_entry.pack(side='left', fill='x', expand=True)
        
        # 7. التاريخ
        self.create_field_label(fields_frame, "تاريخ الاستلام", 6)
        
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
            self.date_entry.grid(row=6, column=1, sticky='w', padx=(10, 0), pady=5)
        except ImportError:
            # في حالة عدم توفر tkcalendar
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
            self.date_entry.grid(row=6, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # الأولوية
        self.create_field_label(fields_frame, "الأولوية", 7)
        self.priority_var = tk.StringVar(value="عادي")
        priority_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.priority_var,
            values=["عاجل", "مهم", "عادي"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=15
        )
        priority_combo.grid(row=7, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # الحالة
        self.create_field_label(fields_frame, "الحالة", 8)
        self.status_var = tk.StringVar(value="جديد")
        status_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.status_var,
            values=["جديد", "قيد المراجعة", "تم الرد", "مؤرشف"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=15
        )
        status_combo.grid(row=8, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # ملاحظات
        self.create_field_label(fields_frame, "ملاحظات", 9)
        notes_frame = tk.Frame(fields_frame, bg='white')
        notes_frame.grid(row=9, column=1, sticky='ew', padx=(10, 0), pady=5)
        
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
            text="💾 حفظ المراسلة",
            font=('Arial Unicode MS', 12, 'bold'),
            bg='#27ae60',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.save_correspondence,
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
        
        # زر مسح الحقول
        clear_btn = tk.Button(
            buttons_frame,
            text="🗑️ مسح الحقول",
            font=('Arial Unicode MS', 12),
            bg='#f39c12',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.clear_fields,
            pady=10
        )
        clear_btn.pack(side='right', padx=5)
        
        # التركيز على أول حقل قابل للتعديل
        self.subject_code_part1_entry.focus()
    
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
    
    def set_auto_reference_number(self):
        """تعيين رقم المراسلة تلقائياً"""
        try:
            # الحصول على آخر رقم مراسلة
            query = "SELECT MAX(CAST(reference_number AS INTEGER)) as max_ref FROM incoming_correspondence WHERE reference_number GLOB '[0-9]*'"
            result = self.db_manager.execute_query(query)
            
            if result and result[0]['max_ref']:
                next_number = result[0]['max_ref'] + 1
            else:
                next_number = 1
            
            self.reference_var.set(str(next_number))
            
        except Exception as e:
            # في حالة الخطأ، استخدم التاريخ والوقت
            timestamp = datetime.now().strftime("%Y%m%d%H%M")
            self.reference_var.set(timestamp)
    
    def validate_subject_code_part1(self, *args):
        """التحقق من صحة الجزء الأول من كود الموضوع (حرفين فقط)"""
        value = self.subject_code_part1_var.get()
        if len(value) > 2:
            self.subject_code_part1_var.set(value[:2])
        
        # التحقق من الأحرف الإنجليزية فقط
        if value and not re.match(r'^[A-Za-z]*$', value):
            # إزالة الأحرف غير الإنجليزية
            clean_value = re.sub(r'[^A-Za-z]', '', value)
            self.subject_code_part1_var.set(clean_value[:2])
    
    def validate_subject_code_part2(self, *args):
        """التحقق من صحة الجزء الثاني من كود الموضوع (4 أحرف/أرقام فقط)"""
        value = self.subject_code_part2_var.get()
        if len(value) > 4:
            self.subject_code_part2_var.set(value[:4])
        
        # التحقق من الأحرف والأرقام الإنجليزية فقط
        if value and not re.match(r'^[A-Za-z0-9]*$', value):
            # إزالة الأحرف غير المسموحة
            clean_value = re.sub(r'[^A-Za-z0-9]', '', value)
            self.subject_code_part2_var.set(clean_value[:4])
    
    def get_subject_code(self):
        """الحصول على كود الموضوع الكامل"""
        part1 = self.subject_code_part1_var.get().strip()
        part2 = self.subject_code_part2_var.get().strip()
        
        if part1 and part2:
            return f"{part1}-{part2}"
        return ""
    
    def set_subject_code(self, code):
        """تعيين كود الموضوع"""
        if code and '-' in code:
            parts = code.split('-', 1)
            self.subject_code_part1_var.set(parts[0][:2])
            self.subject_code_part2_var.set(parts[1][:4])
    
    def clear_fields(self):
        """مسح جميع الحقول"""
        if messagebox.askyesno("تأكيد", "هل تريد مسح جميع الحقول؟"):
            # مسح الحقول النصية
            self.subject_code_part1_var.set("")
            self.subject_code_part2_var.set("")
            self.sender_organization_var.set("")
            self.sender_person_var.set("")
            self.responsible_person_var.set("")
            
            # مسح النصوص
            self.subject_text.delete('1.0', tk.END)
            self.notes_text.delete('1.0', tk.END)
            
            # إعادة تعيين القيم الافتراضية
            self.sender_title_var.set("مهندس")
            self.responsible_title_var.set("مهندس")
            self.priority_var.set("عادي")
            self.status_var.set("جديد")
            
            # إعادة تعيين التاريخ
            try:
                if hasattr(self.date_entry, 'set_date'):
                    self.date_entry.set_date(date.today())
                else:
                    self.date_var.set(date.today().strftime('%Y-%m-%d'))
            except:
                pass
            
            # إعادة تعيين رقم المراسلة
            if not self.correspondence_id:
                self.set_auto_reference_number()
    
    def validate_data(self):
        """التحقق من صحة البيانات"""
        # التحقق من الحقول المطلوبة
        if not self.reference_var.get().strip():
            if self.notify:
                self.notify("رقم المراسلة مطلوب", type_="error")
            else:
                messagebox.showerror("خطأ", "رقم المراسلة مطلوب")
            return False
        
        if not self.get_subject_code():
            if self.notify:
                self.notify("كود الموضوع مطلوب (XX-XXXX)", type_="error")
            else:
                messagebox.showerror("خطأ", "كود الموضوع مطلوب (XX-XXXX)")
            self.subject_code_part1_entry.focus()
            return False
        
        if not self.sender_organization_var.get().strip():
            if self.notify:
                self.notify("يرجى إدخال الجهة المرسلة", type_="error")
            else:
                messagebox.showerror("خطأ", "يرجى إدخال الجهة المرسلة")
            self.sender_organization_entry.focus()
            return False
        
        if not self.sender_person_var.get().strip():
            if self.notify:
                self.notify("يرجى إدخال اسم المهندس المرسل", type_="error")
            else:
                messagebox.showerror("خطأ", "يرجى إدخال اسم المهندس المرسل")
            self.sender_person_entry.focus()
            return False
        
        if not self.subject_text.get('1.0', tk.END).strip():
            if self.notify:
                self.notify("يرجى إدخال موضوع المراسلة", type_="error")
            else:
                messagebox.showerror("خطأ", "يرجى إدخال موضوع المراسلة")
            self.subject_text.focus()
            return False
        
        if not self.responsible_person_var.get().strip():
            if self.notify:
                self.notify("يرجى إدخال اسم المهندس المسئول", type_="error")
            else:
                messagebox.showerror("خطأ", "يرجى إدخال اسم المهندس المسئول")
            self.responsible_person_entry.focus()
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
        
        # تكوين اسم المرسل الكامل
        sender_full_name = f"{self.sender_title_var.get()} {self.sender_person_var.get().strip()}"
        
        # تكوين اسم المسئول الكامل
        responsible_full_name = f"{self.responsible_title_var.get()} {self.responsible_person_var.get().strip()}"
        
        data = {
            'reference_number': self.reference_var.get().strip(),
            'subject_code': self.get_subject_code(),
            'sender': sender_full_name,
            'sender_department': self.sender_organization_var.get().strip(),
            'subject': self.subject_text.get('1.0', tk.END).strip(),
            'responsible_person': responsible_full_name,
            'received_date': date_value,
            'priority': self.priority_var.get(),
            'status': self.status_var.get(),
            'notes': self.notes_text.get('1.0', tk.END).strip() or None,
            'content': self.subject_text.get('1.0', tk.END).strip()  # نسخ الموضوع كمحتوى
        }
        
        return data
    
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
            else:
                messagebox.showinfo("نجح", "تم حفظ المراسلة بنجاح")
            
            # استدعاء callback لتحديث البيانات
            if self.callback:
                self.callback()
            
            self.window.destroy()
            
        except Exception as e:
            if self.notify:
                self.notify(f"فشل في حفظ المراسلة: {e}", type_="error")
            else:
                messagebox.showerror("خطأ", f"فشل في حفظ المراسلة: {e}")
    
    def insert_correspondence(self, data):
        """إدراج مراسلة جديدة"""
        query = '''
            INSERT INTO incoming_correspondence 
            (reference_number, subject_code, sender, sender_department, subject, content, 
             responsible_person, received_date, priority, status, notes, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            data['reference_number'], data['subject_code'], data['sender'], data['sender_department'],
            data['subject'], data['content'], data['responsible_person'], data['received_date'],
            data['priority'], data['status'], data['notes'], self.user_data['id']
        )
        
        result = self.db_manager.execute_update(query, params)
        
        if result:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"إضافة مراسلة واردة رقم {data['reference_number']}",
                table_name="incoming_correspondence",
                record_id=result
            )
    
    def update_correspondence(self, data):
        """تحديث مراسلة موجودة"""
        query = '''
            UPDATE incoming_correspondence 
            SET reference_number=?, subject_code=?, sender=?, sender_department=?, subject=?, 
                content=?, responsible_person=?, received_date=?, priority=?, status=?, notes=?,
                updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        '''
        params = (
            data['reference_number'], data['subject_code'], data['sender'], data['sender_department'],
            data['subject'], data['content'], data['responsible_person'], data['received_date'],
            data['priority'], data['status'], data['notes'], self.correspondence_id
        )
        
        result = self.db_manager.execute_update(query, params)
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"تحديث مراسلة واردة رقم {data['reference_number']}",
                table_name="incoming_correspondence",
                record_id=self.correspondence_id
            )
    
    def load_data(self):
        """تحميل البيانات للتعديل"""
        query = "SELECT * FROM incoming_correspondence WHERE id = ?"
        data = self.db_manager.execute_query(query, (self.correspondence_id,))
        
        if data:
            record = dict(data[0])
            
            # تعيين البيانات
            self.reference_var.set(record['reference_number'])
            
            # تعيين كود الموضوع
            if record.get('subject_code'):
                self.set_subject_code(record['subject_code'])
            
            # تحليل اسم المرسل
            sender_parts = record['sender'].split(' ', 1)
            if len(sender_parts) >= 2:
                self.sender_title_var.set(sender_parts[0])
                self.sender_person_var.set(sender_parts[1])
            else:
                self.sender_person_var.set(record['sender'])
            
            self.sender_organization_var.set(record['sender_department'] or '')
            
            # تعيين الموضوع
            self.subject_text.delete('1.0', tk.END)
            self.subject_text.insert('1.0', record['subject'])
            
            # تحليل المسئول (إذا كان موجوداً في البيانات القديمة)
            if 'responsible_person' in record and record['responsible_person']:
                responsible_parts = record['responsible_person'].split(' ', 1)
                if len(responsible_parts) >= 2:
                    self.responsible_title_var.set(responsible_parts[0])
                    self.responsible_person_var.set(responsible_parts[1])
                else:
                    self.responsible_person_var.set(record['responsible_person'])
            
            # تعيين التاريخ
            try:
                if hasattr(self.date_entry, 'set_date'):
                    date_obj = datetime.strptime(record['received_date'], '%Y-%m-%d').date()
                    self.date_entry.set_date(date_obj)
                else:
                    self.date_var.set(record['received_date'])
            except:
                pass
            
            # تعيين باقي الحقول
            self.priority_var.set(record['priority'])
            self.status_var.set(record['status'])
            
            # تعيين الملاحظات
            self.notes_text.delete('1.0', tk.END)
            if record['notes']:
                self.notes_text.insert('1.0', record['notes'])
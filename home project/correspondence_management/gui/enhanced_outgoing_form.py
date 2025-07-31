#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
نموذج المراسلات الصادرة المحسن
Enhanced Outgoing Correspondence Form
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import re

class EnhancedOutgoingForm:
    def __init__(self, parent, db_manager, auth_manager, user_data, 
                 correspondence_id=None, callback=None):
        
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.user_data = user_data
        self.correspondence_id = correspondence_id
        self.callback = callback
        
        # إنشاء النافذة
        self.window = tk.Toplevel(parent)
        self.setup_window()
        self.create_widgets()
        
        # تحميل البيانات للتعديل
        if correspondence_id:
            self.load_data()
        else:
            # توليد رقم المراسلة التلقائي
            self.generate_reference_number()
            self.generate_subject_code()
    
    def setup_window(self):
        """إعداد النافذة"""
        title = "تعديل مراسلة صادرة" if self.correspondence_id else "إضافة مراسلة صادرة جديدة"
        
        self.window.title(title)
        self.window.geometry("800x700")
        self.window.resizable(False, False)
        self.window.configure(bg='#f8f9fa')
        
        # توسيط النافذة
        self.window.update_idletasks()
        x = (self.window.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.window.winfo_screenheight() // 2) - (700 // 2)
        self.window.geometry(f"800x700+{x}+{y}")
        
        # جعل النافذة في المقدمة
        self.window.transient(self.window.master)
        self.window.grab_set()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار الرئيسي
        main_frame = tk.Frame(self.window, bg='#f8f9fa')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # العنوان
        title_text = "تعديل مراسلة صادرة" if self.correspondence_id else "إضافة مراسلة صادرة جديدة"
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
        ref_entry = tk.Entry(
            fields_frame,
            textvariable=self.reference_var,
            font=('Arial Unicode MS', 11),
            state='readonly',
            bg='#f8f9fa',
            fg='#2c3e50',
            justify='center',
            relief='solid',
            bd=1
        )
        ref_entry.grid(row=0, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # 2. كود الموضوع (XXX-XXXX)
        self.create_field_label(fields_frame, "كود الموضوع", 1)
        code_frame = tk.Frame(fields_frame, bg='white')
        code_frame.grid(row=1, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # الجزء الأول من الكود (3 أحرف قبل الشرطة)
        self.code_prefix_var = tk.StringVar(value="OUT")
        prefix_entry = tk.Entry(
            code_frame,
            textvariable=self.code_prefix_var,
            font=('Arial Unicode MS', 11),
            justify='center',
            relief='solid',
            bd=1,
            width=5
        )
        prefix_entry.pack(side='left')
        prefix_entry.bind('<KeyRelease>', self.validate_code_prefix)
        
        # الشرطة
        dash_label = tk.Label(
            code_frame,
            text="-",
            font=('Arial Unicode MS', 12, 'bold'),
            bg='white'
        )
        dash_label.pack(side='left', padx=2)
        
        # الجزء الثاني من الكود (4 أحرف/أرقام بعد الشرطة)
        self.code_suffix_var = tk.StringVar()
        suffix_entry = tk.Entry(
            code_frame,
            textvariable=self.code_suffix_var,
            font=('Arial Unicode MS', 11),
            justify='center',
            relief='solid',
            bd=1,
            width=8
        )
        suffix_entry.pack(side='left')
        suffix_entry.bind('<KeyRelease>', self.validate_code_suffix)
        
        # زر توليد كود تلقائي
        generate_code_btn = tk.Button(
            code_frame,
            text="🔄",
            font=('Arial Unicode MS', 10),
            bg='#3498db',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.generate_subject_code,
            width=3
        )
        generate_code_btn.pack(side='left', padx=(5, 0))
        
        # 3. صادر إلى (الجهة)
        self.create_field_label(fields_frame, "صادر إلى (الجهة)", 2)
        self.recipient_var = tk.StringVar()
        recipient_entry = tk.Entry(
            fields_frame,
            textvariable=self.recipient_var,
            font=('Arial Unicode MS', 11),
            justify='right',
            relief='solid',
            bd=1
        )
        recipient_entry.grid(row=2, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # 4. صادر إلى (مهندس/مهندسة)
        self.create_field_label(fields_frame, "صادر إلى (مهندس/مهندسة)", 3)
        recipient_person_frame = tk.Frame(fields_frame, bg='white')
        recipient_person_frame.grid(row=3, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # اسم المهندس
        self.recipient_engineer_var = tk.StringVar()
        recipient_engineer_entry = tk.Entry(
            recipient_person_frame,
            textvariable=self.recipient_engineer_var,
            font=('Arial Unicode MS', 11),
            justify='right',
            relief='solid',
            bd=1
        )
        recipient_engineer_entry.pack(side='left', fill='x', expand=True)
        
        # اختيار النوع
        self.recipient_title_var = tk.StringVar(value="مهندس")
        recipient_title_combo = ttk.Combobox(
            recipient_person_frame,
            textvariable=self.recipient_title_var,
            values=["مهندس", "مهندسة"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=8
        )
        recipient_title_combo.pack(side='right', padx=(5, 0))
        
        # 5. الموضوع
        self.create_field_label(fields_frame, "الموضوع", 4)
        subject_frame = tk.Frame(fields_frame, bg='white')
        subject_frame.grid(row=4, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.subject_text = tk.Text(
            subject_frame,
            height=3,
            font=('Arial Unicode MS', 11),
            wrap='word',
            relief='solid',
            bd=1
        )
        subject_scrollbar = ttk.Scrollbar(subject_frame, orient='vertical', command=self.subject_text.yview)
        self.subject_text.configure(yscrollcommand=subject_scrollbar.set)
        
        self.subject_text.pack(side='left', fill='both', expand=True)
        subject_scrollbar.pack(side='right', fill='y')
        
        # 6. ربط بموضوع وارد (اختياري)
        self.create_field_label(fields_frame, "ربط بموضوع وارد (اختياري)", 5)
        
        # إطار للقائمة المنسدلة وزر التحديث
        related_frame = tk.Frame(fields_frame, bg='white')
        related_frame.grid(row=5, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        self.related_incoming_var = tk.StringVar()
        self.related_combo = ttk.Combobox(
            related_frame,
            textvariable=self.related_incoming_var,
            state="readonly",
            font=('Arial Unicode MS', 10)
        )
        self.related_combo.pack(side='left', fill='x', expand=True)
        
        # زر تحديث قائمة المراسلات الواردة
        refresh_incoming_btn = tk.Button(
            related_frame,
            text="🔄",
            font=('Arial Unicode MS', 10),
            bg='#3498db',
            fg='white',
            relief='flat',
            bd=0,
            cursor='hand2',
            command=self.refresh_incoming_list,
            width=3
        )
        refresh_incoming_btn.pack(side='right', padx=(5, 0))
        
        # تحديث القائمة عند البدء
        self.refresh_incoming_list()
        
        # 7. المهندس المسئول
        self.create_field_label(fields_frame, "المهندس المسئول", 6)
        responsible_frame = tk.Frame(fields_frame, bg='white')
        responsible_frame.grid(row=6, column=1, sticky='ew', padx=(10, 0), pady=5)
        
        # اسم المهندس المسئول
        self.responsible_engineer_var = tk.StringVar()
        responsible_entry = tk.Entry(
            responsible_frame,
            textvariable=self.responsible_engineer_var,
            font=('Arial Unicode MS', 11),
            justify='right',
            relief='solid',
            bd=1
        )
        responsible_entry.pack(side='left', fill='x', expand=True)
        
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
        
        # 8. تاريخ الإصدار
        self.create_field_label(fields_frame, "تاريخ الإصدار", 7)
        
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
            self.date_entry.grid(row=7, column=1, sticky='w', padx=(10, 0), pady=5)
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
            self.date_entry.grid(row=7, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # 9. الأولوية
        self.create_field_label(fields_frame, "الأولوية", 8)
        self.priority_var = tk.StringVar(value="عادي")
        priority_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.priority_var,
            values=["عاجل", "مهم", "عادي"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=15
        )
        priority_combo.grid(row=8, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # 10. الحالة
        self.create_field_label(fields_frame, "الحالة", 9)
        self.status_var = tk.StringVar(value="مسودة")
        status_combo = ttk.Combobox(
            fields_frame,
            textvariable=self.status_var,
            values=["مسودة", "تم الإرسال", "تم الاستلام", "مؤرشف"],
            state="readonly",
            font=('Arial Unicode MS', 10),
            width=15
        )
        status_combo.grid(row=9, column=1, sticky='w', padx=(10, 0), pady=5)
        
        # 11. ملاحظات
        self.create_field_label(fields_frame, "ملاحظات", 10)
        notes_frame = tk.Frame(fields_frame, bg='white')
        notes_frame.grid(row=10, column=1, sticky='ew', padx=(10, 0), pady=5)
        
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
    
    def generate_reference_number(self):
        """توليد رقم المراسلة التلقائي"""
        try:
            # الحصول على آخر رقم مراسلة
            query = "SELECT MAX(id) as max_id FROM outgoing_correspondence"
            result = self.db_manager.execute_query(query)
            
            next_id = (result[0]['max_id'] + 1) if result and result[0]['max_id'] else 1
            
            # تنسيق الرقم
            reference_number = f"{next_id}"
            self.reference_var.set(reference_number)
            
        except Exception as e:
            print(f"خطأ في توليد رقم المراسلة: {e}")
            self.reference_var.set("1")
    
    def validate_code_prefix(self, event=None):
        """التحقق من صحة الجزء الأول من الكود"""
        prefix = self.code_prefix_var.get().upper()
        
        # تحديث القيمة بالأحرف الكبيرة
        self.code_prefix_var.set(prefix)
        
        # التحقق من الطول (أقصى 3 أحرف)
        if len(prefix) > 3:
            self.code_prefix_var.set(prefix[:3])
            prefix = prefix[:3]
        
        # التحقق من أن جميع الأحرف صحيحة
        if prefix and not re.match(r'^[A-Z]*$', prefix):
            event.widget.config(bg='#ffebee')
        else:
            event.widget.config(bg='white')
    
    def validate_code_suffix(self, event=None):
        """التحقق من صحة الجزء الثاني من الكود"""
        suffix = self.code_suffix_var.get().upper()
        
        # تحديث القيمة بالأحرف الكبيرة
        self.code_suffix_var.set(suffix)
        
        # التحقق من الطول (أقصى 4 أحرف/أرقام)
        if len(suffix) > 4:
            self.code_suffix_var.set(suffix[:4])
            suffix = suffix[:4]
        
        # التحقق من أن جميع الأحرف/الأرقام صحيحة
        if suffix and not re.match(r'^[A-Z0-9]*$', suffix):
            event.widget.config(bg='#ffebee')
        else:
            event.widget.config(bg='white')
    
    def generate_subject_code(self):
        """توليد كود الموضوع التلقائي"""
        try:
            # الحصول على آخر كود موضوع
            query = "SELECT subject_code FROM outgoing_correspondence WHERE subject_code IS NOT NULL ORDER BY id DESC LIMIT 1"
            result = self.db_manager.execute_query(query)
            
            if result and result[0]['subject_code']:
                last_code = result[0]['subject_code']
                # استخراج الرقم من الكود (XXX-XXXX)
                match = re.search(r'([A-Z]{1,3})-([A-Z]{0,3})(\d+)', last_code)
                if match:
                    prefix = match.group(1)  # OUT
                    letters = match.group(2)  # CHR
                    number = int(match.group(3)) + 1
                    new_suffix = f"{letters}{number}"
                else:
                    prefix = "OUT"
                    new_suffix = "CHR1"
            else:
                prefix = "OUT"
                new_suffix = "CHR1"
            
            self.code_prefix_var.set(prefix)
            self.code_suffix_var.set(new_suffix)
            
        except Exception as e:
            print(f"خطأ في توليد كود الموضوع: {e}")
            self.code_prefix_var.set("OUT")
            self.code_suffix_var.set("CHR1")
    

    
    def refresh_incoming_list(self):
        """تحديث قائمة المراسلات الواردة"""
        try:
            query = '''
                SELECT id, reference_number, subject_code, subject
                FROM incoming_correspondence
                ORDER BY received_date DESC
                LIMIT 50
            '''
            
            data = self.db_manager.execute_query(query)
            
            # تحديث القائمة المنسدلة
            incoming_list = [""]  # خيار فارغ للاختياري
            self.incoming_data = {"": None}
            
            for row in data:
                display_text = f"{row['subject_code'] or 'CHR'} - {row['subject'][:40]}..."
                incoming_list.append(display_text)
                self.incoming_data[display_text] = row['id']
            
            self.related_combo['values'] = incoming_list
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تحديث قائمة المراسلات الواردة: {e}")
    
    def validate_data(self):
        """التحقق من صحة البيانات"""
        if not self.reference_var.get().strip():
            messagebox.showerror("خطأ", "رقم المراسلة مطلوب")
            return False
        
        # التحقق من كود الموضوع
        prefix = self.code_prefix_var.get().strip()
        suffix = self.code_suffix_var.get().strip()
        
        if not prefix:
            messagebox.showerror("خطأ", "الجزء الأول من كود الموضوع مطلوب")
            return False
        
        if not suffix:
            messagebox.showerror("خطأ", "الجزء الثاني من كود الموضوع مطلوب")
            return False
        
        # التحقق من تنسيق كود الموضوع
        if not re.match(r'^[A-Z]{1,3}$', prefix):
            messagebox.showerror("خطأ", "الجزء الأول من الكود يجب أن يكون 1-3 أحرف إنجليزية كبيرة")
            return False
        
        if not re.match(r'^[A-Z0-9]{1,4}$', suffix):
            messagebox.showerror("خطأ", "الجزء الثاني من الكود يجب أن يكون 1-4 أحرف أو أرقام")
            return False
        
        if not self.recipient_var.get().strip():
            messagebox.showerror("خطأ", "يرجى إدخال الجهة المرسل إليها")
            return False
        
        if not self.subject_text.get('1.0', tk.END).strip():
            messagebox.showerror("خطأ", "يرجى إدخال موضوع المراسلة")
            self.subject_text.focus()
            return False
        
        if not self.responsible_engineer_var.get().strip():
            messagebox.showerror("خطأ", "يرجى إدخال اسم المهندس المسئول")
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
        
        # الحصول على المراسلة الواردة المرتبطة
        related_incoming_id = None
        selected_related = self.related_incoming_var.get()
        if selected_related and selected_related in self.incoming_data:
            related_incoming_id = self.incoming_data[selected_related]
        
        # تكوين كود الموضوع الكامل
        full_subject_code = f"{self.code_prefix_var.get().strip()}-{self.code_suffix_var.get().strip()}"
        
        # تكوين أسماء المهندسين مع الألقاب
        recipient_engineer_full = ""
        if self.recipient_engineer_var.get().strip():
            recipient_engineer_full = f"{self.recipient_title_var.get()} {self.recipient_engineer_var.get().strip()}"
        
        responsible_engineer_full = ""
        if self.responsible_engineer_var.get().strip():
            responsible_engineer_full = f"{self.responsible_title_var.get()} {self.responsible_engineer_var.get().strip()}"
        
        data = {
            'reference_number': self.reference_var.get().strip(),
            'subject_code': full_subject_code.upper(),
            'subject': self.subject_text.get('1.0', tk.END).strip(),
            'recipient': self.recipient_var.get().strip(),
            'recipient_engineer': recipient_engineer_full or None,
            'engineer': None,  # حقل محذوف
            'responsible_engineer': responsible_engineer_full or None,
            'sent_date': date_value,
            'priority': self.priority_var.get(),
            'status': self.status_var.get(),
            'notes': self.notes_text.get('1.0', tk.END).strip() or None,
            'related_incoming_id': related_incoming_id
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
            
            messagebox.showinfo("نجح", "تم حفظ المراسلة بنجاح")
            
            # استدعاء callback لتحديث البيانات
            if self.callback:
                self.callback()
            
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في حفظ المراسلة: {e}")
    
    def insert_correspondence(self, data):
        """إدراج مراسلة جديدة"""
        query = '''
            INSERT INTO outgoing_correspondence 
            (reference_number, subject_code, subject, recipient, recipient_engineer,
             engineer, responsible_engineer, sent_date, priority, status, notes, related_incoming_id, created_by)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        '''
        params = (
            data['reference_number'], data['subject_code'], data['subject'],
            data['recipient'], data['recipient_engineer'], data['engineer'], data['responsible_engineer'],
            data['sent_date'], data['priority'], data['status'], data['notes'],
            data['related_incoming_id'], self.user_data['id']
        )
        
        result = self.db_manager.execute_update(query, params)
        
        if result:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"إضافة مراسلة صادرة {data['reference_number']}",
                table_name="outgoing_correspondence",
                record_id=result
            )
    
    def update_correspondence(self, data):
        """تحديث مراسلة موجودة"""
        query = '''
            UPDATE outgoing_correspondence 
            SET reference_number=?, subject_code=?, subject=?, recipient=?, recipient_engineer=?,
                engineer=?, responsible_engineer=?, sent_date=?, priority=?, status=?, notes=?, 
                related_incoming_id=?, updated_at=CURRENT_TIMESTAMP
            WHERE id=?
        '''
        params = (
            data['reference_number'], data['subject_code'], data['subject'],
            data['recipient'], data['recipient_engineer'], data['engineer'], data['responsible_engineer'],
            data['sent_date'], data['priority'], data['status'], data['notes'],
            data['related_incoming_id'], self.correspondence_id
        )
        
        result = self.db_manager.execute_update(query, params)
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"تحديث مراسلة صادرة {data['reference_number']}",
                table_name="outgoing_correspondence",
                record_id=self.correspondence_id
            )
    
    def load_data(self):
        """تحميل البيانات للتعديل"""
        query = "SELECT * FROM outgoing_correspondence WHERE id = ?"
        data = self.db_manager.execute_query(query, (self.correspondence_id,))
        
        if data:
            record = dict(data[0])
            
            # تعيين البيانات
            self.reference_var.set(record['reference_number'])
            
            # تقسيم كود الموضوع
            if record['subject_code']:
                parts = record['subject_code'].split('-', 1)
                if len(parts) == 2:
                    self.code_prefix_var.set(parts[0])
                    self.code_suffix_var.set(parts[1])
                else:
                    self.code_prefix_var.set(record['subject_code'])
                    self.code_suffix_var.set('')
            
            self.recipient_var.set(record['recipient'])
            
            # تحليل المهندس المستلم
            if record['recipient_engineer']:
                parts = record['recipient_engineer'].split(' ', 1)
                if len(parts) == 2 and parts[0] in ['مهندس', 'مهندسة']:
                    self.recipient_title_var.set(parts[0])
                    self.recipient_engineer_var.set(parts[1])
                else:
                    self.recipient_engineer_var.set(record['recipient_engineer'])
            

            
            # تحليل المهندس المسئول
            if record['responsible_engineer']:
                parts = record['responsible_engineer'].split(' ', 1)
                if len(parts) == 2 and parts[0] in ['مهندس', 'مهندسة']:
                    self.responsible_title_var.set(parts[0])
                    self.responsible_engineer_var.set(parts[1])
                else:
                    self.responsible_engineer_var.set(record['responsible_engineer'])
            
            # تعيين الموضوع
            self.subject_text.delete('1.0', tk.END)
            self.subject_text.insert('1.0', record['subject'])
            
            # تعيين التاريخ
            try:
                if hasattr(self.date_entry, 'set_date'):
                    date_obj = datetime.strptime(record['sent_date'], '%Y-%m-%d').date()
                    self.date_entry.set_date(date_obj)
                else:
                    self.date_var.set(record['sent_date'])
            except:
                pass
            
            # تعيين الأولوية والحالة
            self.priority_var.set(record['priority'])
            self.status_var.set(record['status'])
            
            # تعيين الملاحظات
            self.notes_text.delete('1.0', tk.END)
            if record['notes']:
                self.notes_text.insert('1.0', record['notes'])
            
            # تعيين المراسلة الواردة المرتبطة
            if record['related_incoming_id']:
                # البحث عن المراسلة الواردة المرتبطة
                for display_text, incoming_id in self.incoming_data.items():
                    if incoming_id == record['related_incoming_id']:
                        self.related_incoming_var.set(display_text)
                        break
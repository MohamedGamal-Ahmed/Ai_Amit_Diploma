#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تبويب المراسلات الصادرة
Outgoing Correspondence Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

class OutgoingTab:
    def __init__(self, parent, db_manager, auth_manager, user_data):
        self.parent = parent
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.user_data = user_data
        
        # إنشاء الإطار الرئيسي
        self.frame = ttk.Frame(parent)
        
        # إعداد الخطوط
        self.font_normal = ('Arial Unicode MS', 10)
        self.font_bold = ('Arial Unicode MS', 10, 'bold')
        
        # إنشاء الواجهة
        self.create_widgets()
        self.refresh_data()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # الإطار العلوي للأزرار والبحث
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.pack(side='right')
        
        if self.auth_manager.has_permission('add_outgoing'):
            add_btn = ttk.Button(
                buttons_frame,
                text="إضافة مراسلة",
                command=self.add_correspondence
            )
            add_btn.pack(side='right', padx=5)
        
        if self.auth_manager.has_permission('edit_outgoing'):
            edit_btn = ttk.Button(
                buttons_frame,
                text="تعديل",
                command=self.edit_correspondence
            )
            edit_btn.pack(side='right', padx=5)
        
        if self.auth_manager.has_permission('delete_outgoing'):
            delete_btn = ttk.Button(
                buttons_frame,
                text="حذف",
                command=self.delete_correspondence
            )
            delete_btn.pack(side='right', padx=5)
        

        
        # إطار البحث
        search_frame = ttk.Frame(top_frame)
        search_frame.pack(side='left', fill='x', expand=True)
        
        ttk.Label(search_frame, text="البحث:").pack(side='right', padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=self.font_normal,
            justify='right'
        )
        search_entry.pack(side='right', padx=5, fill='x', expand=True)
        
        # إطار الجدول
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # إنشاء الجدول
        self.create_table(table_frame)
    
    def create_table(self, parent):
        """إنشاء جدول المراسلات"""
        # تعريف الأعمدة
        columns = (
            'id', 'reference_number', 'subject_code', 'subject', 'recipient', 
            'recipient_engineer', 'responsible_engineer', 'sent_date', 'priority', 'status', 'related'
        )
        
        # إنشاء Treeview
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        
        # تعريف عناوين الأعمدة
        self.tree.heading('id', text='الرقم')
        self.tree.heading('reference_number', text='رقم المراسلة')
        self.tree.heading('subject_code', text='كود الموضوع')
        self.tree.heading('subject', text='الموضوع')
        self.tree.heading('recipient', text='الجهة')
        self.tree.heading('recipient_engineer', text='المهندس المستلم')
        self.tree.heading('responsible_engineer', text='المهندس المسئول')
        self.tree.heading('sent_date', text='تاريخ الإصدار')
        self.tree.heading('priority', text='الأولوية')
        self.tree.heading('status', text='الحالة')
        self.tree.heading('related', text='مرتبطة بواردة')
        
        # تعيين عرض الأعمدة
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('reference_number', width=100, anchor='center')
        self.tree.column('subject_code', width=100, anchor='center')
        self.tree.column('subject', width=200, anchor='e')
        self.tree.column('recipient', width=120, anchor='e')
        self.tree.column('recipient_engineer', width=120, anchor='e')
        self.tree.column('responsible_engineer', width=120, anchor='e')
        self.tree.column('sent_date', width=100, anchor='center')
        self.tree.column('priority', width=70, anchor='center')
        self.tree.column('status', width=80, anchor='center')
        self.tree.column('related', width=70, anchor='center')
        
        # إضافة شريط التمرير
        scrollbar_v = ttk.Scrollbar(parent, orient='vertical', command=self.tree.yview)
        scrollbar_h = ttk.Scrollbar(parent, orient='horizontal', command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_v.set, xscrollcommand=scrollbar_h.set)
        
        # تخطيط الجدول وشريط التمرير
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_v.grid(row=0, column=1, sticky='ns')
        scrollbar_h.grid(row=1, column=0, sticky='ew')
        
        # تكوين الشبكة
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)
        
        # ربط الأحداث
        self.tree.bind('<Double-1>', self.on_double_click)
        self.tree.bind('<Button-3>', self.show_context_menu)
    
    def refresh_data(self):
        """تحديث بيانات الجدول"""
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # جلب البيانات من قاعدة البيانات
        query = '''
            SELECT oc.id, oc.reference_number, oc.subject_code, oc.subject, oc.recipient, 
                   oc.recipient_engineer, oc.responsible_engineer, oc.sent_date, 
                   oc.priority, oc.status, oc.related_incoming_id,
                   ic.subject_code as related_ref
            FROM outgoing_correspondence oc
            LEFT JOIN incoming_correspondence ic ON oc.related_incoming_id = ic.id
            ORDER BY oc.sent_date DESC, oc.id DESC
        '''
        
        data = self.db_manager.execute_query(query)
        
        # إدراج البيانات في الجدول
        for row in data:
            # تلوين الصفوف حسب الأولوية
            tags = []
            if row['priority'] == 'عاجل':
                tags.append('urgent')
            elif row['priority'] == 'مهم':
                tags.append('important')
            
            # تلوين حسب الحالة
            if row['status'] == 'مسودة':
                tags.append('draft')
            elif row['status'] == 'تم الإرسال':
                tags.append('sent')
            elif row['status'] == 'مؤرشف':
                tags.append('archived')
            
            # عرض كود المراسلة المرتبطة
            related_display = row['related_ref'] if row['related_ref'] else '-'
            
            self.tree.insert('', 'end', values=(
                row['id'],
                row['reference_number'],
                row['subject_code'] or '-',
                row['subject'],
                row['recipient'],
                row['recipient_engineer'] or '-',
                row['responsible_engineer'] or '-',
                row['sent_date'],
                row['priority'],
                row['status'],
                related_display
            ), tags=tags)
        
        # تكوين ألوان الصفوف
        self.tree.tag_configure('urgent', background='#ffebee')
        self.tree.tag_configure('important', background='#fff3e0')
        self.tree.tag_configure('draft', background='#f3e5f5')
        self.tree.tag_configure('sent', background='#e8f5e8')
        self.tree.tag_configure('archived', background='#f5f5f5')
    
    def on_search_change(self, *args):
        """البحث في البيانات"""
        search_term = self.search_var.get().strip()
        
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # تحديد الاستعلام حسب وجود نص البحث
        if search_term:
            query = '''
                SELECT oc.id, oc.reference_number, oc.subject, oc.recipient, 
                       oc.recipient_department, oc.sent_date, oc.priority, oc.status, 
                       oc.content, oc.notes, oc.related_incoming_id,
                       ic.reference_number as related_ref
                FROM outgoing_correspondence oc
                LEFT JOIN incoming_correspondence ic ON oc.related_incoming_id = ic.id
                WHERE oc.reference_number LIKE ? OR oc.subject LIKE ? OR oc.recipient LIKE ?
                ORDER BY oc.sent_date DESC, oc.id DESC
            '''
            search_pattern = f'%{search_term}%'
            params = (search_pattern, search_pattern, search_pattern)
        else:
            query = '''
                SELECT oc.id, oc.reference_number, oc.subject, oc.recipient, 
                       oc.recipient_department, oc.sent_date, oc.priority, oc.status, 
                       oc.content, oc.notes, oc.related_incoming_id,
                       ic.reference_number as related_ref
                FROM outgoing_correspondence oc
                LEFT JOIN incoming_correspondence ic ON oc.related_incoming_id = ic.id
                ORDER BY oc.sent_date DESC, oc.id DESC
            '''
            params = None
        
        data = self.db_manager.execute_query(query, params)
        
        # إدراج النتائج
        for row in data:
            tags = []
            if row['priority'] == 'عاجل':
                tags.append('urgent')
            elif row['priority'] == 'مهم':
                tags.append('important')
            
            if row['status'] == 'مسودة':
                tags.append('draft')
            elif row['status'] == 'تم الإرسال':
                tags.append('sent')
            elif row['status'] == 'مؤرشف':
                tags.append('archived')
            
            related_display = row['related_ref'] if row['related_ref'] else '-'
            
            self.tree.insert('', 'end', values=(
                row['id'],
                row['reference_number'],
                row['subject'],
                row['recipient'],
                row['sent_date'],
                row['priority'],
                row['status'],
                related_display
            ), tags=tags)
    
    def on_double_click(self, event):
        """عند النقر المزدوج على صف"""
        self.view_correspondence()
    
    def show_context_menu(self, event):
        """عرض القائمة المنبثقة"""
        if not self.tree.selection():
            return
        
        context_menu = tk.Menu(self.frame, tearoff=0)
        context_menu.add_command(label="عرض", command=self.view_correspondence)
        
        if self.auth_manager.has_permission('edit_outgoing'):
            context_menu.add_command(label="تعديل", command=self.edit_correspondence)
        
        if self.auth_manager.has_permission('add_followup'):
            context_menu.add_command(label="إضافة متابعة", command=self.add_followup)
        
        # خيارات تغيير الحالة
        if self.auth_manager.has_permission('edit_outgoing'):
            context_menu.add_separator()
            status_menu = tk.Menu(context_menu, tearoff=0)
            context_menu.add_cascade(label="تغيير الحالة", menu=status_menu)
            status_menu.add_command(label="مسودة", command=lambda: self.change_status('مسودة'))
            status_menu.add_command(label="تم الإرسال", command=lambda: self.change_status('تم الإرسال'))
            status_menu.add_command(label="تم الاستلام", command=lambda: self.change_status('تم الاستلام'))
            status_menu.add_command(label="مؤرشف", command=lambda: self.change_status('مؤرشف'))
        
        if self.auth_manager.has_permission('delete_outgoing'):
            context_menu.add_separator()
            context_menu.add_command(label="حذف", command=self.delete_correspondence)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def add_correspondence(self):
        """إضافة مراسلة جديدة"""
        try:
            from gui.enhanced_outgoing_form import EnhancedOutgoingForm
            EnhancedOutgoingForm(
                self.frame, 
                self.db_manager, 
                self.auth_manager, 
                self.user_data,
                callback=self.refresh_data
            )
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في فتح نموذج إضافة المراسلة: {e}")
    
    def edit_correspondence(self):
        """تعديل المراسلة المحددة"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مراسلة للتعديل")
            return
        
        item = self.tree.item(selected[0])
        correspondence_id = item['values'][0]
        
        try:
            from gui.enhanced_outgoing_form import EnhancedOutgoingForm
            EnhancedOutgoingForm(
                self.frame, 
                self.db_manager, 
                self.auth_manager, 
                self.user_data,
                correspondence_id=correspondence_id,
                callback=self.refresh_data
            )
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في فتح نموذج تعديل المراسلة: {e}")
    
    def view_correspondence(self):
        """عرض تفاصيل المراسلة"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مراسلة للعرض")
            return
        
        item = self.tree.item(selected[0])
        correspondence_id = item['values'][0]
        
        from gui.correspondence_view import CorrespondenceView
        CorrespondenceView(
            self.frame, 
            self.db_manager, 
            correspondence_type='outgoing',
            correspondence_id=correspondence_id
        )
    
    def delete_correspondence(self):
        """حذف المراسلة المحددة"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مراسلة للحذف")
            return
        
        result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذه المراسلة؟")
        if not result:
            return
        
        item = self.tree.item(selected[0])
        correspondence_id = item['values'][0]
        
        # حذف المراسلة
        query = "DELETE FROM outgoing_correspondence WHERE id = ?"
        result = self.db_manager.execute_update(query, (correspondence_id,))
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"حذف مراسلة صادرة رقم {correspondence_id}",
                table_name="outgoing_correspondence",
                record_id=correspondence_id
            )
            
            messagebox.showinfo("نجح", "تم حذف المراسلة بنجاح")
            self.refresh_data()
        else:
            messagebox.showerror("خطأ", "فشل في حذف المراسلة")
    
    def change_status(self, new_status):
        """تغيير حالة المراسلة"""
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        correspondence_id = item['values'][0]
        
        # تحديث الحالة
        query = "UPDATE outgoing_correspondence SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        result = self.db_manager.execute_update(query, (new_status, correspondence_id))
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"تغيير حالة المراسلة الصادرة رقم {correspondence_id} إلى {new_status}",
                table_name="outgoing_correspondence",
                record_id=correspondence_id
            )
            
            messagebox.showinfo("نجح", f"تم تغيير الحالة إلى {new_status}")
            self.refresh_data()
        else:
            messagebox.showerror("خطأ", "فشل في تغيير الحالة")
    
    def add_followup(self):
        """إضافة متابعة للمراسلة"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مراسلة لإضافة متابعة")
            return
        
        item = self.tree.item(selected[0])
        correspondence_id = item['values'][0]
        
        from gui.followup_form import FollowUpForm
        FollowUpForm(
            self.frame,
            self.db_manager,
            self.auth_manager,
            self.user_data,
            correspondence_type='outgoing',
            correspondence_id=correspondence_id
        )
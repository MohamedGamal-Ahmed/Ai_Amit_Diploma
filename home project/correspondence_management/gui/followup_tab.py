#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تبويب متابعة الموضوعات
Follow-up Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date

class FollowUpTab:
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
        
        if self.auth_manager.has_permission('add_followup'):
            add_btn = ttk.Button(
                buttons_frame,
                text="إضافة متابعة",
                command=self.add_followup
            )
            add_btn.pack(side='right', padx=5)
        
        if self.auth_manager.has_permission('edit_followup'):
            edit_btn = ttk.Button(
                buttons_frame,
                text="تعديل",
                command=self.edit_followup
            )
            edit_btn.pack(side='right', padx=5)
        
        if self.auth_manager.has_permission('delete_followup'):
            delete_btn = ttk.Button(
                buttons_frame,
                text="حذف",
                command=self.delete_followup
            )
            delete_btn.pack(side='right', padx=5)
        

        
        # إطار الفلاتر
        filter_frame = ttk.Frame(top_frame)
        filter_frame.pack(side='left', fill='x', expand=True)
        
        # فلتر الحالة
        ttk.Label(filter_frame, text="الحالة:").pack(side='right', padx=5)
        
        self.status_var = tk.StringVar(value="الكل")
        status_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.status_var,
            values=["الكل", "معلق", "جاري", "مغلق"],
            state="readonly",
            width=15
        )
        status_combo.pack(side='right', padx=5)
        status_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # فلتر النوع
        ttk.Label(filter_frame, text="النوع:").pack(side='right', padx=5)
        
        self.type_var = tk.StringVar(value="الكل")
        type_combo = ttk.Combobox(
            filter_frame,
            textvariable=self.type_var,
            values=["الكل", "واردة", "صادرة"],
            state="readonly",
            width=15
        )
        type_combo.pack(side='right', padx=5)
        type_combo.bind('<<ComboboxSelected>>', self.on_filter_change)
        
        # البحث
        ttk.Label(filter_frame, text="البحث:").pack(side='right', padx=5)
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.on_search_change)
        search_entry = ttk.Entry(
            filter_frame,
            textvariable=self.search_var,
            font=self.font_normal,
            justify='right',
            width=20
        )
        search_entry.pack(side='right', padx=5)
        
        # إطار الجدول
        table_frame = ttk.Frame(self.frame)
        table_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # إنشاء الجدول
        self.create_table(table_frame)
    
    def create_table(self, parent):
        """إنشاء جدول المتابعات"""
        # تعريف الأعمدة
        columns = (
            'id', 'follow_up_code', 'correspondence_type', 'correspondence_ref', 'follow_up_date',
            'action_required', 'responsible_person', 'status', 'notes'
        )
        
        # إنشاء Treeview
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        
        # تعريف عناوين الأعمدة
        self.tree.heading('id', text='الرقم')
        self.tree.heading('follow_up_code', text='كود المتابعة')
        self.tree.heading('correspondence_type', text='النوع')
        self.tree.heading('correspondence_ref', text='رقم المراسلة')
        self.tree.heading('follow_up_date', text='تاريخ المتابعة')
        self.tree.heading('action_required', text='الإجراء المطلوب')
        self.tree.heading('responsible_person', text='المسؤول')
        self.tree.heading('status', text='الحالة')
        self.tree.heading('notes', text='ملاحظات')
        
        # تعيين عرض الأعمدة
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('follow_up_code', width=120, anchor='center')
        self.tree.column('correspondence_type', width=70, anchor='center')
        self.tree.column('correspondence_ref', width=100, anchor='center')
        self.tree.column('follow_up_date', width=100, anchor='center')
        self.tree.column('action_required', width=180, anchor='e')
        self.tree.column('responsible_person', width=100, anchor='e')
        self.tree.column('status', width=80, anchor='center')
        self.tree.column('notes', width=120, anchor='e')
        
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
            SELECT f.id, f.follow_up_code, f.correspondence_type, f.correspondence_id, f.follow_up_date,
                   f.action_required, f.responsible_person, f.status, f.notes,
                   CASE 
                       WHEN f.correspondence_type = 'incoming' THEN ic.reference_number
                       WHEN f.correspondence_type = 'outgoing' THEN oc.reference_number
                   END as correspondence_ref
            FROM follow_up f
            LEFT JOIN incoming_correspondence ic ON f.correspondence_type = 'incoming' AND f.correspondence_id = ic.id
            LEFT JOIN outgoing_correspondence oc ON f.correspondence_type = 'outgoing' AND f.correspondence_id = oc.id
            ORDER BY f.follow_up_date DESC, f.id DESC
        '''
        
        data = self.db_manager.execute_query(query)
        
        # إدراج البيانات في الجدول
        for row in data:
            # تلوين الصفوف حسب الحالة
            tags = []
            if row['status'] == 'معلق':
                tags.append('pending')
            elif row['status'] == 'جاري':
                tags.append('in_progress')
            elif row['status'] == 'مغلق':
                tags.append('closed')
            
            # تحديد لون حسب تاريخ المتابعة
            follow_date = datetime.strptime(row['follow_up_date'], '%Y-%m-%d').date()
            today = date.today()
            
            if follow_date < today and row['status'] in ['معلق', 'جاري']:
                tags.append('overdue')
            elif follow_date == today and row['status'] in ['معلق', 'جاري']:
                tags.append('due_today')
            
            # تحويل نوع المراسلة للعربية
            type_display = 'واردة' if row['correspondence_type'] == 'incoming' else 'صادرة'
            
            self.tree.insert('', 'end', values=(
                row['id'],
                row['follow_up_code'] or '-',
                type_display,
                row['correspondence_ref'] or '-',
                row['follow_up_date'],
                row['action_required'],
                row['responsible_person'] or '-',
                row['status'],
                row['notes'] or '-'
            ), tags=tags)
        
        # تكوين ألوان الصفوف
        self.tree.tag_configure('pending', background='#fff3e0')      # معلق - أصفر فاتح
        self.tree.tag_configure('in_progress', background='#e3f2fd')  # جاري - أزرق فاتح
        self.tree.tag_configure('closed', background='#f5f5f5')       # مغلق - رمادي فاتح
        self.tree.tag_configure('overdue', background='#ffebee')      # متأخر - أحمر فاتح
        self.tree.tag_configure('due_today', background='#f3e5f5')    # اليوم - بنفسجي فاتح
    
    def on_filter_change(self, event=None):
        """تطبيق الفلاتر"""
        self.apply_filters()
    
    def on_search_change(self, *args):
        """البحث في البيانات"""
        self.apply_filters()
    
    def apply_filters(self):
        """تطبيق الفلاتر والبحث"""
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # بناء الاستعلام
        conditions = []
        params = []
        
        # فلتر الحالة
        if self.status_var.get() != "الكل":
            conditions.append("f.status = ?")
            params.append(self.status_var.get())
        
        # فلتر النوع
        if self.type_var.get() != "الكل":
            type_value = 'incoming' if self.type_var.get() == 'واردة' else 'outgoing'
            conditions.append("f.correspondence_type = ?")
            params.append(type_value)
        
        # البحث
        search_term = self.search_var.get().strip()
        if search_term:
            conditions.append("""(
                f.action_required LIKE ? OR 
                f.responsible_person LIKE ? OR 
                f.notes LIKE ? OR
                ic.reference_number LIKE ? OR
                oc.reference_number LIKE ?
            )""")
            search_pattern = f'%{search_term}%'
            params.extend([search_pattern] * 5)
        
        # بناء الاستعلام النهائي
        base_query = '''
            SELECT f.id, f.correspondence_type, f.correspondence_id, f.follow_up_date,
                   f.action_required, f.responsible_person, f.status, f.notes,
                   CASE 
                       WHEN f.correspondence_type = 'incoming' THEN ic.reference_number
                       WHEN f.correspondence_type = 'outgoing' THEN oc.reference_number
                   END as correspondence_ref
            FROM follow_up f
            LEFT JOIN incoming_correspondence ic ON f.correspondence_type = 'incoming' AND f.correspondence_id = ic.id
            LEFT JOIN outgoing_correspondence oc ON f.correspondence_type = 'outgoing' AND f.correspondence_id = oc.id
        '''
        
        if conditions:
            query = base_query + " WHERE " + " AND ".join(conditions)
        else:
            query = base_query
        
        query += " ORDER BY f.follow_up_date DESC, f.id DESC"
        
        data = self.db_manager.execute_query(query, params if params else None)
        
        # إدراج النتائج
        for row in data:
            tags = []
            if row['status'] == 'معلق':
                tags.append('pending')
            elif row['status'] == 'قيد التنفيذ':
                tags.append('in_progress')
            elif row['status'] == 'مكتمل':
                tags.append('completed')
            elif row['status'] == 'ملغي':
                tags.append('cancelled')
            
            follow_date = datetime.strptime(row['follow_up_date'], '%Y-%m-%d').date()
            today = date.today()
            
            if follow_date < today and row['status'] in ['معلق', 'قيد التنفيذ']:
                tags.append('overdue')
            elif follow_date == today and row['status'] in ['معلق', 'قيد التنفيذ']:
                tags.append('due_today')
            
            type_display = 'واردة' if row['correspondence_type'] == 'incoming' else 'صادرة'
            
            self.tree.insert('', 'end', values=(
                row['id'],
                type_display,
                row['correspondence_ref'] or '-',
                row['follow_up_date'],
                row['action_required'],
                row['responsible_person'] or '-',
                row['status'],
                row['notes'] or '-'
            ), tags=tags)
    
    def on_double_click(self, event):
        """عند النقر المزدوج على صف"""
        self.view_followup()
    
    def show_context_menu(self, event):
        """عرض القائمة المنبثقة"""
        if not self.tree.selection():
            return
        
        context_menu = tk.Menu(self.frame, tearoff=0)
        context_menu.add_command(label="عرض", command=self.view_followup)
        
        if self.auth_manager.has_permission('edit_followup'):
            context_menu.add_command(label="تعديل", command=self.edit_followup)
        
        # خيارات تغيير الحالة
        if self.auth_manager.has_permission('edit_followup'):
            context_menu.add_separator()
            status_menu = tk.Menu(context_menu, tearoff=0)
            context_menu.add_cascade(label="تغيير الحالة", menu=status_menu)
            status_menu.add_command(label="معلق", command=lambda: self.change_status('معلق'))
            status_menu.add_command(label="قيد التنفيذ", command=lambda: self.change_status('قيد التنفيذ'))
            status_menu.add_command(label="مكتمل", command=lambda: self.change_status('مكتمل'))
            status_menu.add_command(label="ملغي", command=lambda: self.change_status('ملغي'))
        
        if self.auth_manager.has_permission('delete_followup'):
            context_menu.add_separator()
            context_menu.add_command(label="حذف", command=self.delete_followup)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def add_followup(self):
        """إضافة متابعة جديدة"""
        try:
            from gui.enhanced_follow_up_form import EnhancedFollowUpForm
            EnhancedFollowUpForm(
                self.frame,
                self.db_manager,
                self.auth_manager,
                self.user_data,
                callback=self.refresh_data
            )
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في فتح نموذج إضافة المتابعة: {e}")
    
    def edit_followup(self):
        """تعديل المتابعة المحددة"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار متابعة للتعديل")
            return
        
        item = self.tree.item(selected[0])
        followup_id = item['values'][0]
        
        try:
            from gui.enhanced_follow_up_form import EnhancedFollowUpForm
            EnhancedFollowUpForm(
                self.frame,
                self.db_manager,
                self.auth_manager,
                self.user_data,
                follow_up_id=followup_id,
                callback=self.refresh_data
            )
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في فتح نموذج تعديل المتابعة: {e}")
    
    def view_followup(self):
        """عرض تفاصيل المتابعة"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار متابعة للعرض")
            return
        
        item = self.tree.item(selected[0])
        followup_id = item['values'][0]
        
        from gui.followup_view import FollowUpView
        FollowUpView(
            self.frame,
            self.db_manager,
            followup_id=followup_id
        )
    
    def delete_followup(self):
        """حذف المتابعة المحددة"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار متابعة للحذف")
            return
        
        result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذه المتابعة؟")
        if not result:
            return
        
        item = self.tree.item(selected[0])
        followup_id = item['values'][0]
        
        # حذف المتابعة
        query = "DELETE FROM follow_up WHERE id = ?"
        result = self.db_manager.execute_update(query, (followup_id,))
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"حذف متابعة رقم {followup_id}",
                table_name="follow_up",
                record_id=followup_id
            )
            
            messagebox.showinfo("نجح", "تم حذف المتابعة بنجاح")
            self.refresh_data()
        else:
            messagebox.showerror("خطأ", "فشل في حذف المتابعة")
    
    def change_status(self, new_status):
        """تغيير حالة المتابعة"""
        selected = self.tree.selection()
        if not selected:
            return
        
        item = self.tree.item(selected[0])
        followup_id = item['values'][0]
        
        # تحديث الحالة
        query = "UPDATE follow_up SET status = ?, updated_at = CURRENT_TIMESTAMP WHERE id = ?"
        result = self.db_manager.execute_update(query, (new_status, followup_id))
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.user_data['id'],
                action=f"تغيير حالة المتابعة رقم {followup_id} إلى {new_status}",
                table_name="follow_up",
                record_id=followup_id
            )
            
            messagebox.showinfo("نجح", f"تم تغيير الحالة إلى {new_status}")
            self.refresh_data()
        else:
            messagebox.showerror("خطأ", "فشل في تغيير الحالة")
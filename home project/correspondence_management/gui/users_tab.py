#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تبويب إدارة المستخدمين
Users Management Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox

class UsersTab:
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
        # الإطار العلوي للأزرار
        top_frame = ttk.Frame(self.frame)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        # أزرار العمليات
        buttons_frame = ttk.Frame(top_frame)
        buttons_frame.pack(side='right')
        
        add_btn = ttk.Button(
            buttons_frame,
            text="إضافة مستخدم",
            command=self.add_user
        )
        add_btn.pack(side='right', padx=5)
        
        edit_btn = ttk.Button(
            buttons_frame,
            text="تعديل",
            command=self.edit_user
        )
        edit_btn.pack(side='right', padx=5)
        
        details_btn = ttk.Button(
            buttons_frame,
            text="تفاصيل المستخدم",
            command=self.show_user_details
        )
        details_btn.pack(side='right', padx=5)
        
        delete_btn = ttk.Button(
            buttons_frame,
            text="تعطيل",
            command=self.disable_user
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
        """إنشاء جدول المستخدمين"""
        # تعريف الأعمدة
        columns = (
            'id', 'username', 'full_name', 'role', 
            'department', 'is_active', 'created_at'
        )
        
        # إنشاء Treeview
        self.tree = ttk.Treeview(parent, columns=columns, show='headings', height=20)
        
        # تعريف عناوين الأعمدة
        self.tree.heading('id', text='الرقم')
        self.tree.heading('username', text='اسم المستخدم')
        self.tree.heading('full_name', text='الاسم الكامل')
        self.tree.heading('role', text='الصلاحية')
        self.tree.heading('department', text='القسم')
        self.tree.heading('is_active', text='نشط')
        self.tree.heading('created_at', text='تاريخ الإنشاء')
        
        # تعيين عرض الأعمدة
        self.tree.column('id', width=50, anchor='center')
        self.tree.column('username', width=120, anchor='center')
        self.tree.column('full_name', width=200, anchor='e')
        self.tree.column('role', width=100, anchor='center')
        self.tree.column('department', width=150, anchor='e')
        self.tree.column('is_active', width=80, anchor='center')
        self.tree.column('created_at', width=150, anchor='center')
        
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
        users = self.auth_manager.get_all_users()
        
        # إدراج البيانات في الجدول
        for user in users:
            # تلوين الصفوف حسب الحالة
            tags = []
            if not user['is_active']:
                tags.append('inactive')
            elif user['role'] == 'admin':
                tags.append('admin')
            
            # تحويل الصلاحية للعربية
            role_names = {
                'admin': 'مدير',
                'employee': 'موظف',
                'viewer': 'مشاهد'
            }
            role_display = role_names.get(user['role'], user['role'])
            
            # تحويل الحالة للعربية
            status_display = 'نشط' if user['is_active'] else 'معطل'
            
            self.tree.insert('', 'end', values=(
                user['id'],
                user['username'],
                user['full_name'],
                role_display,
                user['department'] or '-',
                status_display,
                user['created_at'][:16] if user['created_at'] else '-'
            ), tags=tags)
        
        # تكوين ألوان الصفوف
        self.tree.tag_configure('inactive', background='#f5f5f5', foreground='#999999')
        self.tree.tag_configure('admin', background='#e8f5e8')
    
    def on_search_change(self, *args):
        """البحث في البيانات"""
        search_term = self.search_var.get().strip()
        
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # جلب جميع المستخدمين
        users = self.auth_manager.get_all_users()
        
        # فلترة النتائج
        if search_term:
            filtered_users = []
            for user in users:
                if (search_term.lower() in user['username'].lower() or
                    search_term.lower() in user['full_name'].lower() or
                    (user['department'] and search_term.lower() in user['department'].lower())):
                    filtered_users.append(user)
            users = filtered_users
        
        # إدراج النتائج
        for user in users:
            tags = []
            if not user['is_active']:
                tags.append('inactive')
            elif user['role'] == 'admin':
                tags.append('admin')
            
            role_names = {
                'admin': 'مدير',
                'employee': 'موظف',
                'viewer': 'مشاهد'
            }
            role_display = role_names.get(user['role'], user['role'])
            status_display = 'نشط' if user['is_active'] else 'معطل'
            
            self.tree.insert('', 'end', values=(
                user['id'],
                user['username'],
                user['full_name'],
                role_display,
                user['department'] or '-',
                status_display,
                user['created_at'][:16] if user['created_at'] else '-'
            ), tags=tags)
    
    def on_double_click(self, event):
        """عند النقر المزدوج على صف"""
        self.edit_user()
    
    def show_context_menu(self, event):
        """عرض القائمة المنبثقة"""
        if not self.tree.selection():
            return
        
        context_menu = tk.Menu(self.frame, tearoff=0)
        context_menu.add_command(label="تعديل", command=self.edit_user)
        context_menu.add_command(label="تغيير كلمة المرور", command=self.change_password)
        context_menu.add_separator()
        
        # التحقق من حالة المستخدم
        selected_item = self.tree.item(self.tree.selection()[0])
        is_active = selected_item['values'][5] == 'نشط'
        
        if is_active:
            context_menu.add_command(label="تعطيل", command=self.disable_user)
        else:
            context_menu.add_command(label="تفعيل", command=self.enable_user)
        
        context_menu.add_separator()
        context_menu.add_command(label="عرض سجل النشاطات", command=self.view_user_activity)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()
    
    def add_user(self):
        """إضافة مستخدم جديد"""
        from gui.user_form import UserForm
        UserForm(
            self.frame,
            self.db_manager,
            self.auth_manager,
            self.user_data,
            callback=self.refresh_data,
            notify=getattr(self.parent, 'show_notification', None)
        )
    
    def edit_user(self):
        """تعديل المستخدم المحدد"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مستخدم للتعديل")
            return
        
        item = self.tree.item(selected[0])
        user_id = item['values'][0]
        
        from gui.user_form import UserForm
        UserForm(
            self.frame,
            self.db_manager,
            self.auth_manager,
            self.user_data,
            user_id=user_id,
            callback=self.refresh_data,
            notify=getattr(self.parent, 'show_notification', None)
        )
    
    def disable_user(self):
        """تعطيل المستخدم المحدد"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مستخدم للتعطيل")
            return
        
        item = self.tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        # التحقق من عدم تعطيل المستخدم الحالي
        if user_id == self.user_data['id']:
            messagebox.showerror("خطأ", "لا يمكن تعطيل المستخدم الحالي")
            return
        
        result = messagebox.askyesno("تأكيد التعطيل", f"هل أنت متأكد من تعطيل المستخدم {username}؟")
        if not result:
            return
        
        # تعطيل المستخدم
        if self.auth_manager.update_user(user_id, is_active=False):
            messagebox.showinfo("نجح", "تم تعطيل المستخدم بنجاح")
            self.refresh_data()
        else:
            messagebox.showerror("خطأ", "فشل في تعطيل المستخدم")
    
    def enable_user(self):
        """تفعيل المستخدم المحدد"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مستخدم للتفعيل")
            return
        
        item = self.tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        result = messagebox.askyesno("تأكيد التفعيل", f"هل أنت متأكد من تفعيل المستخدم {username}؟")
        if not result:
            return
        
        # تفعيل المستخدم
        if self.auth_manager.update_user(user_id, is_active=True):
            messagebox.showinfo("نجح", "تم تفعيل المستخدم بنجاح")
            self.refresh_data()
        else:
            messagebox.showerror("خطأ", "فشل في تفعيل المستخدم")
    
    def change_password(self):
        """تغيير كلمة مرور المستخدم"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مستخدم لتغيير كلمة المرور")
            return
        
        item = self.tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        from gui.change_password_dialog import ChangePasswordDialog
        ChangePasswordDialog(
            self.frame,
            self.auth_manager,
            user_id,
            username
        )

    def show_user_details(self):
        """عرض تفاصيل المستخدم في نافذة منبثقة"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تنبيه", "يرجى اختيار مستخدم لعرض التفاصيل")
            return
        item = self.tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]
        full_name = item['values'][2]
        role = item['values'][3]
        department = item['values'][4]
        status = item['values'][5]
        created_at = item['values'][6]
        # نافذة منبثقة عصرية
        win = tk.Toplevel(self.frame)
        win.title(f"تفاصيل المستخدم: {username}")
        win.geometry("400x350")
        win.configure(bg="#f8f9fa")
        # بطاقة بيانات
        card = tk.Frame(win, bg="#3498db", bd=0, relief='ridge', highlightthickness=0)
        card.pack(fill='both', expand=True, padx=30, pady=30)
        icon_label = tk.Label(card, text="👤", font=('Arial Unicode MS', 40), bg="#3498db", fg='white')
        icon_label.pack(pady=(20, 5))
        name_label = tk.Label(card, text=full_name, font=('Arial Unicode MS', 18, 'bold'), bg="#3498db", fg='white')
        name_label.pack(pady=(0, 5))
        user_label = tk.Label(card, text=f"اسم المستخدم: {username}", font=('Arial Unicode MS', 12), bg="#3498db", fg='white')
        user_label.pack(pady=(0, 5))
        role_label = tk.Label(card, text=f"الصلاحية: {role}", font=('Arial Unicode MS', 12), bg="#3498db", fg='white')
        role_label.pack(pady=(0, 5))
        dept_label = tk.Label(card, text=f"القسم: {department}", font=('Arial Unicode MS', 12), bg="#3498db", fg='white')
        dept_label.pack(pady=(0, 5))
        status_label = tk.Label(card, text=f"الحالة: {status}", font=('Arial Unicode MS', 12), bg="#3498db", fg='white')
        status_label.pack(pady=(0, 5))
        created_label = tk.Label(card, text=f"تاريخ الإنشاء: {created_at}", font=('Arial Unicode MS', 12), bg="#3498db", fg='white')
        created_label.pack(pady=(0, 20))
        close_btn = ttk.Button(win, text="إغلاق", command=win.destroy)
        close_btn.pack(pady=(0, 10))

    def view_user_activity(self):
        """عرض سجل نشاطات المستخدم"""
        selected = self.tree.selection()
        if not selected:
            messagebox.showwarning("تحذير", "يرجى اختيار مستخدم لعرض سجل النشاطات")
            return
        
        item = self.tree.item(selected[0])
        user_id = item['values'][0]
        username = item['values'][1]
        
        from gui.user_activity_window import UserActivityWindow
        UserActivityWindow(
            self.frame,
            self.db_manager,
            self.auth_manager,
            user_id,
            username
        )
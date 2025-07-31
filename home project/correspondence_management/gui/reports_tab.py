#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تبويب التقارير
Reports Tab
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date, timedelta
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from collections import defaultdict

# تعيين الخط العربي لـ matplotlib
plt.rcParams['font.family'] = ['Arial Unicode MS', 'Tahoma', 'DejaVu Sans']

class ReportsTab:
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
        self.font_large = ('Arial Unicode MS', 12, 'bold')
        
        # إنشاء الواجهة
        self.create_widgets()
        self.refresh_data()
    
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        # إنشاء notebook للتقارير المختلفة
        self.reports_notebook = ttk.Notebook(self.frame)
        self.reports_notebook.pack(fill='both', expand=True, padx=10, pady=10)
        
        # تبويب الإحصائيات العامة
        self.create_statistics_tab()
        
        # تبويب التقارير الشهرية
        self.create_monthly_reports_tab()
        
        # تبويب تقارير المتابعة
        self.create_followup_reports_tab()
        
        # تبويب الرسوم البيانية
        self.create_charts_tab()
    
    def create_statistics_tab(self):
        """إنشاء تبويب الإحصائيات العامة"""
        stats_frame = ttk.Frame(self.reports_notebook)
        self.reports_notebook.add(stats_frame, text="الإحصائيات العامة")
        
        # إطار العلوي للأزرار
        top_frame = ttk.Frame(stats_frame)
        top_frame.pack(fill='x', padx=10, pady=10)
        
        refresh_btn = ttk.Button(
            top_frame,
            text="تحديث الإحصائيات",
            command=self.refresh_statistics
        )
        refresh_btn.pack(side='right')
        
        export_btn = ttk.Button(
            top_frame,
            text="تصدير التقرير",
            command=self.export_statistics_report
        )
        export_btn.pack(side='right', padx=5)
        
        # إطار الإحصائيات
        self.stats_frame = ttk.Frame(stats_frame)
        self.stats_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
        
        # إنشاء بطاقات الإحصائيات
        self.create_statistics_cards()
    
    def create_statistics_cards(self):
        """إنشاء بطاقات إحصائيات عصرية"""
        # مسح المحتوى السابق
        for widget in self.stats_frame.winfo_children():
            widget.destroy()

        # تصميم عصري: بطاقات كبيرة مع أيقونات وألوان واضحة
        card_data = [
            ("المراسلات الواردة", self.get_incoming_count(), "#3498db", "📥"),
            ("المراسلات الصادرة", self.get_outgoing_count(), "#2ecc71", "📤"),
            ("المتابعات المعلقة", self.get_pending_followups_count(), "#e67e22", "⏳"),
            ("المراسلات الجديدة", self.get_new_incoming_count(), "#f39c12", "🆕"),
            ("واردة هذا الشهر", self.get_monthly_incoming_count(datetime.now().strftime('%Y-%m')), "#9b59b6", "🗓️"),
            ("صادرة هذا الشهر", self.get_monthly_outgoing_count(datetime.now().strftime('%Y-%m')), "#1abc9c", "🗓️"),
            ("متابعات مكتملة", self.get_completed_followups_count(), "#27ae60", "✅"),
            ("متابعات جارية", self.get_ongoing_followups_count(), "#3498db", "🔄"),
            ("مراسلات مؤرشفة", self.get_archived_count(), "#95a5a6", "🗄️"),
        ]

        cards_frame = tk.Frame(self.stats_frame, bg="#f8f9fa")
        cards_frame.pack(fill='x', pady=20)

        for i, (title, value, color, icon) in enumerate(card_data):
            card = tk.Frame(cards_frame, bg=color, bd=0, relief='ridge', highlightthickness=0)
            card.grid(row=0, column=i, padx=12, ipadx=10, sticky='nsew')
            cards_frame.grid_columnconfigure(i, weight=1)

            icon_label = tk.Label(card, text=icon, font=('Arial Unicode MS', 32), bg=color, fg='white')
            icon_label.pack(pady=(10, 0))
            value_label = tk.Label(card, text=str(value), font=('Arial Unicode MS', 28, 'bold'), bg=color, fg='white')
            value_label.pack(pady=(0, 0))
            title_label = tk.Label(card, text=title, font=('Arial Unicode MS', 12, 'bold'), bg=color, fg='white')
            title_label.pack(pady=(0, 10))

        # جدول التفاصيل (تصميم مبسط)
        self.create_details_table()
    
    def create_stat_card(self, parent, title, value, color, row, col):
        """إنشاء بطاقة إحصائية"""
        card_frame = tk.Frame(parent, bg=color, relief='raised', bd=2)
        card_frame.grid(row=row, column=col, padx=10, pady=5, sticky='ew')
        
        # تكوين الأعمدة
        parent.grid_columnconfigure(col, weight=1)
        
        # العنوان
        title_label = tk.Label(
            card_frame,
            text=title,
            font=self.font_bold,
            fg='white',
            bg=color
        )
        title_label.pack(pady=(10, 5))
        
        # القيمة
        value_label = tk.Label(
            card_frame,
            text=str(value),
            font=('Arial Unicode MS', 24, 'bold'),
            fg='white',
            bg=color
        )
        value_label.pack(pady=(0, 10))
    
    def create_details_table(self):
        """إنشاء جدول التفاصيل"""
        # إطار الجدول
        table_frame = ttk.LabelFrame(self.stats_frame, text="تفاصيل الإحصائيات")
        table_frame.pack(fill='both', expand=True, pady=20)
        
        # إنشاء الجدول
        columns = ('category', 'total', 'this_month', 'percentage')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=10)
        
        # تعريف العناوين
        tree.heading('category', text='الفئة')
        tree.heading('total', text='الإجمالي')
        tree.heading('this_month', text='هذا الشهر')
        tree.heading('percentage', text='النسبة المئوية')
        
        # تعيين عرض الأعمدة
        tree.column('category', width=200, anchor='e')
        tree.column('total', width=100, anchor='center')
        tree.column('this_month', width=100, anchor='center')
        tree.column('percentage', width=120, anchor='center')
        
        # إضافة البيانات
        current_month = datetime.now().strftime('%Y-%m')
        
        data = [
            ('المراسلات الواردة', self.get_incoming_count(), self.get_monthly_incoming_count(current_month)),
            ('المراسلات الصادرة', self.get_outgoing_count(), self.get_monthly_outgoing_count(current_month)),
            ('المتابعات المعلقة', self.get_pending_followups_count(), 0),
            ('المتابعات الجارية', self.get_ongoing_followups_count(), 0),
            ('المتابعات المكتملة', self.get_completed_followups_count(), 0),
        ]
        
        for category, total, monthly in data:
            percentage = f"{(monthly/total*100):.1f}%" if total > 0 else "0%"
            tree.insert('', 'end', values=(category, total, monthly, percentage))
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # التخطيط
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def create_monthly_reports_tab(self):
        """إنشاء تبويب التقارير الشهرية"""
        monthly_frame = ttk.Frame(self.reports_notebook)
        self.reports_notebook.add(monthly_frame, text="التقارير الشهرية")
        
        # إطار التحكم
        control_frame = ttk.Frame(monthly_frame)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # اختيار الشهر والسنة
        ttk.Label(control_frame, text="السنة:").pack(side='right', padx=5)
        
        self.year_var = tk.StringVar(value=str(datetime.now().year))
        year_combo = ttk.Combobox(
            control_frame,
            textvariable=self.year_var,
            values=[str(y) for y in range(2020, 2030)],
            state="readonly",
            width=10
        )
        year_combo.pack(side='right', padx=5)
        
        ttk.Label(control_frame, text="الشهر:").pack(side='right', padx=5)
        
        months = [
            "01", "02", "03", "04", "05", "06",
            "07", "08", "09", "10", "11", "12"
        ]
        
        self.month_var = tk.StringVar(value=f"{datetime.now().month:02d}")
        month_combo = ttk.Combobox(
            control_frame,
            textvariable=self.month_var,
            values=months,
            state="readonly",
            width=10
        )
        month_combo.pack(side='right', padx=5)
        
        # زر إنشاء التقرير
        generate_btn = ttk.Button(
            control_frame,
            text="إنشاء التقرير",
            command=self.generate_monthly_report
        )
        generate_btn.pack(side='right', padx=10)
        
        # إطار التقرير
        self.monthly_report_frame = ttk.Frame(monthly_frame)
        self.monthly_report_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    
    def create_followup_reports_tab(self):
        """إنشاء تبويب تقارير المتابعة"""
        followup_frame = ttk.Frame(self.reports_notebook)
        self.reports_notebook.add(followup_frame, text="تقارير المتابعة")
        
        # إطار التحكم
        control_frame = ttk.Frame(followup_frame)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # فلتر الحالة
        ttk.Label(control_frame, text="الحالة:").pack(side='right', padx=5)
        
        self.followup_status_var = tk.StringVar(value="الكل")
        status_combo = ttk.Combobox(
            control_frame,
            textvariable=self.followup_status_var,
            values=["الكل", "معلق", "قيد التنفيذ", "مكتمل", "ملغي"],
            state="readonly"
        )
        status_combo.pack(side='right', padx=5)
        
        # زر إنشاء التقرير
        generate_btn = ttk.Button(
            control_frame,
            text="إنشاء تقرير المتابعة",
            command=self.generate_followup_report
        )
        generate_btn.pack(side='right', padx=10)
        
        # زر تقرير الموضوعات المغلقة والجارية
        status_report_btn = ttk.Button(
            control_frame,
            text="تقرير الموضوعات المغلقة والجارية",
            command=self.generate_status_report
        )
        status_report_btn.pack(side='right', padx=5)
        
        # إطار التقرير
        self.followup_report_frame = ttk.Frame(followup_frame)
        self.followup_report_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    
    def create_charts_tab(self):
        """إنشاء تبويب الرسوم البيانية"""
        charts_frame = ttk.Frame(self.reports_notebook)
        self.reports_notebook.add(charts_frame, text="الرسوم البيانية")
        
        # إطار التحكم
        control_frame = ttk.Frame(charts_frame)
        control_frame.pack(fill='x', padx=10, pady=10)
        
        # نوع الرسم البياني
        ttk.Label(control_frame, text="نوع الرسم:").pack(side='right', padx=5)
        
        self.chart_type_var = tk.StringVar(value="شهري")
        chart_combo = ttk.Combobox(
            control_frame,
            textvariable=self.chart_type_var,
            values=["شهري", "حسب الحالة", "حسب الأولوية"],
            state="readonly"
        )
        chart_combo.pack(side='right', padx=5)
        
        # زر إنشاء الرسم
        generate_btn = ttk.Button(
            control_frame,
            text="إنشاء الرسم البياني",
            command=self.generate_chart
        )
        generate_btn.pack(side='right', padx=10)
        
        # إطار الرسم البياني
        self.chart_frame = ttk.Frame(charts_frame)
        self.chart_frame.pack(fill='both', expand=True, padx=10, pady=(0, 10))
    
    def refresh_data(self):
        """تحديث البيانات"""
        self.refresh_statistics()
    
    def refresh_statistics(self):
        """تحديث الإحصائيات"""
        self.create_statistics_cards()
    
    # دوال الحصول على الإحصائيات
    def get_incoming_count(self):
        """عدد المراسلات الواردة"""
        result = self.db_manager.execute_query("SELECT COUNT(*) as count FROM incoming_correspondence")
        return result[0]['count'] if result else 0
    
    def get_outgoing_count(self):
        """عدد المراسلات الصادرة"""
        result = self.db_manager.execute_query("SELECT COUNT(*) as count FROM outgoing_correspondence")
        return result[0]['count'] if result else 0
    
    def get_pending_followups_count(self):
        """عدد المتابعات المعلقة"""
        result = self.db_manager.execute_query("SELECT COUNT(*) as count FROM follow_up WHERE status = 'معلق'")
        return result[0]['count'] if result else 0
    
    def get_new_incoming_count(self):
        """عدد المراسلات الواردة الجديدة"""
        result = self.db_manager.execute_query("SELECT COUNT(*) as count FROM incoming_correspondence WHERE status = 'جديد'")
        return result[0]['count'] if result else 0
    
    def get_completed_followups_count(self):
        """عدد المتابعات المكتملة"""
        result = self.db_manager.execute_query("SELECT COUNT(*) as count FROM follow_up WHERE status = 'مكتمل'")
        return result[0]['count'] if result else 0
    
    def get_archived_count(self):
        """عدد المراسلات المؤرشفة"""
        incoming = self.db_manager.execute_query("SELECT COUNT(*) as count FROM incoming_correspondence WHERE status = 'مؤرشف'")
        outgoing = self.db_manager.execute_query("SELECT COUNT(*) as count FROM outgoing_correspondence WHERE status = 'مؤرشف'")
        return (incoming[0]['count'] if incoming else 0) + (outgoing[0]['count'] if outgoing else 0)
    
    def get_monthly_incoming_count(self, month):
        """عدد المراسلات الواردة في شهر معين"""
        result = self.db_manager.execute_query(
            "SELECT COUNT(*) as count FROM incoming_correspondence WHERE strftime('%Y-%m', received_date) = ?",
            (month,)
        )
        return result[0]['count'] if result else 0
    
    def get_monthly_outgoing_count(self, month):
        """عدد المراسلات الصادرة في شهر معين"""
        result = self.db_manager.execute_query(
            "SELECT COUNT(*) as count FROM outgoing_correspondence WHERE strftime('%Y-%m', sent_date) = ?",
            (month,)
        )
        return result[0]['count'] if result else 0
    
    def generate_monthly_report(self):
        """إنشاء التقرير الشهري"""
        # مسح المحتوى السابق
        for widget in self.monthly_report_frame.winfo_children():
            widget.destroy()
        
        year = self.year_var.get()
        month = self.month_var.get()
        period = f"{year}-{month}"
        
        # عنوان التقرير
        title_label = tk.Label(
            self.monthly_report_frame,
            text=f"التقرير الشهري - {year}/{month}",
            font=self.font_large,
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # إحصائيات الشهر
        stats_frame = ttk.LabelFrame(self.monthly_report_frame, text="إحصائيات الشهر")
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        incoming_count = self.get_monthly_incoming_count(period)
        outgoing_count = self.get_monthly_outgoing_count(period)
        
        stats_text = f"""
المراسلات الواردة: {incoming_count}
المراسلات الصادرة: {outgoing_count}
إجمالي المراسلات: {incoming_count + outgoing_count}
        """
        
        stats_label = tk.Label(
            stats_frame,
            text=stats_text,
            font=self.font_normal,
            justify='right'
        )
        stats_label.pack(pady=10)
        
        # جدول تفصيلي
        self.create_monthly_details_table(period)
    
    def create_monthly_details_table(self, period):
        """إنشاء جدول تفاصيل الشهر"""
        table_frame = ttk.LabelFrame(self.monthly_report_frame, text="التفاصيل")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # إنشاء الجدول
        columns = ('type', 'reference', 'subject', 'date', 'status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # تعريف العناوين
        tree.heading('type', text='النوع')
        tree.heading('reference', text='رقم المراسلة')
        tree.heading('subject', text='الموضوع')
        tree.heading('date', text='التاريخ')
        tree.heading('status', text='الحالة')
        
        # تعيين عرض الأعمدة
        tree.column('type', width=80, anchor='center')
        tree.column('reference', width=120, anchor='center')
        tree.column('subject', width=300, anchor='e')
        tree.column('date', width=100, anchor='center')
        tree.column('status', width=100, anchor='center')
        
        # جلب البيانات
        # المراسلات الواردة
        incoming_query = """
            SELECT 'واردة' as type, reference_number, subject, received_date as date, status
            FROM incoming_correspondence
            WHERE strftime('%Y-%m', received_date) = ?
            ORDER BY received_date DESC
        """
        incoming_data = self.db_manager.execute_query(incoming_query, (period,))
        
        # المراسلات الصادرة
        outgoing_query = """
            SELECT 'صادرة' as type, reference_number, subject, sent_date as date, status
            FROM outgoing_correspondence
            WHERE strftime('%Y-%m', sent_date) = ?
            ORDER BY sent_date DESC
        """
        outgoing_data = self.db_manager.execute_query(outgoing_query, (period,))
        
        # دمج البيانات وإدراجها
        all_data = list(incoming_data) + list(outgoing_data)
        
        # تعريف ألوان الحالات
        tree.tag_configure('مغلق', background='#e8f8e8')      # أخضر فاتح
        tree.tag_configure('معلق', background='#fff6e0')      # برتقالي فاتح
        tree.tag_configure('متأخر', background='#fae8e8')     # أحمر فاتح
        tree.tag_configure('default', background='#f8f8f8')   # رمادي فاتح

        for row in all_data:
            status = row['status']
            # تحديد إذا كان متأخر
            from datetime import datetime, timedelta
            overdue = False
            try:
                date_val = row['date']
                if date_val:
                    d = datetime.strptime(date_val, '%Y-%m-%d')
                    if status != 'مغلق' and (datetime.now() - d).days > 3:
                        overdue = True
            except:
                pass
            tag = 'متأخر' if overdue else status if status in ['مغلق', 'معلق'] else 'default'
            tree.insert('', 'end', values=(
                row['type'],
                row['reference_number'],
                row['subject'],
                row['date'],
                row['status']
            ), tags=(tag,))
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # التخطيط
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def generate_followup_report(self):
        """إنشاء تقرير المتابعة"""
        # مسح المحتوى السابق
        for widget in self.followup_report_frame.winfo_children():
            widget.destroy()
        
        status_filter = self.followup_status_var.get()
        
        # عنوان التقرير
        title = f"تقرير المتابعة - {status_filter}" if status_filter != "الكل" else "تقرير المتابعة - جميع الحالات"
        title_label = tk.Label(
            self.followup_report_frame,
            text=title,
            font=self.font_large,
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # جدول المتابعات
        table_frame = ttk.Frame(self.followup_report_frame)
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        columns = ('id', 'type', 'reference', 'follow_date', 'action', 'responsible', 'status')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=20)
        
        # تعريف العناوين
        tree.heading('id', text='الرقم')
        tree.heading('type', text='النوع')
        tree.heading('reference', text='رقم المراسلة')
        tree.heading('follow_date', text='تاريخ المتابعة')
        tree.heading('action', text='الإجراء المطلوب')
        tree.heading('responsible', text='المسؤول')
        tree.heading('status', text='الحالة')
        
        # جلب البيانات
        if status_filter == "الكل":
            query = """
                SELECT f.id, f.correspondence_type, f.follow_up_date, f.action_required,
                       f.responsible_person, f.status,
                       CASE 
                           WHEN f.correspondence_type = 'incoming' THEN ic.reference_number
                           WHEN f.correspondence_type = 'outgoing' THEN oc.reference_number
                       END as reference_number
                FROM follow_up f
                LEFT JOIN incoming_correspondence ic ON f.correspondence_type = 'incoming' AND f.correspondence_id = ic.id
                LEFT JOIN outgoing_correspondence oc ON f.correspondence_type = 'outgoing' AND f.correspondence_id = oc.id
                ORDER BY f.follow_up_date DESC
            """
            params = None
        else:
            query = """
                SELECT f.id, f.correspondence_type, f.follow_up_date, f.action_required,
                       f.responsible_person, f.status,
                       CASE 
                           WHEN f.correspondence_type = 'incoming' THEN ic.reference_number
                           WHEN f.correspondence_type = 'outgoing' THEN oc.reference_number
                       END as reference_number
                FROM follow_up f
                LEFT JOIN incoming_correspondence ic ON f.correspondence_type = 'incoming' AND f.correspondence_id = ic.id
                LEFT JOIN outgoing_correspondence oc ON f.correspondence_type = 'outgoing' AND f.correspondence_id = oc.id
                WHERE f.status = ?
                ORDER BY f.follow_up_date DESC
            """
            params = (status_filter,)
        
        data = self.db_manager.execute_query(query, params)
        
        # إدراج البيانات
        # تعريف ألوان الحالات
        tree.tag_configure('مكتمل', background='#e8f8e8')      # أخضر فاتح
        tree.tag_configure('معلق', background='#fff6e0')        # برتقالي فاتح
        tree.tag_configure('متأخر', background='#fae8e8')       # أحمر فاتح
        tree.tag_configure('default', background='#f8f8f8')     # رمادي فاتح

        from datetime import datetime
        for row in data:
            type_display = 'واردة' if row['correspondence_type'] == 'incoming' else 'صادرة'
            status = row['status']
            overdue = False
            try:
                date_val = row['follow_up_date']
                if date_val:
                    d = datetime.strptime(date_val, '%Y-%m-%d')
                    if status not in ['مكتمل', 'ملغي'] and (datetime.now() - d).days > 3:
                        overdue = True
            except:
                pass
            tag = 'متأخر' if overdue else status if status in ['مكتمل', 'معلق'] else 'default'
            tree.insert('', 'end', values=(
                row['id'],
                type_display,
                row['reference_number'] or '-',
                row['follow_up_date'],
                row['action_required'],
                row['responsible_person'] or '-',
                row['status']
            ), tags=(tag,))
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # التخطيط
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
    
    def generate_chart(self):
        """إنشاء الرسم البياني"""
        # مسح المحتوى السابق
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        chart_type = self.chart_type_var.get()
        
        if chart_type == "شهري":
            self.create_monthly_chart()
        elif chart_type == "حسب الحالة":
            self.create_status_chart()
        elif chart_type == "حسب الأولوية":
            self.create_priority_chart()
    
    def create_monthly_chart(self):
        """إنشاء رسم بياني شهري"""
        # جلب البيانات للأشهر الـ 12 الماضية
        months_data = []
        current_date = datetime.now()
        
        for i in range(12):
            month_date = current_date - timedelta(days=30*i)
            month_str = month_date.strftime('%Y-%m')
            
            incoming = self.get_monthly_incoming_count(month_str)
            outgoing = self.get_monthly_outgoing_count(month_str)
            
            months_data.append({
                'month': month_date.strftime('%Y-%m'),
                'incoming': incoming,
                'outgoing': outgoing
            })
        
        months_data.reverse()  # ترتيب تصاعدي
        
        # إنشاء الرسم البياني
        fig, ax = plt.subplots(figsize=(12, 6))
        
        months = [data['month'] for data in months_data]
        incoming_counts = [data['incoming'] for data in months_data]
        outgoing_counts = [data['outgoing'] for data in months_data]
        
        x = range(len(months))
        width = 0.35
        
        ax.bar([i - width/2 for i in x], incoming_counts, width, label='واردة', color='#3498db')
        ax.bar([i + width/2 for i in x], outgoing_counts, width, label='صادرة', color='#2ecc71')
        
        ax.set_xlabel('الشهر')
        ax.set_ylabel('عدد المراسلات')
        ax.set_title('إحصائيات المراسلات الشهرية')
        ax.set_xticks(x)
        ax.set_xticklabels(months, rotation=45)
        ax.legend()
        
        plt.tight_layout()
        
        # إدراج الرسم في الواجهة
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def create_status_chart(self):
        """إنشاء رسم بياني حسب الحالة"""
        # جلب بيانات الحالات
        incoming_statuses = self.db_manager.execute_query("""
            SELECT status, COUNT(*) as count 
            FROM incoming_correspondence 
            GROUP BY status
        """)
        
        outgoing_statuses = self.db_manager.execute_query("""
            SELECT status, COUNT(*) as count 
            FROM outgoing_correspondence 
            GROUP BY status
        """)
        
        # إنشاء الرسم البياني
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
        
        # رسم المراسلات الواردة
        if incoming_statuses:
            labels1 = [row['status'] for row in incoming_statuses]
            sizes1 = [row['count'] for row in incoming_statuses]
            ax1.pie(sizes1, labels=labels1, autopct='%1.1f%%', startangle=90)
            ax1.set_title('المراسلات الواردة حسب الحالة')
        
        # رسم المراسلات الصادرة
        if outgoing_statuses:
            labels2 = [row['status'] for row in outgoing_statuses]
            sizes2 = [row['count'] for row in outgoing_statuses]
            ax2.pie(sizes2, labels=labels2, autopct='%1.1f%%', startangle=90)
            ax2.set_title('المراسلات الصادرة حسب الحالة')
        
        plt.tight_layout()
        
        # إدراج الرسم في الواجهة
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def create_priority_chart(self):
        """إنشاء رسم بياني حسب الأولوية"""
        # جلب بيانات الأولويات
        priority_data = self.db_manager.execute_query("""
            SELECT priority, COUNT(*) as count FROM (
                SELECT priority FROM incoming_correspondence
                UNION ALL
                SELECT priority FROM outgoing_correspondence
            ) GROUP BY priority
        """)
        
        if not priority_data:
            return
        
        # إنشاء الرسم البياني
        fig, ax = plt.subplots(figsize=(10, 6))
        
        priorities = [row['priority'] for row in priority_data]
        counts = [row['count'] for row in priority_data]
        
        colors = {'عاجل': '#e74c3c', 'مهم': '#f39c12', 'عادي': '#3498db'}
        bar_colors = [colors.get(p, '#95a5a6') for p in priorities]
        
        ax.bar(priorities, counts, color=bar_colors)
        ax.set_xlabel('الأولوية')
        ax.set_ylabel('عدد المراسلات')
        ax.set_title('توزيع المراسلات حسب الأولوية')
        
        # إضافة القيم على الأعمدة
        for i, v in enumerate(counts):
            ax.text(i, v + 0.1, str(v), ha='center', va='bottom')
        
        plt.tight_layout()
        
        # إدراج الرسم في الواجهة
        canvas = FigureCanvasTkAgg(fig, self.chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill='both', expand=True)
    
    def export_statistics_report(self):
        """تصدير تقرير الإحصائيات"""
        from tkinter import filedialog
        import csv
        
        filename = filedialog.asksaveasfilename(
            title="حفظ تقرير الإحصائيات",
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv"), ("جميع الملفات", "*.*")]
        )
        
        if filename:
            try:
                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    
                    # كتابة العناوين
                    writer.writerow(['الفئة', 'العدد'])
                    
                    # كتابة البيانات
                    writer.writerow(['المراسلات الواردة', self.get_incoming_count()])
                    writer.writerow(['المراسلات الصادرة', self.get_outgoing_count()])
                    writer.writerow(['المتابعات المعلقة', self.get_pending_followups_count()])
                    writer.writerow(['المراسلات الجديدة', self.get_new_incoming_count()])
                    writer.writerow(['المتابعات المكتملة', self.get_completed_followups_count()])
                    writer.writerow(['المراسلات المؤرشفة', self.get_archived_count()])
                
                messagebox.showinfo("نجح", "تم تصدير التقرير بنجاح")
            except Exception as e:
                messagebox.showerror("خطأ", f"فشل في تصدير التقرير: {e}")
    
    def generate_status_report(self):
        """إنشاء تقرير الموضوعات المغلقة والجارية"""
        # مسح المحتوى السابق
        for widget in self.followup_report_frame.winfo_children():
            widget.destroy()
        
        # عنوان التقرير
        title_label = tk.Label(
            self.followup_report_frame,
            text="تقرير الموضوعات المغلقة والجارية",
            font=self.font_large,
            fg='#2c3e50'
        )
        title_label.pack(pady=10)
        
        # إطار الإحصائيات السريعة
        stats_frame = tk.Frame(self.followup_report_frame, bg='#f8f9fa')
        stats_frame.pack(fill='x', padx=20, pady=10)
        
        # بطاقات الإحصائيات
        closed_count = self.get_closed_followups_count()
        ongoing_count = self.get_ongoing_followups_count()
        pending_count = self.get_pending_followups_count()
        total_count = closed_count + ongoing_count + pending_count
        
        # بطاقة الموضوعات المغلقة
        closed_card = tk.Frame(stats_frame, bg='#27ae60', relief='raised', bd=2)
        closed_card.pack(side='left', fill='both', expand=True, padx=5)
        
        tk.Label(closed_card, text="✅", font=('Arial Unicode MS', 24), bg='#27ae60', fg='white').pack(pady=(10, 0))
        tk.Label(closed_card, text=str(closed_count), font=('Arial Unicode MS', 20, 'bold'), bg='#27ae60', fg='white').pack()
        tk.Label(closed_card, text="موضوعات مغلقة", font=('Arial Unicode MS', 10, 'bold'), bg='#27ae60', fg='white').pack(pady=(0, 10))
        
        # بطاقة الموضوعات الجارية
        ongoing_card = tk.Frame(stats_frame, bg='#3498db', relief='raised', bd=2)
        ongoing_card.pack(side='left', fill='both', expand=True, padx=5)
        
        tk.Label(ongoing_card, text="🔄", font=('Arial Unicode MS', 24), bg='#3498db', fg='white').pack(pady=(10, 0))
        tk.Label(ongoing_card, text=str(ongoing_count), font=('Arial Unicode MS', 20, 'bold'), bg='#3498db', fg='white').pack()
        tk.Label(ongoing_card, text="موضوعات جارية", font=('Arial Unicode MS', 10, 'bold'), bg='#3498db', fg='white').pack(pady=(0, 10))
        
        # بطاقة الموضوعات المعلقة
        pending_card = tk.Frame(stats_frame, bg='#e67e22', relief='raised', bd=2)
        pending_card.pack(side='left', fill='both', expand=True, padx=5)
        
        tk.Label(pending_card, text="⏳", font=('Arial Unicode MS', 24), bg='#e67e22', fg='white').pack(pady=(10, 0))
        tk.Label(pending_card, text=str(pending_count), font=('Arial Unicode MS', 20, 'bold'), bg='#e67e22', fg='white').pack()
        tk.Label(pending_card, text="موضوعات معلقة", font=('Arial Unicode MS', 10, 'bold'), bg='#e67e22', fg='white').pack(pady=(0, 10))
        
        # جدول تفصيلي للموضوعات
        table_frame = ttk.LabelFrame(self.followup_report_frame, text="تفاصيل الموضوعات")
        table_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # إنشاء الجدول
        columns = ('status', 'reference', 'subject', 'responsible', 'date', 'action')
        tree = ttk.Treeview(table_frame, columns=columns, show='headings', height=15)
        
        # تعريف العناوين
        tree.heading('status', text='الحالة')
        tree.heading('reference', text='رقم المراسلة')
        tree.heading('subject', text='الموضوع')
        tree.heading('responsible', text='المسؤول')
        tree.heading('date', text='تاريخ المتابعة')
        tree.heading('action', text='الإجراء المطلوب')
        
        # تعيين عرض الأعمدة
        tree.column('status', width=80, anchor='center')
        tree.column('reference', width=120, anchor='center')
        tree.column('subject', width=200, anchor='e')
        tree.column('responsible', width=120, anchor='center')
        tree.column('date', width=100, anchor='center')
        tree.column('action', width=200, anchor='e')
        
        # تعيين ألوان للحالات
        tree.tag_configure('مغلق', background='#d5f4e6', foreground='#27ae60')
        tree.tag_configure('جاري', background='#d6eaf8', foreground='#3498db')
        tree.tag_configure('معلق', background='#fdeaa7', foreground='#e67e22')
        
        # جلب البيانات
        query = """
            SELECT f.status, f.follow_up_date, f.action_required, f.responsible_person,
                   CASE 
                       WHEN f.correspondence_type = 'incoming' THEN ic.reference_number
                       WHEN f.correspondence_type = 'outgoing' THEN oc.reference_number
                   END as reference_number,
                   CASE 
                       WHEN f.correspondence_type = 'incoming' THEN ic.subject
                       WHEN f.correspondence_type = 'outgoing' THEN oc.subject
                   END as subject
            FROM follow_up f
            LEFT JOIN incoming_correspondence ic ON f.correspondence_type = 'incoming' AND f.correspondence_id = ic.id
            LEFT JOIN outgoing_correspondence oc ON f.correspondence_type = 'outgoing' AND f.correspondence_id = oc.id
            ORDER BY 
                CASE f.status 
                    WHEN 'جاري' THEN 1 
                    WHEN 'معلق' THEN 2 
                    WHEN 'مغلق' THEN 3 
                    ELSE 4 
                END,
                f.follow_up_date DESC
        """
        
        results = self.db_manager.execute_query(query)
        
        for row in results:
            status = row['status'] if row['status'] else 'غير محدد'
            reference = row['reference_number'] if row['reference_number'] else 'غير محدد'
            subject = row['subject'] if row['subject'] else 'غير محدد'
            responsible = row['responsible_person'] if row['responsible_person'] else 'غير محدد'
            date = row['follow_up_date'] if row['follow_up_date'] else 'غير محدد'
            action = row['action_required'] if row['action_required'] else 'غير محدد'
            
            # تحديد اللون حسب الحالة
            tag = status if status in ['مغلق', 'جاري', 'معلق'] else 'default'
            
            tree.insert('', 'end', values=(
                status, reference, subject, responsible, date, action
            ), tags=(tag,))
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient='vertical', command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # التخطيط
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # إطار الملخص
        summary_frame = ttk.LabelFrame(self.followup_report_frame, text="ملخص التقرير")
        summary_frame.pack(fill='x', padx=20, pady=10)
        
        summary_text = f"""
        📊 إجمالي الموضوعات: {total_count}
        ✅ موضوعات مغلقة: {closed_count} ({(closed_count/total_count*100):.1f}% من الإجمالي)
        🔄 موضوعات جارية: {ongoing_count} ({(ongoing_count/total_count*100):.1f}% من الإجمالي)
        ⏳ موضوعات معلقة: {pending_count} ({(pending_count/total_count*100):.1f}% من الإجمالي)
        
        📈 معدل الإنجاز: {(closed_count/total_count*100):.1f}%
        """ if total_count > 0 else "لا توجد موضوعات للمتابعة حالياً"
        
        summary_label = tk.Label(
            summary_frame,
            text=summary_text,
            font=self.font_normal,
            justify='right',
            anchor='e'
        )
        summary_label.pack(padx=10, pady=10)
    
    def get_closed_followups_count(self):
        """عدد المتابعات المغلقة"""
        result = self.db_manager.execute_query("SELECT COUNT(*) as count FROM follow_up WHERE status = 'مغلق'")
        return result[0]['count'] if result else 0
    
    def get_ongoing_followups_count(self):
        """عدد المتابعات الجارية"""
        result = self.db_manager.execute_query("SELECT COUNT(*) as count FROM follow_up WHERE status = 'جاري'")
        return result[0]['count'] if result else 0
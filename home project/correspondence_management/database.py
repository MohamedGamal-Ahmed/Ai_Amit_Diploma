#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة إدارة قاعدة البيانات
Database Management Module
"""

import sqlite3
import os
from datetime import datetime
import hashlib

class DatabaseManager:
    def __init__(self, db_path="correspondence.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # للحصول على النتائج كقاموس
        return conn
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            # جدول المستخدمين
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    full_name TEXT NOT NULL,
                    role TEXT NOT NULL CHECK (role IN ('admin', 'employee', 'viewer')),
                    department TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_active BOOLEAN DEFAULT 1
                )
            ''')
            
            # جدول المراسلات الواردة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS incoming_correspondence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reference_number TEXT UNIQUE NOT NULL,
                    subject TEXT NOT NULL,
                    sender TEXT NOT NULL,
                    sender_department TEXT,
                    received_date DATE NOT NULL,
                    priority TEXT DEFAULT 'عادي' CHECK (priority IN ('عاجل', 'مهم', 'عادي')),
                    status TEXT DEFAULT 'جديد' CHECK (status IN ('جديد', 'قيد المراجعة', 'تم الرد', 'مؤرشف')),
                    content TEXT,
                    notes TEXT,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # جدول المراسلات الصادرة
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS outgoing_correspondence (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    reference_number TEXT UNIQUE NOT NULL,
                    subject TEXT NOT NULL,
                    recipient TEXT NOT NULL,
                    recipient_department TEXT,
                    sent_date DATE NOT NULL,
                    priority TEXT DEFAULT 'عادي' CHECK (priority IN ('عاجل', 'مهم', 'عادي')),
                    status TEXT DEFAULT 'مسودة' CHECK (status IN ('مسودة', 'تم الإرسال', 'تم الاستلام', 'مؤرشف')),
                    content TEXT,
                    notes TEXT,
                    related_incoming_id INTEGER,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (related_incoming_id) REFERENCES incoming_correspondence (id),
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # جدول متابعة الموضوعات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS follow_up (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    correspondence_type TEXT NOT NULL CHECK (correspondence_type IN ('incoming', 'outgoing')),
                    correspondence_id INTEGER NOT NULL,
                    follow_up_date DATE NOT NULL,
                    action_required TEXT NOT NULL,
                    responsible_person TEXT,
                    status TEXT DEFAULT 'معلق' CHECK (status IN ('معلق', 'جاري', 'مغلق')),
                    notes TEXT,
                    created_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (created_by) REFERENCES users (id)
                )
            ''')
            
            # جدول سجل النشاطات
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    action TEXT NOT NULL,
                    table_name TEXT,
                    record_id INTEGER,
                    old_values TEXT,
                    new_values TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                )
            ''')
            
            # إنشاء فهارس لتحسين الأداء
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_incoming_ref ON incoming_correspondence(reference_number)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_outgoing_ref ON outgoing_correspondence(reference_number)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_incoming_date ON incoming_correspondence(received_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_outgoing_date ON outgoing_correspondence(sent_date)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_follow_up_date ON follow_up(follow_up_date)')
            
            # تحديث قاعدة البيانات (إضافة أعمدة جديدة)
            self.update_database_schema(cursor)
            
            conn.commit()
            print("تم إنشاء قاعدة البيانات بنجاح")
            
        except Exception as e:
            print(f"خطأ في إنشاء قاعدة البيانات: {e}")
            conn.rollback()
        finally:
            conn.close()
    
    def update_database_schema(self, cursor):
        """تحديث مخطط قاعدة البيانات - إضافة أعمدة جديدة"""
        try:
            # التحقق من وجود عمود subject_code في جدول incoming_correspondence
            cursor.execute("PRAGMA table_info(incoming_correspondence)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'subject_code' not in columns:
                cursor.execute('ALTER TABLE incoming_correspondence ADD COLUMN subject_code TEXT')
                print("تم إضافة عمود كود الموضوع")
            
            if 'responsible_person' not in columns:
                cursor.execute('ALTER TABLE incoming_correspondence ADD COLUMN responsible_person TEXT')
                print("تم إضافة عمود المسئول")
            
            # تحديث جدول المتابعة
            cursor.execute("PRAGMA table_info(follow_up)")
            follow_up_columns = [column[1] for column in cursor.fetchall()]
            
            if 'follow_up_code' not in follow_up_columns:
                cursor.execute('ALTER TABLE follow_up ADD COLUMN follow_up_code TEXT')
                print("تم إضافة عمود كود المتابعة")
            
            # تحديث حالات المتابعة (تنفيذ كل استعلام منفصل)
            try:
                cursor.execute("UPDATE follow_up SET status = 'جاري' WHERE status = 'قيد التنفيذ'")
                cursor.execute("UPDATE follow_up SET status = 'مغلق' WHERE status = 'مكتمل'")
                cursor.execute("UPDATE follow_up SET status = 'مغلق' WHERE status = 'ملغي'")
                print("تم تحديث حالات المتابعة")
            except Exception as e:
                print(f"تحذير: خطأ في تحديث حالات المتابعة: {e}")
            
            # تحديث جدول المراسلات الصادرة
            cursor.execute("PRAGMA table_info(outgoing_correspondence)")
            outgoing_columns = [column[1] for column in cursor.fetchall()]
            
            if 'subject_code' not in outgoing_columns:
                cursor.execute('ALTER TABLE outgoing_correspondence ADD COLUMN subject_code TEXT')
                print("تم إضافة عمود كود الموضوع للصادرة")
            
            if 'recipient_engineer' not in outgoing_columns:
                cursor.execute('ALTER TABLE outgoing_correspondence ADD COLUMN recipient_engineer TEXT')
                print("تم إضافة عمود المهندس المستلم")
            
            if 'responsible_engineer' not in outgoing_columns:
                cursor.execute('ALTER TABLE outgoing_correspondence ADD COLUMN responsible_engineer TEXT')
                print("تم إضافة عمود المهندس المسئول")
            
            if 'engineer' not in outgoing_columns:
                cursor.execute('ALTER TABLE outgoing_correspondence ADD COLUMN engineer TEXT')
                print("تم إضافة عمود مهندس/مهندسة")
            
            # يمكن إضافة المزيد من التحديثات هنا في المستقبل
            
        except Exception as e:
            print(f"تحذير: خطأ في تحديث قاعدة البيانات: {e}")
    
    def execute_query(self, query, params=None):
        """تنفيذ استعلام قراءة"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor.fetchall()
        except Exception as e:
            print(f"خطأ في تنفيذ الاستعلام: {e}")
            return []
        finally:
            conn.close()
    
    def execute_update(self, query, params=None):
        """تنفيذ استعلام تحديث/إدراج/حذف"""
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"خطأ في تنفيذ التحديث: {e}")
            conn.rollback()
            return None
        finally:
            conn.close()
    
    def log_activity(self, user_id, action, table_name=None, record_id=None, old_values=None, new_values=None):
        """تسجيل نشاط المستخدم"""
        query = '''
            INSERT INTO activity_log (user_id, action, table_name, record_id, old_values, new_values)
            VALUES (?, ?, ?, ?, ?, ?)
        '''
        params = (user_id, action, table_name, record_id, old_values, new_values)
        return self.execute_update(query, params)
    
    def get_statistics(self):
        """الحصول على إحصائيات النظام"""
        stats = {}
        
        # عدد المراسلات الواردة
        result = self.execute_query("SELECT COUNT(*) as count FROM incoming_correspondence")
        stats['total_incoming'] = result[0]['count'] if result else 0
        
        # عدد المراسلات الصادرة
        result = self.execute_query("SELECT COUNT(*) as count FROM outgoing_correspondence")
        stats['total_outgoing'] = result[0]['count'] if result else 0
        
        # المراسلات الواردة الجديدة
        result = self.execute_query("SELECT COUNT(*) as count FROM incoming_correspondence WHERE status = 'جديد'")
        stats['new_incoming'] = result[0]['count'] if result else 0
        
        # المراسلات الصادرة المسودة
        result = self.execute_query("SELECT COUNT(*) as count FROM outgoing_correspondence WHERE status = 'مسودة'")
        stats['draft_outgoing'] = result[0]['count'] if result else 0
        
        # المتابعات المعلقة
        result = self.execute_query("SELECT COUNT(*) as count FROM follow_up WHERE status = 'معلق'")
        stats['pending_followups'] = result[0]['count'] if result else 0
        
        # إحصائيات هذا الشهر
        current_month = datetime.now().strftime('%Y-%m')
        
        result = self.execute_query(
            "SELECT COUNT(*) as count FROM incoming_correspondence WHERE strftime('%Y-%m', received_date) = ?",
            (current_month,)
        )
        stats['incoming_this_month'] = result[0]['count'] if result else 0
        
        result = self.execute_query(
            "SELECT COUNT(*) as count FROM outgoing_correspondence WHERE strftime('%Y-%m', sent_date) = ?",
            (current_month,)
        )
        stats['outgoing_this_month'] = result[0]['count'] if result else 0
        
        return stats
    
    def backup_database(self, backup_path):
        """نسخ احتياطي من قاعدة البيانات"""
        try:
            import shutil
            shutil.copy2(self.db_path, backup_path)
            return True
        except Exception as e:
            print(f"خطأ في إنشاء النسخة الاحتياطية: {e}")
            return False
    
    def restore_database(self, backup_path):
        """استعادة قاعدة البيانات من نسخة احتياطية"""
        try:
            import shutil
            shutil.copy2(backup_path, self.db_path)
            return True
        except Exception as e:
            print(f"خطأ في استعادة النسخة الاحتياطية: {e}")
            return False
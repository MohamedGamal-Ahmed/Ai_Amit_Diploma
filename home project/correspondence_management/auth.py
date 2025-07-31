#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
وحدة إدارة المصادقة والمستخدمين
Authentication and User Management Module
"""

import hashlib
import sqlite3
from datetime import datetime

class AuthManager:
    def __init__(self, db_manager):
        self.db_manager = db_manager
        self.current_user = None
    
    def hash_password(self, password):
        """تشفير كلمة المرور"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def create_user(self, username, password, full_name, role, department=None):
        """إنشاء مستخدم جديد"""
        password_hash = self.hash_password(password)
        
        query = '''
            INSERT INTO users (username, password_hash, full_name, role, department)
            VALUES (?, ?, ?, ?, ?)
        '''
        params = (username, password_hash, full_name, role, department)
        
        user_id = self.db_manager.execute_update(query, params)
        
        if user_id:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=user_id,
                action=f"تم إنشاء مستخدم جديد: {username}",
                table_name="users",
                record_id=user_id
            )
            return user_id
        return None
    
    def authenticate(self, username, password):
        """التحقق من صحة بيانات المستخدم"""
        password_hash = self.hash_password(password)
        
        query = '''
            SELECT id, username, full_name, role, department, is_active
            FROM users 
            WHERE username = ? AND password_hash = ? AND is_active = 1
        '''
        params = (username, password_hash)
        
        result = self.db_manager.execute_query(query, params)
        
        if result:
            user_data = dict(result[0])
            self.current_user = user_data
            
            # تسجيل نشاط تسجيل الدخول
            self.db_manager.log_activity(
                user_id=user_data['id'],
                action="تسجيل دخول",
                table_name="users",
                record_id=user_data['id']
            )
            
            return user_data
        return None
    
    def logout(self):
        """تسجيل الخروج"""
        if self.current_user:
            # تسجيل نشاط تسجيل الخروج
            self.db_manager.log_activity(
                user_id=self.current_user['id'],
                action="تسجيل خروج",
                table_name="users",
                record_id=self.current_user['id']
            )
            self.current_user = None
    
    def user_exists(self, username):
        """التحقق من وجود المستخدم"""
        query = "SELECT id FROM users WHERE username = ?"
        result = self.db_manager.execute_query(query, (username,))
        return len(result) > 0
    
    def get_all_users(self):
        """الحصول على جميع المستخدمين"""
        query = '''
            SELECT id, username, full_name, role, department, is_active, created_at
            FROM users
            ORDER BY created_at DESC
        '''
        return self.db_manager.execute_query(query)
    
    def update_user(self, user_id, username=None, full_name=None, role=None, department=None, is_active=None):
        """تحديث بيانات المستخدم"""
        # الحصول على البيانات القديمة
        old_data = self.get_user_by_id(user_id)
        if not old_data:
            return False
        
        updates = []
        params = []
        
        if username is not None:
            updates.append("username = ?")
            params.append(username)
        
        if full_name is not None:
            updates.append("full_name = ?")
            params.append(full_name)
        
        if role is not None:
            updates.append("role = ?")
            params.append(role)
        
        if department is not None:
            updates.append("department = ?")
            params.append(department)
        
        if is_active is not None:
            updates.append("is_active = ?")
            params.append(is_active)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(user_id)
        
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        
        result = self.db_manager.execute_update(query, params)
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.current_user['id'] if self.current_user else None,
                action=f"تم تحديث بيانات المستخدم: {old_data['username']}",
                table_name="users",
                record_id=user_id,
                old_values=str(dict(old_data)),
                new_values=f"التحديثات: {dict(zip([u.split(' = ')[0] for u in updates[:-1]], params[:-1]))}"
            )
            return True
        return False
    
    def change_password(self, user_id, new_password):
        """تغيير كلمة المرور"""
        password_hash = self.hash_password(new_password)
        
        query = "UPDATE users SET password_hash = ? WHERE id = ?"
        params = (password_hash, user_id)
        
        result = self.db_manager.execute_update(query, params)
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.current_user['id'] if self.current_user else None,
                action=f"تم تغيير كلمة المرور للمستخدم ID: {user_id}",
                table_name="users",
                record_id=user_id
            )
            return True
        return False
    
    def get_user_by_id(self, user_id):
        """الحصول على بيانات المستخدم بالمعرف"""
        query = '''
            SELECT id, username, full_name, role, department, is_active, created_at
            FROM users 
            WHERE id = ?
        '''
        result = self.db_manager.execute_query(query, (user_id,))
        return dict(result[0]) if result else None
    
    def delete_user(self, user_id):
        """حذف المستخدم (تعطيل فقط)"""
        # الحصول على بيانات المستخدم قبل الحذف
        user_data = self.get_user_by_id(user_id)
        if not user_data:
            return False
        
        # تعطيل المستخدم بدلاً من حذفه
        query = "UPDATE users SET is_active = 0 WHERE id = ?"
        result = self.db_manager.execute_update(query, (user_id,))
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.current_user['id'] if self.current_user else None,
                action=f"تم تعطيل المستخدم: {user_data['username']}",
                table_name="users",
                record_id=user_id
            )
            return True
        return False
    
    def has_permission(self, action):
        """التحقق من صلاحيات المستخدم"""
        if not self.current_user:
            return False
        
        role = self.current_user['role']
        
        # صلاحيات المدير
        if role == 'admin':
            return True
        
        # صلاحيات الموظف
        elif role == 'employee':
            allowed_actions = [
                'view_incoming', 'add_incoming', 'edit_incoming', 'delete_incoming',
                'view_outgoing', 'add_outgoing', 'edit_outgoing', 'delete_outgoing',
                'view_followup', 'add_followup', 'edit_followup', 'delete_followup',
                'close_follow_up',  # صلاحية إغلاق المتابعات
                'view_reports'
            ]
            return action in allowed_actions
        
        # صلاحيات المشاهد
        elif role == 'viewer':
            allowed_actions = [
                'view_incoming', 'view_outgoing', 'view_followup', 'view_reports'
            ]
            return action in allowed_actions
        
        return False
    
    def get_user_by_id(self, user_id):
        """الحصول على مستخدم بالمعرف"""
        query = "SELECT * FROM users WHERE id = ?"
        result = self.db_manager.execute_query(query, (user_id,))
        return dict(result[0]) if result else None
    
    def user_exists(self, username):
        """التحقق من وجود اسم المستخدم"""
        query = "SELECT COUNT(*) as count FROM users WHERE username = ?"
        result = self.db_manager.execute_query(query, (username,))
        return result[0]['count'] > 0 if result else False
    
    def create_user(self, username, password, full_name, role='employee', department=None):
        """إنشاء مستخدم جديد"""
        if self.user_exists(username):
            return False
        
        password_hash = self._hash_password(password)
        
        query = '''
            INSERT INTO users (username, password_hash, full_name, role, department, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
        '''
        
        result = self.db_manager.execute_update(
            query, 
            (username, password_hash, full_name, role, department)
        )
        
        if result:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.current_user['id'] if self.current_user else None,
                action=f"إنشاء مستخدم جديد: {username}",
                table_name="users",
                record_id=result
            )
            return True
        
        return False
    
    def update_user(self, user_id, username=None, full_name=None, role=None, 
                   department=None, is_active=None):
        """تحديث بيانات المستخدم"""
        # بناء الاستعلام ديناميكياً
        updates = []
        params = []
        
        if username is not None:
            updates.append("username = ?")
            params.append(username)
        
        if full_name is not None:
            updates.append("full_name = ?")
            params.append(full_name)
        
        if role is not None:
            updates.append("role = ?")
            params.append(role)
        
        if department is not None:
            updates.append("department = ?")
            params.append(department)
        
        if is_active is not None:
            updates.append("is_active = ?")
            params.append(is_active)
        
        if not updates:
            return False
        
        updates.append("updated_at = CURRENT_TIMESTAMP")
        params.append(user_id)
        
        query = f"UPDATE users SET {', '.join(updates)} WHERE id = ?"
        
        result = self.db_manager.execute_update(query, params)
        
        if result is not None:
            # تسجيل النشاط
            self.db_manager.log_activity(
                user_id=self.current_user['id'] if self.current_user else None,
                action=f"تحديث بيانات المستخدم رقم {user_id}",
                table_name="users",
                record_id=user_id
            )
            return True
        
        return False
    
    def get_all_users(self):
        """الحصول على جميع المستخدمين"""
        query = "SELECT * FROM users ORDER BY created_at DESC"
        result = self.db_manager.execute_query(query)
        return [dict(row) for row in result] if result else []
    
    def get_user_activity_log(self, user_id=None, limit=100):
        """الحصول على سجل نشاطات المستخدم"""
        if user_id:
            query = '''
                SELECT al.*, u.username 
                FROM activity_log al
                LEFT JOIN users u ON al.user_id = u.id
                WHERE al.user_id = ?
                ORDER BY al.timestamp DESC
                LIMIT ?
            '''
            params = (user_id, limit)
        else:
            query = '''
                SELECT al.*, u.username 
                FROM activity_log al
                LEFT JOIN users u ON al.user_id = u.id
                ORDER BY al.timestamp DESC
                LIMIT ?
            '''
            params = (limit,)
        
        result = self.db_manager.execute_query(query, params)
        return [dict(row) for row in result] if result else []
    
    def get_user_activity_log(self, user_id=None, limit=100):
        """الحصول على سجل نشاطات المستخدم"""
        if user_id:
            query = '''
                SELECT al.*, u.username, u.full_name
                FROM activity_log al
                LEFT JOIN users u ON al.user_id = u.id
                WHERE al.user_id = ?
                ORDER BY al.timestamp DESC
                LIMIT ?
            '''
            params = (user_id, limit)
        else:
            query = '''
                SELECT al.*, u.username, u.full_name
                FROM activity_log al
                LEFT JOIN users u ON al.user_id = u.id
                ORDER BY al.timestamp DESC
                LIMIT ?
            '''
            params = (limit,)
        
        return self.db_manager.execute_query(query, params)
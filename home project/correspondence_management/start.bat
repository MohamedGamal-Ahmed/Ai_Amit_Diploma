@echo off
chcp 65001 > nul
title نظام إدارة المراسلات - Correspondence Management System

echo.
echo ================================================
echo        نظام إدارة المراسلات
echo    Correspondence Management System
echo ================================================
echo.

echo 🔍 التحقق من Python...
python --version > nul 2>&1
if errorlevel 1 (
    echo ❌ Python غير مثبت. يرجى تثبيت Python أولاً.
    pause
    exit /b 1
)

echo ✅ Python متوفر

echo.
echo 📦 تثبيت المتطلبات...
pip install matplotlib numpy Pillow > nul 2>&1

echo.
echo 🚀 تشغيل البرنامج...
echo.
echo 📋 بيانات تسجيل الدخول الافتراضية:
echo    اسم المستخدم: admin
echo    كلمة المرور: admin123
echo.
echo ================================================

python main.py

if errorlevel 1 (
    echo.
    echo ❌ حدث خطأ في تشغيل البرنامج
    echo 🔧 تأكد من وجود جميع الملفات المطلوبة
    pause
)

echo.
echo تم إغلاق البرنامج
pause
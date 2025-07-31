import tkinter as tk
from tkinter import ttk, messagebox, colorchooser, simpledialog

class SettingsWindow(tk.Toplevel):
    def __init__(self, master, auth_manager, user_data, on_settings_changed=None):
        super().__init__(master)
        self.title("الإعدادات")
        self.geometry("400x400")
        self.auth_manager = auth_manager
        self.user_data = user_data
        self.on_settings_changed = on_settings_changed
        self.configure(bg='#f8f8f8')
        
        self.create_widgets()

    def create_widgets(self):
        # تغيير كلمة المرور
        password_frame = ttk.LabelFrame(self, text="تغيير كلمة المرور")
        password_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(password_frame, text="كلمة المرور الحالية:").pack(anchor="w", padx=5, pady=2)
        self.current_password_entry = ttk.Entry(password_frame, show="*")
        self.current_password_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(password_frame, text="كلمة المرور الجديدة:").pack(anchor="w", padx=5, pady=2)
        self.new_password_entry = ttk.Entry(password_frame, show="*")
        self.new_password_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Label(password_frame, text="تأكيد كلمة المرور الجديدة:").pack(anchor="w", padx=5, pady=2)
        self.confirm_password_entry = ttk.Entry(password_frame, show="*")
        self.confirm_password_entry.pack(fill="x", padx=5, pady=2)
        
        ttk.Button(password_frame, text="تغيير كلمة المرور", command=self.change_password).pack(pady=5)

        # تخصيص الألوان
        customize_frame = ttk.LabelFrame(self, text="تخصيص الواجهة")
        customize_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(customize_frame, text="لون الخلفية:").pack(anchor="w", padx=5, pady=2)
        self.bg_color_btn = ttk.Button(customize_frame, text="اختر اللون", command=self.choose_bg_color)
        self.bg_color_btn.pack(fill="x", padx=5, pady=2)
        
        # حفظ التغييرات
        ttk.Button(self, text="حفظ التغييرات", command=self.save_settings).pack(pady=15)

    def change_password(self):
        current = self.current_password_entry.get()
        new = self.new_password_entry.get()
        confirm = self.confirm_password_entry.get()
        if not current or not new or not confirm:
            messagebox.showwarning("تنبيه", "يرجى ملء جميع الحقول.")
            return
        if new != confirm:
            messagebox.showerror("خطأ", "كلمة المرور الجديدة غير متطابقة.")
            return
        if not self.auth_manager.verify_user(self.user_data['username'], current):
            messagebox.showerror("خطأ", "كلمة المرور الحالية غير صحيحة.")
            return
        self.auth_manager.change_password(self.user_data['username'], new)
        messagebox.showinfo("تم", "تم تغيير كلمة المرور بنجاح.")
        self.current_password_entry.delete(0, 'end')
        self.new_password_entry.delete(0, 'end')
        self.confirm_password_entry.delete(0, 'end')

    def choose_bg_color(self):
        color = colorchooser.askcolor(title="اختر لون الخلفية")
        if color[1]:
            self.bg_color = color[1]
            self.configure(bg=self.bg_color)

    def save_settings(self):
        # يمكن هنا حفظ الإعدادات في ملف أو قاعدة بي��نات
        messagebox.showinfo("تم", "تم حفظ الإعدادات.")
        if self.on_settings_changed:
            self.on_settings_changed()
        self.destroy()

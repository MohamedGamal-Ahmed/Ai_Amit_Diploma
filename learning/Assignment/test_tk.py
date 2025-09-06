import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd

class DataViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Viewer App")
        self.root.geometry("1000x700")

        # Header
        header = tk.Label(self.root, text="Pandas Data Viewer", bg="blue", fg="white", font=("Helvetica", 22, "bold"))
        header.pack(fill=tk.X)

        # Sidebar
        sidebar = tk.Frame(self.root, width=250, bg="lightgrey")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        choose_btn = tk.Button(sidebar, text="Choose CSV File", command=self.choose_file, bg="grey", fg="white", font=("Arial", 14))
        choose_btn.pack(pady=15, fill=tk.X, padx=10)

        view_btn = tk.Button(sidebar, text="View Data", command=self.view_data, bg="green", fg="white", font=("Arial", 14))
        view_btn.pack(pady=15, fill=tk.X, padx=10)

        # Main frame
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(expand=True, fill="both")

        # جدول Treeview
        self.tree = ttk.Treeview(self.main_frame)
        self.tree.pack(expand=True, fill="both")

        # Scrollbars
        vsb = ttk.Scrollbar(self.main_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(self.main_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        vsb.pack(side='right', fill='y')
        hsb.pack(side='bottom', fill='x')

        # File path
        self.file_path = None

    def choose_file(self):
        self.file_path = filedialog.askopenfilename(
            title="Select a CSV file",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if self.file_path:
            messagebox.showinfo("File Selected", f"File chosen:\n{self.file_path}")

    def view_data(self):
        if not self.file_path:
            messagebox.showwarning("No File", "Please choose a file first!")
            return

        try:
            df = pd.read_csv(self.file_path)

            # امسح الجدول القديم
            self.tree.delete(*self.tree.get_children())
            self.tree["columns"] = list(df.columns)
            self.tree["show"] = "headings"

            # إضافة الأعمدة
            for col in df.columns:
                self.tree.heading(col, text=col)
                self.tree.column(col, width=120, anchor="center")

            # إضافة الصفوف (مثلا أول 100 صف)
            for row in df.head(10).to_numpy().tolist():
                self.tree.insert("", "end", values=row)

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = DataViewerApp(root)
    root.mainloop()

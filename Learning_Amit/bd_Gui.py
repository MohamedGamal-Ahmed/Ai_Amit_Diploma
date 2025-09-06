import tkinter as tk
from tkinter import ttk , messagebox
import psycopg2




my_conn = psycopg2.connect(
    host = "localhost",
    database = "Hospital",
    user = "postgres",
    password = "test_12345"

)

cur = my_conn.cursor()

def insert_data():
    name = entery_name.get() .strip()
    phone = entery_phone.get().strip()

    if name == "" or phone == "":
        messagebox.showwarning("Warning add data ",) 

    try:
        cur.execute("INSERT INTO steudent (name, phone) VALUES (%s, %s)", (name, phone))
        my_conn.commit()
        messagebox.showinfo("Success", "Data inserted successfully")
        entery_name.delete(0, tk.END)
        entery_phone.delete(0, tk.END)

        load_date()

    except Exception as e:
        my_conn.rollback()
        messagebox.showerror("Error", f"An error occurred: {e}")


def load_date():
    for row in tree.get_children():
        tree.delete(row)
    cur.execute("SELECT name, phone FROM steudent")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("", tk.END, values=row)


################################ GUI Application designing #####################################
root = tk.Tk()
root.title("Student form") # Title of the window
root.geometry("600x600")

title = tk.Label(root, text="Student Registration Form", font=("Arial", 24)) # Label widget
title . pack(pady=10)


frame_input = tk.Frame(root) # Input frame
frame_input.pack(pady=10) # Padding around the frame
tk.Label(frame_input, text="Name:", font=("Arial", 16)).grid(row=0,  padx=5, pady=5 , sticky="w") # Label widget for name
entery_name = tk.Entry(frame_input, width=30) # Entry widget for name
entery_name.grid(row=0, column=1, padx=5, pady=5) # Grid layout for name entry


tk.Label(frame_input, text="phone:", font=("Arial", 16)).grid(row=1,  padx=5, pady=5 , sticky="w") # Label widget for name
entery_phone = tk.Entry(frame_input, width=30) # Entry widget for name
entery_phone.grid(row=1, column=1, padx=5, pady=5) # Grid layout for name entry

btn_add = tk.Button(root, text="Add", command=insert_data, width=20 , bg = "green", fg= 'white') # Button widget
btn_add.pack(pady=15)


frame_table = tk.Frame(root) # Table frame
frame_table.pack(pady=10 , fill= "both", expand=True) # Padding around the frame

columns = ("name", "phone") # Define columns for the table
tree = ttk.Treeview(frame_table, columns=columns, show="headings" , height=8) # Treeview widget for the table

tree.heading("name", text="Name") # Set heading for Name column
tree.column("name", width=200) # Set width for Name column
tree.heading("phone", text="Phone") # Set heading for Phone column
tree.column("phone", width=200) # Set width for Phone column

tree.pack(side="left", fill="both", expand=True) # Fill the table frame

scrollbar = ttk.Scrollbar(frame_table, orient="vertical", command=tree.yview) # Scrollbar for the table
tree.configure(yscroll=scrollbar.set) # Configure the scrollbar
scrollbar.pack(side="right", fill="y") # Fill the scrollbar frame








root.mainloop()
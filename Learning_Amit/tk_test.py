import tkinter as tk

class GUI_app: # GUI Application Class
    def __init__(self, root):
        self.root = root
        self.root.title("Amit DataScience App") # Title of the window
        self.root.geometry("900x800")

    #def create_widgets(self):
        header = tk.Label(self.root, text="Welcome to Amit's DataScience App", bg="blue", fg="white", font=("Helvetica", 28 , "bold"))
        header.pack(fill=tk.X)

        sidebar = tk.Frame(self.root, width=350, bg="lightgrey")
        sidebar.pack(side=tk.LEFT, fill=tk.Y)

        project_labels = ["Linear Regression", "Project2", "Project3", "Project4", "Project5", "Project6", "Project7", "Project8", "Project9"]
        for label in project_labels:
            lbl = tk.Label(sidebar, text=label, bg="lightgrey", anchor="w", padx=15, font=("Arial", 16))
            lbl.pack(fill=tk.X, padx=7, pady=7)

        # Main section for salary prediction
        main_frame = tk.Frame(self.root)
        main_frame.pack(pady=20)
        title = tk.Label(main_frame, text="Salary Prediction", font=("Arial", 24))
        title.pack(pady=10)

        # Experience input
        label = tk.Label(main_frame, text="Enter years of experience:", font=("Arial", 18))
        label.pack()
        self.experience_entry = tk.Entry(main_frame, font=("Arial", 18))
        self.experience_entry.pack()

        # # Execute button
        execute_button = tk.Button(main_frame, text="Execute", command=" ", bg="grey", fg="black", font=("Arial", 18))
        execute_button.pack(pady=10)

        # Result label
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 20, "bold"))
        self.result_label.pack()
        
        





if __name__ == "__main__":
    root = tk.Tk()
    app = GUI_app(root)
    root.mainloop()
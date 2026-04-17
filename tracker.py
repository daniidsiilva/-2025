import tkinter as tk
from tkinter import ttk, messagebox
import datetime
from tkcalendar import DateEntry

class Student:
    def __init__(self, student_id, name):
        self.id = student_id
        self.name = name
        self.attendance_history = {}

    def get_status(self, date_str):
        return self.attendance_history.get(date_str, "Not Marked")

    def set_status(self, date_str, status):
        if status is None:
            if date_str in self.attendance_history:
                del self.attendance_history[date_str]
        else:
            self.attendance_history[date_str] = status

    def get_stats(self):
        total_days = len(self.attendance_history)
        if total_days == 0:
            return "0% (0/0)"
        
        present_count = list(self.attendance_history.values()).count("Present")
        percentage = (present_count / total_days) * 100
        return f"{percentage:.1f}% ({present_count}/{total_days})"

class AttendanceTrackerApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Student Attendance Tracker (Python/Tkinter)")
        self.geometry("800x600")

        self.students = [
            Student(1, "Alice Smith"),
            Student(2, "Bob Jones"),
            Student(3, "Charlie Day"),
            Student(4, "Diana Prince")
        ]
        self.next_id = 5
        self.current_date_str = datetime.date.today().strftime("%Y-%m-%d")

        self.create_widgets()

    def create_widgets(self):
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.tab_daily = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_daily, text="Daily Entry")
        self.setup_daily_tab()

        self.tab_stats = ttk.Frame(self.notebook)
        self.notebook.add(self.tab_stats, text="Roster & Statistics")
        self.setup_stats_tab()

    def setup_daily_tab(self):
        control_frame = ttk.Frame(self.tab_daily, padding="5 10")
        control_frame.pack(fill=tk.X)

        ttk.Label(control_frame, text="Select Date:").pack(side=tk.LEFT, padx=5)
        
        self.cal = DateEntry(control_frame, width=12, background='darkblue', 
                             foreground='white', borderwidth=2, date_pattern='y-mm-dd')
        self.cal.pack(side=tk.LEFT, padx=5)
        
        self.cal.bind("<<DateEntrySelected>>", lambda e: self.refresh_daily_table())

        tree_frame = ttk.Frame(self.tab_daily)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ("id", "name", "status")
        self.daily_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.daily_tree.heading("id", text="ID")
        self.daily_tree.heading("name", text="Name")
        self.daily_tree.heading("status", text="Status")
        
        self.daily_tree.column("id", width=50, anchor="center")
        self.daily_tree.column("name", width=300)
        self.daily_tree.column("status", width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.daily_tree.yview)
        self.daily_tree.configure(yscroll=scrollbar.set)
        
        self.daily_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        btn_frame = ttk.Frame(self.tab_daily, padding="10")
        btn_frame.pack(fill=tk.X)

        ttk.Button(btn_frame, text="Mark Present", command=lambda: self.mark_selection("Present")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Mark Absent", command=lambda: self.mark_selection("Absent")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Mark Late", command=lambda: self.mark_selection("Late")).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Clear Status", command=lambda: self.mark_selection(None)).pack(side=tk.LEFT, padx=5)

        self.refresh_daily_table()

    def setup_stats_tab(self):
        add_frame = ttk.Frame(self.tab_stats, padding="5 10")
        add_frame.pack(fill=tk.X)

        ttk.Label(add_frame, text="New Student Name:").pack(side=tk.LEFT, padx=5)
        self.new_student_var = tk.StringVar()
        ttk.Entry(add_frame, textvariable=self.new_student_var, width=30).pack(side=tk.LEFT, padx=5)
        ttk.Button(add_frame, text="Add Student", command=self.add_student).pack(side=tk.LEFT, padx=5)

        tree_frame = ttk.Frame(self.tab_stats)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        columns = ("id", "name", "rate")
        self.stats_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        self.stats_tree.heading("id", text="ID")
        self.stats_tree.heading("name", text="Name")
        self.stats_tree.heading("rate", text="Attendance Rate")

        self.stats_tree.column("id", width=50, anchor="center")
        self.stats_tree.column("name", width=300)
        self.stats_tree.column("rate", width=150)

        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.stats_tree.yview)
        self.stats_tree.configure(yscroll=scrollbar.set)

        self.stats_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        refresh_frame = ttk.Frame(self.tab_stats, padding="10")
        refresh_frame.pack(fill=tk.X)
        ttk.Button(refresh_frame, text="Refresh Statistics", command=self.refresh_stats_table).pack(side=tk.RIGHT)

        self.refresh_stats_table()


    def refresh_daily_table(self):
        for item in self.daily_tree.get_children():
            self.daily_tree.delete(item)

        date_key = self.cal.get_date().strftime("%Y-%m-%d")
        
        for student in self.students:
            status = student.get_status(date_key)
            self.daily_tree.insert("", tk.END, iid=student.id, values=(student.id, student.name, status))

    def refresh_stats_table(self):
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)

        for student in self.students:
            stats = student.get_stats()
            self.stats_tree.insert("", tk.END, values=(student.id, student.name, stats))

    def mark_selection(self, status):
        selected_items = self.daily_tree.selection()
        if not selected_items:
            messagebox.showwarning("Selection Error", "Please select a student from the list.")
            return

        date_key = self.cal.get_date().strftime("%Y-%m-%d")

        for item_id in selected_items:
            student_id = int(item_id)
            student = next((s for s in self.students if s.id == student_id), None)
            
            if student:
                student.set_status(date_key, status)
                current_values = self.daily_tree.item(item_id, "values")
                new_status = status if status else "Not Marked"
                self.daily_tree.item(item_id, values=(current_values[0], current_values[1], new_status))

        self.refresh_stats_table()

    def add_student(self):
        name = self.new_student_var.get().strip()
        if not name:
            messagebox.showwarning("Input Error", "Please enter a name.")
            return

        new_student = Student(self.next_id, name)
        self.students.append(new_student)
        self.next_id += 1
        
        self.new_student_var.set("")
        
        self.refresh_daily_table()
        self.refresh_stats_table()
        messagebox.showinfo("Success", f"{name} added to roster.")

if __name__ == "__main__":
    app = AttendanceTrackerApp()
    app.mainloop()
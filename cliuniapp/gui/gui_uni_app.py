import tkinter as tk
from tkinter import messagebox
import random
from ..models.database import Database
from ..models.student import Student


class GUIUniApp(tk.Tk):
    def __init__(self, db_path: str = "students.data"):
        super().__init__()
        self.title("GUIUniApp - Login")
        self.geometry("420x260")
        self.db = Database(db_path)
        self.student = None
        self._build_login()

    def _build_login(self):
        self._clear()
        tk.Label(self, text="Student Login", font=("Arial", 14, "bold")).pack(pady=8)

        frm = tk.Frame(self)
        frm.pack(pady=10)

        tk.Label(frm, text="Email:").grid(row=0, column=0, sticky="e")
        self.email_var = tk.StringVar()
        tk.Entry(frm, textvariable=self.email_var, width=32).grid(row=0, column=1, padx=6)

        tk.Label(frm, text="Password:").grid(row=1, column=0, sticky="e")
        self.pw_var = tk.StringVar()
        tk.Entry(frm, textvariable=self.pw_var, show="*", width=32).grid(row=1, column=1, padx=6)

        tk.Button(self, text="Login", command=self._do_login).pack(pady=10)
    def _do_login(self):
        email = self.email_var.get().strip()
        pw = self.pw_var.get().strip()

        if not email or not pw:
            messagebox.showerror("Error", "Login fields cannot be empty.")
            return
        if not Student.is_valid_email(email):
            messagebox.showerror("Error", "Email must end with @university.com")
            return

        stu = self.db.find_by_email(email)
        if not stu or stu.password != pw:
            messagebox.showerror("Error", "Invalid credentials.")
            return

        self.student = stu
        self._build_enrolment()

    def _build_enrolment(self):
        self._clear()
        self.title("GUIUniApp - Enrolment")
        tk.Label(self, text=f"Welcome {self.student.name} (ID {self.student.id})", font=("Arial", 12, "bold")).pack(pady=6)

        btns = tk.Frame(self)
        btns.pack(pady=6)
        tk.Button(btns, text="Enrol Subject", command=self._enrol_subject).grid(row=0, column=0, padx=5)
        tk.Button(btns, text="Show Average", command=self._show_subjects).grid(row=0, column=1, padx=5)

        self.subj_list = tk.Listbox(self, width=60, height=8)
        self.subj_list.pack(pady=8)
        self._refresh_subjects()

    def _enrol_subject(self):
        if not self.student.can_enrol_more():
            messagebox.showwarning("Limit", "You cannot enrol in more than 4 subjects.")
            return

        # Random subject auto-enrolment (same logic as CLI)
        available_subjects = [
            "Data Analytics", "AI Techniques", "Operating Systems",
            "Database Systems", "Networks", "Machine Learning",
            "Software Engineering", "Cyber Security"
        ]

        sub_name = random.choice(available_subjects)
        # sub_id = random.randint(100, 999)
        # mark = random.randint(50, 95)
        # grade = "HD" if mark >= 85 else "D" if mark >= 75 else "C" if mark >= 65 else "P"

        try:
            sub = self.student.enrol_subject(sub_name)
            # sub.id = sub_id
            # sub.mark = mark
            # sub.grade = grade
            self.db.update_student(self.student)
            self._refresh_subjects()
            messagebox.showinfo("Enrolled",
                                f"Enrolled in {sub.name}\n"
                                f"Subject ID: {sub.id}\n"
                                f"Mark: {sub.mark}\nGrade: {sub.grade}\n"
                                f"Total Enrolled: {len(self.student.subjects)}/4")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def _show_subjects(self):
        self._refresh_subjects()
        avg = self.student.average_mark()
        overall = self.student.overall_grade()
        status = "PASS" if self.student.passed() else "FAIL"
        messagebox.showinfo("Subjects Summary", f"Average: {avg:.2f}\nOverall Grade: {overall}\nStatus: {status}")

    def _refresh_subjects(self):
        self.subj_list.delete(0, tk.END)
        if not self.student.subjects:
            self.subj_list.insert(tk.END, "No subjects enrolled.")
        else:
            for s in self.student.subjects:
                self.subj_list.insert(tk.END, f"{s.id}: {s.name} | Mark={s.mark} | Grade={s.grade}")

    def _clear(self):
        for w in self.winfo_children():
            w.destroy()


if __name__ == "__main__":
    app = GUIUniApp()
    app.mainloop()
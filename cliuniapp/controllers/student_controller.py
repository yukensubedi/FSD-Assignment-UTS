
from __future__ import annotations
from typing import Optional
from getpass import getpass
from ..models.database import Database
from ..models.student import Student

class StudentController:
    def __init__(self, db: Database):
        self.db = db
        self.logged_in: Optional[Student] = None

    def menu(self):
        while True:
            print("\nStudent System")
            print("(l) login")
            print("(r) register")
            print("(x) exit")
            choice = input("Choose an option: ").strip().lower()
            if choice == 'l':
                self.login()
            elif choice == 'r':
                self.register()
            elif choice == 'x':
                break
            else:
                print("Invalid option.")

    def register(self):
        print("\n-- Register --")
        name = input("Full Name: ").strip()
        email = input("Email (must end with @university.com): ").strip()
        password = getpass("Password: ").strip()

        if not Student.is_valid_email(email):
            print("Invalid email format (must end with @university.com).")
            return
        if not Student.is_valid_password(password):
            print("Invalid password format: start with uppercase, 5+ letters total, ends with 3+ digits.")
            return
        new_stu = Student(name=name, email=email, password=password)
        if self.db.add_student(new_stu):
            print(f"Registered successfully with ID: {new_stu.id}")
        else:
            print("Student already exists with this email.")

    def login(self):
        print("\n-- Login --")
        email = input("Email: ").strip()
        password = getpass("Password: ").strip()

        stu = self.db.find_by_email(email)
        if not stu:
            print("No such registered student.")
            return
        if stu.password != password:
            print("Incorrect password.")
            return

        self.logged_in = stu
        print(f"Welcome {stu.name} (ID: {stu.id})")
        self.subject_enrolment_menu()

    def subject_enrolment_menu(self):
        assert self.logged_in is not None
        while True:
            print("\nSubject Enrolment System")
            print("(c) change password")
            print("(e) enrol subject")
            print("(r) remove subject")
            print("(s) show enrolled subjects")
            print("(x) exit")
            choice = input("Choose an option: ").strip().lower()

            if choice == 'c':
                self.change_password()
            elif choice == 'e':
                self.enrol_subject()
            elif choice == 'r':
                self.remove_subject()
            elif choice == 's':
                self.show_enrolments()
            elif choice == 'x':
                # persist any changes before leaving
                self.db.update_student(self.logged_in)
                print("Exiting to Student menu.")
                break
            else:
                print("Invalid option.")

    def change_password(self):
        assert self.logged_in is not None
        new_pw = getpass("New Password: ").strip()
        try:
            self.logged_in.change_password(new_pw)
            self.db.update_student(self.logged_in)
            print("Password updated.")
        except ValueError as e:
            print(f"Error: {e}")

    def enrol_subject(self):
        assert self.logged_in is not None
        if not self.logged_in.can_enrol_more():
            print("You already have 4 subjects.")
            return
        name = input("Subject name: ").strip()
        try:
            sub = self.logged_in.enrol_subject(name)
            self.db.update_student(self.logged_in)
            print(f"Enrolled in {sub.name} [ID {sub.id}] | Mark={sub.mark}, Grade={sub.grade}")
            print(f"New average: {self.logged_in.average_mark():.2f}")
        except ValueError as e:
            print(f"Error: {e}")

    def remove_subject(self):
        assert self.logged_in is not None
        sid = input("Enter Subject ID to remove: ").strip()
        if self.logged_in.remove_subject(sid):
            self.db.update_student(self.logged_in)
            print("Subject removed.")
        else:
            print("No such subject ID.")

    def show_enrolments(self):
        assert self.logged_in is not None
        if not self.logged_in.subjects:
            print("No subjects enrolled.")
            return
        print("\nYour Subjects:")
        for s in self.logged_in.subjects:
            print(f"- {s.id}: {s.name} | Mark={s.mark}, Grade={s.grade}")
        print(f"Average: {self.logged_in.average_mark():.2f} | Overall Grade: {self.logged_in.overall_grade()} | {'PASS' if self.logged_in.passed() else 'FAIL'}")


from __future__ import annotations
from collections import defaultdict
from ..models.database import Database

class AdminController:
    def __init__(self, db: Database):
        self.db = db

    def menu(self):
        while True:
            print("\nAdmin System")
            print("(s) show all students")
            print("(g) group students by grade")
            print("(p) partition students PASS/FAIL")
            print("(r) remove student by ID")
            print("(c) clear database")
            print("(x) exit")
            choice = input("Choose an option: ").strip().lower()

            if choice == 's':
                self.show_all()
            elif choice == 'g':
                self.group_by_grade()
            elif choice == 'p':
                self.partition_pass_fail()
            elif choice == 'r':
                self.remove_student()
            elif choice == 'c':
                self.clear_database()
            elif choice == 'x':
                break
            else:
                print("Invalid option.")

    def show_all(self):
        students = self.db.list_students()
        if not students:
            print("No students in the database.")
            return
        print("\nAll Students:")
        for s in students:
            print(f"- ID:{s.id} | {s.name} | {s.email} | Avg={s.average_mark():.2f} | Grade={s.overall_grade()} | {'PASS' if s.passed() else 'FAIL'}")

    def group_by_grade(self):
        students = self.db.list_students()
        buckets = defaultdict(list)
        for s in students:
            buckets[s.overall_grade()].append(s)
        if not students:
            print("No students in the database.")
            return
        print("\nGrouped by Grade:")
        for grade in sorted(buckets.keys(), reverse=True):
            print(f"{grade}:")
            for s in buckets[grade]:
                print(f"  - ID:{s.id} | {s.name} | Avg={s.average_mark():.2f}")

    def partition_pass_fail(self):
        students = self.db.list_students()
        passed = [s for s in students if s.passed()]
        failed = [s for s in students if not s.passed()]
        print("\nPASS:")
        for s in passed:
            print(f"  - ID:{s.id} | {s.name} | Avg={s.average_mark():.2f}")
        print("FAIL:")
        for s in failed:
            print(f"  - ID:{s.id} | {s.name} | Avg={s.average_mark():.2f}")

    def remove_student(self):
        sid = input("Enter Student ID to remove: ").strip()
        if self.db.remove_student_by_id(sid):
            print("Student removed.")
        else:
            print("No student with that ID.")

    def clear_database(self):
        confirm = input("Type 'CLEAR' to remove ALL students: ").strip()
        if confirm == "CLEAR":
            self.db.clear_all()
            print("All students cleared.")
        else:
            print("Cancelled.")




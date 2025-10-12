
from __future__ import annotations
from ..models.database import Database
from .student_controller import StudentController
from .admin_controller import AdminController

class UniversitySystem:
    def __init__(self, db_path: str = "students.data"):
        self.db = Database(db_path)
        self.student_controller = StudentController(self.db)
        self.admin_controller = AdminController(self.db)

    def menu(self):
        while True:
            print("\nUniversity System:")
            print("(A) Admin")
            print("(S) Student")
            print("(X) Exit")
            choice = input("Choose an option: ").strip().lower()
            if choice == 'a':
                self.admin_controller.menu()
            elif choice == 's':
                self.student_controller.menu()
            elif choice == 'x':
                print("Goodbye.")
                break
            else:
                print("Invalid option.")

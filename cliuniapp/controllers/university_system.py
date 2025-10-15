from __future__ import annotations
from ..models.database import Database
from .student_controller import StudentController
from .admin_controller import AdminController
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

class UniversitySystem:
    def __init__(self, db_path: str = "students.data"):
        self.db = Database(db_path)
        self.student_controller = StudentController(self.db)
        self.admin_controller = AdminController(self.db)

    def menu(self):
        while True:
            choice = input(
                f"{Fore.CYAN}University System: (A)dmin, (S)tudent, or X : {Style.RESET_ALL}"
            ).strip().lower()

            if choice == 'a':
                self.admin_controller.menu()

            elif choice == 's':
                self.student_controller.menu()

            elif choice == 'x':
                print(f"{Fore.YELLOW}Thank You{Style.RESET_ALL}")
                break

            else:
                print(f"{Fore.RED}Invalid option.{Style.RESET_ALL}")

from __future__ import annotations
from collections import defaultdict
from colorama import Fore, Style
from ..models.database import Database


class AdminController:
    def __init__(self, db: Database):
        self.db = db

    def menu(self):
        while True:
            choice = input(
                f"{Fore.CYAN}Admin System (c/g/p/r/s/x): {Style.RESET_ALL}"
            ).strip().lower()

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
                print(f"{Fore.YELLOW}Thank You{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Invalid option.{Style.RESET_ALL}")

    def show_all(self):
        students = self.db.list_students()
        if not students:
            print(f"{Fore.YELLOW}< Nothing to Display >{Style.RESET_ALL}")
            return

        print(f"{Fore.GREEN}Student List{Style.RESET_ALL}")
        for s in students:
            print(
                f"{Fore.CYAN}{s.name}{Style.RESET_ALL} : {s.id} "
                f"{Fore.YELLOW}--> Email:{Style.RESET_ALL} {s.email}"
            )

    def group_by_grade(self):
        students = self.db.list_students()
        if not students:
            print(f"{Fore.YELLOW}< Nothing to Display >{Style.RESET_ALL}")
            return

        buckets = defaultdict(list)
        for s in students:
            buckets[s.overall_grade()].append(s)

        print(f"{Fore.GREEN}Grade Grouping{Style.RESET_ALL}")
        for grade in sorted(buckets.keys(), reverse=True):
            print(f"{Fore.YELLOW}{grade}{Style.RESET_ALL}")
            for s in buckets[grade]:
                print(
                    f"   {Fore.CYAN}-> {s.name}{Style.RESET_ALL} : {s.id} "
                    f"{Fore.YELLOW}==> GRADE:{Style.RESET_ALL} {grade} "
                    f"{Fore.YELLOW}- MARK:{Style.RESET_ALL} {s.average_mark():.2f}"
                )

    def partition_pass_fail(self):
        students = self.db.list_students()
        if not students:
            print(f"{Fore.YELLOW}< Nothing to Display >{Style.RESET_ALL}")
            return

        passed = [s for s in students if s.passed()]
        failed = [s for s in students if not s.passed()]

        print(f"{Fore.GREEN}PASS/FAIL Partition{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}PASS -->{Style.RESET_ALL}", end=" ")
        if passed:
            for s in passed:
                print(
                    f"{Fore.CYAN}{s.name}{Style.RESET_ALL} : {s.id} "
                    f"{Fore.YELLOW}==> GRADE:{Style.RESET_ALL} {s.overall_grade()} "
                    f"{Fore.YELLOW}- MARK:{Style.RESET_ALL} {s.average_mark():.2f}",
                    end=", "
                )
            print()
        else:
            print("[]")

        print(f"{Fore.YELLOW}FAIL -->{Style.RESET_ALL}", end=" ")
        if failed:
            for s in failed:
                print(
                    f"{Fore.CYAN}{s.name}{Style.RESET_ALL} : {s.id} "
                    f"{Fore.YELLOW}==> GRADE:{Style.RESET_ALL} {s.overall_grade()} "
                    f"{Fore.YELLOW}- MARK:{Style.RESET_ALL} {s.average_mark():.2f}",
                    end=", "
                )
            print()
        else:
            print("[]")

    def remove_student(self):
        sid = input(f"{Fore.CYAN}Remove by ID: {Style.RESET_ALL}").strip()

        if self.db.remove_student_by_id(sid):
            print(f"{Fore.YELLOW}Removing Student {sid} Account{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Student {sid} does not exist{Style.RESET_ALL}")

    def clear_database(self):
        print(f"{Fore.YELLOW}Clearing students database{Style.RESET_ALL}")
        confirm = input(
            f"{Fore.RED}Are you sure you want to clear the database (Y)ES/(N)O: {Style.RESET_ALL}"
        ).strip().lower()

        if confirm == 'y' or confirm == 'yes':
            self.db.clear_all()
            print(f"{Fore.GREEN}Students data cleared{Style.RESET_ALL}")
        else:
            print(f"{Fore.YELLOW}Cancelled clearing operation{Style.RESET_ALL}")

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
                f"\t{Fore.CYAN}Admin System (c/g/p/r/s/x): {Style.RESET_ALL}"
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
                break
            else:
                print(f"\t{Fore.RED}Invalid option.{Style.RESET_ALL}")

    def show_all(self):
        students = self.db.list_students()
        print(f"\t{Fore.YELLOW}Student List{Style.RESET_ALL}")
        if not students:
            print(f"\t\t< Nothing to Display >{Style.RESET_ALL}")
            return

        
        for s in students:
            print(
                f"\t{s.name}{Style.RESET_ALL} :: {s.id} "
                f"--> Email:{Style.RESET_ALL} {s.email}"
            )

    def group_by_grade(self):
        students = self.db.list_students()
        print(f"\t{Fore.YELLOW}Grade Grouping{Style.RESET_ALL}")
        if not students:
            print(f"\t\t< Nothing to Display >{Style.RESET_ALL}")
            return

        buckets = defaultdict(list)
        for s in students:
            buckets[s.overall_grade()].append(s)

        
         # Sort grades descending (e.g., HD > D > C > P > Z)
        for grade in sorted(buckets.keys(), reverse=True):
            grade_str = ", ".join(
                [
                    f"{s.name}{Style.RESET_ALL} :: {s.id} --> GRADE:{Style.RESET_ALL} {grade} - MARK:{Style.RESET_ALL} {s.average_mark():.2f}"
                    for s in buckets[grade]
                ]
            )
            print(f"\t{grade} --> [{grade_str}]{Style.RESET_ALL}")
           

    def partition_pass_fail(self):
        students = self.db.list_students()
       

        passed = [s for s in students if s.passed()]
        failed = [s for s in students if not s.passed()]

        print(f"\t{Fore.YELLOW}PASS/FAIL Partition{Style.RESET_ALL}")
        print(f"\tPASS -->{Style.RESET_ALL}", end=" ")
       
        if passed:
            pass_str = ", ".join(
                [
                    f"{s.name}{Style.RESET_ALL} :: {s.id} --> GRADE:{Style.RESET_ALL} {s.overall_grade()} - MARK:{Style.RESET_ALL} {s.average_mark():.2f}"
                    for s in passed
                ]
            )
            print(f"[{pass_str}]{Style.RESET_ALL}")
        else:
            print("[]")

        print(f"\tFAIL -->{Style.RESET_ALL}", end=" ")
       
        if failed:
            fail_str = ", ".join(
                [
                    f"{s.name}{Style.RESET_ALL} :: {s.id} --> GRADE:{Style.RESET_ALL} {s.overall_grade()} - MARK:{Style.RESET_ALL} {s.average_mark():.2f}"
                    for s in failed
                ]
            )
            print(f"[{fail_str}]{Style.RESET_ALL}")
        else:
            print("[]")

    def remove_student(self):
        sid = input(f"\tRemove by ID: {Style.RESET_ALL}").strip()

        if self.db.remove_student_by_id(sid):
            print(f"\t{Fore.YELLOW}Removing Student {sid} Account{Style.RESET_ALL}")
        else:
            print(f"\t{Fore.RED}Student {sid} does not exist{Style.RESET_ALL}")

    def clear_database(self):
        print(f"\t{Fore.YELLOW}Clearing students database{Style.RESET_ALL}")
        confirm = input(
            f"\t{Fore.RED}Are you sure you want to clear the database (Y)ES/(N)O: {Style.RESET_ALL}"
        ).strip().lower()

        if confirm == 'y' or confirm == 'yes':
            self.db.clear_all()
            print(f"\t{Fore.YELLOW}Students data cleared{Style.RESET_ALL}")
        else:
            print(f"\t{Fore.RED}Cancelled clearing operation{Style.RESET_ALL}")
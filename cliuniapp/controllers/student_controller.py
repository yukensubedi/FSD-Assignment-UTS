from __future__ import annotations
from typing import Optional
from getpass import getpass
from colorama import Fore, Style
import random
from ..models.database import Database
from ..models.student import Student


class StudentController:
    def __init__(self, db: Database):
        self.db = db
        self.logged_in: Optional[Student] = None

    def menu(self):
        while True:
            choice = input(
                f"{Fore.CYAN}Student System (l/r/x): {Style.RESET_ALL}"
            ).strip().lower()

            if choice == 'l':
                self.login()
            elif choice == 'r':
                self.register()
            elif choice == 'x':
                break
            else:
                print(f"{Fore.RED}Invalid option.{Style.RESET_ALL}")

    def register(self):
        print(f"{Fore.GREEN}Student Sign Up{Style.RESET_ALL}")
        email = input(f"{Fore.CYAN}Email: {Style.RESET_ALL}").strip()
        password = getpass(f"{Fore.CYAN}Password: {Style.RESET_ALL}").strip()

        if not Student.is_valid_email(email) or not Student.is_valid_password(password):
            print(f"{Fore.RED}Incorrect email or password format{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}email and password formats acceptable{Style.RESET_ALL}")
        name = input(f"{Fore.CYAN}Name: {Style.RESET_ALL}").strip()
        new_stu = Student(name=name, email=email, password=password)

        if self.db.add_student(new_stu):
            print(f"{Fore.GREEN}Enrolling Student {new_stu.name}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Student {new_stu.name} already exists{Style.RESET_ALL}")

    def login(self):
        print(f"{Fore.GREEN}Student Sign In{Style.RESET_ALL}")

        email = input(f"{Fore.CYAN}Email: {Style.RESET_ALL}").strip()
        password = getpass(f"{Fore.CYAN}Password: {Style.RESET_ALL}").strip()

        # Validate format
        if not Student.is_valid_email(email) or not Student.is_valid_password(password):
            print(f"{Fore.RED}Incorrect email or password format{Style.RESET_ALL}")
            return

        print(f"{Fore.YELLOW}email and password formats acceptable{Style.RESET_ALL}")

        stu = self.db.find_by_email(email)
        if not stu:
            print(f"{Fore.RED}Student does not exist{Style.RESET_ALL}")
            return
        if stu.password != password:
            print(f"{Fore.RED}Incorrect password{Style.RESET_ALL}")
            return

        self.logged_in = stu
        print(f"{Fore.YELLOW}Welcome {stu.name} (ID: {stu.id}){Style.RESET_ALL}")
        self.subject_enrolment_menu()

    def subject_enrolment_menu(self):
        assert self.logged_in is not None
        while True:
            choice = input(
                f"{Fore.CYAN}Student Course Menu (c/e/r/s/x): {Style.RESET_ALL}"
            ).strip().lower()

            if choice == 'c':
                self.change_password()
            elif choice == 'e':
                self.enrol_subject()
            elif choice == 'r':
                self.remove_subject()
            elif choice == 's':
                self.show_enrolments()
            elif choice == 'x':
                self.db.update_student(self.logged_in)
                break
            else:
                print(f"{Fore.RED}Invalid option.{Style.RESET_ALL}")

    def change_password(self):
        assert self.logged_in is not None
        print(f"{Fore.YELLOW}Updating Password{Style.RESET_ALL}")

        new_pw = getpass(f"{Fore.CYAN}New Password: {Style.RESET_ALL}").strip()
        confirm_pw = getpass(f"{Fore.CYAN}Confirm Password: {Style.RESET_ALL}").strip()

        if new_pw != confirm_pw:
            print(f"{Fore.RED}Password does not match – Try again{Style.RESET_ALL}")
            return

        if not Student.is_valid_password(new_pw):
            print(f"{Fore.RED}Invalid password format.{Style.RESET_ALL}")
            return

        self.logged_in.change_password(new_pw)
        self.db.update_student(self.logged_in)
        print(f"{Fore.GREEN}Password updated successfully.{Style.RESET_ALL}")

    def enrol_subject(self):
        assert self.logged_in is not None

        if len(self.logged_in.subjects) >= 4:
            print(f"{Fore.RED}students are allowed to enrol in 4 subjects only{Style.RESET_ALL}")
            return

        available_subjects = [
            "Data Analytics", "AI Techniques", "Operating Systems",
            "Database Systems", "Networks", "Machine Learning",
            "Software Engineering", "Cyber Security"
        ]

        sub_name = random.choice(available_subjects)
        sub_id = random.randint(100, 999)
        mark = random.randint(50, 95)

        print(f"{Fore.GREEN}Enrolling in Subject-{sub_id}{Style.RESET_ALL}")

        sub = self.logged_in.enrol_subject(sub_name)
        sub.id = sub_id
        sub.mark = mark
        sub.grade = (
            "HD" if mark >= 85 else
            "D" if mark >= 75 else
            "C" if mark >= 65 else "P"
        )

        self.db.update_student(self.logged_in)
        print(f"{Fore.YELLOW}You are now enrolled in {len(self.logged_in.subjects)} out of 4 subjects{Style.RESET_ALL}")

    def remove_subject(self):
        assert self.logged_in is not None
        sid = input(f"{Fore.CYAN}Remove Subject by ID: {Style.RESET_ALL}").strip()

        removed = False
        for s in list(self.logged_in.subjects):
            if str(s.id) == sid:
                print(f"{Fore.YELLOW}Dropping Subject-{s.id}{Style.RESET_ALL}")
                self.logged_in.subjects.remove(s)
                removed = True
                break

        if removed:
            self.db.update_student(self.logged_in)
            print(f"{Fore.YELLOW}You are now enrolled in {len(self.logged_in.subjects)} out of 4 subjects{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}No such subject found.{Style.RESET_ALL}")

    def show_enrolments(self):
        assert self.logged_in is not None
        subs = self.logged_in.subjects

        print(f"{Fore.YELLOW}Showing {len(subs)} subjects{Style.RESET_ALL}")
        if not subs:
            return

        for s in subs:
            print(f"{Fore.GREEN}| Subject:{s.id} -- mark={s.mark} -- grade={s.grade} |{Style.RESET_ALL}")

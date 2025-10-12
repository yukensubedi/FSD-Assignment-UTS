
from __future__ import annotations
import os
import pickle
from typing import List, Optional
from .student import Student

class Database:
    def __init__(self, path: str = "students.data"):
        self.path = path
        self._ensure_exists()

    def _ensure_exists(self):
        if not os.path.exists(self.path):
            with open(self.path, "wb") as f:
                pickle.dump([], f)

    def _read_all(self) -> List[Student]:
        self._ensure_exists()
        with open(self.path, "rb") as f:
            return pickle.load(f)

    def _write_all(self, students: List[Student]):
        with open(self.path, "wb") as f:
            pickle.dump(students, f)

    # CRUD-like helpers
    def list_students(self) -> List[Student]:
        return self._read_all()

    def find_by_email(self, email: str) -> Optional[Student]:
        for s in self._read_all():
            if s.email.lower() == email.lower():
                return s
        return None

    def find_by_id(self, student_id: str) -> Optional[Student]:
        for s in self._read_all():
            if s.id == student_id:
                return s
        return None

    def add_student(self, student: Student) -> bool:
        students = self._read_all()
        if any(s.email.lower() == student.email.lower() for s in students):
            return False
        students.append(student)
        self._write_all(students)
        return True

    def update_student(self, student: Student) -> None:
        students = self._read_all()
        for i, s in enumerate(students):
            if s.id == student.id:
                students[i] = student
                self._write_all(students)
                return
        # If not found, add
        students.append(student)
        self._write_all(students)

    def remove_student_by_id(self, student_id: str) -> bool:
        students = self._read_all()
        new_students = [s for s in students if s.id != student_id]
        removed = len(new_students) != len(students)
        if removed:
            self._write_all(new_students)
        return removed

    def clear_all(self):
        self._write_all([])

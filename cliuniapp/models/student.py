
from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
import random
import re
from .subject import Subject

EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@university\.com$")

PASSWORD_RE = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")

def _rand_student_id() -> str:
    return f"{random.randint(1, 999_999):06d}"

@dataclass
class Student:
    name: str
    email: str
    password: str
    id: str = field(default_factory=_rand_student_id)
    subjects: List[Subject] = field(default_factory=list)

    MAX_SUBJECTS: int = 4

    @staticmethod
    def is_valid_email(email: str) -> bool:
        return bool(EMAIL_RE.match(email))

    @staticmethod
    def is_valid_password(pw: str) -> bool:
        return bool(PASSWORD_RE.match(pw))

    def can_enrol_more(self) -> bool:
        return len(self.subjects) < self.MAX_SUBJECTS

    def enrol_subject(self, subject_name: str) -> Subject:
        if not self.can_enrol_more():
            raise ValueError("Cannot enrol in more than 4 subjects.")
        sub = Subject(subject_name)
        self.subjects.append(sub)
        return sub

    def remove_subject(self, subject_id: str) -> bool:
        for i, s in enumerate(self.subjects):
            if s.id == subject_id:
                self.subjects.pop(i)
                return True
        return False

    def change_password(self, new_password: str):
        if not self.is_valid_password(new_password):
            raise ValueError("Password does not satisfy required pattern.")
        self.password = new_password

    def average_mark(self) -> float:
        if not self.subjects:
            return 0.0
        return sum(s.mark for s in self.subjects) / len(self.subjects)

    def passed(self) -> bool:
        return self.average_mark() >= 50

    def overall_grade(self) -> str:
        avg = self.average_mark()
        if avg >= 75:
            return "D"
        elif avg >= 65:
            return "C"
        elif avg >= 50:
            return "P"
        return "Z"

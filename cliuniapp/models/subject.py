
from dataclasses import dataclass, field
import random

def _rand_subject_id() -> str:
    return f"{random.randint(1, 999):03d}"

def _grade_from_mark(mark: int) -> str:
    if mark >= 75:
        return "D"
    elif mark >= 65:
        return "C"
    elif mark >= 50:
        return "P"
    return "Z"

@dataclass
class Subject:
    name: str
    id: str = field(default_factory=_rand_subject_id)
    mark: int = field(default_factory=lambda: random.randint(25, 100))
    grade: str = field(init=False)

    def __post_init__(self):
        self.grade = _grade_from_mark(self.mark)

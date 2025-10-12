
from dataclasses import dataclass, field
import random

def _rand_subject_id() -> str:
    return f"{random.randint(1, 999):03d}"

def _grade_from_mark(mark: int) -> str:
    # Grade bands (adjust if your rubric differs)
    # HD: 85-100, D: 75-84, C: 65-74, P: 50-64, F: <50
    if mark >= 85:
        return "HD"
    if mark >= 75:
        return "D"
    if mark >= 65:
        return "C"
    if mark >= 50:
        return "P"
    return "F"

@dataclass
class Subject:
    name: str
    id: str = field(default_factory=_rand_subject_id)
    mark: int = field(default_factory=lambda: random.randint(25, 100))
    grade: str = field(init=False)

    def __post_init__(self):
        self.grade = _grade_from_mark(self.mark)

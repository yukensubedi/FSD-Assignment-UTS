# seed_demo.py
from cliuniapp.models.database import Database
from cliuniapp.models.student import Student

def seed(db_path="students.data"):
    db = Database(db_path)

    # name, email (must end with @university.com per spec), password (Uppercase + ≥5 letters + ≥3 digits)
    records = [
        ("Alice Smith", "alice.smith@university.com", "AlphaFive123",
         ["Math 101", "Physics 102", "Programming 1"]),
        ("Bob Johnson", "bob.johnson@university.com", "BraveHeart123",
         ["Chemistry 101", "Data Science 101", "Algorithms", "Networks"]),
        ("Cara Patel", "cara.patel@university.com", "CamelCase123",
         ["UX 101"]),
        ("David Nguyen", "david.nguyen@university.com", "DeltaForce123",
         []),
        ("Emily Zhang", "emily.zhang@university.com", "EchoWorld123",
         ["Databases", "Operating Systems", "Discrete Math", "AI 101"]),
    ]

    created = 0
    updated = 0

    for name, email, pw, subjects in records:
        s = db.find_by_email(email)
        if not s:
            s = Student(name=name, email=email, password=pw)
            # Enrol up to 4 subjects; mark & grade are auto-random/derived on enrol
            for sub in subjects[:Student.MAX_SUBJECTS]:
                s.enrol_subject(sub)
            db.add_student(s)
            created += 1
        else:
            # Top up enrolments if demo was run before (idempotent-ish)
            existing = {subj.name for subj in s.subjects}
            for sub in subjects:
                if sub not in existing and s.can_enrol_more():
                    s.enrol_subject(sub)
            db.update_student(s)
            updated += 1

    print(f"Seeding complete. Created={created}, Updated={updated}")

if __name__ == "__main__":
    seed()

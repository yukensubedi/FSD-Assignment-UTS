from .controllers.university_system import UniversitySystem

def main():
    app = UniversitySystem(db_path="students.data")
    app.menu()

if __name__ == "__main__":
    main()

# 🎓 CLIUniApp & GUIUniApp

University Application System — built for UTS FSD Assignment 1 (Part 2 & 3).

This project includes:
- **CLI Application** for Students and Admins  
- **GUI Application** (Tkinter) for the challenge task  

---

## 🧰 Requirements
- Python **3.10+**
- `tkinter` (comes with most Python installs)

---

## 🏃 How to Run

### ▶️ CLI Application
Run this from the **parent folder** (where `cliuniapp` is located):

```bash
python -m cliuniapp.main
```

**Menus:**
```
(A) Admin
(S) Student
(X) Exit
```

**Student Registration Rules:**
- Email must end with `@university.com`
- Password must:
  - Start with an uppercase letter  
  - Contain at least 5 letters  
  - End with 3 or more digits  
  - Example: `YukenSubedi123`

---

### 🖥️ GUI Application
To launch the Tkinter GUI version:

```bash
python -m cliuniapp.gui.gui_uni_app
```

**Features:**
- Student login using `students.data`
- Enrol in up to 4 subjects  
- View subjects, marks, grades  
- Change password  
- Error popups for invalid input or over-enrolment

---

## 📁 Folder Structure
```
FSD-Assignment-UTS/
├── README.md
├── students.data
└── cliuniapp/
    ├── main.py
    ├── controllers/
    ├── models/
    └── gui/
```

---

## 🧾 Notes
- All student and subject data is stored in `students.data`
- Use **Admin → Clear Database** or delete the file to reset
- Works on Windows, macOS, and Linux

---

**© 2025 University of Technology Sydney – FSD Assignment 1**

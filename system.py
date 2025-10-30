import csv
import os

MASTERLIST_FILE = "masterlist.csv"
COURSES = ["BSHM", "BSED", "BSCS/ACT", "BEED"]
SECTIONS = [
    "1A", "1B", "1C", "1D",
    "2A", "2B", "2C", "2D",
    "3A", "3B", "3C", "3D",
    "4A", "4B", "4C", "4D"
]
MAX_STUDENTS_PER_SECTION = 50

# Predefined subjects for regular students based on their year level and course
REGULAR_SUBJECTS = {
    "BSHM": {
        1: {"1st_sem": ["Introduction to Hospitality", "Basic Culinary Arts"],
            "2nd_sem": ["Fundamentals of Tourism", "Food and Beverage Service"]},
        2: {"1st_sem": ["Food and Beverage Management", "Introduction to Tourism"],
            "2nd_sem": ["Advanced Culinary Arts", "Hospitality Accounting"]},
        3: {"1st_sem": ["Hotel Operations", "Tourism Marketing"],
            "2nd_sem": ["Advanced Hospitality Management", "Event Planning"]},
        4: {"1st_sem": ["Internship", "Hospitality Research"],
            "2nd_sem": ["Advanced Hospitality Leadership", "Capstone Project"]},
    },
    "BSED": {
        1: {"1st_sem": ["Introduction to Education", "Child Development"],
            "2nd_sem": ["Principles of Teaching", "Educational Psychology"]},
        2: {"1st_sem": ["Teaching Methods", "Curriculum Design"],
            "2nd_sem": ["Classroom Management", "Inclusive Education"]},
        3: {"1st_sem": ["Educational Leadership", "Research Methods"],
            "2nd_sem": ["Instructional Design", "Assessment Techniques"]},
        4: {"1st_sem": ["Student Teaching", "Advanced Pedagogy"],
            "2nd_sem": ["Capstone Project", "Educational Technology"]},
    },
    "BSCS/ACT": {
        1: {"1st_sem": ["Introduction to Programming", "Discrete Mathematics"],
            "2nd_sem": ["Object-Oriented Programming", "Web Development"]},
        2: {"1st_sem": [
                "The Entrepreneurial Mind",
                "Physical Activities Towards Health and Fitness 3",
                "Application Development and Emerging Technologies",
                "Discrete Structures 2",
                "Architecture and Organizations",
                "Algorithms and Complexity",
                "Information Management",
                "Life, Works and Writings of Rizal"
            ],
            "2nd_sem": ["Database Management", "Software Engineering"]},
        3: {"1st_sem": ["Computer Networks", "Operating Systems"],
            "2nd_sem": ["Software Testing", "Artificial Intelligence"]},
        4: {"1st_sem": [
                "Software Engineering 2",
                "Automata Theory and Formal Languages",
                "CS Thesis Writing 1",
                "Network and Communications 2",
                "Robotics",
                "Foreign Language"
            ],
            "2nd_sem": ["Advanced Programming Techniques", "Capstone Project"]},
    },
    "BEED": {
        1: {"1st_sem": ["Fundamentals of Education", "Child Development"],
            "2nd_sem": ["Educational Psychology", "Philosophy of Education"]},
        2: {"1st_sem": ["Curriculum Design", "Instructional Methods"],
            "2nd_sem": ["Educational Technology", "Classroom Management"]},
        3: {"1st_sem": ["Special Education", "Inclusive Education"],
            "2nd_sem": ["Assessment Strategies", "Educational Leadership"]},
        4: {"1st_sem": ["Student Teaching", "Research Methods"],
            "2nd_sem": ["Capstone Project", "Educational Policy"]},
    },
}

# === Validation Functions ===
def validate_contact_number(number):
    return number.isdigit() and len(number) == 11

def validate_email(email):
    return email.endswith("@gmail.com")

# === File Handling ===
def load_masterlist():
    if not os.path.exists(MASTERLIST_FILE):
        return []
    with open(MASTERLIST_FILE, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def save_masterlist(data):
    with open(MASTERLIST_FILE, mode="w", newline="") as f:
        fieldnames = ["student_number", "name", "contact_number", "email", "course", "section", "year_level", "regular_irregular", "subjects"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

# === Helper Functions ===
def generate_student_number(masterlist):
    last_number = masterlist[-1]["student_number"] if masterlist else "2025-0000"
    last_number = int(last_number.split("-")[1])
    return f"2025-{last_number + 1:04d}"

def get_section_enrollment(masterlist, course, section):
    return sum(1 for s in masterlist if s.get("course") == course and s.get("section") == section)

def auto_assign_section(masterlist, course, year_level):
    start_idx = (year_level - 1) * 4
    sections = SECTIONS[start_idx:start_idx + 4]
    for section in sections:
        if get_section_enrollment(masterlist, course, section) < MAX_STUDENTS_PER_SECTION:
            return section
    return None

# === Enrollment Process ===
def enroll_student(masterlist):
    print("\n=== Student Enrollment ===")
    name = input("Enter student name: ").strip()

    while True:
        contact_number = input("Enter contact number (11 digits): ").strip()
        if validate_contact_number(contact_number):
            break
        print("❌ Invalid contact number. Must be 11 digits.")

    while True:
        email = input("Enter email (must end with '@gmail.com'): ").strip()
        if validate_email(email):
            break
        print("❌ Invalid email. Must end with '@gmail.com'.")

    student_number = generate_student_number(masterlist)
    print(f"✅ Assigned Student Number: {student_number}")

    while True:
        print("\nAvailable Courses:")
        for idx, c in enumerate(COURSES, 1):
            print(f"{idx}. {c}")
        choice = input("Select your course (1-4): ").strip()
        if choice.isdigit() and 1 <= int(choice) <= 4:
            course = COURSES[int(choice) - 1]
            break
        print("❌ Invalid choice. Please select a valid course.")

    while True:
        year_level = input("Enter year level (1-4): ").strip()
        if year_level.isdigit() and 1 <= int(year_level) <= 4:
            year_level = int(year_level)
            break
        print("❌ Invalid year level. Please enter 1–4.")

    while True:
        regular_irregular = input("Are you a regular or irregular student? (regular/irregular): ").strip().lower()
        if regular_irregular in ["regular", "irregular"]:
            break
        print("❌ Invalid choice. Type 'regular' or 'irregular'.")

    section = auto_assign_section(masterlist, course, year_level)
    if not section:
        print(f"⚠️ Sorry, all sections for {course} Year {year_level} are full.")
        return
    print(f"✅ Assigned Section: {section}")

    if regular_irregular == "regular":
        subjects_info = REGULAR_SUBJECTS.get(course, {}).get(year_level, {})
        subjects = [sub for sem, subs in subjects_info.items() for sub in subs]
        print(f"\nSubjects for {course} Year {year_level}:")
        for sem, subs in subjects_info.items():
            print(f"  {sem.capitalize()}: {', '.join(subs)}")
    else:
        completed_subjects = []
        print("\nEnter the subjects you have already completed (type 'done' when finished):")
        while True:
            subj = input("Completed Subject: ").strip()
            if subj.lower() == "done":
                break
            if subj:
                completed_subjects.append(subj)

        all_subjects = [sub for sem, subs in REGULAR_SUBJECTS.get(course, {}).get(year_level, {}).items() for sub in subs]
        subjects = [s for s in all_subjects if s not in completed_subjects]
        print(f"\nRemaining subjects: {', '.join(subjects)}")

    student_data = {
        "student_number": student_number,
        "name": name,
        "contact_number": contact_number,
        "email": email,
        "course": course,
        "section": section,
        "year_level": year_level,
        "regular_irregular": regular_irregular,
        "subjects": ", ".join(subjects)
    }

    masterlist.append(student_data)
    save_masterlist(masterlist)
    print(f"\n✅ Student {name} successfully enrolled in {course} - Section {section}.")

    generate_and_submit_report(masterlist, "registrar")
    generate_and_submit_report(masterlist, "librarian")

# === Reports ===
def group_students_by_course_year(masterlist):
    grouped = {}
    for s in masterlist:
        course = s.get("course")
        year_level = int(s.get("year_level", 0))
        reg_irreg = s.get("regular_irregular", "regular")
        key = (course, year_level)
        grouped.setdefault(key, {"regular": [], "irregular": []})
        grouped[key][reg_irreg].append(s)
    return grouped

def generate_and_submit_report(masterlist, role):
    filename = f"{role}_report.csv"
    grouped = group_students_by_course_year(masterlist)
    with open(filename, "w", newline="") as f:
        fieldnames = ["student_number", "name", "contact_number", "email", "course", "section", "year_level", "regular_irregular", "subjects"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for (course, year_level), categories in grouped.items():
            for status, students in categories.items():
                for s in students:
                    writer.writerow(s)
    print(f"📄 {role.capitalize()} report generated and submitted: {filename}")

# === List Students ===
def list_enrolled_students(masterlist):
    if not masterlist:
        print("No students enrolled yet.")
        return
    print("\n=== Enrolled Students ===")
    print(f"{'Student No.':<15}{'Name':<30}{'Course':<10}{'Section':<8}{'Year Level':<12}{'Regular/Irregular':<15}{'Subjects'}")
    print("-" * 120)
    for s in masterlist:
        print(f"{s['student_number']:<15}{s['name']:<30}{s['course']:<10}{s['section']:<8}{s['year_level']:<12}{s['regular_irregular']:<15}{s['subjects']}")
    print("-" * 120)

# === Main ===
def main():
    masterlist = load_masterlist()
    while True:
        print("\nOptions:")
        print("1. Enroll new student")
        print("2. View enrolled students")
        print("3. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            enroll_student(masterlist)
        elif choice == "2":
            list_enrolled_students(masterlist)
        elif choice == "3":
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid option. Try again.")

if __name__ == "__main__":
    main()

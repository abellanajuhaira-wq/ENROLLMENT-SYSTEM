import csv
import os
import shutil
from datetime import datetime

# File paths
MAIN_FILE = "students.csv"
REGISTRAR_FILE = "Registrar/students_masterlist.csv"
LIBRARIAN_FILE = "Librarian/students_masterlist.csv"

# Ensure folders exist
os.makedirs("Registrar", exist_ok=True)
os.makedirs("Librarian", exist_ok=True)

# Generate student number
def generate_student_number():
    if not os.path.exists(MAIN_FILE):
        return "2025-0001"
    with open(MAIN_FILE, "r") as file:
        reader = csv.reader(file)
        next(reader, None)
        rows = list(reader)
        if not rows:
            return "2025-0001"
        last_number = rows[-1][0]
        num = int(last_number.split("-")[1]) + 1
        return f"2025-{num:04d}"

# Assign section automatically
def assign_section(year_level):
    sections = ["A", "B", "C", "D"]
    counts = {f"{year_level}{sec}": 0 for sec in sections}

    if os.path.exists(MAIN_FILE):
        with open(MAIN_FILE, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                section = row["Section"]
                if section.startswith(str(year_level)):
                    counts[section] += 1

    for sec, count in counts.items():
        if count < 40:
            return sec
    return f"{year_level}D"

# Subject Database (simplified with 3 units default)
SUBJECTS = {
    "BSHM": {
        "1": {
            "1": ["NSTP 1", "GEI 1", "ABM 1", "PATHFIT 1", "GE 8"],
            "2": ["Quality Service Management in Tourism and Hospitality",
                  "Philippine Culture and Tourism Geography",
                  "Kitchen Essentials and Basic Food Preparation",
                  "Housekeeping Operations",
                  "NSTP 2"]
        },
        "2": {
            "1": ["HPC 3", "ABM 3", "GE 4", "FL 1", "HMPE 1 LEC"],
            "2": ["Science, Technology, and Society", "Ethics", "Front Office Operations",
                  "Bar and Beverage Management", "Legal Aspects in Tourism and Hospitality"]
        },
        "3": {
            "1": ["BME 1", "RES 101", "HMPE 4", "HMPE 3", "THC 7"],
            "2": ["Strategic Management in Tourism and Hospitality", "Asian Cuisine",
                  "Multicultural Diversity in the Workplace", "Entrepreneurship in Tourism and Hospitality",
                  "Research Methods in Hospitality Management"]
        },
        "4": {
            "1": ["HPC 9", "HMPE 6 LEC", "HMPE 6", "HMPE 8", "HMPE 7", "GE 9"],
            "2": ["Practicum 2 (600 Hours)", "Professional Development and Applied Ethics",
                  "Trends and Issues in Hospitality Industry", "Hospitality Facilities Planning and Design",
                  "Event Management and Catering Services"]
        }
    },
    "BSCS": {
        "1": {
            "1": ["Fundamentals of Programming", "Introduction to Computing", "Literacy/Civic Welfare/Military Science 1",
                  "Physical Education 1", "Art Appreciation", "Ethics", "Mathematics in the Modern World"],
            "2": ["CCS 1201 Intermediate Programming", "Analysis 1 for CS", "Social and Professional Issues in Computing",
                  "Literacy/Civic Welfare/Military Science 2", "Physical Education 2", "Purposive Communication",
                  "Readings in Philippine History", "Understanding the Self"]
        },
        "2": {
            "1": ["Discrete Structures 1", "Object-Oriented Programming", "Data Structures and Algorithms",
                  "Human Computer Interaction", "Information Management", "Analysis 2 for CS",
                  "Physical Education 3", "The Contemporary World"],
            "2": ["Architecture and Organization", "Discrete Structures 2", "Operating Systems",
                  "Statistics for CS", "Information Assurance and Security 1", "Integrative Programming and Technologies 1",
                  "Software Engineering 1", "Physical Education 4"]
        },
        "3": {
            "1": ["Physics for CS (with Electromagnetism)", "Algorithm and Complexity", "Methods of Research for CS",
                  "Networks and Communications", "Software Engineering 2", "Data Analytics", "Multimedia Systems"],
            "2": ["Artificial Intelligence", "Automata Theory and Formal Languages", "Thesis Writing 1 for CS",
                  "Professional Elective 1", "Applications Development and Emerging Technologies",
                  "GE Elective 1", "Effective Communication with Personality Development 3"]
        },
        "4": {
            "1": ["Modeling and Simulation", "Programming Languages", "Thesis Writing 2 for CS",
                  "Professional Elective 2", "Numerical Analysis for ITE", "Science, Technology, and Society",
                  "Life and Works of Rizal"],
            "2": ["Digital Electronics and Logic Design", "Professional Elective 3", "Professional Elective 4",
                  "Technopreneurship", "GE Elective 2", "GE Elective 3"]
        }
    },
    "BEED": {
        "1": {
            "1": ["Understanding the Self", "Mathematics in the Modern World", "Purposive Communication",
                  "Science, Technology, and Society", "The Contemporary World"],
            "2": ["Music in the Elementary Grades", "Art Appreciation", "The Life and Works of Rizal",
                  "Teaching Science in the Elementary Grades", "Teaching Social Studies in the Elementary Grades"]
        },
        "2": {
            "1": ["Facilitating Learner-Centered Teaching", "Foundation of Special and Inclusive Education",
                  "Teaching Science in the Elementary Grades", "Teaching Social Studies in the Elementary Grades",
                  "Teaching Mathematics in the Intermediate Grades"],
            "2": ["Technology for Teaching and Learning 1", "Assessment in Learning 1",
                  "Teaching English in the Elementary Grades", "Pagtuturo ng Filipino sa Elementarya 2",
                  "Teaching Arts in the Elementary Grade"]
        },
        "3": {
            "1": ["Assessment in Learning 2", "The Teaching Profession", "The Teacher and the School Curriculum",
                  "Teaching English in the Elementary Grades through Literature", "Education in Home & Livelihood"],
            "2": ["The Teacher and the Community", "School Culture & Organizational Leadership",
                  "Building and Enhancing New Literacies Across the Curriculum", "Research in Education",
                  "Technology for Teaching and Learning in the Elementary Grades 2", "Indigenous Creative Crafts"]
        },
        "4": {
            "1": ["Observation of Teaching-Learning in Actual School Environment", "Participation and Teaching Assistantship",
                  "Seminar on Professional Education Courses", "Undergraduate Seminar on General Education Courses",
                  "Philippine Education Laws & System with Administration & Supervision Principles"],
            "2": ["Teaching Internship", "Professional Education Seminar", "Action Research Writing",
                  "Trends & Issues in Education", "Professional Development Ethics"]
        }
    },
    "BSED": {
        "1": {
            "1": ["Introduction to Linguistics", "Language, Culture, and Society", "Structures of English",
                  "Children and Adolescent Literature", "Literacy/Civic Welfare/Military Science 1",
                  "Physical Education 1", "Mathematics in the Modern World", "Science, Technology, and Society",
                  "Understanding the Self"],
            "2": ["Contemporary, Popular, and Emergent Literature", "Mythology and Folklore",
                  "The Child and Adolescent Learners and Learning Principles", "Technology for Teaching and Learning 1",
                  "Physical Education 2", "Readings in Philippine History", "Art Appreciation"]
        },
        "2": {
            "2": ["Survey of Literatures", "The Teacher and the Community", "Purposive Communication",
                  "Life and Works of Rizal", "Teaching Strategies in English", "Physical Education 4"]
        },
        "3": {
            "2": ["Assessment of Learning 2", "Teaching English in the Secondary Level", "Curriculum Development",
                  "Educational Technology 2", "Major Elective", "Field Study 2"]
        },
        "4": {
            "2": ["The Teacher and the Community, School Culture, and Organizational Leadership",
                  "Field Study / Teaching Internship", "Professional Electives", "Life and Works of Rizal"]
        }
    }
}

# Save student data
def save_student(data):
    header = ["Student Number", "Name", "Age", "Birthdate", "Sex", "Phone Number", "Emergency Contact",
              "Emergency Number", "Street", "City/Municipality", "Province", "Postal Code",
              "Status", "Nationality", "Course", "Year Level", "Semester", "Section",
              "Subjects", "Total Units"]
    new_file = not os.path.exists(MAIN_FILE)

    with open(MAIN_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        if new_file:
            writer.writerow(header)
        writer.writerow(data)

    shutil.copy(MAIN_FILE, REGISTRAR_FILE)
    shutil.copy(MAIN_FILE, LIBRARIAN_FILE)

# Enrollment process
def enroll_student():
    print("\n--- Student Registration ---")
    student_number = generate_student_number()
    name = input("Full Name: ")
    birthdate_str = input("Birthdate (YYYY-MM-DD): ")
    birthdate = datetime.strptime(birthdate_str, "%Y-%m-%d")
    age = int(input("Age: "))
    if age != (datetime.now().year - birthdate.year):
        print("⚠️ Age and birthdate do not match!")
        return
    sex = input("Sex (M/F): ")
    phone = input("Phone Number (11 digits): ")
    if not (phone.isdigit() and len(phone) == 11):
        print("⚠️ Invalid phone number!")
        return
    emergency_contact = input("Emergency Contact Person: ")
    emergency_number = input("Emergency Contact Number: ")
    street = input("Street Name: ")
    city = input("City/Municipality: ")
    province = input("Province: ")
    postal = input("Postal Code: ")
    if not postal.isdigit():
        print("⚠️ Invalid postal code!")
        return
    status = input("Status: ")
    nationality = input("Nationality: ")

    print("\nCourses Available: BSCS, BSHM, BEED, BSED")
    course = input("Course: ").upper()
    year = input("Year Level (1-4): ")
    sem = input("Semester (1/2): ")

    if course not in SUBJECTS or year not in SUBJECTS[course] or sem not in SUBJECTS[course][year]:
        print("⚠️ Invalid course/year/semester selection.")
        return

    print("\nAvailable Subjects:")
    for subj in SUBJECTS[course][year][sem]:
        print("-", subj)

    subjects_enrolled = []
    while True:
        sub = input("Enter subject to enroll (or 'done' to finish): ").strip()
        if sub.lower() == "done":
            break
        if any(sub.lower() == s.lower() for s in SUBJECTS[course][year][sem]):
            subjects_enrolled.append(sub)
        else:
            print("⚠️ Invalid subject, please type it exactly as shown.")

    total_units = len(subjects_enrolled) * 3
    section = assign_section(year)

    student_data = [student_number, name, age, birthdate_str, sex, phone, emergency_contact,
                    emergency_number, street, city, province, postal, status, nationality,
                    course, year, sem, section, ", ".join(subjects_enrolled), total_units]
    save_student(student_data)
    print(f"\n✅ Enrollment successful! Student number: {student_number}")
    print(f"Assigned Section: {section}")
    print(f"Total Units: {total_units}")

# View all students
def view_students():
    if not os.path.exists(MAIN_FILE):
        print("No students enrolled yet.")
        return
    with open(MAIN_FILE, "r") as file:
        reader = csv.reader(file)
        for row in reader:
            print(row)

# Menu
def main_menu():
    while True:
        print("\n===== ENROLLMENT SYSTEM =====")
        print("1. Enroll New Student")
        print("2. View Student List")
        print("3. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            enroll_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            print("Exiting system...")
            break
        else:
            print("Invalid choice. Try again.")

# Run program
if __name__ == "__main__":
    main_menu()

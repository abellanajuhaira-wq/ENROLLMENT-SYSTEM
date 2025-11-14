import csv
import os
import shutil
import sys
from datetime import datetime

# File paths
MAIN_FILE = "students.csv"
REGISTRAR_FILE = "Registrar/students_masterlist.csv"
LIBRARIAN_FILE = "Librarian/students_masterlist.csv"

# Ensure folders exist
os.makedirs("Registrar", exist_ok=True)
os.makedirs("Librarian", exist_ok=True)

# Room Assignments based on Section
ROOM_ASSIGNMENTS = {
    "1A": "PC-201", "1B": "PC-301", "1C": "PC-302", "1D": "PC-303",
    "2A": "PC-401", "2B": "PC-402", "2C": "PC-403", "2D": "PC-404",
    "3A": "PC-501", "3B": "PC-502", "3C": "PC-503", "3D": "PC-504",
    "4A": "PC-601", "4B": "PC-602", "4C": "PC-603", "4D": "PC-604",
}

# Postal Code Mapping for Philippine Cities/Municipalities
POSTAL_CODES = {
    # Metro Manila
    "Manila": "1000", "Quezon City": "1100", "Caloocan": "1400", "Las Piñas": "1740",
    "Makati": "1200", "Malabon": "1470", "Mandaluyong": "1550", "Marikina": "1800",
    "Muntinlupa": "1770", "Navotas": "1485", "Parañaque": "1700", "Pasay": "1300",
    "Pasig": "1600", "Pateros": "1620", "San Juan": "1500", "Taguig": "1630",
    "Valenzuela": "1440",
    
    
    # Bulacan
    "Malolos": "3000", "Meycauayan": "3020", "San Jose del Monte": "3023",
    "Marilao": "3019", "Bocaue": "3018", "Santa Maria": "3022", "Norzagaray": "3013",
    
    # Cavite
    "Bacoor": "4102", "Imus": "4103", "Dasmariñas": "4114", "Tagaytay": "4120",
    "Cavite City": "4100", "General Trias": "4107", "Trece Martires": "4109",
    
    # Laguna
    "Calamba": "4027", "San Pedro": "4023", "Santa Rosa": "4026", "Biñan": "4024",
    "Los Baños": "4030", "San Pablo": "4000", "Cabuyao": "4025",
    
    # Rizal
    "Antipolo": "1870", "Cainta": "1900", "Taytay": "1920", "Angono": "1930",
    "Binangonan": "1940", "San Mateo": "1850",
    
    # Pampanga
    "Angeles": "2009", "San Fernando": "2000", "Mabalacat": "2010", "Mexico": "2021",
    
    # Batangas
    "Batangas City": "4200", "Lipa": "4217", "Tanauan": "4232", "Calaca": "4212",
    
    # Cebu
    "Cebu City": "6000", "Lapu-Lapu": "6015", "Mandaue": "6014", "Talisay": "6045",
    
    # Davao
    "Davao City": "8000", "Tagum": "8100", "Digos": "8002",
    
    # Iloilo
    "Iloilo City": "5000", "Passi": "5037",
    
    # Baguio
    "Baguio": "2600",
    
    # Cagayan de Oro
    "Cagayan de Oro": "9000",
    
    # Zamboanga
    "Zamboanga City": "7000",
}

def get_postal_code(city, province=""):
    """Get postal code based on city/municipality and province."""
    # Normalize input (remove extra spaces, convert to title case)
    city_normalized = city.strip().title() if city else ""
    province_normalized = province.strip().title() if province else ""
    
    # Try exact city match first
    if city_normalized in POSTAL_CODES:
        return POSTAL_CODES[city_normalized]
    
    # Try case-insensitive match
    for city_key, postal in POSTAL_CODES.items():
        if city_key.lower() == city_normalized.lower():
            return postal
    
    # If not found, return empty string (will be handled as optional)
    return ""

# Subject Database (using codes and names as tuples)
SUBJECTS = {
    "BSHM": {
        "1st Year": {
            "1st Semester": [
                ("NSTP1", "NSTP 1"),
                ("GEI1", "GEI 1"),
                ("ABM1", "ABM 1"),
                ("PF1", "PATHFIT 1"),
                ("GE8", "GE 8")
            ],
            "2nd Semester": [
                ("QSMTH", "Quality Service Management in Tourism and Hospitality"),
                ("PCTG", "Philippine Culture and Tourism Geography"),
                ("KEBFP", "Kitchen Essentials and Basic Food Preparation"),
                ("HO", "Housekeeping Operations"),
                ("NSTP2", "NSTP 2")
            ]
        },
        "2nd Year": {
            "1st Semester": [
                ("HPC3", "HPC 3"),
                ("ABM3", "ABM 3"),
                ("GE4", "GE 4"),
                ("FL1", "FL 1"),
                ("HMPE1L", "HMPE 1 LEC")
            ],
            "2nd Semester": [
                ("STS", "Science, Technology, and Society"),
                ("ETHICS", "Ethics"),
                ("FOO", "Front Office Operations"),
                ("BBM", "Bar and Beverage Management"),
                ("LATVH", "Legal Aspects in Tourism and Hospitality")
            ]
        },
        "3rd Year": {
            "1st Semester": [
                ("BME1", "BME 1"),
                ("RES101", "RES 101"),
                ("HMPE4", "HMPE 4"),
                ("HMPE3", "HMPE 3"),
                ("THC7", "THC 7")
            ],
            "2nd Semester": [
                ("SMTH", "Strategic Management in Tourism and Hospitality"),
                ("AC", "Asian Cuisine"),
                ("MDW", "Multicultural Diversity in the Workplace"),
                ("ETHTH", "Entrepreneurship in Tourism and Hospitality"),
                ("RMHM", "Research Methods in Hospitality Management")
            ]
        },
        "4th Year": {
            "1st Semester": [
                ("HPC9", "HPC 9"),
                ("HMPE6L", "HMPE 6 LEC"),
                ("HMPE6", "HMPE 6"),
                ("HMPE8", "HMPE 8"),
                ("HMPE7", "HMPE 7"),
                ("GE9", "GE 9")
            ],
            "2nd Semester": [
                ("PRAC2", "Practicum 2 (600 Hours)"),
                ("PDAE", "Professional Development and Applied Ethics"),
                ("TIHI", "Trends and Issues in Hospitality Industry"),
                ("HFPD", "Hospitality Facilities Planning and Design"),
                ("EMCS", "Event Management and Catering Services")
            ]
        }
    },
    "BSCS": {
        "1st Year": {
            "1st Semester": [
                ("FOP", "Fundamentals of Programming"),
                ("ITC", "Introduction to Computing"),
                ("LIT1", "Literacy/Civic Welfare/Military Science 1"),
                ("PE1", "Physical Education 1"),
                ("APPR", "Art Appreciation"),
                ("ETHICS", "Ethics"),
                ("MMW", "Mathematics in the Modern World")
            ],
            "2nd Semester": [
                ("CCS1201", "Intermediate Programming"),
                ("A1CS", "Analysis 1 for CS"),
                ("SPI", "Social and Professional Issues in Computing"),
                ("LIT2", "Literacy/Civic Welfare/Military Science 2"),
                ("PE2", "Physical Education 2"),
                ("PC", "Purposive Communication"),
                ("RPH", "Readings in Philippine History"),
                ("UTS", "Understanding the Self")
            ]
        },
        "2nd Year": {
            "1st Semester": [
                ("DS1", "Discrete Structures 1"),
                ("OOP", "Object-Oriented Programming"),
                ("DSA", "Data Structures and Algorithms"),
                ("HCI", "Human Computer Interaction"),
                ("IM", "Information Management"),
                ("A2CS", "Analysis 2 for CS"),
                ("PE3", "Physical Education 3"),
                ("TCC", "The Contemporary World")
            ],
            "2nd Semester": [
                ("AO", "Architecture and Organization"),
                ("DS2", "Discrete Structures 2"),
                ("OS", "Operating Systems"),
                ("SCS", "Statistics for CS"),
                ("IAS1", "Information Assurance and Security 1"),
                ("IPT1", "Integrative Programming and Technologies 1"),
                ("SE1", "Software Engineering 1"),
                ("PE4", "Physical Education 4")
            ]
        },
        "3rd Year": {
            "1st Semester": [
                ("PCS", "Physics for CS (with Electromagnetism)"),
                ("AC", "Algorithm and Complexity"),
                ("MRCS", "Methods of Research for CS"),
                ("NC", "Networks and Communications"),
                ("SE2", "Software Engineering 2"),
                ("DA", "Data Analytics"),
                ("MS", "Multimedia Systems")
            ],
            "2nd Semester": [
                ("AI", "Artificial Intelligence"),
                ("ATFL", "Automata Theory and Formal Languages"),
                ("TW1CS", "Thesis Writing 1 for CS"),
                ("PE1", "Professional Elective 1"),
                ("ADE", "Applications Development and Emerging Technologies"),
                ("GEE1", "GE Elective 1"),
                ("ECPD3", "Effective Communication with Personality Development 3")
            ]
        },
        "4th Year": {
            "1st Semester": [
                ("MS", "Modeling and Simulation"),
                ("PL", "Programming Languages"),
                ("TW2CS", "Thesis Writing 2 for CS"),
                ("PE2", "Professional Elective 2"),
                ("NAITE", "Numerical Analysis for ITE"),
                ("STS", "Science, Technology, and Society"),
                ("LWR", "Life and Works of Rizal")
            ],
            "2nd Semester": [
                ("DELD", "Digital Electronics and Logic Design"),
                ("PE3", "Professional Elective 3"),
                ("PE4", "Professional Elective 4"),
                ("TECHNO", "Technopreneurship"),
                ("GEE2", "GE Elective 2"),
                ("GEE3", "GE Elective 3")
            ]
        }
    },
    "BEED": {
        "1st Year": {
            "1st Semester": [
                ("UTS", "Understanding the Self"),
                ("MMW", "Mathematics in the Modern World"),
                ("PC", "Purposive Communication"),
                ("STS", "Science, Technology, and Society"),
                ("TCC", "The Contemporary World"),
                ("PE1", "Physical Education 1"),
                ("NSTP1", "NSTP 1")
            ],
            "2nd Semester": [
                ("MEG", "Mother Earth and Geography"),
                ("APPR", "Art Appreciation"),
                ("LWR", "Life and Works of Rizal"),
                ("TSE", "Teaching Science in Elementary"),
                ("TSS", "Teaching Social Studies in Elementary"),
                ("PE2", "Physical Education 2"),
                ("NSTP2", "NSTP 2")
            ]
        },
        "2nd Year": {
            "1st Semester": [
                ("FILD1", "Filipino 1"),
                ("ENG1", "English 1"),
                ("MATH1", "Teaching Mathematics in Primary Grades"),
                ("SCI1", "Teaching Science in Primary Grades"),
                ("SS1", "Teaching Social Studies in Primary Grades"),
                ("PE3", "Physical Education 3"),
                ("RPH", "Readings in Philippine History")
            ],
            "2nd Semester": [
                ("FILD2", "Filipino 2"),
                ("ENG2", "English 2"),
                ("MATH2", "Teaching Mathematics in Intermediate Grades"),
                ("SCI2", "Teaching Science in Intermediate Grades"),
                ("SS2", "Teaching Social Studies in Intermediate Grades"),
                ("PE4", "Physical Education 4"),
                ("ETHICS", "Ethics")
            ]
        },
        "3rd Year": {
            "1st Semester": [
                ("FM1", "Facilitating Learner-Centered Teaching"),
                ("CHILD", "Child and Adolescent Development"),
                ("ASSESS1", "Assessment of Learning 1"),
                ("RES1", "Action Research 1"),
                ("PE", "Physical Education for Elementary"),
                ("HEALTH", "Health Education for Elementary"),
                ("MUSIC", "Music Education for Elementary")
            ],
            "2nd Semester": [
                ("FM2", "The Teacher and the School Curriculum"),
                ("ASSESS2", "Assessment of Learning 2"),
                ("RES2", "Action Research 2"),
                ("ART", "Art Education for Elementary"),
                ("VALUES", "Values Education"),
                ("TECH", "Technology for Teaching and Learning"),
                ("READING", "Teaching Reading and Literacy")
            ]
        },
        "4th Year": {
            "1st Semester": [
                ("FIELD", "Field Study 1"),
                ("STU", "Student Teaching"),
                ("PROF", "The Teaching Profession"),
                ("SPED", "Foundation of Special and Inclusive Education"),
                ("MGMT", "Classroom Management"),
                ("PARA", "Building and Enhancing New Literacies")
            ],
            "2nd Semester": [
                ("FIELD2", "Field Study 2"),
                ("PRAC", "Practice Teaching"),
                ("RES3", "Thesis Writing"),
                ("LEAD", "Educational Leadership"),
                ("EVAL", "Educational Evaluation"),
                ("COMM", "Community Extension Services")
            ]
        }
    },
    "BSED": {
        "1st Year": {
            "1st Semester": [
                ("IL", "Introduction to Literature"),
                ("LCS", "Language, Culture, and Society"),
                ("SE", "Structure of English"),
                ("CAL", "Contemporary, Popular, and Emergent Literature"),
                ("LIT1", "Literacy/Civic Welfare/Military Science 1"),
                ("PE1", "Physical Education 1"),
                ("MMW", "Mathematics in the Modern World"),
                ("STS", "Science, Technology, and Society"),
                ("UTS", "Understanding the Self")
            ],
            "2nd Semester": [
                ("CPAEL", "Critical Approaches to Philippine, Asian, and World Literature"),
                ("MFL", "Mythology and Folklore"),
                ("CALLLP", "Creative and Academic Writing and Literary Portfolio"),
                ("TTL1", "Technology for Teaching and Learning 1"),
                ("PE2", "Physical Education 2"),
                ("RPH", "Readings in Philippine History"),
                ("APPR", "Art Appreciation")
            ]
        },
        "2nd Year": {
            "1st Semester": [
                ("FIL1", "Filipino 1"),
                ("ENG1", "English 1"),
                ("LING", "Introduction to Linguistics"),
                ("PHON", "Phonetics and Phonology"),
                ("PE3", "Physical Education 3"),
                ("TCC", "The Contemporary World"),
                ("ETHICS", "Ethics")
            ],
            "2nd Semester": [
                ("FIL2", "Filipino 2"),
                ("ENG2", "English 2"),
                ("MORPH", "Morphology and Syntax"),
                ("SEMANT", "Semantics and Pragmatics"),
                ("PE4", "Physical Education 4"),
                ("LWR", "Life and Works of Rizal"),
                ("PC", "Purposive Communication")
            ]
        },
        "3rd Year": {
            "1st Semester": [
                ("FM1", "Facilitating Learner-Centered Teaching"),
                ("CHILD", "Child and Adolescent Development"),
                ("ASSESS1", "Assessment of Learning 1"),
                ("RES1", "Action Research 1"),
                ("METHOD1", "Methods of Teaching English"),
                ("LIT2", "Literacy/Civic Welfare/Military Science 2")
            ],
            "2nd Semester": [
                ("FM2", "The Teacher and the School Curriculum"),
                ("ASSESS2", "Assessment of Learning 2"),
                ("RES2", "Action Research 2"),
                ("METHOD2", "Advanced Methods of Teaching English"),
                ("TTL2", "Technology for Teaching and Learning 2"),
                ("READING", "Teaching Reading and Writing")
            ]
        },
        "4th Year": {
            "1st Semester": [
                ("FIELD", "Field Study 1"),
                ("STU", "Student Teaching"),
                ("PROF", "The Teaching Profession"),
                ("SPED", "Foundation of Special and Inclusive Education"),
                ("MGMT", "Classroom Management"),
                ("PARA", "Building and Enhancing New Literacies")
            ],
            "2nd Semester": [
                ("FIELD2", "Field Study 2"),
                ("PRAC", "Practice Teaching"),
                ("RES3", "Thesis Writing"),
                ("LEAD", "Educational Leadership"),
                ("EVAL", "Educational Evaluation"),
                ("COMM", "Community Extension Services")
            ]
        }
    }
}


def clear_screen():
    """Clear the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


# ==================== UTILITY FUNCTIONS ====================

def print_separator(char="=", length=80):
    """Print a separator line."""
    print(char * length)


def print_header(title):
    """Print a formatted header."""
    print()
    print("=" * 80)
    print(title.center(80))
    print("=" * 80)
    print()


def print_success(message):
    """Print success message."""
    print(f"SUCCESS: {message}")


def print_error(message):
    """Print error message."""
    print(f"ERROR: {message}")


def print_warning(message):
    """Print warning message."""
    print(f"WARNING: {message}")


def print_info(message):
    """Print info message."""
    print(message)


def print_prompt(message):
    """Print prompt message."""
    print(message, end="")


# ==================== VALIDATION FUNCTIONS ====================

def check_back_command(user_input):
    """Check if user wants to go back to main menu."""
    return user_input.upper() in ["BACK", "CANCEL", "EXIT", "B", "C", "E", "MENU"]

def check_prev_command(user_input):
    """Check if user wants to go back to previous field."""
    return user_input.upper() in ["PREV", "PREVIOUS", "P"]

def get_field_input(prompt, validation_func, error_message, current_value="", is_numeric=False, allow_empty=False):
    """Get input for a field with ability to go back to previous field."""
    while True:
        try:
            if current_value:
                print_prompt(f"{prompt}[Current: {current_value}] (or 'prev' to go back, 'menu' to cancel): ")
            else:
                print_prompt(f"{prompt}(or 'prev' to go back, 'menu' to cancel): ")
            user_input = input().strip()
            
            # Check for menu command
            if check_back_command(user_input):
                return "BACK_TO_MENU"
            
            # Check for previous field command
            if check_prev_command(user_input):
                return "BACK_TO_PREV"
            
            if not user_input:
                if allow_empty:
                    return ""
                if current_value:
                    # If there's a current value and user presses enter, keep it
                    return current_value
                print_error("Input cannot be empty. Please try again.")
                continue

            if is_numeric:
                # Remove common separators for phone numbers
                cleaned_input = user_input.replace("-", "").replace(" ", "").replace("+", "")
                if not cleaned_input.isdigit():
                    print_error("Invalid input. Must contain only numbers. Please try again.")
                    continue
                if validation_func(cleaned_input):
                    return cleaned_input
                else:
                    print_error(error_message)
            else:
                if validation_func(user_input):
                    return user_input
                else:
                    print_error(error_message)
        except KeyboardInterrupt:
            print_error("\nOperation cancelled by user.")
            raise
        except Exception as e:
            print_error(f"An unexpected error occurred: {str(e)}")
            continue


def get_validated_input(prompt, validation_func, error_message, is_numeric=False, allow_empty=False, allow_back=False):
    """Get validated input from user with error handling. Continues on error instead of returning None."""
    while True:
        try:
            print_prompt(prompt)
            user_input = input().strip()
            
            # Check for back command
            if allow_back and check_back_command(user_input):
                return "BACK_TO_MENU"
            
            if not user_input:
                if allow_empty:
                    return ""
                print_error("Input cannot be empty. Please try again.")
                continue

            if is_numeric:
                # Remove common separators for phone numbers
                cleaned_input = user_input.replace("-", "").replace(" ", "").replace("+", "")
                if not cleaned_input.isdigit():
                    print_error("Invalid input. Must contain only numbers. Please try again.")
                    continue
                if validation_func(cleaned_input):
                    return cleaned_input
                else:
                    print_error(error_message)
            else:
                if validation_func(user_input):
                    return user_input
                else:
                    print_error(error_message)
        except KeyboardInterrupt:
            print_error("\nOperation cancelled by user.")
            raise  # Re-raise to handle at higher level
        except Exception as e:
            print_error(f"An unexpected error occurred: {str(e)}")
            continue


def validate_date(date_string):
    """Validate date format YYYY-MM-DD."""
    try:
        datetime.strptime(date_string, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_phone_philippines(phone):
    """Validate Philippine phone number. Must start with 63 (country code) or 09 (local format)."""
    if not phone.isdigit():
        return False
    
    # Remove + if present at start
    if phone.startswith("+"):
        phone = phone[1:]
    
    # Philippine format: 
    # - International: 63XXXXXXXXXX (12 digits, starts with 63)
    # - Local: 09XXXXXXXXX (11 digits, starts with 09)
    if phone.startswith("63") and len(phone) == 12:
        return True
    elif phone.startswith("09") and len(phone) == 11:
        return True
    return False


def validate_phone(phone):
    """Validate phone number for Philippines (63+ or 09 format)."""
    return validate_phone_philippines(phone)


def validate_age(age_str):
    """Validate age is a positive number."""
    try:
        age = int(age_str)
        return age > 0 and age < 150
    except ValueError:
        return False


def format_name(last_name, first_name, middle_initial="", suffix=""):
    """Format name components into full name string (Last Name, First Name M./Middle Suffix)."""
    # Capitalize first letter of each word in last and first names
    last_name_formatted = " ".join(word.capitalize() for word in last_name.split())
    first_name_formatted = " ".join(word.capitalize() for word in first_name.split())
    name_parts = [last_name_formatted]
    
    # Add first name
    first_part = first_name_formatted
    if middle_initial:
        # If it's a single letter, add period (e.g., "M.")
        # If it's longer, treat as full middle name (e.g., "Michael")
        if len(middle_initial.strip()) == 1:
            first_part += f" {middle_initial.upper()}."
        else:
            first_part += f" {middle_initial}"
    name_parts.append(first_part)
    
    # Add suffix if present
    if suffix:
        name_parts.append(suffix)
    
    return ", ".join(name_parts)


# ==================== CORE FUNCTIONS ====================

def generate_student_number():
    """Generate unique student number in format YYYY-####."""
    try:
        if not os.path.exists(MAIN_FILE):
            return "2025-0001"

        with open(MAIN_FILE, "r", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            rows = list(reader)

            if not rows:
                return "2025-0001"

            # Find the highest student number
            last_number = max([row[0] for row in rows if row])
            num = int(last_number.split("-")[1]) + 1
            return f"2025-{num:04d}"
    except Exception as e:
        print_error(f"Error generating student number: {str(e)}")
        return "2025-0001"


def assign_section(year_level):
    """Assign section and room automatically based on capacity (40 students per room)."""
    sections = ["A", "B", "C", "D"]
    MAX_CAPACITY = 40
    
    # Track counts by (section, room) combination
    section_room_counts = {}
    
    try:
        if os.path.exists(MAIN_FILE):
            with open(MAIN_FILE, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    # Skip archived students
                    if row.get("Archived", "No").upper() == "YES":
                        continue
                    
                    section = row.get("Section", "")
                    room = row.get("Room", "")
                    
                    if section.startswith(str(year_level)) and room:
                        key = (section, room)
                        section_room_counts[key] = section_room_counts.get(key, 0) + 1

        # Find first section/room combination with available capacity
        for sec in [f"{year_level}{s}" for s in sections]:
            room = ROOM_ASSIGNMENTS.get(sec, "Room Not Assigned")
            key = (sec, room)
            current_count = section_room_counts.get(key, 0)
            
            if current_count < MAX_CAPACITY:
                return sec

        # If all sections/rooms are full, try to assign to next available section
        # This handles overflow - assign to next section even if it means going beyond normal capacity
        print_warning(f"All rooms for Year {year_level} are at capacity (40 students each).")
        print_warning(f"Assigning to {year_level}D (may exceed capacity).")
        return f"{year_level}D"
    except Exception as e:
        print_error(f"Error assigning section: {str(e)}")
        return f"{year_level}A"


def save_student(data, update_mode=False, student_number=None):
    """Save student data to main file and copy to Registrar and Librarian directories."""
    try:
        header = [
            "Student Number", "Last Name", "First Name", "Middle Initial", "Suffix",
            "Full Name", "Age", "Birthdate", "Sex", "Phone Number",
            "Emergency Contact", "Emergency Number", "Street", "Barangay", "City/Municipality",
            "Province", "Postal Code", "Nationality", "Course",
            "Year Level", "Semester", "Section", "Room", "Subjects", "Total Units", "Archived"
        ]
        
        if update_mode:
            # Update existing student
            if not os.path.exists(MAIN_FILE):
                print_error("No students file found.")
                return False
            
            # Read all students
            students = []
            with open(MAIN_FILE, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                fieldnames = reader.fieldnames
                for row in reader:
                    if row.get("Student Number", "") == student_number:
                        # Update this student's data
                        students.append(data)
                    else:
                        students.append(row)
            
            # Write back to file
            with open(MAIN_FILE, "w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(students)
        else:
            # Add new student
            new_file = not os.path.exists(MAIN_FILE)
            with open(MAIN_FILE, "a", newline="", encoding="utf-8") as file:
                writer = csv.writer(file)
                if new_file:
                    writer.writerow(header)
                writer.writerow(data)

        # Copy to Registrar and Librarian directories
        shutil.copy(MAIN_FILE, REGISTRAR_FILE)
        shutil.copy(MAIN_FILE, LIBRARIAN_FILE)

        print_success("Student data saved and copied to Registrar and Librarian directories.")
        return True
    except Exception as e:
        print_error(f"Error saving student data: {str(e)}")
        return False


# ==================== ENROLLMENT PROCESS ====================

def enroll_student():
    """Main enrollment function with comprehensive validation and improved error handling."""
    # Store all entered data
    data = {}
    current_field = 0
    
    # Field definitions with their prompts and validation
    fields = [
        ("last_name", "Last Name: ", lambda x: len(x.strip()) > 0 and all(c.isalpha() or c in " -'." for c in x), 
         "Last name must contain only letters, spaces, hyphens, apostrophes, or periods.", False, False),
        ("first_name", "First Name: ", lambda x: len(x.strip()) > 0 and all(c.isalpha() or c in " -'." for c in x),
         "First name must contain only letters, spaces, hyphens, apostrophes, or periods.", False, False),
        ("middle_initial", "Middle Initial/Name (Optional, press Enter to skip): ",
         lambda x: len(x) == 0 or (len(x.strip()) > 0 and all(c.isalpha() or c in " -'." for c in x)),
         "Middle initial/name must contain only letters, spaces, hyphens, apostrophes, or periods.", False, True),
        ("suffix", "Suffix (Optional, e.g., Jr., Sr., III - press Enter to skip): ",
         lambda x: len(x) == 0 or (len(x) <= 10 and all(c.isalpha() or c in " .," for c in x)),
         "Suffix must not contain numbers (e.g., Jr., Sr., III) or be empty.", False, True),
        ("sex", "Sex (M/F): ", lambda x: x.upper() in ["M", "F"],
         "Invalid sex. Must be M or F.", False, False),
        ("nationality", "Nationality [Default: Filipino]: ", lambda x: True,
         "", False, True),
    ]
    
    clear_screen()
    print_header("STUDENT ENROLLMENT SYSTEM")
    
    print()
    print("NOTICE: Type 'prev' to go back to previous field, 'menu' to cancel enrollment")
    print()

    try:
        # Generate student number
        student_number = generate_student_number()
        print(f"Student Number: {student_number}")
        print()

        # 1. Name Information (Separated Fields)
        print("BASIC INFORMATION")
        print_separator("-")
        print()
        
        # Process fields with back navigation
        while current_field < len(fields):
            field_key, prompt, validation_func, error_msg, is_numeric, allow_empty = fields[current_field]
            
            # Get current value if exists
            current_value = data.get(field_key, "")
            
            # Special handling for nationality default
            if field_key == "nationality" and not current_value:
                current_value = "Filipino"
            
            result = get_field_input(prompt, validation_func, error_msg, current_value, is_numeric, allow_empty)
            
            if result == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif result == "BACK_TO_PREV":
                if current_field > 0:
                    current_field -= 1
                    clear_screen()
                    print_header("STUDENT ENROLLMENT SYSTEM")
                    print()
                    print(f"Student Number: {student_number}")
                    print()
                    print("BASIC INFORMATION")
                    print_separator("-")
                    print()
                    print_info("Going back to previous field...")
                    print()
                else:
                    print_warning("You are already at the first field.")
                continue
            else:
                # Store the value
                if field_key == "sex":
                    data[field_key] = result.upper()
                elif field_key == "middle_initial" and result:
                    data[field_key] = " ".join(word.capitalize() for word in result.split())
                elif field_key == "nationality":
                    data[field_key] = result or "Filipino"
                else:
                    data[field_key] = result
                current_field += 1
        
        # Format full name
        last_name = data.get("last_name", "")
        first_name = data.get("first_name", "")
        middle_initial = data.get("middle_initial", "")
        suffix = data.get("suffix", "")
        full_name = format_name(last_name, first_name, middle_initial, suffix)
        print_info(f"Full Name: {full_name}")
        print()
        
        sex = data.get("sex", "")
        nationality = data.get("nationality", "Filipino")

        # 2. Personal Details with Validation
        print()
        print("PERSONAL DETAILS")
        print_separator("-")
        print()
        
        birthdate_str = data.get("birthdate", "")
        age = data.get("age", 0)
        
        while True:
            if birthdate_str:
                result = get_field_input("Birthdate (YYYY-MM-DD): ", validate_date,
                                        "Invalid date format. Please use YYYY-MM-DD.", birthdate_str)
            else:
                result = get_field_input("Birthdate (YYYY-MM-DD): ", validate_date,
                                        "Invalid date format. Please use YYYY-MM-DD.", "")
            
            if result == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif result == "BACK_TO_PREV":
                # Re-open BASIC INFORMATION fields for editing (supports full prev navigation)
                current_field = len(fields) - 1
                while current_field < len(fields):
                    field_key, prompt, validation_func, error_msg, is_numeric, allow_empty = fields[current_field]
                    current_value = data.get(field_key, "")
                    if field_key == "nationality" and not current_value:
                        current_value = "Filipino"

                    edit_result = get_field_input(prompt, validation_func, error_msg, current_value, is_numeric, allow_empty)

                    if edit_result == "BACK_TO_MENU":
                        print_info("Returning to main menu...")
                        return
                    elif edit_result == "BACK_TO_PREV":
                        if current_field > 0:
                            current_field -= 1
                        else:
                            print_warning("You are already at the first field.")
                        continue
                    else:
                        if field_key == "sex":
                            data[field_key] = edit_result.upper()
                        elif field_key == "middle_initial" and edit_result:
                            data[field_key] = " ".join(word.capitalize() for word in edit_result.split())
                        elif field_key == "nationality":
                            data[field_key] = edit_result or "Filipino"
                        else:
                            data[field_key] = edit_result
                        current_field += 1

                # Recompute full name after edits and return to birthdate
                last_name = data.get("last_name", "")
                first_name = data.get("first_name", "")
                middle_initial = data.get("middle_initial", "")
                suffix = data.get("suffix", "")
                full_name = format_name(last_name, first_name, middle_initial, suffix)
                print_info(f"Full Name: {full_name}")
                print()
                continue

            try:
                birthdate = datetime.strptime(result, "%Y-%m-%d")
            except ValueError:
                print_error("Invalid date. Please try again.")
                continue

            # Check if birthdate is in the future
            if birthdate > datetime.now():
                print_error("Birthdate cannot be in the future. Please try again.")
                continue

            # Automatically calculate age from birthdate
            today = datetime.now()
            age = today.year - birthdate.year
            
            # Adjust for birthday this year
            if today.month < birthdate.month or (
                today.month == birthdate.month and today.day < birthdate.day
            ):
                age -= 1

            # Validate calculated age
            if age < 1 or age > 150:
                print_error(f"Invalid birthdate. Calculated age ({age}) is out of valid range (1-150).")
                continue

            # Store values
            data["birthdate"] = result
            data["age"] = age
            birthdate_str = result

            # Display calculated age
            print_info(f"Calculated Age: {age} years old")
            break

        # 3. Contact Information
        contact_section_complete = False
        while not contact_section_complete:
            print()
            print("CONTACT INFORMATION")
            print_separator("-")
            print()
            
            phone = get_field_input(
                "Phone Number (Philippines: 63XXXXXXXXXX or 09XXXXXXXXX): ",
                validate_phone,
                "Invalid phone number! Must start with 63 (12 digits) or 09 (11 digits) for Philippines.",
                data.get("phone", ""), True, False
            )
            if phone == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif phone == "BACK_TO_PREV":
                # Go back to birthdate section - restart from there
                break
            data["phone"] = phone
            
            emergency_contact = get_field_input(
                "Emergency Contact Person: ",
                lambda x: True,
                "",
                data.get("emergency_contact", ""), False, True
            )
            if emergency_contact == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif emergency_contact == "BACK_TO_PREV":
                # Go back to phone field
                continue
            if not emergency_contact:
                print_warning("Emergency contact is empty. Please consider providing one.")
            data["emergency_contact"] = emergency_contact

            emergency_number = get_field_input(
                "Emergency Contact Number (Philippines: 63XXXXXXXXXX or 09XXXXXXXXX): ",
                lambda x: validate_phone_philippines(x) or (x.isdigit() and len(x) >= 7),
                "Invalid emergency number. Must be Philippine format (63+ or 09+) or at least 7 digits.",
                data.get("emergency_number", ""), True, False
            )
            if emergency_number == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif emergency_number == "BACK_TO_PREV":
                # Go back to emergency contact field
                continue
            data["emergency_number"] = emergency_number
            contact_section_complete = True
        
        if phone == "BACK_TO_PREV":
            # Restart birthdate section
            data["birthdate"] = ""
            data["age"] = 0
            # This will be handled by going back to birthdate loop
            pass

        # 4. Address Information
        address_section_complete = False
        while not address_section_complete:
            print()
            print("ADDRESS INFORMATION")
            print_separator("-")
            print()
            
            street = get_field_input("Street Name: ", lambda x: True, "", data.get("street", ""), False, True)
            if street == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif street == "BACK_TO_PREV":
                # Go back to contact section
                contact_section_complete = False
                break
            data["street"] = street
            
            barangay = get_field_input("Barangay: ", lambda x: True, "", data.get("barangay", ""), False, True)
            if barangay == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif barangay == "BACK_TO_PREV":
                continue
            data["barangay"] = barangay
            
            city = get_field_input("City/Municipality: ", lambda x: True, "", data.get("city", ""), False, False)
            if city == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif city == "BACK_TO_PREV":
                continue
            data["city"] = city
            
            province = get_field_input("Province: ", lambda x: True, "", data.get("province", ""), False, False)
            if province == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif province == "BACK_TO_PREV":
                continue
            data["province"] = province
            
            # Automatically get postal code based on city/municipality
            postal = get_postal_code(city, province)
            if postal:
                print_info(f"Postal Code automatically assigned: {postal}")
                data["postal"] = postal
            else:
                print_warning(f"Postal code not found for {city}. Please enter manually.")
                postal = get_field_input(
                    "Postal Code (4 digits for Philippines): ",
                    lambda x: x.isdigit() and len(x) == 4,
                    "Invalid postal code. Must be 4 digits.",
                    data.get("postal", ""), False, False
                )
                if postal == "BACK_TO_MENU":
                    print_info("Returning to main menu...")
                    return
                elif postal == "BACK_TO_PREV":
                    continue
                data["postal"] = postal
            address_section_complete = True
        
        if not address_section_complete:
            # Restart contact section if needed
            contact_section_complete = False
            # Note: To go back further, use 'menu' to cancel and start over

        # 5. Course and Year Level Selection
        print()
        print("COURSE SELECTION")
        print_separator("-")
        print()
        print_info(f"Available Courses: {', '.join(SUBJECTS.keys())}")

        while True:
            course_input = get_field_input(
                "Course: ",
                lambda x: x.upper().strip() in SUBJECTS,
                f"Invalid course. Please choose from: {', '.join(SUBJECTS.keys())}",
                data.get("course", ""), False, False
            )
            if course_input == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif course_input == "BACK_TO_PREV":
                address_section_complete = False
                break
            course = course_input.upper().strip()
            if course in SUBJECTS:
                data["course"] = course
                break
        
        year_levels = list(SUBJECTS[course].keys())
        print_info(f"Available Year Levels: {', '.join(year_levels)}")

        while True:
            year_input = get_field_input(
                "Year Level: ",
                lambda x: x.strip() in year_levels,
                f"Invalid year level. Please choose from: {', '.join(year_levels)}",
                data.get("year", ""), False, False
            )
            if year_input == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif year_input == "BACK_TO_PREV":
                # Go back to course selection
                break
            year = year_input.strip()
            if year in year_levels:
                data["year"] = year
                break
        
        semesters = list(SUBJECTS[course][year].keys())
        print_info(f"Available Semesters: {', '.join(semesters)}")

        while True:
            sem_input = get_field_input(
                "Semester: ",
                lambda x: x.strip() in semesters,
                f"Invalid semester. Please choose from: {', '.join(semesters)}",
                data.get("sem", ""), False, False
            )
            if sem_input == "BACK_TO_MENU":
                print_info("Returning to main menu...")
                return
            elif sem_input == "BACK_TO_PREV":
                # Go back to year level - will restart year level selection
                break
            sem = sem_input.strip()
            if sem in semesters:
                data["sem"] = sem
                break
        
        if sem_input == "BACK_TO_PREV":
            # Restart year level selection by continuing the year level loop
            # This will be handled by the year level while loop above
            pass

        # 6. Subject Selection
        print()
        print("SUBJECT ENROLLMENT")
        print_separator("-")
        print()
        course = data.get("course", "")
        year = data.get("year", "")
        sem = data.get("sem", "")
        available_subjects = SUBJECTS[course][year][sem]
        
        print("Available Subjects:")
        for idx, (code, name) in enumerate(available_subjects, 1):
            print(f"  {idx}. {code} - {name}")
        print()

        subjects_enrolled = []
        subject_names_list = []

        while True:
            print_prompt("Enter subject NUMBER to enroll (or 'done' to finish): ")
            sub_input = input().strip()

            if check_back_command(sub_input):
                print_info("Returning to main menu...")
                return

            if sub_input.lower() == "done":
                if not subjects_enrolled:
                    print_error("No subjects were enrolled. Please enroll at least one subject.")
                    continue
                break

            if sub_input.isdigit():
                sel = int(sub_input)
                if 1 <= sel <= len(available_subjects):
                    full_subject = available_subjects[sel - 1]

                    if full_subject not in subjects_enrolled:
                        subjects_enrolled.append(full_subject)
                        subject_names_list.append(f"{full_subject[0]} ({full_subject[1]})")
                        print_success(f"Enrolled in: {full_subject[1]}")
                        print_info(f"Total subjects enrolled: {len(subjects_enrolled)}")
                    else:
                        print_warning(f"Already enrolled in: {full_subject[1]}")
                else:
                    print_error(f"Invalid number. Please choose 1-{len(available_subjects)} or 'done' to finish.")
            else:
                print_error("Invalid input. Enter a number from the list or 'done' to finish.")

        # 7. Final Processing
        print()
        print("FINALIZING ENROLLMENT")
        print_separator("-")
        print()
        
        total_units = len(subjects_enrolled) * 3
        year_level_num = year.replace("st Year", "").replace("nd Year", "").replace("rd Year", "").replace("th Year", "")
        section = assign_section(year_level_num)
        room = ROOM_ASSIGNMENTS.get(section, "Room Not Assigned")

        # Prepare student data with separate name fields
        student_data = [
            student_number, data.get("last_name", ""), data.get("first_name", ""), 
            data.get("middle_initial", ""), data.get("suffix", ""), full_name,
            data.get("age", 0), data.get("birthdate", ""), data.get("sex", ""), 
            data.get("phone", ""),
            data.get("emergency_contact", ""), data.get("emergency_number", ""), 
            data.get("street", ""), data.get("barangay", ""), data.get("city", ""), 
            data.get("province", ""),
            data.get("postal", ""), data.get("nationality", "Filipino"), 
            course, year, sem, 
            section, room,
            ", ".join(subject_names_list), total_units, "No"
        ]

        # Save student data
        if save_student(student_data):
            print()
            print_header("ENROLLMENT COMPLETE")
            print_info(f"Student Number: {student_number}")
            print_info(f"Full Name: {full_name}")
            print_info(f"Course: {course}")
            print_info(f"Year Level: {year}")
            print_info(f"Semester: {sem}")
            print_info(f"Section: {section}")
            print_info(f"Room: {room}")
            print_info(f"Subjects Enrolled: {len(subjects_enrolled)}")
            print_info(f"Total Units: {total_units}")
            print()
            print_success("Enrollment successful!")
            print()

    except KeyboardInterrupt:
        print_error("\nEnrollment cancelled by user.")
        input("\nPress Enter to return to main menu...")
    except Exception as e:
        print_error(f"An error occurred during enrollment: {str(e)}")
        input("\nPress Enter to return to main menu...")


# ==================== VIEW FUNCTIONS ====================

def view_students():
    """Display all enrolled students."""
    clear_screen()
    print_header("STUDENT MASTER LIST")
    print()

    try:
        if not os.path.exists(MAIN_FILE):
            print_error("No students enrolled yet.")
            input("\nPress Enter to continue...")
            return

        with open(MAIN_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            students = list(reader)

            if not students:
                print_error("No students found in the database.")
                input("\nPress Enter to continue...")
                return

            # Define column widths
            col_no = 5
            col_student = 15
            col_name = 35
            col_course = 8
            col_year = 15
            col_section = 10
            col_room = 12
            
            # Print header
            header = (f"{'No.':<{col_no}} | "
                     f"{'Student Number':<{col_student}} | "
                     f"{'Full Name':<{col_name}} | "
                     f"{'Course':<{col_course}} | "
                     f"{'Year Level':<{col_year}} | "
                     f"{'Section':<{col_section}} | "
                     f"{'Room':<{col_room}}")
            print(header)
            print_separator("-", length=len(header))

            active_count = 0
            for student in students:
                # Skip archived students
                if student.get('Archived', 'No').upper() == 'YES':
                    continue
                
                active_count += 1
                # Handle both old format (Name) and new format (Full Name)
                name = student.get('Full Name', student.get('Name', 'N/A'))
                student_num = student.get('Student Number', 'N/A')
                course = student.get('Course', 'N/A')
                year = student.get('Year Level', 'N/A')
                section = student.get('Section', 'N/A')
                room = student.get('Room', 'N/A')
                
                # Truncate long names
                if len(name) > col_name:
                    name = name[:col_name-3] + "..."
                
                # Print row with proper alignment
                row = (f"{str(active_count):<{col_no}} | "
                      f"{student_num:<{col_student}} | "
                      f"{name:<{col_name}} | "
                      f"{course:<{col_course}} | "
                      f"{year:<{col_year}} | "
                      f"{section:<{col_section}} | "
                      f"{room:<{col_room}}")
                print(row)

            print()
            print(f"Total Active Students: {active_count}")

    except Exception as e:
        print_error(f"Error viewing students: {str(e)}")
    
    input("\nPress Enter to continue...")


def view_student_details():
    """View detailed information about a specific student."""
    clear_screen()
    print_header("STUDENT DETAILED INFORMATION")

    try:
        if not os.path.exists(MAIN_FILE):
            print_error("No students enrolled yet.")
            input("\nPress Enter to continue...")
            return

        print_prompt("Enter Student Number: ")
        student_number = input().strip()

        with open(MAIN_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            found = False

            for student in reader:
                if student.get("Student Number", "").upper() == student_number.upper():
                    found = True
                    print()
                    
                    # Handle both old and new format
                    full_name = student.get('Full Name', student.get('Name', 'N/A'))
                    last_name = student.get('Last Name', 'N/A')
                    first_name = student.get('First Name', 'N/A')
                    middle_initial = student.get('Middle Initial', '')
                    suffix = student.get('Suffix', '')
                    
                    print("STUDENT NUMBER")
                    print_separator("-")
                    print(f"  {student.get('Student Number', 'N/A')}")
                    print()
                    
                    print("PERSONAL INFORMATION")
                    print_separator("-")
                    if last_name != 'N/A':
                        print(f"  Last Name: {last_name}")
                        print(f"  First Name: {first_name}")
                        if middle_initial:
                            print(f"  Middle Initial: {middle_initial}")
                        if suffix:
                            print(f"  Suffix: {suffix}")
                    print(f"  Full Name: {full_name}")
                    print(f"  Age: {student.get('Age', 'N/A')}")
                    print(f"  Birthdate: {student.get('Birthdate', 'N/A')}")
                    print(f"  Sex: {student.get('Sex', 'N/A')}")
                    print()
                    
                    print("CONTACT INFORMATION")
                    print_separator("-")
                    print(f"  Phone Number: {student.get('Phone Number', 'N/A')}")
                    print(f"  Emergency Contact: {student.get('Emergency Contact', 'N/A')}")
                    print(f"  Emergency Number: {student.get('Emergency Number', 'N/A')}")
                    print()
                    
                    print("ADDRESS")
                    print_separator("-")
                    barangay = student.get('Barangay', '')
                    address_parts = [student.get('Street', 'N/A')]
                    if barangay:
                        address_parts.append(f"Brgy. {barangay}")
                    city = student.get('City/Municipality', '') or 'N/A'
                    province = student.get('Province', '') or 'N/A'
                    postal_code = student.get('Postal Code', '') or 'N/A'
                    address_parts.extend([city, province, postal_code])
                    address = ", ".join(address_parts)
                    print(f"  Address: {address}")
                    print()
                    
                    print("ACADEMIC INFORMATION")
                    print_separator("-")
                    print(f"  Nationality: {student.get('Nationality', 'N/A')}")
                    print(f"  Course: {student.get('Course', 'N/A')}")
                    print(f"  Year Level: {student.get('Year Level', 'N/A')}")
                    print(f"  Semester: {student.get('Semester', 'N/A')}")
                    print(f"  Section: {student.get('Section', 'N/A')}")
                    print(f"  Room: {student.get('Room', 'N/A')}")
                    print(f"  Total Units: {student.get('Total Units', 'N/A')}")
                    print()
                    
                    print("SUBJECTS ENROLLED")
                    print_separator("-")
                    subjects = student.get('Subjects', 'N/A')
                    if subjects and subjects != 'N/A':
                        subject_list = [s.strip() for s in subjects.split(',')]
                        for idx, subject in enumerate(subject_list, 1):
                            print(f"  {idx}. {subject}")
                    else:
                        print("  No subjects enrolled.")
                    print()
                    break

            if not found:
                print_error(f"Student number {student_number} not found.")

    except Exception as e:
        print_error(f"Error viewing student details: {str(e)}")
    
    input("\nPress Enter to continue...")


# ==================== REPORT GENERATION ====================

def generate_class_lists():
    """Generate class list reports per section/room."""
    clear_screen()
    print_header("GENERATE CLASS LISTS")

    try:
        if not os.path.exists(MAIN_FILE):
            print_error("No students enrolled to generate class lists.")
            input("\nPress Enter to continue...")
            return

        # Read all students and group by (Section, Room)
        students_by_section = {}

        with open(MAIN_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Skip archived students
                if row.get("Archived", "No").upper() == "YES":
                    continue
                    
                section = row.get("Section", "")
                room = row.get("Room", "Room Not Assigned")

                key = (section, room)
                if key not in students_by_section:
                    students_by_section[key] = []

                # Handle both old and new format
                full_name = row.get("Full Name", row.get("Name", ""))

                class_list_data = {
                    "Student Number": row.get("Student Number", ""),
                    "Full Name": full_name,
                    "Course": row.get("Course", ""),
                    "Year Level": row.get("Year Level", ""),
                    "Section": section,
                    "Room": room,
                    "Subjects Enrolled": row.get("Subjects", ""),
                    "Total Units": row.get("Total Units", "")
                }
                students_by_section[key].append(class_list_data)

        # Create Reports folder
        reports_dir = "Class_Lists_Reports"
        os.makedirs(reports_dir, exist_ok=True)

        if not students_by_section:
            print_error("No data found to generate reports.")
            input("\nPress Enter to continue...")
            return

        print_info("Generating class list reports...")
        print_separator("-")

        # Generate CSV for each Section/Room
        for (section, room), students in students_by_section.items():
            clean_room = room.replace('/', '-').replace(' ', '_')
            filename = f"{reports_dir}/{section}_{clean_room}_ClassList.csv"

            print_info(f"Generating: Section {section} - Room {room} ({len(students)} students)")

            if students:
                # Sort students by student number for formal presentation
                students_sorted = sorted(students, key=lambda x: x.get("Student Number", ""))
                
                # Display formatted table preview
                print()
                print(f"CLASS LIST - Section {section} - Room {room}")
                print_separator("-")
                
                # Define column widths for display
                col_no = 5
                col_student = 15
                col_name = 30
                col_course = 8
                col_year = 15
                col_units = 12
                
                # Print header
                header = (f"{'No.':<{col_no}} | "
                         f"{'Student Number':<{col_student}} | "
                         f"{'Full Name':<{col_name}} | "
                         f"{'Course':<{col_course}} | "
                         f"{'Year Level':<{col_year}} | "
                         f"{'Total Units':<{col_units}}")
                print(header)
                print_separator("-", length=len(header))
                
                # Print student rows
                for idx, student in enumerate(students_sorted, 1):
                    student_num = student.get("Student Number", "")
                    full_name = student.get("Full Name", "")
                    course = student.get("Course", "")
                    year_level = student.get("Year Level", "")
                    total_units = student.get("Total Units", "")
                    
                    # Truncate long names
                    if len(full_name) > col_name:
                        full_name = full_name[:col_name-3] + "..."
                    
                    row = (f"{str(idx):<{col_no}} | "
                          f"{student_num:<{col_student}} | "
                          f"{full_name:<{col_name}} | "
                          f"{course:<{col_course}} | "
                          f"{year_level:<{col_year}} | "
                          f"{total_units:<{col_units}}")
                    print(row)
                
                print()
                
                # Create formal CSV with proper headers and formatting
                with open(filename, "w", newline="", encoding="utf-8") as outfile:
                    # Write formal header information
                    outfile.write("CLASS LIST REPORT\n")
                    outfile.write("=" * 80 + "\n")
                    outfile.write(f"Section: {section}\n")
                    outfile.write(f"Room: {room}\n")
                    outfile.write(f"Academic Year: {datetime.now().year}\n")
                    outfile.write(f"Total Students: {len(students_sorted)}\n")
                    outfile.write("=" * 80 + "\n\n")
                    
                    # Write CSV data with formal headers
                    fieldnames = [
                        "No.", "Student Number", "Full Name", "Course", 
                        "Year Level", "Section", "Room", "Total Units", "Subject Code", "Subject Name"
                    ]
                    
                    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                    writer.writeheader()
                    
                    # Write student data with numbering and formatted subjects
                    for idx, student in enumerate(students_sorted, 1):
                        subjects_str = student.get("Subjects Enrolled", "")
                        student_num = student.get("Student Number", "")
                        full_name = student.get("Full Name", "")
                        course = student.get("Course", "")
                        year_level = student.get("Year Level", "")
                        section = student.get("Section", "")
                        room = student.get("Room", "")
                        total_units = student.get("Total Units", "")
                        
                        if subjects_str and subjects_str != 'N/A':
                            # Parse subjects from comma-separated string
                            subject_list = [s.strip() for s in subjects_str.split(',')]
                            
                            # Write one row per subject
                            for subj_idx, subject in enumerate(subject_list):
                                # Parse subject code and name
                                if ' (' in subject and ')' in subject:
                                    code_end = subject.find(' (')
                                    subject_code = subject[:code_end]
                                    subject_name = subject[code_end+2:-1] if subject.endswith(')') else subject[code_end+2:]
                                else:
                                    subject_code = subject
                                    subject_name = ""
                                
                                # Write row - only include student info in first subject row
                                if subj_idx == 0:
                                    row = {
                                        "No.": str(idx),
                                        "Student Number": student_num,
                                        "Full Name": full_name,
                                        "Course": course,
                                        "Year Level": year_level,
                                        "Section": section,
                                        "Room": room,
                                        "Total Units": total_units,
                                        "Subject Code": subject_code,
                                        "Subject Name": subject_name
                                    }
                                else:
                                    # Subsequent subjects - leave student info blank
                                    row = {
                                        "No.": "",
                                        "Student Number": "",
                                        "Full Name": "",
                                        "Course": "",
                                        "Year Level": "",
                                        "Section": "",
                                        "Room": "",
                                        "Total Units": "",
                                        "Subject Code": subject_code,
                                        "Subject Name": subject_name
                                    }
                                writer.writerow(row)
                        else:
                            # No subjects enrolled
                            row = {
                                "No.": str(idx),
                                "Student Number": student_num,
                                "Full Name": full_name,
                                "Course": course,
                                "Year Level": year_level,
                                "Section": section,
                                "Room": room,
                                "Total Units": total_units,
                                "Subject Code": "N/A",
                                "Subject Name": "No subjects enrolled"
                            }
                            writer.writerow(row)
                    
                    # Write footer
                    outfile.write("\n" + "=" * 80 + "\n")
                    outfile.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                    outfile.write("=" * 80 + "\n")

        print_separator("-")
        print_success(f"All class list reports generated successfully in '{reports_dir}' folder.")

    except Exception as e:
        print_error(f"Error generating class lists: {str(e)}")
    
    input("\nPress Enter to continue...")


# ==================== EDIT STUDENT ====================

def edit_student():
    """Edit student information."""
    clear_screen()
    print_header("EDIT STUDENT INFORMATION")
    
    print()
    print("NOTICE: Type 'back', 'cancel', or 'exit' at any prompt to return to main menu")
    print()

    try:
        if not os.path.exists(MAIN_FILE):
            print_error("No students enrolled yet.")
            input("\nPress Enter to continue...")
            return

        print_prompt("Enter Student Number to edit: ")
        student_number = input().strip()

        # Read all students
        students = []
        student_to_edit = None
        
        with open(MAIN_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get("Student Number", "").upper() == student_number.upper():
                    student_to_edit = row
                    students.append(row)
                else:
                    students.append(row)

        if not student_to_edit:
            print_error(f"Student number {student_number} not found.")
            input("\nPress Enter to continue...")
            return

        print()
        print("CURRENT STUDENT INFORMATION")
        print_separator("-")
        print()
        print_info(f"Student Number: {student_to_edit.get('Student Number', 'N/A')}")
        print_info(f"Full Name: {student_to_edit.get('Full Name', student_to_edit.get('Name', 'N/A'))}")
        print()
        print("EDIT FIELDS")
        print("(Press Enter to keep current value)")
        print_separator("-")
        print()

        # Edit fields
        last_name = student_to_edit.get("Last Name", "")
        first_name = student_to_edit.get("First Name", "")
        middle_initial = student_to_edit.get("Middle Initial", "")
        suffix = student_to_edit.get("Suffix", "")
        
        print_prompt(f"Last Name [{last_name}]: ")
        new_last = input().strip()
        if check_back_command(new_last):
            print_info("Edit cancelled.")
            input("\nPress Enter to continue...")
            return
        if new_last:
            last_name = new_last

        print_prompt(f"First Name [{first_name}]: ")
        new_first = input().strip()
        if check_back_command(new_first):
            print_info("Edit cancelled.")
            input("\nPress Enter to continue...")
            return
        if new_first:
            first_name = new_first

        print_prompt(f"Middle Initial/Name [{middle_initial}] (Enter to skip): ")
        new_mi = input().strip()
        if check_back_command(new_mi):
            print_info("Edit cancelled.")
            input("\nPress Enter to continue...")
            return
        if new_mi:
            # Capitalize first letter of each word if provided
            middle_initial = " ".join(word.capitalize() for word in new_mi.split())

        print_prompt(f"Suffix [{suffix}] (Enter to skip): ")
        new_suffix = input().strip()
        if check_back_command(new_suffix):
            print_info("Edit cancelled.")
            input("\nPress Enter to continue...")
            return
        if new_suffix:
            if any(c.isdigit() for c in new_suffix):
                print_warning("Suffix cannot contain numbers. Keeping previous value.")
            else:
                suffix = new_suffix

        full_name = format_name(last_name, first_name, middle_initial, suffix)

        print_prompt(f"Phone Number [{student_to_edit.get('Phone Number', '')}]: ")
        new_phone = input().strip()
        if check_back_command(new_phone):
            print_info("Edit cancelled.")
            input("\nPress Enter to continue...")
            return
        phone = new_phone if new_phone else student_to_edit.get("Phone Number", "")

        print_prompt(f"Barangay [{student_to_edit.get('Barangay', '')}]: ")
        new_barangay = input().strip()
        if check_back_command(new_barangay):
            print_info("Edit cancelled.")
            input("\nPress Enter to continue...")
            return
        barangay = new_barangay if new_barangay else student_to_edit.get("Barangay", "")

        # Update student data
        updated_student = dict(student_to_edit)
        updated_student["Last Name"] = last_name
        updated_student["First Name"] = first_name
        updated_student["Middle Initial"] = middle_initial
        updated_student["Suffix"] = suffix
        updated_student["Full Name"] = full_name
        if new_phone:
            updated_student["Phone Number"] = phone
        if new_barangay:
            updated_student["Barangay"] = barangay

        # Write back
        with open(MAIN_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            for row in students:
                if row.get("Student Number", "") == student_number:
                    writer.writerow(updated_student)
                else:
                    writer.writerow(row)

        # Copy to Registrar and Librarian
        shutil.copy(MAIN_FILE, REGISTRAR_FILE)
        shutil.copy(MAIN_FILE, LIBRARIAN_FILE)

        print()
        print_success("Student information updated successfully!")
        input("\nPress Enter to continue...")

    except Exception as e:
        print_error(f"Error editing student: {str(e)}")
        input("\nPress Enter to continue...")


# ==================== ARCHIVE STUDENT ====================

def archive_student():
    """Archive or unarchive a student."""
    clear_screen()
    print_header("ARCHIVE STUDENT")

    try:
        if not os.path.exists(MAIN_FILE):
            print_error("No students enrolled yet.")
            input("\nPress Enter to continue...")
            return

        print_prompt("Enter Student Number: ")
        student_number = input().strip()

        # Read all students
        students = []
        student_found = False
        current_archive_status = "No"
        
        with open(MAIN_FILE, "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            fieldnames = reader.fieldnames
            for row in reader:
                if row.get("Student Number", "").upper() == student_number.upper():
                    student_found = True
                    current_archive_status = row.get("Archived", "No")
                    # Toggle archive status
                    row["Archived"] = "Yes" if current_archive_status.upper() != "YES" else "No"
                    students.append(row)
                else:
                    students.append(row)

        if not student_found:
            print_error(f"Student number {student_number} not found.")
            input("\nPress Enter to continue...")
            return

        # Write back
        with open(MAIN_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(students)

        # Copy to Registrar and Librarian
        shutil.copy(MAIN_FILE, REGISTRAR_FILE)
        shutil.copy(MAIN_FILE, LIBRARIAN_FILE)

        action = "archived" if current_archive_status.upper() != "YES" else "unarchived"
        print()
        print_success(f"Student {student_number} has been {action} successfully!")
        input("\nPress Enter to continue...")

    except Exception as e:
        print_error(f"Error archiving student: {str(e)}")
        input("\nPress Enter to continue...")


# ==================== MAIN MENU ====================

def main_menu():
    """Main menu loop."""
    while True:
        clear_screen()
        print_header("ENROLLMENT SYSTEM")
        
        print("  Please select an option:")
        print()
        print("  1. Enroll New Student")
        print("  2. View Student List")
        print("  3. View Student Details")
        print("  4. Edit Student Information")
        print("  5. Generate Class List Reports")
        print("  6. Exit")
        print()
        print_separator("-")

        print_prompt("Enter your choice (1-6): ")
        choice = input().strip()

        if choice == "1":
            enroll_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            view_student_details()
        elif choice == "4":
            edit_student()
        elif choice == "5":
            generate_class_lists()
        elif choice == "6":
            clear_screen()
            print_header("EXITING SYSTEM")
            print_info("Thank you for using the Enrollment System!")
            print()
            print_separator("-")
            break
        else:
            print_error("Invalid choice. Please enter a number between 1-6.")
            input("\nPress Enter to continue...")


# ==================== PROGRAM ENTRY POINT ====================

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print_error("\n\nProgram interrupted by user. Exiting...")
    except Exception as e:
        print_error(f"Fatal error: {str(e)}")
        print_info("Please contact system administrator.")
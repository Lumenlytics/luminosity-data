import csv
import random
import math
from collections import defaultdict

# CONFIG
MAX_CLASS_SIZE = 15
ELEMENTARY_SUBJECTS = ["Homeroom", "Math", "Reading", "Science", "Social Studies"]
MIDDLE_SUBJECTS = ["Math", "ELA", "Science", "Social Studies", "Art", "PE", "Technology"]
HIGH_SCHOOL_SUBJECTS = ["Algebra I", "Geometry", "Biology", "Chemistry", "English", "US History", "Civics", "Health", "Spanish"]

# Load students and teachers
def load_csv(path):
    with open(path, newline='') as f:
        return list(csv.DictReader(f))

students = load_csv("2015/csv/students.csv")
teachers = load_csv("2015/csv/teachers.csv")


# Organize students by grade (from the 'grade' column)
grade_counts = defaultdict(int)
for s in students:
    grade = int(s["grade"])
    grade_counts[grade] += 1


# Assign teachers to grade levels based on role_label
teacher_pool = defaultdict(list)

for t in teachers:
    role = t["role_label"].lower()
    floater = str(t.get("is_floater", "")).lower() == "true"

    if "elementary" in role or (floater and not role):
        grade_range = range(0, 6)  # K–5
    elif "middle" in role:
        grade_range = range(6, 9)  # 6–8
    elif "high" in role:
        grade_range = range(9, 13)  # 9–12
    elif floater:
        grade_range = range(0, 13)  # All grades
    else:
        continue  # Unknown role — skip

    for grade in grade_range:
        teacher_pool[grade].append(t)


# Determine subjects per grade level
def get_subjects(grade):
    if grade <= 5:
        return ELEMENTARY_SUBJECTS
    elif 6 <= grade <= 8:
        return MIDDLE_SUBJECTS
    else:
        return HIGH_SCHOOL_SUBJECTS

# Generate class sections
classes = []
class_id = 1
warnings = []

for grade in sorted(grade_counts):
    student_total = grade_counts[grade]
    subjects = get_subjects(grade)

    for subject in subjects:
        num_sections = math.ceil(student_total / MAX_CLASS_SIZE)
        available_teachers = teacher_pool.get(grade, []).copy()

        if len(available_teachers) < num_sections:
            warnings.append(f"⚠️ Not enough teachers for Grade {grade} - {subject}. Needed: {num_sections}, Available: {len(available_teachers)}")

        for section in range(1, num_sections + 1):
            if available_teachers:
                teacher = available_teachers.pop()
            else:
                teacher = {"teacher_id": "UNASSIGNED"}

            classes.append({
                "class_id": class_id,
                "class_name": f"Grade {grade} - {subject} (Section {section})",
                "grade_level": grade,
                "subject": subject,
                "teacher_id": teacher["teacher_id"]
            })
            class_id += 1

# Write classes.csv
with open("2015/csv/classes.csv", "w", newline='') as f:
    writer = csv.DictWriter(f, fieldnames=["class_id", "class_name", "grade_level", "subject", "teacher_id"])
    writer.writeheader()
    writer.writerows(classes)

print(f"✅ Generated {len(classes)} classes in classes.csv")


import pandas as pd
import random
from datetime import date, timedelta
import math
from pathlib import Path

# -------------------------------------------------------------------
# CONFIG
CLASSES_PATH   = Path("2015/csv/classes.csv")
TEACHERS_PATH  = Path("2015/csv/teachers.csv")
DEPTS_PATH     = Path("2015/csv/departments.csv")  # optional, for dept_id lookup
MAX_SECTIONS_PER_TEACHER = 5                      # realistic teaching load
SUBJECTS = ["Art", "ELA", "Math", "PE", "Science",
            "Social Studies", "Technology"]

# Simple name pools (expand if desired)
FIRST_NAMES = ["Alex", "Jordan", "Taylor", "Morgan", "Casey",
               "Riley", "Sydney", "Devin", "Quinn", "Avery"]
LAST_NAMES  = ["Smith", "Johnson", "Brown", "Lee", "Garcia",
               "Martinez", "Davis", "Lopez", "Clark", "Lewis"]

# -------------------------------------------------------------------
# Load data
classes = pd.read_csv(CLASSES_PATH)
teachers = pd.read_csv(TEACHERS_PATH)

# Optional: department lookup (subject -> department_id)
dept_map = {}
if DEPTS_PATH.exists():
    depts = pd.read_csv(DEPTS_PATH)
    for _, row in depts.iterrows():
        dept_map[row["name"].strip().lower()] = int(row["department_id"])

# -------------------------------------------------------------------
# Count missing sections by subject in grades 6-8
missing = classes[(classes["teacher_id"] == "UNASSIGNED") &
                  (classes["grade_level"].between(6, 8))]
missing_counts = (
    missing.groupby("subject")
           .size()
           .reindex(SUBJECTS, fill_value=0)
           .to_dict()
)

# Calculate teachers to add
teachers_needed = {
    subj: math.ceil(cnt / MAX_SECTIONS_PER_TEACHER)
    for subj, cnt in missing_counts.items()
    if cnt > 0
}

if not teachers_needed:
    print("✅ No missing middle-school sections. Nothing to do.")
    exit()

print("🛠️  Adding teachers to cover missing sections:")
for subj, n in teachers_needed.items():
    print(f"   • {subj}: {n} new teacher(s)")

# -------------------------------------------------------------------
# Helper to generate random dates
def random_date(start_year, end_year):
    start = date(start_year, 1, 1)
    end   = date(end_year, 12, 31)
    delta = end - start
    return start + timedelta(days=random.randint(0, delta.days))

# -------------------------------------------------------------------
# Append new teachers
next_id = teachers["teacher_id"].max() + 1
new_rows = []

for subject, qty in teachers_needed.items():
    for _ in range(qty):
        first = random.choice(FIRST_NAMES)
        last  = random.choice(LAST_NAMES)
        new_rows.append({
            "teacher_id"   : next_id,
            "first_name"   : first,
            "last_name"    : last,
            "birthdate"    : random_date(1970, 1995).isoformat(),
            "hire_date"    : random_date(2018, 2024).isoformat(),
            "department_id": dept_map.get(subject.lower(), 0),
            "is_floater"   : False,
            "role_label"   : "Middle School Subject"
        })
        next_id += 1

teachers = pd.concat([teachers, pd.DataFrame(new_rows)], ignore_index=True)
teachers.to_csv(TEACHERS_PATH, index=False)

print(f"✅ Added {len(new_rows)} teachers.")
print("👉 Now re-run:  python scripts/generate_classes.py")

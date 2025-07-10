"""
generate_teachers_classrooms.py
—————————————
• 18 classrooms (room_number, capacity, special_use flag)
• ~48 teachers broken down per staffing plan
  – 28 elementary homeroom
  –  7 secondary core (Math, Eng, Sci, SocSt, CompSci, Econ)
  –  6 specials (Art, Music, PE, Health, Spanish, French)
  –  4 support (Reading spec, ESL, SPED, Counselor)
  –  2 floaters
• teacher_subjects.csv maps each teacher to 1–3 subjects
"""

import csv, os, random
from pathlib import Path
from datetime import date, timedelta
from faker import Faker

fake = Faker()
random.seed(42)
Faker.seed(42)

YEAR          = 2015
OUT_DIR       = Path(f"{YEAR}/csv")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ------------ SUBJECT & DEPARTMENT REFS -----------------
# These IDs should match your subjects.csv / departments.csv
SUBJECTS = {
    "Elementary Core" : 101,   # placeholder subject_id for homeroom blocks
    "Math"            : 201,
    "English"         : 202,
    "Science"         : 203,
    "Social Studies"  : 204,
    "Computer Science": 205,
    "Economics"       : 206,
    "Art"             : 301,
    "Music"           : 302,
    "PE"              : 303,
    "Health"          : 304,
    "Spanish"         : 401,
    "French"          : 402,
    "Reading Support" : 501,
    "ESL"             : 502,
    "Special Ed"      : 503,
    "Counseling"      : 504,
}

# ------------ CLASSROOMS --------------------------------
classrooms = []
for i in range(1, 19):                     # Rooms 101-118
    classrooms.append({
        "classroom_id": i,
        "room_number": f"{100+i}",
        "capacity": random.randint(25, 30),
        "floor": 1 if i<=9 else 2,
        "building": "Main",
        "is_special_use": (i in (3, 7, 12, 16))  # mark a few special rooms
    })

# ------------ TEACHERS ----------------------------------
teachers      = []
teacher_subj  = []
tid           = 1
hire_start    = date(YEAR-20, 8, 1)

def add_teacher(role:str, subj_keys:list[str], is_floater=False):
    global tid
    teachers.append({
        "teacher_id":     tid,
        "first_name":     fake.first_name(),
        "last_name":      fake.last_name(),
        "birthdate":      fake.date_of_birth(minimum_age=25, maximum_age=62),
        "hire_date":      fake.date_between(hire_start, date(YEAR, 8, 1)),
        "department_id":  1,         # simplify: use dept 1 for all
        "is_floater":     is_floater,
        "role_label":     role
    })
    # subject links
    for key in subj_keys:
        teacher_subj.append({
            "teacher_id": tid,
            "subject_id": SUBJECTS[key]
        })
    tid += 1

# 28 elementary homeroom teachers (teach “Elementary Core”)
for _ in range(28):
    add_teacher("Elementary Homeroom", ["Elementary Core"])

# 7 secondary core teachers
core_map = [
    ("Math Teacher",   ["Math"]),
    ("English Teacher",["English"]),
    ("Science Teacher",["Science"]),
    ("SocSt Teacher",  ["Social Studies"]),
    ("CompSci Teacher",["Computer Science"]),
    ("Economics Teacher",["Economics"]),
    ("Integrated Sci/Math",["Science","Math"])
]
for role, subs in core_map:
    add_teacher(role, subs)

# 6 specials teachers
specials_map = [
    ("Art Teacher",      ["Art"]),
    ("Music Teacher",    ["Music"]),
    ("PE Teacher",       ["PE","Health"]),
    ("Spanish Teacher",  ["Spanish"]),
    ("French Teacher",   ["French"]),
    ("Health Teacher",   ["Health"])
]
for role, subs in specials_map:
    add_teacher(role, subs)

# 4 support
support_map = [
    ("Reading Specialist",["Reading Support"]),
    ("ESL Specialist",    ["ESL"]),
    ("Special-Ed Teacher",["Special Ed"]),
    ("School Counselor",  ["Counseling"])
]
for role, subs in support_map:
    add_teacher(role, subs)

# 2 floaters (no primary subjects)
for _ in range(2):
    add_teacher("Floater", [], is_floater=True)

# ------------ SAVE CSVs ---------------------------------
with open(OUT_DIR/"classrooms.csv","w",newline="") as f:
    csv.DictWriter(f,fieldnames=classrooms[0]).writeheader()
    csv.writer(f).writerows([c.values() for c in classrooms])

with open(OUT_DIR/"teachers.csv","w",newline="") as f:
    csv.DictWriter(f,fieldnames=teachers[0]).writeheader()
    csv.writer(f).writerows([t.values() for t in teachers])

with open(OUT_DIR/"teacher_subjects.csv","w",newline="") as f:
    csv.DictWriter(f,fieldnames=teacher_subj[0]).writeheader()
    csv.writer(f).writerows([ts.values() for ts in teacher_subj])

print(f"✅ Created {len(teachers)} teachers, {len(classrooms)} classrooms, {len(teacher_subj)} teacher-subject links")

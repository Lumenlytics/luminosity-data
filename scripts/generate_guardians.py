"""
generate_guardians.py
Links guardians to the 2015 student roster.

Outputs
-------
2015/csv/guardians.csv
2015/csv/student_guardians.csv
"""

import os, csv, random
from pathlib import Path
from faker import Faker
import pandas as pd

fake = Faker()
random.seed(42)
Faker.seed(42)

STUDENTS_CSV  = Path("2015/csv/students.csv")
OUT_DIR       = Path("2015/csv")
OUT_DIR.mkdir(parents=True, exist_ok=True)

if not STUDENTS_CSV.exists():
    raise SystemExit("❌ students.csv not found – run generate_students.py first")

students = pd.read_csv(STUDENTS_CSV)

# Guardian type IDs (should match guardian_types.csv)
MOTHER, FATHER = 1, 2
AUNT, UNCLE, GRANDM, GRANDP, LEGAL = 7, 8, 5, 6, 9

guardian_pool   = {}   # key: (first,last) -> guardian_id
guardians_rows  = []
student_guardian_rows = []
next_guardian_id = 1

def get_or_create_guardian(first, last, gtype):
    global next_guardian_id
    key = (first, last, gtype)
    if key in guardian_pool:
        return guardian_pool[key]
    gid = next_guardian_id
    guardian_pool[key] = gid
    guardians_rows.append({
        "guardian_id": gid,
        "first_name":  first,
        "last_name":   last,
        "guardian_type_id": gtype
    })
    next_guardian_id += 1
    return gid

for _, stu in students.iterrows():
    sid   = stu["student_id"]
    s_last= stu["last_name"]

    # decide parent structure
    two_parents = random.random() < 0.70
    guardians_for_student = []

    # primary parent(s) with same surname
    if two_parents or random.random() < 0.5:
        # mother
        g_first = fake.first_name_female()
        gid     = get_or_create_guardian(g_first, s_last, MOTHER)
        guardians_for_student.append( (gid, True) )
    # father
    if two_parents:
        g_first = fake.first_name_male()
        gid     = get_or_create_guardian(g_first, s_last, FATHER)
        guardians_for_student.append( (gid, True if len(guardians_for_student)==0 else False) )
    elif not guardians_for_student:  # ensure at least one
        g_first = fake.first_name_male()
        gid     = get_or_create_guardian(g_first, s_last, FATHER)
        guardians_for_student.append( (gid, True) )

    # 10 % chance of an extra non-parent guardian with different surname
    if random.random() < 0.10:
        gtype  = random.choice([AUNT, UNCLE, GRANDM, GRANDP, LEGAL])
        g_last = fake.last_name()
        # ensure different last name from student
        while g_last == s_last:
            g_last = fake.last_name()
        g_first = fake.first_name_female() if gtype in (AUNT, GRANDM) else fake.first_name_male()
        gid     = get_or_create_guardian(g_first, g_last, gtype)
        guardians_for_student.append( (gid, False) )

    # link rows
    for gid, primary in guardians_for_student:
        student_guardian_rows.append({
            "student_id": sid,
            "guardian_id": gid,
            "primary_contact": primary
        })

# ---------- SAVE ----------
pd.DataFrame(guardians_rows).to_csv(OUT_DIR / "guardians.csv", index=False)
pd.DataFrame(student_guardian_rows).to_csv(OUT_DIR / "student_guardians.csv", index=False)

print(f"✅ Created {len(guardians_rows)} guardians for {len(students)} students")

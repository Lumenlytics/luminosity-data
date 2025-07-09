"""
generate_students.py
Creates ~500 logically-consistent student records for 2015-2016.

• 70 % only-children, 30 % siblings
  – 37 pairs, 14 trios, 6 quads, 2 quints
  – 4 twin sets, 2 triplet sets
• ~50 / 50 gender mix
• 80 % grades 1-7
• Unique family surnames from a 1 000-name US list
"""

import os, csv, random
from pathlib import Path
from datetime import date
from faker import Faker

# ---------- CONFIG ----------
YEAR              = 2015
OUTPUT_DIR        = Path("2015/csv")
SURNAME_FILE      = Path("utils/surnames.txt")
NUM_STUDENTS      = 500

# sibling structure
ONLY_CHILDREN = 350
PAIRS, TRIOS, QUADS, QUINTS = 37, 14, 6, 2
TWIN_SETS, TRIPLET_SETS     = 4, 2

# grade distribution weights
GRADE_WEIGHTS = {
    1:0.12, 2:0.12, 3:0.11, 4:0.10, 5:0.10, 6:0.10, 7:0.15,
    8:0.06, 9:0.05, 10:0.04, 11:0.03, 12:0.02
}

fake = Faker()
random.seed(42)
Faker.seed(42)

# ---------- LOAD SURNAME POOL ----------
if not SURNAME_FILE.exists():
    # auto-download 1000 surnames
    import urllib.request, ssl
    url = ("https://gist.githubusercontent.com/craigh411/"
           "19a4479b289ae6c3f6edb95152214efc/raw/"
           "d25a1afd3de42f10abdea7740ed098d41de3c330/"
           "List%20of%20the%201,000%20Most%20Common%20Last%20Names%20(USA)")
    ssl._create_default_https_context = ssl._create_unverified_context
    text = urllib.request.urlopen(url).read().decode()
    SURNAME_FILE.parent.mkdir(parents=True, exist_ok=True)
    SURNAME_FILE.write_text(text)

surname_pool = [n.strip().strip(",") for n in SURNAME_FILE.read_text().splitlines() if n.strip()]
random.shuffle(surname_pool)

# ---------- HELPERS ----------
def weighted_grade():
    return random.choices(list(GRADE_WEIGHTS), weights=GRADE_WEIGHTS.values())[0]

def dob_for_grade(grade:int) -> str:
    """Return ISO DOB so age on 1 Sep 2015 fits grade."""
    ref = date(2015,9,1)
    age  = random.choice([5+grade, 6+grade])  # 6-7 for 1st, etc.
    y    = ref.year - age
    m    = random.randint(1, 12)
    d    = min(random.randint(1, 28), 28)     # keep safe day
    try:
        return date(y, m, d).isoformat()
    except ValueError:                         # Feb 29 fallback
        return date(y, m, 28).isoformat()

# ---------- BUILD FAMILIES ----------
families = (
      [{"size":1} for _ in range(ONLY_CHILDREN)]
    + [{"size":2} for _ in range(PAIRS)]
    + [{"size":3} for _ in range(TRIOS)]
    + [{"size":4} for _ in range(QUADS)]
    + [{"size":5} for _ in range(QUINTS)]
)
random.shuffle(families)

# assign unique surnames
for fam in families:
    fam["surname"] = surname_pool.pop()

# mark twins / triplets
tw, tri = 0, 0
for fam in families:
    if fam["size"]>=2 and tw< TWIN_SETS:
        fam["twin_idx"]=[0,1]; tw+=1
    if fam["size"]>=3 and tri<TRIPLET_SETS:
        fam["trip_idx"]=[0,1,2]; tri+=1
    if tw>=TWIN_SETS and tri>=TRIPLET_SETS: break

# ---------- GENERATE STUDENTS ----------
students, grades = [], []
student_id = 1
for fam in families:
    base_grade = weighted_grade()
    for i in range(fam["size"]):
        gender = "M" if student_id%2==0 else "F"
        first  = fake.first_name_male() if gender=="M" else fake.first_name_female()
        last   = fam["surname"]

        # share DOBs for twins/triplets
        if "twin_idx" in fam and i in fam["twin_idx"]:
            fam.setdefault("twin_dob", dob_for_grade(base_grade))
            dob = fam["twin_dob"]
        elif "trip_idx" in fam and i in fam["trip_idx"]:
            fam.setdefault("trip_dob", dob_for_grade(base_grade))
            dob = fam["trip_dob"]
        else:
            dob = dob_for_grade(base_grade)

        students.append({
            "student_id": student_id,
            "first_name": first,
            "last_name":  last,
            "birthdate":  dob,
            "gender":     gender
        })

        grades.append({
            "student_id": student_id,
            "academic_year_id": 1,
            "grade_level_id":   base_grade
        })

        # next sibling +/- one grade (except twins/triplets)
        if i==0: next_grade = base_grade
        else:    next_grade = max(1, min(12, base_grade + random.choice([-1,0,1])))
        base_grade = next_grade
        student_id +=1

# ---------- SAVE CSVs ----------
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_DIR/"students.csv","w",newline="") as f:
    csv.DictWriter(f,fieldnames=students[0]).writeheader(); csv.writer(f).writerows([s.values() for s in students])

with open(OUTPUT_DIR/"student_grade_history.csv","w",newline="") as f:
    csv.DictWriter(f,fieldnames=grades[0]).writeheader(); csv.writer(f).writerows([g.values() for g in grades])

print(f"✅ Generated {len(students)} students (M/F ~50 / 50)")

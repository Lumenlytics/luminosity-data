# scripts/transform_csvs.py  –  one-file cleaner, paths are absolute to this file
import pandas as pd
from pathlib import Path

# ----------------------------------------------------------
# Locate folders RELATIVE to this script, so path issues vanish
BASE_DIR = Path(__file__).resolve().parent        # …/luminosity-data/scripts
SRC_DIR  = BASE_DIR.parent / "2015" / "csv"       # …/luminosity-data/2015/csv
DEST_DIR = BASE_DIR.parent / "clean_csv"          # …/luminosity-data/clean_csv
DEST_DIR.mkdir(exist_ok=True)
# ----------------------------------------------------------

SCHEMA_SPECS = {
    "students": {
        "expected": ["student_id","first_name","last_name","birthdate","gender","grade"],
    },
    "guardians": {
        "rename": {"guardian_type_id": None},
        "add":    ["phone","email"],
        "expected": ["guardian_id","first_name","last_name","phone","email"]
    },
    "guardian_types": {
        "rename": {"name":"type_name"},
        "expected": ["guardian_type_id","type_name"]
    },
    "student_guardians": {
        "rename": {"primary_contact": None},
        "add":    ["guardian_type_id"],
        "expected": ["student_id","guardian_id","guardian_type_id"]
    },
    "teachers": {
        "drop": ["birthdate","hire_date","department_id","is_floater","role_label"],
        "expected": ["teacher_id","first_name","last_name"]
    },
    "departments": {
        "rename": {"name":"department_name"},
        "expected": ["department_id","department_name"]
    },
    "teacher_subjects": {
        "rename": {"subject_id":"subject"},
        "add":    ["department_id"],
        "expected": ["teacher_id","subject","department_id"]
    },
    "classes": {
    "drop": ["class_name"],                 
    "add":  ["room_id", "period_id", "term_id"],
    "expected": ["class_id", "subject", "grade_level", "teacher_id",
                 "room_id", "period_id", "term_id"]
},
    "enrollments": {
        "add": ["enrollment_id"],
        "expected": ["enrollment_id","student_id","class_id"]
    },
    "assignments": {
        "expected": ["assignment_id","class_id","title","due_date",
                     "points_possible","category"]
    },
    "grades": {
        "expected": ["grade_id","student_id","assignment_id","score","submitted_on"]
    },
    "grade_levels": {
        "rename": {"grade_level_id":"grade","name":"level_name"},
        "drop":   ["level_order"],
        "expected": ["grade","level_name"]
    },
    "student_grade_history": {
        "rename": {"academic_year_id":"year_id","grade_level_id":"grade"},
        "add":    ["history_id"],
        "expected": ["history_id","student_id","year_id","grade"]
    },
    "periods": { "expected": ["period_id","name","start_time","end_time"] },
    "classrooms": {
        "rename": {"classroom_id":"room_id"},
        "drop": ["capacity","floor","is_special_use"],
        "expected": ["room_id","building","room_number"]
    },
    "school_years": {
    "rename": {"school_year_id": "year_id"},   # spelling exactly like this
    "drop":   ["year_label"],
    "add":    ["school_id"],
    "expected": ["year_id", "school_id", "start_date", "end_date"]
},
    "terms": {
    "rename": {"school_year_id": "year_id"},      # map CSV → expected
    "expected": ["term_id", "year_id", "name", "start_date", "end_date"]
},
    "fee_types": { "expected": ["fee_type_id","name","amount","due_by","recurring"] },
    "payments": {
        "expected": ["payment_id","student_id","fee_type_id","amount_paid","date_paid"]
    },
    "attendance": { "expected": ["attendance_id","student_id","date","status"] },
    "discipline_reports": {
        "expected": ["report_id","student_id","date","type","severity",
                     "action_taken","description"]
    },
    "standardized_tests": {
        "expected": ["test_id","student_id","test_name","test_date",
                     "subject","score","percentile"]
    },
}

# -------------------- MAIN LOOP -------------------- #
if __name__ == "__main__":
    for table, spec in SCHEMA_SPECS.items():
        csv_path = SRC_DIR / f"{table}.csv"
        if not csv_path.exists():
            print(f"⚠️  {table}.csv not found – skipping")
            continue

        df = pd.read_csv(csv_path)
        df.columns = df.columns.str.strip().str.replace("\ufeff", "", regex=False)  # remove spaces + BOM

        # ... (rest of the loop body, indented 4 spaces)

for table, spec in SCHEMA_SPECS.items():
    csv_path = SRC_DIR / f"{table}.csv"
    if not csv_path.exists():
        print(f"⚠️  {csv_path.relative_to(BASE_DIR.parent)} missing – skipping")
        continue

    df = pd.read_csv(csv_path)

    # 1) rename / drop
    rename_map = {k:v for k,v in (spec.get("rename") or {}).items() if v}
    df = df.rename(columns=rename_map)
    to_drop  = [k for k,v in (spec.get("rename") or {}).items() if v is None]
    to_drop += spec.get("drop", [])
    df = df.drop(columns=[c for c in to_drop if c in df])

    # 2) add missing blank cols
    for col in spec.get("add", []):
        if col not in df.columns:
            df[col] = ""

    # 3) reorder & assert
    expected = spec["expected"]
    df = df[expected]   # raises if any column missing
    if list(df.columns) != expected:
        raise ValueError(f"{table}: column mismatch after transform")

    # 4) write out
    out_path = DEST_DIR / f"{table}.csv"
    df.to_csv(out_path, index=False)
    print(f"✅  {table:<25} → {out_path.relative_to(BASE_DIR.parent)}")

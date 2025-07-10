#!/usr/bin/env python3
"""
generate_assignments_and_grades.py
---------------------------------
• Creates realistic assignments & grades for a school-portal demo dataset.

INPUT  (in --data_dir)
  ├── classes.csv      # class_id, subject, grade_level, teacher_id, ...
  ├── students.csv     # student_id, first_name, last_name, ...
  └── enrollments.csv  # class_id, student_id  (one row per roster entry)

OUTPUT (to --out_dir)
  ├── assignments.csv  # assignment_id, class_id, title, due_date, points_possible, category
  └── grades.csv       # grade_id, student_id, assignment_id, score, submitted_on

Run `python generate_assignments_and_grades.py -h` for options.
"""

from __future__ import annotations
import argparse, itertools, random, uuid
from pathlib import Path
from datetime import datetime, timedelta

import numpy as np
import pandas as pd


# ── CONFIG ────────────────────────────────────────────────────────────

SCHOOL_START = datetime(2015, 9, 1)
SCHOOL_END   = datetime(2016, 6, 15)

# Subject-specific weighting of assignment categories & point values
SUBJECT_CATEGORIES: dict[str, list[tuple[str, int]]] = {
    "Math":        [("Homework", 10), ("Quiz", 20), ("Test", 100), ("Project", 50)],
    "ELA":         [("Essay", 100), ("Reading Quiz", 20), ("Homework", 10)],
    "Science":     [("Lab", 50), ("Quiz", 20), ("Test", 100), ("Homework", 10)],
    "Social Studies": [("Project", 100), ("Quiz", 20), ("Homework", 10)],
    "PE":          [("Participation", 10)],
    "Art":         [("Project", 100), ("Sketchbook", 10)],
    # Fallback defaults for any uncategorized subject
    "_default":    [("Homework", 10), ("Quiz", 20), ("Test", 100)],
}

ASSIGNMENTS_PER_WEEK_RANGE = (1, 2)      # inclusive
LATE_SUBMISSION_PROB       = 0.05        # 5 % chance a submission is late
PERFECT_SCORE_PROB         = 0.03        # 3 % chance of 100 %
FAILING_SCORE_PROB         = 0.07        # 7 % chance below 60 %

# ----------------------------------------------------------------------


def next_uuid(prefix: str) -> str:
    """Return a short unique ID like 'A_c1a2b3'."""
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


def load_data(data_dir: Path) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    classes = pd.read_csv(data_dir / "classes.csv")
    students = pd.read_csv(data_dir / "students.csv")
    enrollments = pd.read_csv(data_dir / "enrollments.csv")
    return classes, students, enrollments


def daterange_by_week(start: datetime, end: datetime):
    cur = start
    while cur <= end:
        yield cur
        cur += timedelta(days=7)


def choose_category(subject: str) -> tuple[str, int]:
    pool = SUBJECT_CATEGORIES.get(subject, SUBJECT_CATEGORIES["_default"])
    return random.choice(pool)


def generate_assignments(classes: pd.DataFrame) -> pd.DataFrame:
    records = []
    for _, row in classes.iterrows():
        class_id = row["class_id"]
        subject  = row.get("subject", "General")
        weeks = list(daterange_by_week(SCHOOL_START, SCHOOL_END))

        for week_start in weeks:
            num_asn = random.randint(*ASSIGNMENTS_PER_WEEK_RANGE)
            for _ in range(num_asn):
                category, points = choose_category(subject)
                due_date = week_start + timedelta(days=random.randint(0, 4))  # Mon-Fri
                title    = f"{category}: {subject} Week {due_date.isocalendar().week}"
                assignment_id = next_uuid("A")
                records.append({
                    "assignment_id": assignment_id,
                    "class_id": class_id,
                    "title": title,
                    "due_date": due_date.strftime("%Y-%m-%d"),
                    "points_possible": points,
                    "category": category,
                })
    return pd.DataFrame.from_records(records)


def generate_grades(assignments: pd.DataFrame,
                    enrollments: pd.DataFrame,
                    students: pd.DataFrame) -> pd.DataFrame:
    # Map students to per-student ability & trend
    ability = {
        sid: np.clip(np.random.normal(loc=80, scale=10), 50, 100)
        for sid in students["student_id"]
    }
    trend = {
        sid: np.random.choice([-0.1, 0, 0.1])  # -, flat, improving
        for sid in students["student_id"]
    }

    grade_records = []
    for _, asn in assignments.iterrows():
        asn_id  = asn["assignment_id"]
        class_id = asn["class_id"]
        points_possible = asn["points_possible"]
        due_date_dt = datetime.strptime(asn["due_date"], "%Y-%m-%d")

        roster = enrollments.loc[enrollments["class_id"] == class_id, "student_id"]
        for sid in roster:
            # Base score from ability + trend (later assignments get trend added)
            weeks_since_start = (due_date_dt - SCHOOL_START).days / 7
            base = ability[sid] + trend[sid] * weeks_since_start
            score_pct = np.clip(np.random.normal(base, 10), 0, 100)

            # Inject perfect / failing scores
            if random.random() < PERFECT_SCORE_PROB:
                score_pct = 100
            elif random.random() < FAILING_SCORE_PROB:
                score_pct = np.random.uniform(0, 59)

            score = round(points_possible * (score_pct / 100))

            # Submission date
            if random.random() < LATE_SUBMISSION_PROB:
                submitted = due_date_dt + timedelta(days=random.randint(1, 5))
            else:
                submitted = due_date_dt - timedelta(days=random.randint(0, 1))

            grade_records.append({
                "grade_id": next_uuid("G"),
                "student_id": sid,
                "assignment_id": asn_id,
                "score": score,
                "submitted_on": submitted.strftime("%Y-%m-%d"),
            })
    return pd.DataFrame.from_records(grade_records)


def main():
    parser = argparse.ArgumentParser(description="Generate assignments and grades.")
    parser.add_argument("--data_dir", required=True, type=Path,
                        help="Folder containing classes.csv, students.csv, enrollments.csv")
    parser.add_argument("--out_dir", default=None, type=Path,
                        help="Where to write assignments.csv & grades.csv (defaults to data_dir)")
    args = parser.parse_args()
    out_dir = args.out_dir or args.data_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    print("[1/4] Loading data …")
    classes, students, enrollments = load_data(args.data_dir)

    print("[2/4] Generating assignments …")
    assignments = generate_assignments(classes)
    assignments.to_csv(out_dir / "assignments.csv", index=False)
    print(f"      → {len(assignments):,} assignments saved.")

    print("[3/4] Generating grades …")
    grades = generate_grades(assignments, enrollments, students)
    grades.to_csv(out_dir / "grades.csv", index=False)
    print(f"      → {len(grades):,} grades saved.")

    print("[4/4] Done! 👍  Files written to", out_dir.resolve())


if __name__ == "__main__":
    main()

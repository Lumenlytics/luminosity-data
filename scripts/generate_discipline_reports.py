#!/usr/bin/env python3
"""
generate_discipline_reports.py
------------------------------
Simulates student discipline incidents throughout the school year.

INPUT
  ├── students.csv
  └── school_calendar.csv  (must include is_school_day = True)

OUTPUT
  └── discipline_reports.csv
"""

import pandas as pd
import random
import uuid
from pathlib import Path


def next_id():
    return f"D_{uuid.uuid4().hex[:6]}"


# Common discipline event types by severity
INCIDENTS = [
    ("Disruption", "Minor", "Verbal Warning"),
    ("Tardiness", "Minor", "Warning"),
    ("Dress Code Violation", "Minor", "Parent Contact"),
    ("Defiance", "Moderate", "Detention"),
    ("Inappropriate Language", "Moderate", "Detention"),
    ("Skipping Class", "Moderate", "Parent Meeting"),
    ("Fighting", "Severe", "Suspension"),
    ("Bullying", "Severe", "Suspension"),
    ("Physical Aggression", "Severe", "Suspension"),
]

DESCRIPTIONS = {
    "Disruption": "Talked loudly or interrupted class repeatedly.",
    "Tardiness": "Arrived late without a valid excuse.",
    "Dress Code Violation": "Wore clothing not in line with dress policy.",
    "Defiance": "Refused to follow teacher directions.",
    "Inappropriate Language": "Used offensive or inappropriate words.",
    "Skipping Class": "Did not attend assigned class without excuse.",
    "Fighting": "Engaged in a physical altercation with another student.",
    "Bullying": "Repeated harassment or intimidation of a peer.",
    "Physical Aggression": "Pushed, hit, or physically harmed another student.",
}


def generate_reports(students: pd.DataFrame, calendar: pd.DataFrame) -> pd.DataFrame:
    reports = []

    school_days = list(calendar[calendar["is_school_day"] == True]["calendar_date"])

    for _, student in students.iterrows():
        student_id = student["student_id"]

        # Random chance a student has discipline issues
        if random.random() < 0.2:  # 20% of students
            num_incidents = random.randint(1, 5)

            for _ in range(num_incidents):
                incident_type, severity, action = random.choice(INCIDENTS)
                description = DESCRIPTIONS[incident_type]
                date = random.choice(school_days)

                reports.append({
                    "report_id": next_id(),
                    "student_id": student_id,
                    "date": date,
                    "type": incident_type,
                    "severity": severity,
                    "action_taken": action,
                    "description": description
                })

    return pd.DataFrame(reports)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate student discipline reports.")
    parser.add_argument("--data_dir", required=True, type=Path)
    parser.add_argument("--out_file", required=True, type=Path)
    args = parser.parse_args()

    print("[1/3] Loading students and school calendar …")
    students = pd.read_csv(args.data_dir / "students.csv")
    calendar = pd.read_csv(args.data_dir / "school_calendar.csv")

    print("[2/3] Generating reports …")
    reports = generate_reports(students, calendar)
    print(f"      → {len(reports):,} total reports generated.")

    print("[3/3] Saving to file …")
    reports.to_csv(args.out_file, index=False)
    print(f"✅ Saved to {args.out_file.resolve()}")


if __name__ == "__main__":
    main()

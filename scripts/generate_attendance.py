#!/usr/bin/env python3
"""
generate_attendance.py
-----------------------
Creates daily attendance records for each student, based on school calendar.

INPUT (in --data_dir)
  ├── students.csv
  └── school_calendar.csv  # must include 'date' and 'is_school_day'

OUTPUT
  └── attendance.csv
"""

import pandas as pd
import random
import uuid
from pathlib import Path


def next_id(prefix="A"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


def load_data(data_dir: Path):
    students = pd.read_csv(data_dir / "students.csv")
    calendar = pd.read_csv(data_dir / "school_calendar.csv")
    calendar = calendar[calendar["is_school_day"] == True]  # only school days
    return students, calendar


def generate_attendance(students: pd.DataFrame, calendar: pd.DataFrame) -> pd.DataFrame:
    attendance = []

    for _, student in students.iterrows():
        student_id = student["student_id"]
        # Assign a "reliability" score: 0.0 = always absent, 1.0 = always present
        reliability = random.uniform(0.85, 0.99)

        for _, day in calendar.iterrows():
            date = day["calendar_date"]
            r = random.random()
            if r < reliability:
                status = "Present"
            elif r < reliability + 0.03:
                status = "Tardy"
            else:
                status = "Absent"

            attendance.append({
                "attendance_id": next_id(),
                "student_id": student_id,
                "date": date,
                "status": status
            })

    return pd.DataFrame(attendance)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate student attendance records.")
    parser.add_argument("--data_dir", required=True, type=Path)
    parser.add_argument("--out_file", required=True, type=Path)
    args = parser.parse_args()

    print("[1/3] Loading students and school calendar …")
    students, calendar = load_data(args.data_dir)

    print(f"[2/3] Generating attendance for {len(students):,} students over {len(calendar):,} days …")
    df = generate_attendance(students, calendar)
    print(f"      → {len(df):,} records generated.")

    print("[3/3] Saving to file …")
    df.to_csv(args.out_file, index=False)
    print(f"✅ Done! Saved to {args.out_file.resolve()}")


if __name__ == "__main__":
    main()

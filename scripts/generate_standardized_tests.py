#!/usr/bin/env python3
"""
generate_standardized_tests.py
------------------------------
Generates standardized test results for high school students.

INPUT
  └── students.csv

OUTPUT
  └── standardized_tests.csv
"""

import pandas as pd
import random
import uuid
from datetime import datetime
from pathlib import Path


def next_id():
    return f"T_{uuid.uuid4().hex[:6]}"


TEST_DEFINITIONS = {
    9: ("PSAT", "2015-10-20"),
    10: ("PSAT", "2015-10-20"),
    11: ("SAT", "2016-03-05"),
    12: ("ACT", "2016-04-10"),
}

SUBJECTS = {
    "PSAT": ["Math", "Reading", "Writing"],
    "SAT": ["Math", "Reading", "Writing"],
    "ACT": ["Math", "Reading", "Science", "English"]
}


def generate_tests(students: pd.DataFrame) -> pd.DataFrame:
    test_records = []

    for _, student in students.iterrows():
        grade = student["grade"]
        student_id = student["student_id"]

        if grade in TEST_DEFINITIONS:
            test_name, test_date = TEST_DEFINITIONS[grade]

            for subject in SUBJECTS[test_name]:
                # Simulate a test score (out of 800 for SAT/PSAT, 36 for ACT)
                if test_name == "ACT":
                    score = random.randint(14, 35)
                else:
                    score = random.randint(300, 750)

                percentile = min(99, max(1, int(random.normalvariate(50, 20))))

                test_records.append({
                    "test_id": next_id(),
                    "student_id": student_id,
                    "test_name": test_name,
                    "test_date": test_date,
                    "subject": subject,
                    "score": score,
                    "percentile": percentile
                })

    return pd.DataFrame(test_records)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate standardized test data.")
    parser.add_argument("--data_dir", required=True, type=Path)
    parser.add_argument("--out_file", required=True, type=Path)
    args = parser.parse_args()

    print("[1/3] Loading students …")
    students = pd.read_csv(args.data_dir / "students.csv")

    print("[2/3] Generating test scores …")
    test_data = generate_tests(students)
    print(f"      → {len(test_data):,} test records created.")

    print("[3/3] Saving to file …")
    test_data.to_csv(args.out_file, index=False)
    print(f"✅ Saved to {args.out_file.resolve()}")


if __name__ == "__main__":
    main()

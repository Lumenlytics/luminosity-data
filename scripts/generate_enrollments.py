#!/usr/bin/env python3
"""
generate_enrollments.py
-----------------------
Assigns students to appropriate classes based on grade level and class subject.

INPUT (in --data_dir)
  ├── students.csv      # student_id, grade_level, ...
  └── classes.csv       # class_id, grade_level, subject, ...

OUTPUT (to --out_file)
  └── enrollments.csv   # class_id, student_id
"""

import argparse
import pandas as pd
import random
from pathlib import Path


def load_data(data_dir: Path):
    students = pd.read_csv(data_dir / "students.csv")
    classes = pd.read_csv(data_dir / "classes.csv")
    return students, classes


def assign_students_to_classes(students: pd.DataFrame, classes: pd.DataFrame) -> pd.DataFrame:
    enrollments = []

    # Loop through each student
    for _, student in students.iterrows():
        student_id = student["student_id"]
        grade_level = student["grade"]

        # Filter classes for that grade
        eligible_classes = classes[classes["grade_level"] == grade_level]

        # If no classes found for this grade, skip
        if eligible_classes.empty:
            continue

        # Determine number of classes to assign based on grade
        if grade_level <= 5:
            # Elementary: 1 homeroom + 2–4 specials
            homerooms = eligible_classes[eligible_classes["subject"] == "Homeroom"]
            specials  = eligible_classes[eligible_classes["subject"] != "Homeroom"]
            assigned = []

            if not homerooms.empty:
                assigned += random.sample(list(homerooms["class_id"]), k=1)

            num_specials = random.randint(2, 4)
            if len(specials) >= num_specials:
                assigned += random.sample(list(specials["class_id"]), k=num_specials)
            else:
                assigned += list(specials["class_id"])

        else:
            # Middle/High: 5–7 classes
            num_classes = random.randint(5, 7)
            available_ids = list(eligible_classes["class_id"])
            assigned = random.sample(available_ids, k=min(num_classes, len(available_ids)))

        for class_id in assigned:
            enrollments.append({"class_id": class_id, "student_id": student_id})

    return pd.DataFrame(enrollments)


def main():
    parser = argparse.ArgumentParser(description="Generate student class enrollments.")
    parser.add_argument("--data_dir", required=True, type=Path,
                        help="Folder containing students.csv and classes.csv")
    parser.add_argument("--out_file", required=True, type=Path,
                        help="File to save enrollments.csv to")
    args = parser.parse_args()

    print("[1/3] Loading data …")
    students, classes = load_data(args.data_dir)

    print("[2/3] Assigning students to classes …")
    enrollments = assign_students_to_classes(students, classes)
    print(f"      → {len(enrollments):,} enrollments generated.")

    print("[3/3] Saving to file …")
    enrollments.to_csv(args.out_file, index=False)
    print(f"      ✅ Done! Saved to {args.out_file.resolve()}")


if __name__ == "__main__":
    main()

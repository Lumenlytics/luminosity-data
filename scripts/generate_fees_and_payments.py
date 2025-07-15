#!/usr/bin/env python3
"""
generate_fees_and_payments.py
-----------------------------
Creates fee_types.csv and payments.csv for school data.

INPUT
  └── students.csv

OUTPUT
  ├── fee_types.csv
  └── payments.csv
"""

import pandas as pd
import random
import uuid
from datetime import datetime, timedelta
from pathlib import Path


def next_id(prefix="FEE"):
    return f"{prefix}_{uuid.uuid4().hex[:6]}"


def generate_fee_types():
    return pd.DataFrame([
        {"fee_type_id": "FEE01", "name": "Tuition", "amount": 5000, "due_by": "2015-09-30", "recurring": "Annual"},
        {"fee_type_id": "FEE02", "name": "Lunch Plan", "amount": 400, "due_by": "2015-09-10", "recurring": "Monthly"},
        {"fee_type_id": "FEE03", "name": "Technology Fee", "amount": 100, "due_by": "2015-10-15", "recurring": "One-Time"},
        {"fee_type_id": "FEE04", "name": "Field Trip Fund", "amount": 50, "due_by": "2015-11-20", "recurring": "One-Time"},
        {"fee_type_id": "FEE05", "name": "Graduation Fee", "amount": 150, "due_by": "2016-05-01", "recurring": "One-Time"},
    ])


def generate_payments(students: pd.DataFrame, fee_types: pd.DataFrame):
    payments = []

    for _, student in students.iterrows():
        student_id = student["student_id"]

        for _, fee in fee_types.iterrows():
            fee_id = fee["fee_type_id"]
            amount_due = fee["amount"]
            due_by = datetime.strptime(fee["due_by"], "%Y-%m-%d")

            # Decide if the student pays (90% chance)
            paid = random.random() < 0.9

            if paid:
                amount_paid = amount_due
                pay_date = due_by - timedelta(days=random.randint(-5, 10))
                date_paid = pay_date.strftime("%Y-%m-%d")
            else:
                amount_paid = 0
                date_paid = ""

            payments.append({
                "payment_id": f"P_{uuid.uuid4().hex[:6]}",
                "student_id": student_id,
                "fee_type_id": fee_id,
                "amount_paid": amount_paid,
                "date_paid": date_paid
            })

    return pd.DataFrame(payments)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate school fees and student payments.")
    parser.add_argument("--data_dir", required=True, type=Path)
    parser.add_argument("--out_dir", required=True, type=Path)
    args = parser.parse_args()

    print("[1/4] Loading students …")
    students = pd.read_csv(args.data_dir / "students.csv")

    print("[2/4] Creating fee types …")
    fee_types = generate_fee_types()
    fee_types.to_csv(args.out_dir / "fee_types.csv", index=False)
    print("      → fee_types.csv created")

    print("[3/4] Creating payments …")
    payments = generate_payments(students, fee_types)
    payments.to_csv(args.out_dir / "payments.csv", index=False)
    print(f"      → {len(payments):,} payment records saved")

    print("[4/4] Done! Files saved to", args.out_dir.resolve())


if __name__ == "__main__":
    main()

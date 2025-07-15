#!/usr/bin/env python3
"""
check_schema_coverage.py
-------------------------
Scans /2015/csv for actual CSVs and compares to expected schema tables.
"""

from pathlib import Path

# List of all planned or schema-based table names
expected_tables = {
    "students", "guardians", "teachers", "classes", "enrollments",
    "assignments", "grades", "attendance", "school_years", "terms",
    "school_calendar", "periods", "payments", "fee_types",
    "users", "announcements", "discipline_reports", "standardized_tests"
}

# Path to your CSV directory
csv_dir = Path("2015/csv")
actual_csvs = {f.stem for f in csv_dir.glob("*.csv")}

print("✅ Existing CSV files:")
for name in sorted(actual_csvs):
    print(f"  - {name}")

print("\n🧩 Missing (still need to generate):")
missing = expected_tables - actual_csvs
for name in sorted(missing):
    print(f"  ❌ {name}")

print("\n📦 Extra (in folder but not in schema):")
extra = actual_csvs - expected_tables
for name in sorted(extra):
    print(f"  ⚠️  {name}")

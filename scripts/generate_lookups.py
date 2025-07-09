import pandas as pd
import os

# Define output directory
output_dir = os.path.join("2015", "csv")
os.makedirs(output_dir, exist_ok=True)

# Grade levels
grade_levels = [
    {"grade_level_id": 1, "name": "1st Grade", "level_order": 1},
    {"grade_level_id": 2, "name": "2nd Grade", "level_order": 2},
    {"grade_level_id": 3, "name": "3rd Grade", "level_order": 3},
    {"grade_level_id": 4, "name": "4th Grade", "level_order": 4},
    {"grade_level_id": 5, "name": "5th Grade", "level_order": 5},
    {"grade_level_id": 6, "name": "6th Grade", "level_order": 6},
    {"grade_level_id": 7, "name": "7th Grade", "level_order": 7},
    {"grade_level_id": 8, "name": "8th Grade", "level_order": 8},
    {"grade_level_id": 9, "name": "9th Grade", "level_order": 9},
    {"grade_level_id": 10, "name": "10th Grade", "level_order": 10},
    {"grade_level_id": 11, "name": "11th Grade", "level_order": 11},
    {"grade_level_id": 12, "name": "12th Grade", "level_order": 12},
]

# Guardian types
guardian_types = [
    {"guardian_type_id": 1, "name": "Mother"},
    {"guardian_type_id": 2, "name": "Father"},
    {"guardian_type_id": 3, "name": "Step-Mother"},
    {"guardian_type_id": 4, "name": "Step-Father"},
    {"guardian_type_id": 5, "name": "Grandmother"},
    {"guardian_type_id": 6, "name": "Grandfather"},
    {"guardian_type_id": 7, "name": "Aunt"},
    {"guardian_type_id": 8, "name": "Uncle"},
    {"guardian_type_id": 9, "name": "Legal Guardian"},
    {"guardian_type_id": 10, "name": "Other"},
]

# Departments
departments = [
    {"department_id": 1, "name": "Mathematics"},
    {"department_id": 2, "name": "Science"},
    {"department_id": 3, "name": "English"},
    {"department_id": 4, "name": "Social Studies"},
    {"department_id": 5, "name": "Foreign Languages"},
    {"department_id": 6, "name": "Physical Education"},
    {"department_id": 7, "name": "Fine Arts"},
    {"department_id": 8, "name": "Technology"},
    {"department_id": 9, "name": "Electives"},
]

# Save as CSVs
pd.DataFrame(grade_levels).to_csv(os.path.join(output_dir, "grade_levels.csv"), index=False)
pd.DataFrame(guardian_types).to_csv(os.path.join(output_dir, "guardian_types.csv"), index=False)
pd.DataFrame(departments).to_csv(os.path.join(output_dir, "departments.csv"), index=False)

print("Lookup CSVs generated in '2015/csv/'")

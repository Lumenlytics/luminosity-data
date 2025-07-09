import pandas as pd
import os

# Output directory
output_dir = os.path.join("2015", "csv")
os.makedirs(output_dir, exist_ok=True)

# Terms for 2015–2016 school year
terms = [
    {"term_id": 1, "school_year_id": 1, "name": "Q1 2015", "start_date": "2015-08-24", "end_date": "2015-10-30"},
    {"term_id": 2, "school_year_id": 1, "name": "Q2 2015", "start_date": "2015-11-02", "end_date": "2016-01-15"},
    {"term_id": 3, "school_year_id": 1, "name": "Q3 2016", "start_date": "2016-01-19", "end_date": "2016-03-25"},
    {"term_id": 4, "school_year_id": 1, "name": "Q4 2016", "start_date": "2016-03-28", "end_date": "2016-06-09"},
]

# Save as CSV
df = pd.DataFrame(terms)
df.to_csv(os.path.join(output_dir, "terms.csv"), index=False)

print("✅ terms.csv generated in '2015/csv/'")

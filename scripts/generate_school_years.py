import pandas as pd
import os

# Define output directory
output_dir = os.path.join("2015", "csv")
os.makedirs(output_dir, exist_ok=True)

# School year entry
school_years = [
    {
        "school_year_id": 1,
        "year_label": "2015–2016",
        "start_date": "2015-08-24",
        "end_date": "2016-06-09"
    }
]

# Save as CSV
df = pd.DataFrame(school_years)
df.to_csv(os.path.join(output_dir, "school_years.csv"), index=False)

print("✅ school_years.csv generated in '2015/csv/'")

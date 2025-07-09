import pandas as pd
import os

# Output location
output_dir = os.path.join("2015", "csv")
os.makedirs(output_dir, exist_ok=True)

# Define the periods
periods = [
    {"period_id": 1, "name": "Period 1", "start_time": "08:00:00", "end_time": "08:50:00"},
    {"period_id": 2, "name": "Period 2", "start_time": "09:00:00", "end_time": "09:50:00"},
    {"period_id": 3, "name": "Period 3", "start_time": "10:00:00", "end_time": "10:50:00"},
    {"period_id": 4, "name": "Period 4", "start_time": "11:00:00", "end_time": "11:50:00"},
    {"period_id": 5, "name": "Period 5", "start_time": "12:30:00", "end_time": "13:20:00"},
    {"period_id": 6, "name": "Period 6", "start_time": "13:30:00", "end_time": "14:20:00"},
    {"period_id": 7, "name": "Period 7", "start_time": "14:30:00", "end_time": "15:20:00"},
]

# Save to CSV
df = pd.DataFrame(periods)
df.to_csv(os.path.join(output_dir, "periods.csv"), index=False)

print("✅ periods.csv generated in '2015/csv/'")

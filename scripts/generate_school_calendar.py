import pandas as pd
import os
from datetime import datetime, timedelta

# ---------- CONFIG ----------
START_DATE = datetime(2015, 8, 24)
END_DATE   = datetime(2016, 6, 9)

# Holidays / breaks (inclusive ranges)
HOLIDAYS = {
    "Labor Day":               ("2015-09-07", "2015-09-07"),
    "Fall PD Day":             ("2015-10-09", "2015-10-09"),
    "Thanksgiving Break":      ("2015-11-26", "2015-11-27"),
    "Winter Break":            ("2015-12-21", "2016-01-04"),
    "Martin Luther King Jr Day":("2016-01-18", "2016-01-18"),
    "Presidents' Day PD":      ("2016-02-15", "2016-02-15"),
    "Spring Break":            ("2016-03-28", "2016-04-01"),
    "Memorial Day":            ("2016-05-30", "2016-05-30"),
}

# ---------- BUILD CALENDAR ----------
rows = []
current = START_DATE
while current <= END_DATE:
    date_str = current.strftime("%Y-%m-%d")
    weekday = current.weekday()  # 0 = Monday
    is_weekend = weekday >= 5    # Sat/Sun
    
    # default flags
    is_school_day = not is_weekend
    is_holiday    = False
    holiday_name  = ""
    comment       = ""
    
    # mark holidays / breaks
    for name, (start, end) in HOLIDAYS.items():
        if start <= date_str <= end:
            is_holiday = True
            is_school_day = False
            holiday_name = name
            break
    
    # weekends are not school days
    if is_weekend:
        is_school_day = False
        comment = "Weekend"
    
    rows.append({
        "calendar_date": date_str,
        "is_school_day": is_school_day,
        "is_holiday": is_holiday,
        "holiday_name": holiday_name,
        "comment": comment
    })
    
    current += timedelta(days=1)

# ---------- SAVE ----------
output_dir = os.path.join("2015", "csv")
os.makedirs(output_dir, exist_ok=True)
pd.DataFrame(rows).to_csv(os.path.join(output_dir, "school_calendar.csv"), index=False)

print("✅ school_calendar.csv generated with", len(rows), "rows")

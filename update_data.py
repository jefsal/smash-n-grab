# File: update_data.py
# Author: Jeffrey Salinas
# Description: Fetch data from DataSF API and save to csv, 
#               sf_vis.py will read from csv
import os
import csv
import io
from datetime import datetime
from zoneinfo import ZoneInfo
import requests

# declare absolute output file and path, easy access for streamlit
OUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "current_month_data.csv",
)
DATA_URL = "https://data.sfgov.org/resource/wg3w-h783.csv"
LOCAL_TZ = ZoneInfo("America/Los_Angeles")
EXPECTED_COLUMNS = {
    "incident_datetime",
    "incident_date",
    "report_datetime",
    "incident_subcategory",
    "latitude",
    "longitude",
}


def get_month_window(today=None):
    today = today or datetime.now(LOCAL_TZ)
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    if month_start.month == 12:
        next_month_start = month_start.replace(year=month_start.year + 1, month=1)
    else:
        next_month_start = month_start.replace(month=month_start.month + 1)

    return month_start, next_month_start


def validate_csv(csv_text):
    reader = csv.DictReader(io.StringIO(csv_text))
    columns = set(reader.fieldnames or [])
    missing_columns = EXPECTED_COLUMNS - columns
    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise ValueError(f"DataSF response missing expected columns: {missing}")


# fetch current month data daily with filters
def fetch_current_month_data():
    # format dates for SoQL query compatability
    month_start, next_month_start = get_month_window()
    f_month_start = month_start.strftime("%Y-%m-%d")
    f_next_month_start = next_month_start.strftime("%Y-%m-%d")

    # SoQL filter to only fetch from the API the
    #   subcategory "Larceny - from vehicle"
    #   incidents after the first day of the month
    #       AND
    #   incidents before the the first day of next month
    where_filter = (
        'incident_subcategory = "Larceny - From Vehicle" '
        f"AND incident_date >= '{f_month_start}' "
        f"AND incident_date < '{f_next_month_start}'"
    ) 

    # API call parameters
    params = {
        "$where": where_filter,
        "$order": "incident_datetime ASC",
        "$limit": "50000",
    }

    # API call and catch HTTP errors
    response = requests.get(DATA_URL, params=params, timeout=30)
    response.raise_for_status()

    return response


# save data to file and return rows saved
def save_monthly_data_to_file():
    # save current month data to csv file
    current_data = fetch_current_month_data()
    validate_csv(current_data.text)

    with open(OUT_FILE, "w", encoding="utf-8", newline="") as out_f:
        out_f.write(current_data.text)

    # count data rows, excluding the header
    total_rows = max(len(current_data.text.splitlines()) - 1, 0)
    return total_rows


if __name__ == "__main__":
    saved_data_rows = save_monthly_data_to_file()
    print(f"Saved {saved_data_rows} rows to {OUT_FILE}")

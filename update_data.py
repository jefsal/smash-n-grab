# File: update_data.py
# Author: Jeffrey Salinas
# Description: Fetch data from DataSF API and save to csv, 
#               sf_vis.py will read from csv
import os
from datetime import datetime
import requests

# delcare output file and path, easy access for streamlit
OUT_FILE = os.path.join(
    os.path.dirname(__file__),
    "current_month_data.csv",
)

# fetch current month data daily and cache on server for 60s
def fetch_current_month_data():
    # public API endpoint from DataSF
    url = "https://data.sfgov.org/resource/wg3w-h783.csv"
 
    # format dates for SoQL query compatability
    today = datetime.now()
    month_start = today.replace(day=1, hour=0, minute=0, second=0)
    f_month_start = month_start.strftime("%Y-%m-%d")

    next_month_start = today.replace(month=today.month + 1, day=1, hour=0, minute=0, second=0)
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
    }

    # API call and catch HTTP errors
    response = requests.get(url, params=params, timeout=10)
    response.raise_for_status()

    # clean date values ?? maybe?
    return response

# save data to file and return rows saved
def save_monthly_data_to_file():
    # save current month data to csv file
    current_data = fetch_current_month_data()
    with open(OUT_FILE, "w", encoding="utf-8", newline="") as out_f:
        out_f.write(current_data.text)

    # count total rows 
    total_rows = len(current_data.text.splitlines())
    return total_rows

# print success
saved_data_rows= save_monthly_data_to_file()
print(f"Saved {saved_data_rows} rows to {OUT_FILE}")

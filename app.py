# File: app.py
# Author: Jeffrey Salinas
# Description : Process local csv data about SF crime, larceny, rendered into a
#                web page in just python using streamlit
#

# import numpy as np
import streamlit as st
import pandas as pd
import os
import json
from datetime import datetime


col1, col2 = st.columns(2)
with col1:
    # Short intro
    st.title("Crime in San Francisco")
    st.write("There is a popular form of crime that San Francisco has become accostomed to, Larceny Theft and more specifically larceny theft from a vehicle. Better known as \"smash and grab.\"")
    st.write("I am curious about what trends and patterns, if any, we can identify by pulling public data from police reports and filtering for larceny theft from a vehicle.")
with col2:
    # image 
    st.image("assets/car-window-break-in.jpg")
    st.caption("POV your macbook is gone")
st.divider()


# 2025 larceny theft records 
st.subheader("Smash and Grabs This Month")

# declare the absolute csv path for curent month
current_month_csv_path = os.path.join(
    os.path.dirname(__file__),
    "current_month_data.csv",
)
last_updated_path = os.path.join(
    os.path.dirname(__file__),
    "data_update_metadata.json",
)

# Fetch data from csv and cache
@st.cache_data
def load_current_month_data():
    # read saved data from csv
    saved_data = pd.read_csv(current_month_csv_path)

    # format incident date time for dt accessor
    saved_data["incident_date"] = pd.to_datetime(saved_data["incident_date"])
    saved_data["incident_datetime"] = pd.to_datetime(saved_data["incident_datetime"])
    saved_data["report_datetime"] = pd.to_datetime(saved_data["report_datetime"])

    return saved_data


# fetch the date the local csv was last updated
@st.cache_data
def load_last_update_date():
    try:
        with open(last_updated_path, encoding="utf-8") as metadata_f:
            metadata = json.load(metadata_f)

        last_successful_update = datetime.fromisoformat(
            metadata["last_successful_update"]
        )
    except (FileNotFoundError, KeyError, TypeError, ValueError):
        return "Unknown"

    return (
        f"{last_successful_update:%B} "
        f"{last_successful_update.day}, "
        f"{last_successful_update:%Y}"
    )


try:
    # read from local save csv file
    current_month = load_current_month_data()
    last_update_date = load_last_update_date()

    if current_month.empty:
        st.write("No incidents this month!")
    else:
        current_month_name = current_month["incident_date"].dt.month_name().iloc[0]

        # categorize incidents by day for chart readability
        # dt.normalize() to remove time, group all incidents on the same day
        current_month_per_day = (
                current_month.assign(
                    incident_day=current_month["incident_date"].dt.normalize()
                )
                .groupby("incident_day")
                .size()
                .reset_index(name="Reports")
                .sort_values("incident_day").set_index("incident_day")
        )

        st.write("Larceny - from vehicle")
        # summarize metrics, verify query to local csv worked successfully

        col3, col4 = st.columns(2)
        with col3:
            st.caption(f"rows loaded from local csv: {len(current_month)}")

        with col4:
            st.caption(f"data last updated on: {last_update_date}")

        # show monthly chart grouped by day
        st.subheader(f"Reported incidents in {current_month_name} grouped by day")
        st.line_chart(current_month_per_day)
        st.divider()

        # if row has coordinates, show on map
        map_data = current_month.dropna(subset=["latitude", "longitude"])

        st.subheader("Incidnet Map")
        st.map(map_data[["latitude","longitude"]])

        st.write("Here we have the current month's Larceny from a vehicle incidents displayed over a map of San Francisco.") 
        st.write("This is possible because with most police reports latitude and longitude coordinates are included, although they only point to the nearest intersection and not the exact coordinates of the incident.")
except FileNotFoundError:
    st.error("The saved local file was not found")
except Exception as unexpected_error:
    st.error(f"Unexpected error found while running: {unexpected_error}") 
    

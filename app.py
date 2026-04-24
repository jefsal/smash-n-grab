# File: app.py
# Author: Jeffrey Salinas
# Description : Process local csv data about SF crime, larceny, rendered into a
#                web page in just python using streamlit
#

# import numpy as np
import streamlit as st
import pandas as pd
import os


col1, col2 = st.columns(2)
with col1:
    # Short intro
    st.title("Crime in San Francisco")
    st.write("There is a popular form of crime that San Francisco has become accostomed to, Larceny Theft and more specifically larceny theft from a vehicle. Better known as \"smash and grab.\"")
    st.write("I am curious about what trends and patterns, if any, we can identify by pulling public data from police reports and filtering for larceny theft from a vehicle.")
with col2:
    # image 
    st.image("car-window-break-in.jpg")
    st.caption("POV your macbook is gone")


st.divider()

# 2025 larceny theft records 
st.subheader("Smash and Grabs This Month")

# declare the absolute csv path for curent month
current_month_csv_path = os.path.join(
    os.path.dirname(__file__),
    "current_month_data.csv",
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


try:
    # read from local save csv file
    current_month = load_current_month_data()

    if current_month.empty:
        st.write("No incidents this month!")
    else:
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
        # summarize metrics, verify query to local csv worked
        st.caption(f"rows loaded from local csv: {len(current_month)}")

        # show monthly chart grouped by day
        st.subheader("Current month reported incidents grouped by day")
        st.area_chart(current_month_per_day)
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
    

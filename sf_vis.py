# File: sf_vis.py
# Author: Jeffrey Salinas
# 
#

import numpy as np
import streamlit as st
import pandas as pd

# Short intro
st.title("Crime in San Francisco")
st.write("There is a popular form of crime that San Francisco has become accostomed to, Larceny Theft and more specifically larceny theft from a vehicle. Better known as \"smash and grab.\" I am curious about what trends, if any, we can identify by pulling public data from police reports and filtering for larceny theft from a vehicle.")

# 2025 larceny theft records 
st.subheader("2025")

# Fetch current month data daily and cache on server for 60s
@st.cache_data(ttl=60)
def fetch_current_month_data():
    # public API endpoint from DataSF
    url = "https://data.sfgov.org/resource/wg3w-h783.json"

    today = datetime.now()
    month_start = now.replace(day=1, hour=0, minute=0)


    # SoQL filter to only fetch from the API the
    #   subcategory "Larceny - from vehicle"
    #   incidents after the first day of the month
    #       AND
    #   incidents before the the first day of next month
    


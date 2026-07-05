# smash and grab

live here: https://smashandgrab.streamlit.app/

Small Streamlit app for visualizing San Francisco larceny-from-vehicle incidents using publicly available police incident data from DataSF.

## What It Is

This project pulls current-month incident data for `Larceny - From Vehicle` in San Francisco, saves it locally as a CSV, and displays it in a Streamlit dashboard with:

- a daily incident trend chart
- a map of reported incident locations

## Why

I started this project because I was curious on what data visualization can allow us to see from the publicly available data from [DataSF](https://data.sfgov.org) on larceny from a vehicle in San Francisco. I also wanted to refresh my Python skills by using a new framework, [Streamlit](https://streamlit.io/).

## Project Structure

```text
bip-maps/
├── app.py                   # Main Streamlit app
├── update_data.py           # Fetches current-month data from DataSF
├── sf_vis.py                # Alternate Streamlit app variant
├── current_month_data.csv   # Local saved dataset
├── car-window-break-in.jpg  # App image asset
├── requirements.txt         # Python dependencies
└── README.md
```

## Data Source

Official source used by this project:

- DataSF Police Department Incident Reports (2018 to Present): https://data.sfgov.org/Public-Safety/Police-Department-Incident-Reports-2018-to-Present/wg3w-h783/about_data

## Run

```bash
python3 update_data.py
streamlit run app.py
```

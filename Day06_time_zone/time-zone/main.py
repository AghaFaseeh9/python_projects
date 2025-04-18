import streamlit as st
from datetime import datetime
from zoneinfo import ZoneInfo

# List of time zones
TIME_ZONE = [
    "UTC",
    "Asia/Karachi",
    "America/New_York",
    "Europe/London",
    "Asia/Tokyo",
    "Australia/Sydney",
    "America/Los_Angeles",
    "Europe/Berlin",
    "Asia/Dubai",
    "Asia/Kolkata",
]

# title of application
st.title("Time Zone Application")

# Selection of time zone
selected_timezone = st.multiselect(
    "Select the Zone", TIME_ZONE, default=["UTC", "Asia/Karachi"]
)

# subheading
st.subheader("Selected Timezones")
for tz in selected_timezone:
    current_time = datetime.now(ZoneInfo(tz)).strftime("%Y-%m-%d %I:%M:%S %p")
    st.write(f"**{tz}**:{current_time}")

st.subheader("Convert Time Between Timezones")
current_time = st.time_input("Current Time", value=datetime.now().time())
from_tz = st.selectbox("From TimeZone", TIME_ZONE, index=0)
to_tz = st.selectbox("To TimeZone", TIME_ZONE, index=1)

if st.button("Convert Time"):
    dt = datetime.combine(datetime.today(), current_time, tzinfo=ZoneInfo(from_tz))
    converted_time = dt.astimezone(ZoneInfo(to_tz)).strftime("%Y-%M-%d %I:%M:%S %p")
    st.success(f"Converted Time in {converted_time}")

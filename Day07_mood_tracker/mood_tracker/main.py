import streamlit as st
import os
import csv
import datetime
import pandas as pd
from datetime import timedelta

# Constants
MOOD_FILE = "mood_log.csv"
MOODS = {
    "😊 Happy": "Happy",
    "😌 Calm": "Calm",
    "😐 Neutral": "Neutral",
    "😔 Sad": "Sad",
    "😤 Angry": "Angry",
    "😰 Stressed": "Stressed",
    "😴 Tired": "Tired",
    "🤔 Thoughtful": "Thoughtful"
}

# Initialize session state
if 'last_mood' not in st.session_state:
    st.session_state.last_mood = None

# Page configuration
st.set_page_config(
    page_title="Mood Tracker",
    page_icon="😊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .success {
        padding: 1rem;
        border-radius: 0.5rem;
        background-color: #D4EDDA;
        color: #155724;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def load_mood_data():
    """Load and process mood data from CSV file."""
    if not os.path.exists(MOOD_FILE):
        # Create file with headers if it doesn't exist
        with open(MOOD_FILE, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Mood", "Notes"])
        return pd.DataFrame(columns=["Date", "Mood", "Notes"])
    
    try:
        df = pd.read_csv(MOOD_FILE)
        if df.empty:
            return pd.DataFrame(columns=["Date", "Mood", "Notes"])
        
        # Clean up the data
        df = df.dropna(how='all')
        df = df.fillna({'Notes': ''})  # Fill NaN notes with empty string
        
        # Convert Date column to datetime
        df['Date'] = pd.to_datetime(df['Date'])
        
        # Sort by date
        df = df.sort_values('Date')
        
        return df
    except Exception as e:
        st.error(f"Error loading mood data: {str(e)}")
        return pd.DataFrame(columns=["Date", "Mood", "Notes"])

def save_mood_data(date, mood, notes):
    """Save mood data to CSV file."""
    try:
        with open(MOOD_FILE, "a", newline='') as file:
            writer = csv.writer(file)
            writer.writerow([date, mood, notes])
        return True
    except Exception as e:
        st.error(f"Error saving mood: {str(e)}")
        return False

def get_latest_mood(data, date):
    """Get the latest mood for a specific date."""
    day_data = data[data['Date'].dt.date == date]
    if day_data.empty:
        return None, None
    latest = day_data.iloc[-1]
    return latest['Mood'], latest['Notes']

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Log Mood", "View Analytics", "Export Data"])

if page == "Log Mood":
    st.title("Mood Tracker")
    st.markdown("### How are you feeling today?")
    
    # Mood selection with emojis
    mood_display = st.selectbox(
        "Select your mood",
        list(MOODS.keys()),
        index=0
    )
    selected_mood = MOODS[mood_display]
    
    # Notes section
    notes = st.text_area("Add any notes about your mood (optional)")
    
    # Log mood button
    if st.button("Log Mood", type="primary"):
        today = datetime.date.today()
        if save_mood_data(today, selected_mood, notes):
            st.session_state.last_mood = selected_mood
            st.success("Mood logged successfully! 🎉")
            st.rerun()
    
    # Show today's latest mood
    data = load_mood_data()
    if not data.empty:
        today = datetime.date.today()
        latest_mood, latest_notes = get_latest_mood(data, today)
        if latest_mood:
            st.info(f"Today's latest mood: {latest_mood}")
            if latest_notes:
                st.info(f"Notes: {latest_notes}")

elif page == "View Analytics":
    st.title("Mood Analytics")
    
    data = load_mood_data()
    if not data.empty:
        # Date range selector
        min_date = data['Date'].min().date()
        max_date = data['Date'].max().date()
        
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", min_date)
        with col2:
            end_date = st.date_input("End Date", max_date)
        
        if start_date <= end_date:
            filtered_data = data[
                (data['Date'].dt.date >= start_date) & 
                (data['Date'].dt.date <= end_date)
            ]
            
            if not filtered_data.empty:
                # Mood distribution
                st.subheader("Mood Distribution")
                mood_counts = filtered_data['Mood'].value_counts()
                st.bar_chart(mood_counts)
                
                # Mood trends
                st.subheader("Mood Trends Over Time")
                mood_trends = filtered_data.set_index('Date')['Mood']
                st.line_chart(mood_trends)
                
                # Statistics
                st.subheader("Mood Statistics")
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Entries", len(filtered_data))
                with col2:
                    most_common = filtered_data['Mood'].mode().iloc[0]
                    st.metric("Most Common Mood", most_common)
                with col3:
                    unique_moods = filtered_data['Mood'].nunique()
                    st.metric("Unique Moods", unique_moods)
                
                # Recent entries
                st.subheader("Recent Entries")
                recent_data = filtered_data.sort_values('Date', ascending=False).head()
                st.dataframe(
                    recent_data[['Date', 'Mood', 'Notes']].style.format({
                        'Date': lambda x: x.strftime('%Y-%m-%d')
                    })
                )
            else:
                st.info("No data available for selected date range.")
        else:
            st.error("End date must be after start date.")
    else:
        st.info("No mood data available yet. Start logging your moods!")

elif page == "Export Data":
    st.title("Export Mood Data")
    
    data = load_mood_data()
    if not data.empty:
        # Export options
        export_format = st.selectbox("Select export format", ["CSV", "Excel"])
        
        if st.button("Export Data"):
            try:
                if export_format == "CSV":
                    csv_data = data.to_csv(index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_data,
                        file_name="mood_data.csv",
                        mime="text/csv"
                    )
                else:
                    # Convert datetime to string for Excel export
                    data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
                    excel_data = data.to_excel(index=False)
                    st.download_button(
                        label="Download Excel",
                        data=excel_data,
                        file_name="mood_data.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                    )
                st.success("Data ready for download!")
            except Exception as e:
                st.error(f"Error preparing export: {str(e)}")
    else:
        st.info("No data available to export. Start logging your moods!")

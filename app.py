import streamlit as st
import pandas as pd

# Set up the main page
st.set_page_config(page_title="Exams Timetable", layout="wide")
st.title("Exams Timetable")

# Load the Excel data
@st.cache_data
def load_data():
    df = pd.read_excel('data.xlsx')
    return df

try:
    df = load_data()
except FileNotFoundError:
    st.error("Could not find data.xlsx. Please ensure the file is in the same folder.")
    st.stop() # Stops the rest of the app from running if there's an error

# --- SIDEBAR FILTERS ---
st.sidebar.header("Filter Timetable")

# 1. Get unique values for each column and add an "All" option at the beginning
days = ["All"] + list(df['Date'].unique())
subjects = ["All"] + list(df['Subject'].unique())
classes = ["All"] + list(df['Class'].unique())
teachers = ["All"] + list(df['Teacher'].unique())

# 2. Create the dropdown menus in the sidebar

selected_day = st.sidebar.selectbox("By Date", days)
selected_subject = st.sidebar.selectbox("By Subject", subjects)
selected_class = st.sidebar.selectbox("By Class", classes)
selected_teacher = st.sidebar.selectbox("By Teacher", teachers)

# --- FILTERING LOGIC ---
# Start with the full table
filtered_df = df.copy()

# Apply filters one by one if the user selected something other than "All"
if selected_day != "All":
    filtered_df = filtered_df[filtered_df['Date'] == selected_day]
    
if selected_subject != "All":
    filtered_df = filtered_df[filtered_df['Subject'] == selected_subject]
    
if selected_class != "All":
    filtered_df = filtered_df[filtered_df['Class'] == selected_class]
    
if selected_teacher != "All":
    filtered_df = filtered_df[filtered_df['Teacher'] == selected_teacher]

# --- DISPLAY DATA ---
# Show the number of results found
st.write(f"Showing {len(filtered_df)} exams:")

# Display the final filtered table
st.dataframe(filtered_df, use_container_width=True)


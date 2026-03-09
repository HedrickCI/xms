import streamlit as st
import pandas as pd

# 1. Page Configuration
# Setting initial_sidebar_state to collapsed gives more screen space on mobile
st.set_page_config(page_title="Exams Timetable", layout="wide", initial_sidebar_state="collapsed")
st.title("Exams Timetable")

# 2. Data Loading and Header Cleaning
@st.cache_data
def load_data():
    df = pd.read_excel('data.xlsx')
    # Clean headers: strip hidden spaces and standardize capitalization
    df.columns = df.columns.str.strip().str.title()
    return df

try:
    df = load_data()
except Exception as e:
    st.error("Could not load data.xlsx. Please ensure the file is in the same folder and is a valid Excel file.")
    st.stop()

# 3. Mobile-Friendly Filter UI
# The expander keeps the UI clean on small screens
with st.expander("🔍 Tap here to filter the timetable", expanded=False):
    # Columns stack vertically on mobile, but sit side-by-side on desktop
    col1, col2 = st.columns(2)
    
    filters = {}
    
    # Helper function to generate dropdowns safely
    def create_filter(col_layout, column_name, label):
        if column_name in df.columns:
            # Get unique values, ignore blanks, and sort alphabetically
            unique_vals = [val for val in df[column_name].unique() if pd.notna(val)]
            options = ["All"] + sorted(unique_vals)
            with col_layout:
                selected = st.selectbox(label, options)
                if selected != "All":
                    filters[column_name] = selected

    # Build the dropdowns in their respective columns
    create_filter(col1, 'Day', 'By Day')
    create_filter(col1, 'Subject', 'By Subject')
    create_filter(col2, 'Class', 'By Class')
    create_filter(col2, 'Teacher', 'By Teacher')

# 4. Apply Filters
filtered_df = df.copy()
for col_name, selected_val in filters.items():
    filtered_df = filtered_df[filtered_df[col_name] == selected_val]

# 5. Display the Results
st.write(f"**Showing {len(filtered_df)} exams:**")
st.dataframe(filtered_df, use_container_width=True)

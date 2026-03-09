import streamlit as st
import pandas as pd

st.set_page_config(page_title="Exams Timetable", layout="wide")
st.title("Exams Timetable")

@st.cache_data
def load_data():
    df = pd.read_excel('data.xlsx')
    # Strip accidental leading or trailing spaces from column headers
    df.columns = df.columns.str.strip()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading data: {e}")
    st.stop()

st.sidebar.header("Filter Timetable")
filtered_df = df.copy()

# Define the filters we want to create
target_filters = ['Day', 'Subject', 'Class', 'Teacher']

# Loop through our targets and build filters dynamically
for target in target_filters:
    # Find the matching column in the dataframe, ignoring uppercase/lowercase differences
    matching_cols = [col for col in df.columns if str(col).lower() == target.lower()]
    
    if matching_cols:
        actual_col = matching_cols[0]
        # Get unique values, remove any blank cells, and sort them alphabetically
        unique_vals = [val for val in df[actual_col].unique() if pd.notna(val)]
        options = ["All"] + sorted(unique_vals)
        
        selected = st.sidebar.selectbox(f"By {target}", options)
        
        # Apply the filter if something other than "All" is selected
        if selected != "All":
            filtered_df = filtered_df[filtered_df[actual_col] == selected]

st.write(f"Showing {len(filtered_df)} exams:")
st.dataframe(filtered_df, use_container_width=True)

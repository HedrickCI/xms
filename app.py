import streamlit as st
import pandas as pd

# 1. Configure the page settings
st.set_page_config(page_title="My Data Viewer", layout="wide")

st.title("Local Spreadsheet Viewer")

# 2. Define a function to load the data
# The @st.cache_data decorator ensures the file is only read once, speeding up the app
@st.cache_data
def load_data():
    # Make sure this matches your exact Excel file name
    df = pd.read_excel('data.xlsx')
    return df

# 3. Load and display the data
try:
    data = load_data()
    # st.dataframe creates an interactive table with built-in sorting and searching
    st.dataframe(data, use_container_width=True)
except FileNotFoundError:
    st.error("Could not find data.xlsx. Please ensure the file is in the same folder.")
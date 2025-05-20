import requests
import pandas as pd
import streamlit as st
from utils import elements

# Constants
tables = [
    "aut_nums",
    "as_sets",
    "route_sets",
    "peering_sets",
    "filter_sets",
    "as_routes",
]

# Page configs
st.set_page_config(
    page_title="My App", layout="wide", initial_sidebar_state="collapsed"
)

# Page state
for table in tables:
    if f"{table}_skip" not in st.session_state:
        st.session_state[f"{table}_skip"] = 0
    if f"{table}_limit" not in st.session_state:
        st.session_state[f"{table}_limit"] = 10

# Header
elements.small_header()

# Multiselection of data to be displayed
options = st.multiselect(
    label="Which tables do you want to see?",
    options=tables,
    default=tables[:2],
)

# Displays each table
for option in options:
    # Getting the data
    r = requests.get(
        f"http://localhost:8000/{option}?skip={st.session_state[f"{option}_skip"]}&limit={st.session_state[f"{option}_limit"]}"
    )
    data = r.json()

    # Showing the data
    st.header(option, divider="gray")
    df = pd.DataFrame.from_dict(data["data"], orient="index")
    st.dataframe(df)

    # Data navigation controls
    st.session_state.count = data["count"]
    elements.navigation_controls(option)

    st.divider()

# Footer
elements.footer()

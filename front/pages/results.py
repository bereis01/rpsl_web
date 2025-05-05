import requests
import pandas as pd
import streamlit as st
from utils import elements

# Page configs
st.set_page_config(
    page_title="My App",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Search space
logo_space, search_space, _ = st.columns(
    [0.1, 0.4, 0.5], vertical_alignment="center", gap="large"
)
logo_space.image("assets/internet.png")
with search_space:
    query = st.text_input(
        label="Enter a prefix, IP address, AS number or AS/route set name.",
        value=st.session_state.query,
        placeholder="Prefix, IP, ASN or AS/route-set",
    )

# Query results
if query:
    st.markdown("#####")
    st.title(f"Results for {query}")

    # Getting the data
    r = requests.get(f"http://localhost:8000/search/asn/{query}")
    data = r.json()

    # Showing the aut_nums data
    st.header("Routing Policies", divider="gray")
    with st.container(height=200, border=True):
        st.text(data["aut_nums"]["body"])
    st.subheader("Imports")
    df = pd.DataFrame.from_records(
        data["aut_nums"]["imports"], columns=["Type", "Peers", "Filter"]
    )
    with st.container(height=300, border=True):
        st.table(df)
    st.subheader("Exports")
    df = pd.DataFrame.from_records(
        data["aut_nums"]["exports"], columns=["Type", "Peers", "Filter"]
    )
    with st.container(height=300, border=True):
        st.table(df)
    st.divider()

    # Showing the as_sets data
    """ st.header("AS Sets", divider="gray")
    df = pd.DataFrame.from_records(data["as_sets"])
    st.table(df)
    st.divider() """

# Footer
elements.footer()

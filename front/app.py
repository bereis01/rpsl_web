import requests
import pandas as pd
import streamlit as st
from utils.results.asn import show_results_asn

st.set_page_config(
    page_title="RPSLweb",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Header
_, logo_space, _, _ = st.columns([0.2, 0.15, 0.45, 0.2], vertical_alignment="bottom")
_, search_space, _ = st.columns([0.2, 0.6, 0.2], vertical_alignment="top")

# Displays the logo
logo_space.image("assets/logo.png")

# Search box
with search_space:
    query = st.text_input(
        label="Enter an AS number.",
        value=st.session_state.query if "query" in st.session_state else None,
        placeholder="ASN",
    )

# Body
_, results_space, _ = st.columns([0.2, 0.6, 0.2], vertical_alignment="center")
_, results_space_condensed, _ = st.columns([0.3, 0.4, 0.3], vertical_alignment="center")

# Shows temporary text before any query is made
if not query:
    with results_space_condensed:
        st.markdown(
            """
            <div style="text-align: center">
            <strong>rpslweb.</strong> makes available useful information regarding data contained within the IRR.

            You can query for AS numbers, AS set names, route sets and other keywords and receive digested analysis and information, as well as the source data used to generate it.
            
            All the data used here comes from IRR repositories and is parsed by <a href="https://github.com/SichangHe/internet_route_verification">RPSLyzer</a>, an open-source tool developed to breakdown policies written in RPSL into an intermediate, more processable representation.
            </div>
            """,
            unsafe_allow_html=True,
        )

# Shows results after query was made
else:
    with results_space:
        st.title(f"Results for {query}")

        # Getting the data
        r = requests.get(f"http://localhost:8000/search?query={query}")
        data = r.json()

        # Showing the data
        match data["type"]:
            case "asn":
                show_results_asn(data["results"])

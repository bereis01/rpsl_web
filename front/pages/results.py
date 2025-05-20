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
        value=st.session_state.query if "query" in st.session_state else None,
        placeholder="Prefix, IP, ASN or AS/route-set",
    )

# Query results
if not query:
    st.markdown("#####")
    st.title("No results")
    st.divider()

else:
    st.markdown("#####")
    st.title(f"Results for {query}")

    # Getting the data
    r = requests.get(f"http://localhost:8000/search/asn/{query}")
    data = r.json()

    # Showing the data
    st.header("Routing Policies", divider="gray")

    st.subheader("RPSL Object")
    with st.container(
        height=min(data["aut_nums"]["body"].count("\n") * 30, 300), border=True
    ):
        st.text(data["aut_nums"]["body"])

    st.subheader("Import Rules")
    df = pd.DataFrame.from_records(data["imports"])
    st.dataframe(df)

    st.subheader("Export Rules")
    df = pd.DataFrame.from_records(data["exports"])
    st.dataframe(df)

    st.subheader("Relationships")
    df = pd.DataFrame.from_records(data["relationships"])
    st.dataframe(df)

    st.divider()

# Footer
elements.footer()

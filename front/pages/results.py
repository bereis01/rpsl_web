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

# Footer
elements.footer()

import streamlit as st
from utils import elements

st.set_page_config(
    page_title="My App",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Header
elements.big_header()

# Description
st.write(
    "RPSL Explorer shows various data related to RPSL policies stored within the IRR."
)

# Search box
query = st.text_input(
    label="Enter a prefix, IP address, AS number or AS/route set name.",
    placeholder="Prefix, IP, ASN or AS/route-set",
)
if query:
    st.session_state.query = query
    st.switch_page("pages/results.py")

# Footer
elements.footer()

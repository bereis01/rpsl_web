import requests
import streamlit as st
from streamlit import session_state as ss


def show_results_prefix(query: str):
    # Announced by
    if "announced_by" not in ss:
        ss["announced_by"] = requests.get(
            f"http://localhost:8000/prefix/announced_by/{query.replace("/", "\\")}"
        ).json()

    st.header("Announced By", divider="gray")

    if ss["announced_by"]["result"]["announced_by"]:
        st.write("The prefix is announced by the following ASes:")
        st.dataframe({"AS Numbers": ss["announced_by"]["result"]["announced_by"]})
    else:
        st.write("*The prefix is not announced by any AS*")

    st.divider()

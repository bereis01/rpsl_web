import streamlit as st
from utils import backend
from streamlit import session_state as ss


def show_results_prefix(query: str):
    # Announced by
    if "announced_by" not in ss:
        ss["announced_by"] = backend.get(f"addr/announced_by/{query}").json()

    st.header("Announced By", divider="gray")

    if ss["announced_by"]["result"]["announced_by"]:
        st.write("The prefix is announced by the following ASes:")
        st.dataframe({"AS Numbers": ss["announced_by"]["result"]["announced_by"]})
    else:
        st.write("*The prefix is not announced by any AS*")

    st.divider()

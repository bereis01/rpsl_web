import streamlit as st
from utils import backend
from streamlit import session_state as ss


def show_results_as_set(query: str):
    # Basic info
    if "as_set" not in ss:
        ss["as_set"] = backend.get(f"as_set/as_set/{query}").json()

    st.header("Basic Info", divider="gray")
    st.write("General information contained within the AS Set 'as_set' RPSL object.")
    with st.container(
        height=min(ss["as_set"]["result"]["body"].count("\n") * 30, 300), border=True
    ):
        st.text(ss["as_set"]["result"]["body"])

    st.divider()

    # Members Info
    st.header("Members", divider="gray")

    if ss["as_set"]["result"]["members"]:
        st.write("The AS set contains the following AS members:")
        st.dataframe({"AS Members": ss["as_set"]["result"]["members"]})
    else:
        st.write("*The AS set does not contain any AS member*")

    if ss["as_set"]["result"]["set_members"]:
        st.write("The AS set contains the following set members:")
        st.dataframe({"Set Members": ss["as_set"]["result"]["set_members"]})
    else:
        st.write("*The AS set does not contain any set member*")

    st.divider()

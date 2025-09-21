import streamlit as st
from utils import backend
from streamlit import session_state as ss


def show_results_route_set(query: str):
    # Basic info
    if "route_set" not in ss:
        ss["route_set"] = backend.get(f"rs/members/{query}").json()

    st.header("Basic Info", divider="gray")
    st.write("General information contained within the route set RPSL object.")
    with st.container(
        height=min(ss["route_set"]["result"]["body"].count("\n") * 30, 300), border=True
    ):
        st.text(ss["route_set"]["result"]["body"])

    st.divider()

    # Members Info
    st.header("Members", divider="gray")

    if ss["route_set"]["result"]["members"]:
        st.write("The route set contains the following members:")
        st.dataframe({"Members": ss["route_set"]["result"]["members"]})
    else:
        st.write("*The AS set does not contain any AS member*")

    st.divider()

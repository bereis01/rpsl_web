import streamlit as st
from utils import view
from utils import backend
from streamlit import session_state as ss


def show_results_route_set(query: str):
    # Basic info
    if "attributes" not in ss:
        ss["attributes"] = backend.get(f"rs/attributes/{query}").json()

    st.header("Basic Info", divider="gray")
    view.present_attributes(ss["attributes"]["result"])
    st.divider()

    # Members Info
    if "members" not in ss:
        ss["members"] = backend.get(f"rs/members/{query}").json()

    st.header("Members", divider="gray")

    if ss["members"]["result"]["members"]:
        st.write("The route set contains the following members:")
        st.dataframe({"Members": ss["members"]["result"]["members"]})
    else:
        st.write("*The AS set does not contain any AS member*")

    st.divider()

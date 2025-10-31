import streamlit as st
from utils import view
from utils import backend
from streamlit import session_state as ss


def show_results_as_set(query: str):
    # Basic info
    if "attributes" not in ss:
        ss["attributes"] = backend.get(f"asset/attributes/{query}").json()

    st.header("Basic Info", divider="gray")
    view.present_attributes(ss["attributes"]["result"])
    st.divider()

    # Members Info
    if "members" not in ss:
        ss["members"] = backend.get(f"asset/members/{query}").json()

    st.header("Members", divider="gray")

    if ss["members"]["result"]["members"]:
        st.write("The AS set contains the following AS members:")
        st.dataframe({"AS Members": ss["members"]["result"]["members"]})
    else:
        st.write("*The AS set does not contain any AS member*")

    if ss["members"]["result"]["set_members"]:
        st.write("The AS set contains the following set members:")
        st.dataframe({"Set Members": ss["members"]["result"]["set_members"]})
    else:
        st.write("*The AS set does not contain any set member*")

    st.divider()

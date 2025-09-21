import streamlit as st
from utils import backend
from streamlit import session_state as ss
from utils.parsing import parse_attributes


def show_results_route_set(query: str):
    # Basic info
    if "attributes" not in ss:
        ss["attributes"] = backend.get(f"rs/attributes/{query}").json()
        ss["parsed_attributes"] = parse_attributes(ss["attributes"]["result"])

    st.header("Basic Info", divider="gray")
    other_info, remarks = st.columns(2)
    with other_info:
        with st.container(
            height=min(ss["parsed_attributes"][0].count("\n") * 30 + 1, 300),
            border=False,
        ):
            st.markdown(ss["parsed_attributes"][0])
    with remarks:
        with st.container(
            height=min(ss["parsed_attributes"][1].count("\n") * 40 + 1, 300),
            border=True,
        ):
            st.text(ss["parsed_attributes"][1])

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

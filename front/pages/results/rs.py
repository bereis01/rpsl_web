import streamlit as st
from utils import view
from utils import backend
from streamlit import session_state as ss

SEARCH_HELP = (
    "Search the data for keywords, each separated by a comma (e.g. False, External). "
    "The search is made based on the objects in the source data. "
    "For example, if searching for an AS of number 123, type only the number '123', and not 'AS123'. "
    "The search is case insensitive. "
)


def show_results_route_set(query: str):
    # Basic info
    if "attributes" not in ss:
        ss["attributes"] = backend.get(f"rs/attributes/{query}").json()

    st.header("Basic Info", divider="gray")
    view.present_attributes(ss["attributes"]["result"])
    st.divider()

    ## Members Info
    # Formatting
    rs_members_header, rs_members_search = st.columns(
        [0.7, 0.3], vertical_alignment="center"
    )

    # Header
    with rs_members_header:
        st.header("Members", divider="gray")
    st.write("Information about the members of the given route set.")

    # Key instantiation
    if "rs_members_search" not in ss:
        ss["rs_members_search"] = None
    if "rs_members_changed" not in ss:
        ss["rs_members_changed"] = True
    if "rs_members_skip" not in ss:
        ss["rs_members_skip"] = 0
    if "rs_members_limit" not in ss:
        ss["rs_members_limit"] = 10

    # Search bar
    with rs_members_search:
        rs_members_search = st.text_input(
            "Search",
            help=SEARCH_HELP,
            key="rs_members_text_input",
            placeholder="Type, Member, ...",
        )
        if rs_members_search != ss["rs_members_search"]:
            ss["rs_members_search"] = rs_members_search
            ss["rs_members_changed"] = True
            ss["rs_members_skip"] = 0
            ss["rs_members_limit"] = 10

    # Getting data
    with st.spinner("Getting results..."):
        if ss["rs_members_changed"]:
            ss["rs_members_page"] = backend.get(
                f"rs/members/{query}?skip={ss["rs_members_skip"]}&limit={ss["rs_members_limit"]}"
                + (f"&search={rs_members_search}" if rs_members_search else "")
            ).json()
            ss["rs_members_count"] = ss["rs_members_page"]["count"]

    # Showing results
    view.present_rs_members(ss["rs_members_page"]["result"])

    st.divider()

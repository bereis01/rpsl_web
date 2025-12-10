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


def show_results_as_set(query: str):
    # Basic info
    if "attributes" not in ss:
        ss["attributes"] = backend.get(f"asset/attributes/{query}").json()

    st.header("Basic Info", divider="gray")
    view.present_attributes(ss["attributes"]["result"])
    st.divider()

    ## Members Info
    st.header("Members", divider="gray")
    st.write("Information about the members of the given AS set.")

    # Formatting
    as_members_header, as_members_search = st.columns(
        [0.7, 0.3], vertical_alignment="center"
    )

    # Key instantiation
    if "as_members_search" not in ss:
        ss["as_members_search"] = None
    if "as_members_changed" not in ss:
        ss["as_members_changed"] = True
    if "as_members_skip" not in ss:
        ss["as_members_skip"] = 0
    if "as_members_limit" not in ss:
        ss["as_members_limit"] = 10

    # Header
    with as_members_header:
        st.subheader("AS Members")

    # Search bar
    with as_members_search:
        as_members_search = st.text_input(
            "Search",
            help=SEARCH_HELP,
            key="as_members_text_input",
            placeholder="ASN, ...",
        )
        if as_members_search != ss["as_members_search"]:
            ss["as_members_search"] = as_members_search
            ss["as_members_changed"] = True
            ss["as_members_skip"] = 0
            ss["as_members_limit"] = 10

    # Getting data
    with st.spinner("Getting results..."):
        if ss["as_members_changed"]:
            ss["as_members_page"] = backend.get(
                f"asset/as_members/{query}?skip={ss["as_members_skip"]}&limit={ss["as_members_limit"]}"
                + (f"&search={as_members_search}" if as_members_search else "")
            ).json()
            ss["as_members_count"] = ss["as_members_page"]["count"]

    # Showing results
    view.present_asset_members(ss["as_members_page"]["result"], "as_members")

    # Formatting
    set_members_header, set_members_search = st.columns(
        [0.7, 0.3], vertical_alignment="center"
    )

    # Key instantiation
    if "set_members_search" not in ss:
        ss["set_members_search"] = None
    if "set_members_changed" not in ss:
        ss["set_members_changed"] = True
    if "set_members_skip" not in ss:
        ss["set_members_skip"] = 0
    if "set_members_limit" not in ss:
        ss["set_members_limit"] = 10

    # Header
    with set_members_header:
        st.subheader("Set Members")

    # Search bar
    with set_members_search:
        set_members_search = st.text_input(
            "Search",
            help=SEARCH_HELP,
            key="set_members_text_input",
            placeholder="AS set name, ...",
        )
        if set_members_search != ss["set_members_search"]:
            ss["set_members_search"] = set_members_search
            ss["set_members_changed"] = True
            ss["set_members_skip"] = 0
            ss["set_members_limit"] = 10

    # Getting data
    with st.spinner("Getting results..."):
        if ss["set_members_changed"]:
            ss["set_members_page"] = backend.get(
                f"asset/set_members/{query}?skip={ss["set_members_skip"]}&limit={ss["set_members_limit"]}"
                + (f"&search={set_members_search}" if set_members_search else "")
            ).json()
            ss["set_members_count"] = ss["set_members_page"]["count"]

    # Showing results
    view.present_asset_members(ss["set_members_page"]["result"], "set_members")

    st.divider()

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


def show_results_prefix(query: str):
    """# Announced by
    if "announced_by" not in ss:
        ss["announced_by"] = backend.get(f"addr/announced_by/{query}").json()

    st.header("Announced By", divider="gray")

    if ss["announced_by"]["result"]["announced_by"]:
        st.write("The prefix is announced by the following ASes:")
        st.dataframe({"AS Numbers": ss["announced_by"]["result"]["announced_by"]})
    else:
        st.write("*The prefix is not announced by any AS*")

    st.divider()"""

    # Formatting
    announced_by_header, announced_by_search = st.columns(
        [0.7, 0.3], vertical_alignment="center"
    )

    # Key instantiation
    if "announced_by_search" not in ss:
        ss["announced_by_search"] = None
    if "announced_by_changed" not in ss:
        ss["announced_by_changed"] = True
    if "announced_by_skip" not in ss:
        ss["announced_by_skip"] = 0
    if "announced_by_limit" not in ss:
        ss["announced_by_limit"] = 10

    # Header
    with announced_by_header:
        st.header("AS Members", divider="gray")
    st.write("ASes for which this address prefix is registered as a route object.")

    # Search bar
    with announced_by_search:
        announced_by_search = st.text_input(
            "Search",
            help=SEARCH_HELP,
            key="announced_by_text_input",
            placeholder="ASN, ...",
        )
        if announced_by_search != ss["announced_by_search"]:
            ss["announced_by_search"] = announced_by_search
            ss["announced_by_changed"] = True
            ss["announced_by_skip"] = 0
            ss["announced_by_limit"] = 10

    # Getting data
    with st.spinner("Getting results..."):
        if ss["announced_by_changed"]:
            ss["announced_by_page"] = backend.get(
                f"addr/announced_by/{query}?skip={ss["announced_by_skip"]}&limit={ss["announced_by_limit"]}"
                + (f"&search={announced_by_search}" if announced_by_search else "")
            ).json()
            ss["announced_by_count"] = ss["announced_by_page"]["count"]

    # Showing results
    view.present_addr_announced_by(ss["announced_by_page"]["result"])

    st.divider()

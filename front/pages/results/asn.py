import pandas as pd
import streamlit as st
from utils import backend
from streamlit import session_state as ss
from utils.elements import navigation_controls
from utils.parsing import (
    parse_attributes,
    parse_relationships,
    parse_membership,
    parse_announcement,
)

SEARCH_HELP = (
    "The search is made based on the objects in the source data. "
    "For example, if searching for an AS of number 123, type only the number '123', and not 'AS123'."
)


def show_basic_info(query: str):
    # Basic info
    if "attributes" not in ss:
        ss["attributes"] = backend.get(f"asn/attributes/{query}").json()
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


def show_relationship_info(query: str):
    # Formatting
    tor_header, tor_search = st.columns([0.7, 0.3], vertical_alignment="center")

    # Key instantiation
    if "tor_search" not in ss:
        ss["tor_search"] = None
    if "tor_changed" not in ss:
        ss["tor_changed"] = True
    if "tor_skip" not in ss:
        ss["tor_skip"] = 0
    if "tor_limit" not in ss:
        ss["tor_limit"] = 10

    # Header
    with tor_header:
        st.header("Relationship Inference", divider="gray")
    st.write("Infered relationships with other ASes based on various heuristics.")

    # Search bar
    with tor_search:
        tor_search = st.text_input("Search", help=SEARCH_HELP, key="tor_text_input")
        if tor_search != ss["tor_search"]:
            ss["tor_search"] = tor_search
            ss["tor_changed"] = True
            ss["tor_skip"] = 0
            ss["tor_limit"] = 10

    # Getting data
    with st.spinner("Getting results..."):
        if ss["tor_changed"]:
            ss["relationships_page"] = backend.get(
                f"asn/relationships/{query}?skip={ss["tor_skip"]}&limit={ss["tor_limit"]}"
                + (f"&search={tor_search}" if tor_search else "")
            ).json()
            ss["tor_changed"] = False
            ss["tor_count"] = ss["relationships_page"]["count"]

    # Showing results
    st.table(parse_relationships(ss["relationships_page"]["result"]))
    navigation_controls("tor")

    # Getting source data
    with st.spinner("Getting source data..."):
        if "imports" not in ss:
            ss["imports"] = backend.get(f"asn/imports/{query}").json()
            ss["imports"] = pd.DataFrame.from_records(ss["imports"]["result"]).astype(
                str
            )

        if "exports" not in ss:
            ss["exports"] = backend.get(f"asn/exports/{query}").json()
            ss["exports"] = pd.DataFrame.from_records(ss["exports"]["result"]).astype(
                str
            )

    # Showing source data
    with st.expander("Source data"):
        st.subheader("Import Rules")
        st.dataframe(ss["imports"])

        st.subheader("Export Rules")
        st.dataframe(ss["exports"])

    st.divider()


def show_set_information(query: str):
    # Formatting
    memb_header, memb_search = st.columns([0.7, 0.3], vertical_alignment="center")

    # Key instantiation
    if "memb_search" not in ss:
        ss["memb_search"] = None
    if "memb_changed" not in ss:
        ss["memb_changed"] = True
    if "memb_skip" not in ss:
        ss["memb_skip"] = 0
    if "memb_limit" not in ss:
        ss["memb_limit"] = 5

    # Header
    with memb_header:
        st.header("AS Set Membership", divider="gray")
    st.write("Information about the AS set membership of the given AS.")

    # Search bar
    with memb_search:
        memb_search = st.text_input("Search", help=SEARCH_HELP, key="memb_text_input")
        if memb_search != ss["memb_search"]:
            ss["memb_search"] = memb_search
            ss["memb_changed"] = True
            ss["memb_skip"] = 0

    # Getting data
    with st.spinner("Getting results..."):
        if ss["memb_changed"]:
            ss["membership_page"] = backend.get(
                f"asset/membership/{query}?skip={ss["memb_skip"]}&limit={ss["memb_limit"]}"
                + (f"&search={memb_search}" if memb_search else "")
            ).json()
            ss["memb_changed"] = False
        parsed_membership = parse_membership(ss["membership_page"]["result"])
        ss["memb_count"] = ss["membership_page"]["count"]

    # Showing results
    with st.container(border=False):
        st.write(
            parsed_membership
            if parsed_membership
            else "*This AS is not member of any AS sets or the search yielded no results*"
        )
    navigation_controls("memb")

    # Getting source data
    with st.spinner("Getting source data..."):
        if "membership" not in ss:
            ss["membership"] = backend.get(f"asset/membership/{query}").json()

    # Showing source data
    with st.expander("Source data"):
        st.subheader("AS Sets")
        if ss["membership"]["result"] != None:
            df = pd.DataFrame.from_dict(
                ss["membership"]["result"], orient="index"
            ).astype(str)
            st.dataframe(df)
        else:
            st.write("*There is not an entry for this object in the database*\n")

    st.divider()


def show_addr_information(query: str):
    # Formatting
    route_header, route_search = st.columns([0.7, 0.3], vertical_alignment="center")

    # Key instantiation
    if "route_search" not in ss:
        ss["route_search"] = None
    if "route_changed" not in ss:
        ss["route_changed"] = True
    if "route_skip" not in ss:
        ss["route_skip"] = 0
    if "route_limit" not in ss:
        ss["route_limit"] = 5

    # Header
    with route_header:
        st.header("Originated Prefixes", divider="gray")
    st.write("Information about the address prefixes originated by the given AS.")

    # Search bar
    with route_search:
        route_search = st.text_input("Search", help=SEARCH_HELP, key="route_text_input")
        if route_search != ss["route_search"]:
            ss["route_search"] = route_search
            ss["route_changed"] = True
            ss["route_skip"] = 0

    # Getting data
    with st.spinner("Getting results..."):
        if ss["route_changed"]:
            ss["announcement_page"] = backend.get(
                f"addr/announcement/{query}?skip={ss["route_skip"]}&limit={ss["route_limit"]}"
                + (f"&search={route_search}" if route_search else "")
            ).json()
            ss["route_changed"] = False
        parsed_announcement = parse_announcement(ss["announcement_page"]["result"])
        ss["route_count"] = ss["announcement_page"]["count"]

    # Showing results
    with st.container(border=False):
        st.write(
            parsed_announcement
            if parsed_announcement
            else "*This AS does not announce any routes/prefixes or the search yielded no results*"
        )
    navigation_controls("route")

    # Getting source data
    with st.spinner("Getting source data..."):
        if "announcement" not in ss:
            ss["announcement"] = backend.get(f"addr/announcement/{query}").json()

    # Showing source data
    with st.expander("Source data"):
        st.subheader("AS Routes")
        if ss["announcement"]["result"] != None:
            df = pd.DataFrame.from_dict(
                ss["announcement"]["result"], orient="index"
            ).astype(str)
            st.dataframe(df)
        else:
            st.write("*There is not an entry for this object in the database*\n")

    st.divider()


def show_results_asn(query: str):
    show_basic_info(query)
    show_relationship_info(query)
    show_set_information(query)
    show_addr_information(query)

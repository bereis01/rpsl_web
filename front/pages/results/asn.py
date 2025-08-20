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


def show_results_asn(query: str):
    # Basic info
    if "attributes" not in ss:
        ss["attributes"] = backend.get(f"asn/attributes/{query}").json()
        ss["parsed_attributes"] = parse_attributes(ss["attributes"]["result"])

    st.header("Basic Info", divider="gray")
    other_info, remarks = st.columns(2)
    with other_info:
        with st.container(
            height=min(ss["parsed_attributes"][0].count("\n") * 30, 300),
            border=False,
        ):
            st.markdown(ss["parsed_attributes"][0])
    with remarks:
        with st.container(
            height=min(ss["parsed_attributes"][1].count("\n") * 30, 300),
            border=True,
        ):
            st.text(ss["parsed_attributes"][1])

    ## Getting source data
    with st.spinner("Getting source data..."):
        if "aut_num" not in ss:
            ss["aut_num"] = backend.get(f"asn/aut_num/{query}").json()

    ## Showing source data
    with st.expander("Source data"):
        with st.container(
            height=min(ss["aut_num"]["result"]["body"].count("\n") * 30, 300),
            border=True,
        ):
            st.text(ss["aut_num"]["result"]["body"])

    st.divider()

    # Relationships inference
    st.header("Relationship Inference", divider="gray")
    st.write(
        "Infered relationships with other ASes based on the import and export rules of the given AS."
    )

    # Simple Relationships
    ## Getting the data
    with st.spinner("Getting results..."):
        if "summary" not in ss:
            ss["summary"] = backend.get(f"asn/summary/{query}").json()["result"]

    ## Showing the data
    st.subheader(
        "Simple Relationships",
        help="These relationships are of the form: the customer exports all the routes defined by itself (its AS number) to the provider, who exports all of its routes to the customer.",
    )
    st.write("This AS is possibly a customer/provider of the following ASes:")
    df = pd.DataFrame.from_dict(
        {
            "Customer": [ss["summary"]["simple_customer"]],
            "Provider": [ss["summary"]["simple_provider"]],
        },
        orient="index",
        columns=["AS Number"],
    )
    st.dataframe(df)

    # Detailed relationships
    ## Formatting
    tor_header, tor_search = st.columns([0.7, 0.3], vertical_alignment="center")

    ## Key instantiation
    if "tor_search" not in ss:
        ss["tor_search"] = None
    if "tor_changed" not in ss:
        ss["tor_changed"] = True
    if "tor_skip" not in ss:
        ss["tor_skip"] = 0
    if "tor_limit" not in ss:
        ss["tor_limit"] = 10

    ## Header
    with tor_header:
        st.subheader(
            "Detailed Relationships",
            help="- **Asymmetric/Symmetric:** A symmetric relationship could be infered from both ends, while an assymetric relationship could only be infered from the information pertaining to one of the ASes;",
        )
    st.write(
        "This AS possibly establishes the following relationships with other ASes:"
    )

    ## Search bar
    with tor_search:
        tor_search = st.text_input("Search", help=SEARCH_HELP, key="tor_text_input")
        if tor_search != ss["tor_search"]:
            ss["tor_search"] = tor_search
            ss["tor_changed"] = True
            ss["tor_skip"] = 0
            ss["tor_limit"] = 10

    ## Getting data
    with st.spinner("Getting results..."):
        if ss["tor_changed"]:
            ss["relationships_page"] = backend.get(
                f"asn/tor/{query}?skip={ss["tor_skip"]}&limit={ss["tor_limit"]}"
                + (f"&search={tor_search}" if tor_search else "")
            ).json()
            ss["tor_changed"] = False
        parsed_relationships = parse_relationships(ss["relationships_page"]["result"])
        ss["tor_count"] = ss["relationships_page"]["count"]

    ## Showing results
    with st.container(
        height=min(int(len(parsed_relationships) * 0.25), 400), border=False
    ):
        st.write(
            parsed_relationships
            if parsed_relationships
            else "*No relationships could be infered or the search yielded no results*"
        )
    navigation_controls("tor")

    ## Getting source data
    with st.spinner("Getting source data..."):
        if "relationships" not in ss:
            ss["relationships"] = backend.get(f"asn/tor/{query}").json()

        if "imports" not in ss:
            ss["imports"] = backend.get(f"asn/imports/{query}").json()

        if "exports" not in ss:
            ss["exports"] = backend.get(f"asn/exports/{query}").json()

    ## Showing source data
    with st.expander("Source data"):
        st.subheader("Relationships")
        df = pd.DataFrame.from_records(ss["relationships"]["result"]).astype(str)
        st.dataframe(df)

        st.subheader("Import Rules")
        df = pd.DataFrame.from_records(ss["imports"]["result"]).astype(str)
        st.dataframe(df)

        st.subheader("Export Rules")
        df = pd.DataFrame.from_records(ss["exports"]["result"]).astype(str)
        st.dataframe(df)

    st.divider()

    # Set membership
    ## Formatting
    memb_header, memb_search = st.columns([0.7, 0.3], vertical_alignment="center")

    # Key instantiation
    if "memb_search" not in ss:
        ss["memb_search"] = None
    if "memb_changed" not in ss:
        ss["memb_changed"] = True
    if "memb_skip" not in ss:
        ss["memb_skip"] = 0
    if "memb_limit" not in ss:
        ss["memb_limit"] = 10

    ## Header
    with memb_header:
        st.header("AS Set Membership", divider="gray")
    st.write("Information about the AS set membership of the given AS.")

    ## Search bar
    with memb_search:
        memb_search = st.text_input("Search", help=SEARCH_HELP, key="memb_text_input")
        if memb_search != ss["memb_search"]:
            ss["memb_search"] = memb_search
            ss["memb_changed"] = True
            ss["memb_skip"] = 0
            ss["memb_limit"] = 10

    ## Getting data
    with st.spinner("Getting results..."):
        if ss["memb_changed"]:
            ss["membership_page"] = backend.get(
                f"asn/membership/{query}?skip={ss["memb_skip"]}&limit={ss["memb_limit"]}"
                + (f"&search={memb_search}" if memb_search else "")
            ).json()
            ss["memb_changed"] = False
        parsed_membership = parse_membership(ss["membership_page"]["result"])
        ss["memb_count"] = ss["membership_page"]["count"]

    ## Showing results
    with st.container(
        height=min(int(len(parsed_membership) * 0.75), 400), border=False
    ):
        st.write(
            parsed_membership
            if parsed_membership
            else "*This AS is not member of any AS sets or the search yielded no results*"
        )
    navigation_controls("memb")

    ## Getting source data
    with st.spinner("Getting source data..."):
        if "membership" not in ss:
            ss["membership"] = backend.get(f"asn/membership/{query}").json()

    ## Showing source data
    with st.expander("Source data"):
        st.subheader("AS Sets")
        df = pd.DataFrame.from_dict(ss["membership"]["result"], orient="index").astype(
            str
        )
        st.dataframe(df)

    st.divider()

    # Announced routes
    ## Formatting
    route_header, route_search = st.columns([0.7, 0.3], vertical_alignment="center")

    # Key instantiation
    if "route_search" not in ss:
        ss["route_search"] = None
    if "route_changed" not in ss:
        ss["route_changed"] = True
    if "route_skip" not in ss:
        ss["route_skip"] = 0
    if "route_limit" not in ss:
        ss["route_limit"] = 10

    ## Header
    with route_header:
        st.header("Originated Prefixes", divider="gray")
    st.write("Information about the address prefixes originated by the given AS.")

    ## Search bar
    with route_search:
        route_search = st.text_input("Search", help=SEARCH_HELP, key="route_text_input")
        if route_search != ss["route_search"]:
            ss["route_search"] = route_search
            ss["route_changed"] = True
            ss["route_skip"] = 0
            ss["route_limit"] = 10

    ## Getting data
    with st.spinner("Getting results..."):
        if ss["route_changed"]:
            ss["announcement_page"] = backend.get(
                f"asn/announcement/{query}?skip={ss["route_skip"]}&limit={ss["route_limit"]}"
                + (f"&search={route_search}" if route_search else "")
            ).json()
            ss["route_changed"] = False
        parsed_announcement = parse_announcement(ss["announcement_page"]["result"])
        ss["route_count"] = ss["announcement_page"]["count"]

    ## Showing results
    with st.container(
        height=min(int(len(parsed_announcement) * 1.25), 400), border=False
    ):
        st.write(
            parsed_announcement
            if parsed_announcement
            else "*This AS does not announce any routes/prefixes or the search yielded no results*"
        )
    navigation_controls("route")

    ## Getting source data
    with st.spinner("Getting source data..."):
        if "announcement" not in ss:
            ss["announcement"] = backend.get(f"asn/announcement/{query}").json()

    ## Showing source data
    with st.expander("Source data"):
        st.subheader("AS Routes")
        df = pd.DataFrame.from_dict(
            ss["announcement"]["result"], orient="index"
        ).astype(str)
        st.dataframe(df)

    st.divider()

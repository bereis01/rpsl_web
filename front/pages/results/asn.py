import requests
import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from utils.parsing import parse_relationships, parse_membership, parse_announcement
from utils.elements import navigation_controls


def show_results_asn(query: str):
    # Basic info
    if "aut_num" not in ss:
        ss["aut_num"] = requests.get(
            f"http://localhost:8000/asn/aut_num/{query}"
        ).json()

    st.header("Basic Info", divider="gray")
    st.write("General information contained within the AS 'aut_num' RPSL object.")
    with st.container(
        height=min(ss["aut_num"]["result"]["body"].count("\n") * 30, 300), border=True
    ):
        st.text(ss["aut_num"]["result"]["body"])

    st.divider()

    # Relationships inference
    tor_header, tor_search = st.columns([0.7, 0.3], vertical_alignment="center")

    if "tor_search" not in ss:
        ss["tor_search"] = None

    with tor_search:
        tor_search = st.text_input("Search")
        if tor_search != ss["tor_search"]:
            ss["tor_search"] = tor_search
            ss["tor_changed"] = True

    if "tor_changed" not in ss:
        ss["tor_changed"] = True
    if "tor_skip" not in ss:
        ss["tor_skip"] = 0
    if "tor_limit" not in ss:
        ss["tor_limit"] = 10

    with st.spinner():
        if ss["tor_changed"]:
            ss["relationships_page"] = requests.get(
                f"http://localhost:8000/asn/tor/{query}?skip={ss["tor_skip"]}&limit={ss["tor_limit"]}"
                + (f"&search={tor_search}" if tor_search else "")
            ).json()
            ss["tor_changed"] = False
        parsed_relationships = parse_relationships(ss["relationships_page"]["result"])

    ss["tor_count"] = ss["relationships_page"]["count"]

    with tor_header:
        st.header("Relationships Inference", divider="gray")
    st.write(
        "Infered relationships with other ASes based on the import and export rules of the given AS."
    )

    with st.container(
        height=min(parsed_relationships.count("\n") * 30, 400), border=False
    ):
        st.write(
            parsed_relationships
            if parsed_relationships
            else "*No relationships could be infered*"
        )
    navigation_controls("tor")

    # Source for relationships inference
    with st.expander("Source data"):
        if "relationships" not in ss:
            ss["relationships"] = requests.get(
                f"http://localhost:8000/asn/tor/{query}"
            ).json()
        st.subheader("Relationships")
        df = pd.DataFrame.from_records(ss["relationships"]["result"])
        st.dataframe(df)

        if "imports" not in ss:
            ss["imports"] = requests.get(
                f"http://localhost:8000/asn/imports/{query}"
            ).json()
        st.subheader("Import Rules")
        df = pd.DataFrame.from_records(ss["imports"]["result"])
        st.dataframe(df)

        if "exports" not in ss:
            ss["exports"] = requests.get(
                f"http://localhost:8000/asn/exports/{query}"
            ).json()
        st.subheader("Export Rules")
        df = pd.DataFrame.from_records(ss["exports"]["result"])
        st.dataframe(df)

    st.divider()

    # AS set membership
    member_header, member_search = st.columns([0.7, 0.3], vertical_alignment="center")
    with member_header:
        st.header("AS Set Membership", divider="gray")
    with member_search:
        member_search = st.text_input("Search", key="member_search")

    with st.spinner():
        if "membership" not in ss:
            ss["membership"] = requests.get(
                f"http://localhost:8000/asn/membership/{query}"
            ).json()
        parsed_membership = parse_membership(ss["membership"]["result"], member_search)

    if parsed_membership != "":
        st.write("This AS is member of the following AS sets:")
        with st.container(
            height=min(parsed_membership.count("\n") * 30, 400), border=False
        ):
            st.write(parsed_membership)
    else:
        st.write(
            "*This AS is not member of any AS sets or the search yielded no results*"
        )

    # Source for set membership
    with st.expander("Source data"):
        st.subheader("AS Sets")
        df = pd.DataFrame.from_dict(ss["membership"]["result"], orient="index")
        st.dataframe(df)

    st.divider()

    # Exported routes
    route_header, route_search = st.columns([0.7, 0.3], vertical_alignment="center")
    with route_header:
        st.header("Announced Routes", divider="gray")
    with route_search:
        route_search = st.text_input("Search", key="route_search")

    with st.spinner():
        if "announcement" not in ss:
            ss["announcement"] = requests.get(
                f"http://localhost:8000/asn/routes/{query}"
            ).json()
        parsed_announcement = parse_announcement(
            ss["announcement"]["result"], route_search
        )

    if parsed_announcement != "":
        st.write("This AS announces the following routes:")
        with st.container(
            height=min(parsed_announcement.count("\n") * 30, 400), border=False
        ):
            st.write(parsed_announcement)
    else:
        st.write(
            "*This AS does not announce any route or the search yielded no results*"
        )

    # Source for route announcement
    with st.expander("Source data"):
        st.subheader("AS Routes")
        df = pd.DataFrame.from_dict(ss["announcement"]["result"], orient="index")
        st.dataframe(df)

    st.divider()

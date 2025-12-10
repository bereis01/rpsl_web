import pandas as pd
from utils import view
import streamlit as st
from utils import backend
from streamlit import session_state as ss
from utils.elements import navigation_controls

SEARCH_HELP = (
    "Search the data for keywords, each separated by a comma (e.g. False, External). "
    "The search is made based on the objects in the source data. "
    "For example, if searching for an AS of number 123, type only the number '123', and not 'AS123'. "
    "The search is case insensitive. "
)


def show_basic_info(query: str):
    # Basic info
    if "attributes" not in ss:
        ss["attributes"] = backend.get(f"asn/attributes/{query}").json()

    st.header("Basic Info", divider="gray")
    view.present_attributes(ss["attributes"]["result"])
    st.divider()


def show_policies_info(query: str):
    st.header("Routing Policies", divider="gray")
    st.write("Information about the routing policies defined by the given AS.")

    # Formatting
    imports_header, imports_search = st.columns([0.7, 0.3], vertical_alignment="center")

    # Key instantiation
    if "imports_search" not in ss:
        ss["imports_search"] = None
    if "imports_changed" not in ss:
        ss["imports_changed"] = True
    if "imports_skip" not in ss:
        ss["imports_skip"] = 0
    if "imports_limit" not in ss:
        ss["imports_limit"] = 10

    # Header
    with imports_header:
        st.subheader("Import Rules")

    # Search bar
    with imports_search:
        imports_search = st.text_input(
            "Search",
            help=SEARCH_HELP,
            key="imports_text_input",
            placeholder="ipv4, unicast, ...",
        )
        if imports_search != ss["imports_search"]:
            ss["imports_search"] = imports_search
            ss["imports_changed"] = True
            ss["imports_skip"] = 0
            ss["imports_limit"] = 10

    # Getting data
    with st.spinner("Getting results..."):
        if ss["imports_changed"]:
            ss["imports_page"] = backend.get(
                f"asn/imports/{query}?skip={ss["imports_skip"]}&limit={ss["imports_limit"]}"
                + (f"&search={imports_search}" if imports_search else "")
            ).json()
            ss["imports_count"] = ss["imports_page"]["count"]

    # Showing results
    view.present_asn_rules(ss["imports_page"]["result"], "imports")

    # Resets parsing
    if ss["imports_changed"]:
        ss["imports_changed"] = False

    # Formatting
    exports_header, exports_search = st.columns([0.7, 0.3], vertical_alignment="center")

    # Key instantiation
    if "exports_search" not in ss:
        ss["exports_search"] = None
    if "exports_changed" not in ss:
        ss["exports_changed"] = True
    if "exports_skip" not in ss:
        ss["exports_skip"] = 0
    if "exports_limit" not in ss:
        ss["exports_limit"] = 10

    # Header
    with exports_header:
        st.subheader("Export Rules")

    # Search bar
    with exports_search:
        exports_search = st.text_input(
            "Search",
            help=SEARCH_HELP,
            key="exports_text_input",
            placeholder="ipv4, unicast, ...",
        )
        if exports_search != ss["exports_search"]:
            ss["exports_search"] = exports_search
            ss["exports_changed"] = True
            ss["exports_skip"] = 0
            ss["exports_limit"] = 10

    # Getting data
    with st.spinner("Getting results..."):
        if ss["exports_changed"]:
            ss["exports_page"] = backend.get(
                f"asn/exports/{query}?skip={ss["exports_skip"]}&limit={ss["exports_limit"]}"
                + (f"&search={exports_search}" if exports_search else "")
            ).json()
            ss["exports_count"] = ss["exports_page"]["count"]

    # Showing results
    view.present_asn_rules(ss["exports_page"]["result"], "exports")

    # Resets parsing
    if ss["exports_changed"]:
        ss["exports_changed"] = False

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
        tor_search = st.text_input(
            "Search",
            help=SEARCH_HELP,
            key="tor_text_input",
            placeholder="4552, Internal, ...",
        )
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
            ss["tor_count"] = ss["relationships_page"]["count"]

    # Showing results
    view.present_asn_relationships(ss["relationships_page"]["result"])

    # Resets parsing
    if ss["tor_changed"]:
        ss["tor_changed"] = False

    # Gettings exchanged objects
    with st.spinner("Getting results..."):
        if "exchanged_objects" not in ss:
            ss["exchanged_objects"] = backend.get(
                f"asn/exchanged_objects/{query}"
            ).json()["result"]

    # Showing exchanged objects
    with st.expander("Exchanged objects"):
        st.subheader("Imported Objects")
        df = pd.DataFrame.from_dict(
            ss["exchanged_objects"]["imports"],
            orient="index",
            columns=["N° of times imported"],
        )
        st.table(df, border="horizontal")
        st.subheader("Exported Objects")
        df = pd.DataFrame.from_dict(
            ss["exchanged_objects"]["exports"],
            orient="index",
            columns=["N° of times exported"],
        )
        st.table(df, border="horizontal")

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
        ss["memb_limit"] = 10

    # Header
    with memb_header:
        st.header("AS Set Membership", divider="gray")
    st.write("Information about the AS set membership of the given AS.")

    # Search bar
    with memb_search:
        memb_search = st.text_input(
            "Search",
            help=SEARCH_HELP,
            key="memb_text_input",
            placeholder="as-example-test, False, ...",
        )
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
            ss["memb_count"] = ss["membership_page"]["count"]

    # Showing results
    view.present_asn_set_membership(ss["membership_page"]["result"])

    # Resets parsing
    if ss["memb_changed"]:
        ss["memb_changed"] = False

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
        ss["route_limit"] = 10

    # Header
    with route_header:
        st.header("Route Objects", divider="gray")
    st.write("Information about the address prefixes registered for the given AS.")

    # Search bar
    with route_search:
        route_search = st.text_input(
            "Search",
            help=SEARCH_HELP,
            key="route_text_input",
            placeholder="0.0.0.0/0, Detected, ...",
        )
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
            ss["route_count"] = ss["announcement_page"]["count"]

    # Showing results
    view.present_addr_announcement(ss["announcement_page"]["result"])

    # Resets parsing
    if ss["route_changed"]:
        ss["route_changed"] = False

    st.divider()


def show_results_asn(query: str):
    show_basic_info(query)
    show_policies_info(query)
    show_relationship_info(query)
    show_set_information(query)
    show_addr_information(query)

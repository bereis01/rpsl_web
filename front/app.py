import streamlit as st
from utils import backend
from utils.state import clear_cache
from utils.regex import process_query
from streamlit import session_state as ss
from pages.results.asn import show_results_asn
from pages.results.as_set import show_results_as_set
from pages.results.prefix import show_results_prefix

st.set_page_config(
    page_title="rpslweb",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Header
_, logo_space, _, _ = st.columns([0.2, 0.15, 0.45, 0.2], vertical_alignment="bottom")
_, search_space, _ = st.columns([0.2, 0.6, 0.2], vertical_alignment="top")

# Displays the logo
logo_space.image("assets/logo.png")

# Search box
if "query" not in ss:
    ss["query"] = None

with search_space:
    query = st.text_input(
        label="Enter an AS number, AS set name or route/prefix.",
        placeholder="ASN, AS Set, Route/Prefix",
    )

# Body
_, results_space, _ = st.columns([0.2, 0.6, 0.2], vertical_alignment="center")
_, results_space_condensed, _ = st.columns([0.3, 0.4, 0.3], vertical_alignment="center")

# Shows temporary text before any query is made
if not query:
    with results_space_condensed:
        st.markdown(
            """
            <div style="text-align: center">
            <strong>rpslweb</strong> makes available useful information regarding data contained within the IRR.

            You can query for AS numbers, AS set names, route sets and other keywords and receive digested analysis and information, as well as the source data used to generate it.
            
            All the data used here comes from IRR repositories and is parsed by <a href="https://github.com/SichangHe/internet_route_verification">RPSLyzer</a>, an open-source tool developed to breakdown policies written in RPSL into an intermediate, more processable representation.
            </div>
            """,
            unsafe_allow_html=True,
        )

# Shows results after query was made
else:
    # Clears cache if query has changed
    if query != ss["query"]:
        ss["query"] = query
        clear_cache(["query"])

    # Matches the results function to the query type
    with results_space:
        query_type, processed_query = process_query(query)
        match query_type:
            case "asn":
                r = backend.get(
                    f"asn/{processed_query}"
                )  # Checks if asn is in database
                if r.json()["result"]:
                    st.title(f"Results for AS{processed_query}")
                    show_results_asn(processed_query)
                else:
                    st.title(f"No results for AS{query}")
            case "asset":
                r = backend.get(
                    f"as_set/{processed_query}"
                )  # Checks if as_set is in database
                if r.json()["result"]:
                    st.title(f"Results for {processed_query}")
                    show_results_as_set(processed_query)
                else:
                    st.title(f"No results for {query}")
            case "prefix":
                r = backend.get(
                    f"prefix/{processed_query}"
                )  # Checks if prefix is in database
                if r.json()["result"]:
                    st.title(f"Results for {processed_query}")
                    show_results_prefix(processed_query)
                else:
                    st.title(f"No results for {query}")
            case "invalid":
                st.title(f"No results for {query}")

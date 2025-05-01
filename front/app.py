import json
import requests
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="My App", layout="wide")

logo_space, search_space, _ = st.columns([0.2, 0.6, 0.2])

with logo_space:
    st.title(":green[RPSL Web] ✨")

with search_space:
    as_num = st.text_input("AS Num")

st.markdown("#####")

if as_num:
    r = requests.get(f"http://127.0.0.1:8000/aut_num/{as_num}").json()

    for asn in r["data"]:

        st.title("AS " + str(asn["as_num"]))

        st.header("RPSL Specification", divider="gray")
        with st.container(height=400):
            st.text(asn["body"])

        st.divider()

        st.header("Imports", divider="gray")
        df = pd.DataFrame(
            {
                "Type": [
                    "`ipv4` `unicast`"
                    for _ in range(len(asn["imports"]["ipv4"]["unicast"]))
                ],
                "Filter": [
                    rule["mp_filter"] for rule in asn["imports"]["ipv4"]["unicast"]
                ],
                "Peers": [
                    str(rule["mp_peerings"])
                    for rule in asn["imports"]["ipv4"]["unicast"]
                ],
            }
        )
        with st.container(height=400, border=False):
            st.table(df)

        st.divider()

        st.header("Exports", divider="gray")
        df = pd.DataFrame(
            {
                "Type": [
                    "ipv4, unicast"
                    for _ in range(len(asn["exports"]["ipv4"]["unicast"]))
                ],
                "Filter": [
                    rule["mp_filter"] for rule in asn["exports"]["ipv4"]["unicast"]
                ],
                "Peers": [
                    str(rule["mp_peerings"])
                    for rule in asn["exports"]["ipv4"]["unicast"]
                ],
            }
        )
        st.dataframe(df)

        st.divider()

    st.header("Raw Results")
    data = pd.DataFrame.from_dict(r["data"])
    st.dataframe(data)

    st.divider()

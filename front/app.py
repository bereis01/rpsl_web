import json
import requests
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="My App", layout="wide")

as_num = st.text_input("AS Num")
if as_num:
    r = requests.get(f"http://127.0.0.1:8000/aut_num/{as_num}").json()

    for asn in r["data"]:

        st.title("AS " + str(asn["as_num"]))

        with st.container(height=400):
            st.text(asn["body"])

        st.subheader("Imports")
        df = pd.DataFrame(
            {
                "Type": [
                    "ipv4, unicast"
                    for _ in range(len(asn["imports"]["ipv4"]["unicast"]))
                ]
                + [
                    "ipv6, unicast"
                    for _ in range(len(asn["imports"]["ipv6"]["unicast"]))
                ],
                "Rule": asn["imports"]["ipv4"]["unicast"]
                + asn["imports"]["ipv6"]["unicast"],
            }
        )
        st.dataframe(df)

        st.subheader("Exports")
        df = pd.DataFrame(
            {
                "Type": [
                    "ipv4, unicast"
                    for _ in range(len(asn["exports"]["ipv4"]["unicast"]))
                ]
                + [
                    "ipv6, unicast"
                    for _ in range(len(asn["exports"]["ipv6"]["unicast"]))
                ],
                "Rule": asn["exports"]["ipv4"]["unicast"]
                + asn["exports"]["ipv6"]["unicast"],
            }
        )
        st.dataframe(df)

    st.divider()
    st.title("Raw Results")
    data = pd.DataFrame.from_dict(r["data"])
    st.dataframe(data)

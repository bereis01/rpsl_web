import pandas as pd
import streamlit as st
from utils.parsing import parse_relationships


def show_results_asn(data):
    raw = data["raw"]
    analysis = data["analysis"]
    sources = data["sources"]

    st.header("Routing Policies", divider="gray")

    st.subheader("RPSL Object")
    with st.container(
        height=min(raw["aut_nums"]["body"].count("\n") * 30, 300), border=True
    ):
        st.text(raw["aut_nums"]["body"])

    st.subheader("Relationships Inference")
    df = pd.DataFrame.from_records(analysis["relationships"])
    with st.spinner():
        parsed_relationships = parse_relationships(df)
    with st.container(
        height=min(parsed_relationships.count("\n") * 30, 300), border=False
    ):
        st.write(parsed_relationships)

    with st.expander("Source data"):
        st.subheader("Relationships")
        df = pd.DataFrame.from_records(analysis["relationships"])
        st.dataframe(df)

        st.subheader("Import Rules")
        df = pd.DataFrame.from_records(sources["relationships"]["imports"])
        st.dataframe(df)

        st.subheader("Export Rules")
        df = pd.DataFrame.from_records(sources["relationships"]["exports"])
        st.dataframe(df)

    st.divider()

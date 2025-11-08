import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from utils.elements import navigation_controls
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode


def present_attributes(attributes):
    # Treats the case in which there are no results
    if attributes == None:
        st.markdown("*No basic information was found for the given query*")

    # Parses the object
    attributes_str = ""
    if "as-name" in attributes.keys():
        attributes_str += "**Name:** " + attributes["as-name"] + "\n\n"
    if "descr" in attributes.keys():
        attributes_str += "**Description:** " + attributes["descr"] + "\n\n"
    if "source" in attributes.keys():
        attributes_str += "**Registered in:** " + attributes["source"] + "\n\n"
    if "tech-c" in attributes.keys():
        attributes_str += "**Technical contact:** " + attributes["tech-c"] + "\n\n"
    if "admin-c" in attributes.keys():
        attributes_str += (
            "**Administrative contact:** " + attributes["admin-c"] + "\n\n"
        )
    if "mnt-by" in attributes.keys():
        attributes_str += "**Maintained by:** " + attributes["mnt-by"] + "\n\n"
    if "changed" in attributes.keys():
        attributes_str += "**Last changed by:** " + attributes["changed"] + "\n\n"
    if "upd-to" in attributes.keys():
        attributes_str += (
            "**Unauthorized modification attempts are notified to:** "
            + attributes["upd-to"]
            + "\n\n"
        )
    if "mnt-nfy" in attributes.keys():
        attributes_str += (
            "**Modifications are notified to:** " + attributes["mnt-nfy"] + "\n\n"
        )
    if "notify" in attributes.keys():
        attributes_str += (
            "**Changes should be notified to:** " + attributes["notify"] + "\n\n"
        )
    remarks_str = "No remarks to be shown\n"
    if "remarks" in attributes.keys():
        remarks_str = attributes["remarks"]

    # Presents the parsed information
    other_info, remarks = st.columns(2)
    with other_info:
        with st.container(height=300, border=False):
            st.markdown(attributes_str)
    with remarks:
        with st.container(height=300, border=True):
            st.text(remarks_str)


def present_asn_relationships(relationships):
    # Treats the case in which there are no results
    if relationships == None:
        st.markdown("*No relationships were found for the given query*")

    # Parses the dictionary
    parsed_relationships = {}
    for key in relationships.keys():
        link = relationships[key].copy()
        link["bidirectional"] = (
            "🟢 True" if link["bidirectional"] == True else "🔴 False"
        )
        link["agreement"] = "🟢 True" if link["agreement"] == True else "🔴 False"
        link["reliability"] = float(link["reliability"])
        if link["reliability"] >= 0.66:
            link["reliability"] = "🟢 " + str(link["reliability"])[:4]
        elif link["reliability"] < 0.33:
            link["reliability"] = "🔴 " + str(link["reliability"])[:4]
        else:
            link["reliability"] = "🟡 " + str(link["reliability"])[:4]
        link["representative"] = (
            "🟢 True" if link["representative"] == True else "🔴 False"
        )
        link["source"] = (
            "🔵 Internal" if link["source"] == "internal" else "🟠 External"
        )
        parsed_relationships[key] = link
    df = pd.DataFrame.from_dict(parsed_relationships, orient="index")
    df = df.reset_index()
    df = df.rename(
        columns={
            "index": "ASN",
            "tor": "Relationship",
            "bidirectional": "Bidirectionality",
            "agreement": "Agreement",
            "reliability": "Reliability",
            "representative": "Representative",
            "source": "Source",
        }
    )

    # Presents the results
    builder = GridOptionsBuilder.from_dataframe(df)
    grid_options = builder.build()

    grid_options["autoSizeStrategy"]["type"] = "fitGridWidth"
    grid_options["defaultColDef"]["resizable"] = False
    grid_options["defaultColDef"]["suppressMovable"] = True

    grid_return = AgGrid(
        df,
        key=f"{ss["query"]}_relationships_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        theme="streamlit",
        height=325,
        allow_unsafe_jscode=True,
    )

    # Controls redirecting the search
    if (grid_return.event_data != None) and (
        grid_return.event_data["column"]["colId"] == "ASN"
    ):
        ss["query"] = grid_return.event_data["value"]
        st.rerun()

    navigation_controls("tor")


def present_asn_set_membership(membership):
    # Treats the case in which there are no results
    if membership == None:
        st.markdown("*No set membership information was found for the given query*")

    # Parses the object
    full_membership_str = ""
    for as_set, value in membership.items():
        members = value["members"]
        set_members = value["set_members"]
        membership_str = f":orange-background[**{as_set}**]\n"
        if members:
            membership_str += f"- **Members:** AS{members[0]}"
            for member in members[1:5]:
                membership_str += f", AS{member}"
            if len(members) > 5:
                membership_str += ", ..."
        membership_str += "\n"
        if set_members:
            membership_str += f"- **Set members:** {set_members[0]}"
            for set_member in set_members[1:5]:
                membership_str += f", {set_member}"
            if len(set_members) > 5:
                membership_str += ", ..."
        membership_str += "\n\n"
        full_membership_str += membership_str

    # Presents
    with st.container(border=False):
        st.write(full_membership_str)
    navigation_controls("memb")


def present_addr_announcement(announcement):
    # Treats the case in which there are no results
    if announcement == None:
        st.markdown("*No announcement information was found for the given query*")

    # Parsing
    full_announcement_str = ""
    for route, value in announcement.items():
        announced_by = value["announced_by"]
        announcement_str = f":violet-background[**{route}**]\n"
        if announced_by:
            announcement_str += f"- **Announced by:** AS{announced_by[0]}"
            for asn in announced_by[1:5]:
                announcement_str += f", AS{asn}"
            if len(announced_by) > 5:
                announcement_str += ", ..."
        announcement_str += "\n\n"
        full_announcement_str += announcement_str

    # Presenting
    with st.container(border=False):
        st.write(full_announcement_str)
    navigation_controls("route")

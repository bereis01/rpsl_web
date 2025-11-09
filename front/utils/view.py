import pandas as pd
import streamlit as st
from streamlit import session_state as ss
from utils.elements import navigation_controls
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode


def present_attributes(attributes):
    # Treats the case in which there are no results
    if (attributes == None) or (len(attributes) == 0):
        st.markdown("*No basic information was found for the given query*")
        return

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


def present_asn_rules(rules, type: str):
    # Treats the case in which there are no results
    if (rules == None) or (len(rules) == 0):
        st.markdown("*No rules were found for the given query*")
        return

    # Parses the object
    parsed_rules = []
    for rule in rules:
        parsed_rules.append(rule.copy())
        if "value" in parsed_rules[-1]["peering"]["remote_as"].keys():
            parsed_rules[-1]["peering"] = parsed_rules[-1]["peering"]["remote_as"][
                "value"
            ]
        else:
            parsed_rules[-1]["peering"] = "Other"
        if "value" in parsed_rules[-1]["filter"].keys():
            parsed_rules[-1]["filter"] = parsed_rules[-1]["filter"]["value"]
        else:
            parsed_rules[-1]["filter"] = "Other"

        if parsed_rules[-1]["version"] == "ipv4":
            parsed_rules[-1]["version"] = "🟣 ipv4"
        elif parsed_rules[-1]["version"] == "ipv6":
            parsed_rules[-1]["version"] = "🟠 ipv6"
        elif parsed_rules[-1]["version"] == "any":
            parsed_rules[-1]["version"] = "⚪ any"

        if parsed_rules[-1]["cast"] == "unicast":
            parsed_rules[-1]["cast"] = "🔵 unicast"
        elif parsed_rules[-1]["cast"] == "multicast":
            parsed_rules[-1]["cast"] = "🟡 multicast"
        elif parsed_rules[-1]["cast"] == "any":
            parsed_rules[-1]["cast"] = "⚪ any"

    df = pd.DataFrame(parsed_rules).astype(str)

    # Presents the results
    builder = GridOptionsBuilder.from_dataframe(df)
    grid_options = builder.build()

    grid_options["autoSizeStrategy"]["type"] = "fitGridWidth"
    grid_options["defaultColDef"]["resizable"] = False
    grid_options["defaultColDef"]["sortable"] = False
    grid_options["defaultColDef"]["suppressMovable"] = True
    grid_options["defaultColDef"]["suppressHeaderFilterButton"] = True
    grid_options["tooltipShowDelay"] = 0

    grid_options["columnDefs"] = [
        {"field": "version", "headerName": "Version"},
        {"field": "cast", "headerName": "Cast"},
        {"field": "peering", "headerName": "Peer"},
        {"field": "actions", "headerName": "Actions"},
        {"field": "filter", "headerName": "Filter"},
    ]

    asn_rules_grid_return = AgGrid(
        df,
        key=f"{ss["query"]}_{type}_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        theme="streamlit",
        height=325,
    )

    navigation_controls(f"{type}")


def present_asn_relationships(relationships):
    # Treats the case in which there are no results
    if (relationships == None) or (len(relationships) == 0):
        st.markdown("*No relationships were found for the given query*")
        return

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
    df = pd.DataFrame.from_dict(parsed_relationships, orient="index").astype(str)
    df = df.reset_index()

    # Presents the results
    builder = GridOptionsBuilder.from_dataframe(df)
    grid_options = builder.build()

    grid_options["autoSizeStrategy"]["type"] = "fitGridWidth"
    grid_options["defaultColDef"]["resizable"] = False
    grid_options["defaultColDef"]["sortable"] = False
    grid_options["defaultColDef"]["suppressMovable"] = True
    grid_options["defaultColDef"]["suppressHeaderFilterButton"] = True
    grid_options["tooltipShowDelay"] = 0

    grid_options["columnDefs"] = [
        {
            "field": "index",
            "headerName": "ASN",
            "cellStyle": {
                "color": "#0000EE",
                "text-decoration": "underline",
            },
        },
        {"field": "tor", "headerName": "Relationship"},
        {
            "field": "bidirectional",
            "headerName": "Bidirectionality",
            "headerTooltip": "If the relationship can be infered from both ends.",
        },
        {
            "field": "agreement",
            "headerName": "Agreement",
            "headerTooltip": "If the relationships infered from both ends agree (e.g. provider infered from one end and customer infered from the other).",
        },
        {
            "field": "reliability",
            "headerName": "Reliability",
            "headerTooltip": "Score based on amount the of relationships that agree from the AS from which they were infered.",
        },
        {
            "field": "representative",
            "headerName": "Representative",
            "headerTooltip": "If the object exchanged (exported by the client and imported by the provider) is the one that the client most exports. Always false for peers.",
        },
        {
            "field": "source",
            "headerName": "Source",
            "headerTooltip": "If the relationship was infered from this AS or from the other end.",
        },
    ]

    asn_relationships_grid_return = AgGrid(
        df,
        key=f"{ss["query"]}_relationships_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        theme="streamlit",
        height=325,
    )

    # Controls redirecting the search
    if (asn_relationships_grid_return.event_data != None) and (
        asn_relationships_grid_return.event_data["column"]["colId"] == "index"
    ):
        ss["query"] = asn_relationships_grid_return.event_data["value"]
        st.rerun()

    navigation_controls("tor")


def present_asn_set_membership(membership):
    # Treats the case in which there are no results
    if (membership == None) or (len(membership) == 0):
        st.markdown("*No set membership information was found for the given query*")
        return

    # Parses the object
    for key in membership.keys():
        membership[key]["members"] = str(len(membership[key]["members"]))
        membership[key]["set_members"] = str(len(membership[key]["set_members"]))
        membership[key].pop("body", None)
        membership[key]["is_any"] = (
            "🟢 True" if membership[key]["is_any"] == True else "🔴 False"
        )

    df = pd.DataFrame.from_dict(membership, orient="index").astype(str)
    df = df.reset_index()

    # Presents
    builder = GridOptionsBuilder.from_dataframe(df)
    grid_options = builder.build()

    grid_options["autoSizeStrategy"]["type"] = "fitGridWidth"
    grid_options["defaultColDef"]["resizable"] = False
    grid_options["defaultColDef"]["sortable"] = False
    grid_options["defaultColDef"]["suppressMovable"] = True
    grid_options["defaultColDef"]["suppressHeaderFilterButton"] = True
    grid_options["tooltipShowDelay"] = 0

    grid_options["columnDefs"] = [
        {
            "field": "index",
            "headerName": "Name",
            "cellStyle": {
                "color": "#0000EE",
                "text-decoration": "underline",
            },
        },
        {"field": "members", "headerName": "AS Members Count"},
        {"field": "set_members", "headerName": "Set Members Count"},
        {"field": "is_any", "headerName": "Is Any?"},
    ]

    set_membership_grid_return = AgGrid(
        df,
        key=f"{ss["query"]}_set_membership_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        theme="streamlit",
        height=325,
    )

    # Controls redirecting the search
    if (set_membership_grid_return.event_data != None) and (
        set_membership_grid_return.event_data["column"]["colId"] == "index"
    ):
        ss["query"] = set_membership_grid_return.event_data["value"]
        st.rerun()

    navigation_controls("memb")


def present_addr_announcement(announcement):
    # Treats the case in which there are no results
    if (announcement == None) or (len(announcement) == 0):
        st.markdown("*No announcement information was found for the given query*")
        return

    # Parses the object
    parsed_announcement = {}
    for key in announcement.keys():
        parsed_announcement[key] = {}
        parsed_announcement[key]["overlap"] = (
            "🔴 Detected"
            if len(announcement[key]["announced_by"]) > 1
            else "🟢 Not detected"
        )
        parsed_announcement[key]["announced_by"] = ", ".join(
            announcement[key]["announced_by"]
        )

    df = pd.DataFrame.from_dict(parsed_announcement, orient="index").astype(str)
    df = df.reset_index()

    # Presents
    builder = GridOptionsBuilder.from_dataframe(df)
    grid_options = builder.build()

    grid_options["autoSizeStrategy"]["type"] = "fitGridWidth"
    grid_options["defaultColDef"]["resizable"] = False
    grid_options["defaultColDef"]["sortable"] = False
    grid_options["defaultColDef"]["suppressMovable"] = True
    grid_options["defaultColDef"]["suppressHeaderFilterButton"] = True
    grid_options["tooltipShowDelay"] = 0

    grid_options["columnDefs"] = [
        {
            "field": "index",
            "headerName": "Address/Prefix",
            "cellStyle": {
                "color": "#0000EE",
                "text-decoration": "underline",
            },
        },
        {
            "field": "overlap",
            "headerName": "Overlap",
            "headerTooltip": "If the object is registered with more than one AS.",
        },
        {"field": "announced_by", "headerName": "Registered By"},
    ]

    addr_announcement_grid_return = AgGrid(
        df,
        key=f"{ss["query"]}_addr_announcement_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        theme="streamlit",
        height=325,
    )

    # Controls redirecting the search
    if (addr_announcement_grid_return.event_data != None) and (
        addr_announcement_grid_return.event_data["column"]["colId"] == "index"
    ):
        ss["query"] = addr_announcement_grid_return.event_data["value"]
        st.rerun()

    navigation_controls("route")

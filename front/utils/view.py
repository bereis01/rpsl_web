import pandas as pd
import streamlit as st
from streamlit import query_params as qp
from streamlit import session_state as ss
from utils.elements import navigation_controls
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

hyperlinkRenderer = JsCode(
    """
    class UrlCellRenderer {
        init(params) {
        this.eGui = document.createElement('a');
        this.eGui.innerText = params.value;
        this.eGui.setAttribute('href', 'https://rpslweb.snes.dcc.ufmg.br/?query=' + params.value);
        this.eGui.setAttribute('style', "text-decoration:none");
        this.eGui.setAttribute('target', "_blank");
        }
        getGui() {
        return this.eGui;
        }
    }
    """
)


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
    if ss[f"{type}_changed"]:
        for rule in rules:
            if "value" in rule["peering"]["remote_as"].keys():
                rule["peering"] = rule["peering"]["remote_as"]["value"]
            else:
                rule["peering"] = "Other"

            if "value" in rule["filter"].keys():
                rule["filter"] = rule["filter"]["value"]
            else:
                rule["filter"] = "Other"

            if rule["version"] == "ipv4":
                rule["version"] = "🟣 ipv4"
            elif rule["version"] == "ipv6":
                rule["version"] = "🟠 ipv6"
            elif rule["version"] == "any":
                rule["version"] = "⚪ any"

            if rule["cast"] == "unicast":
                rule["cast"] = "🔵 unicast"
            elif rule["cast"] == "multicast":
                rule["cast"] = "🟡 multicast"
            elif rule["cast"] == "any":
                rule["cast"] = "⚪ any"

    df = pd.DataFrame(rules).astype(str)

    # Creates a tags column with various values merged
    df["tags"] = df["version"] + ", " + df["cast"]
    df = df.drop(["version", "cast"], axis=1)

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
        {"field": "peering", "tooltipField": "peering", "headerName": "Peer"},
        {"field": "actions", "tooltipField": "actions", "headerName": "Actions"},
        {"field": "filter", "tooltipField": "filter", "headerName": "Filter"},
        {"field": "tags", "tooltipField": "tags", "headerName": "Tags"},
    ]

    asn_rules_grid_return = AgGrid(
        df,
        key=f"{qp["query"]}_{type}_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        theme="streamlit",
        height=325,
    )

    del df

    navigation_controls(f"{type}")


def present_asn_relationships(relationships):
    # Treats the case in which there are no results
    if (relationships == None) or (len(relationships) == 0):
        st.markdown("*No relationships were found for the given query*")
        return

    # Parses the dictionary
    if ss["tor_changed"]:
        for key in relationships.keys():
            relationships[key]["bidirectional"] = (
                "🟢 True" if relationships[key]["bidirectional"] == True else "🔴 False"
            )

            relationships[key]["agreement"] = (
                "🟢 True" if relationships[key]["agreement"] == True else "🔴 False"
            )

            relationships[key]["reliability"] = float(relationships[key]["reliability"])
            if relationships[key]["reliability"] >= 0.66:
                relationships[key]["reliability"] = (
                    "🟢 " + str(relationships[key]["reliability"])[:4]
                )
            elif relationships[key]["reliability"] < 0.33:
                relationships[key]["reliability"] = (
                    "🔴 " + str(relationships[key]["reliability"])[:4]
                )
            else:
                relationships[key]["reliability"] = (
                    "🟡 " + str(relationships[key]["reliability"])[:4]
                )

            relationships[key]["representative"] = (
                "🟢 True"
                if relationships[key]["representative"] == True
                else "🔴 False"
            )

            relationships[key]["source"] = (
                "🔵 Internal"
                if relationships[key]["source"] == "internal"
                else "🟠 External"
            )

    df = pd.DataFrame.from_dict(relationships, orient="index").astype(str)
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
            "tooltipField": "index",
            "headerName": "ASN",
            "cellRenderer": hyperlinkRenderer,
        },
        {"field": "tor", "tooltipField": "tor", "headerName": "Relationship"},
        {
            "field": "bidirectional",
            "tooltipField": "bidirectional",
            "headerName": "Bidirectionality",
            "headerTooltip": "If the relationship can be infered from both ends.",
        },
        {
            "field": "agreement",
            "tooltipField": "agreement",
            "headerName": "Agreement",
            "headerTooltip": "If the relationships infered from both ends agree (e.g. provider infered from one end and customer infered from the other).",
        },
        {
            "field": "reliability",
            "tooltipField": "reliability",
            "headerName": "Reliability",
            "headerTooltip": "Score based on the amount of the relationships that agree from the AS from which they were infered.",
        },
        {
            "field": "representative",
            "tooltipField": "representative",
            "headerName": "Representative",
            "headerTooltip": "If the object exchanged (exported by the client and imported by the provider) is the one that the client most exports. Always false for peers.",
        },
        {
            "field": "source",
            "tooltipField": "source",
            "headerName": "Source",
            "headerTooltip": "If the relationship was infered from this AS or from the other end.",
        },
    ]

    asn_relationships_grid_return = AgGrid(
        df,
        key=f"{qp["query"]}_relationships_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        # theme="streamlit",
        height=325,
        allow_unsafe_jscode=True,
    )

    del df

    # Controls redirecting the search
    if (asn_relationships_grid_return.event_data != None) and (
        asn_relationships_grid_return.event_data["column"]["colId"] == "index"
    ):
        qp["query"] = asn_relationships_grid_return.event_data["value"]
        st.rerun()

    navigation_controls("tor")


def present_asn_set_membership(membership):
    # Treats the case in which there are no results
    if (membership == None) or (len(membership) == 0):
        st.markdown("*No set membership information was found for the given query*")
        return

    # Parses the object
    if ss["memb_changed"]:
        for key in membership.keys():
            if membership[key]["members"]:
                membership[key]["members"] = ", ".join(membership[key]["members"])
            else:
                membership[key]["members"] = ""

            if membership[key]["set_members"]:
                membership[key]["set_members"] = ", ".join(
                    membership[key]["set_members"]
                )
            else:
                membership[key]["set_members"] = ""

            membership[key].pop("body", None)

            membership[key].pop("is_any", None)

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
            "tooltipField": "index",
            "headerName": "Name",
            "cellRenderer": hyperlinkRenderer,
        },
        {
            "field": "members",
            "tooltipField": "members",
            "headerName": "AS Members",
        },
        {
            "field": "set_members",
            "tooltipField": "set_members",
            "headerName": "Set Members",
        },
    ]

    set_membership_grid_return = AgGrid(
        df,
        key=f"{qp["query"]}_set_membership_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        theme="streamlit",
        height=325,
        allow_unsafe_jscode=True,
    )

    del df

    # Controls redirecting the search
    if (set_membership_grid_return.event_data != None) and (
        set_membership_grid_return.event_data["column"]["colId"] == "index"
    ):
        qp["query"] = set_membership_grid_return.event_data["value"]
        st.rerun()

    navigation_controls("memb")


def present_addr_announcement(announcement):
    # Treats the case in which there are no results
    if (announcement == None) or (len(announcement) == 0):
        st.markdown("*No announcement information was found for the given query*")
        return

    # Parses the object
    if ss["route_changed"]:
        for key in announcement.keys():
            if len(announcement[key]["announced_by"]) > 1:
                announcement[key]["announced_by"] = "🔴 " + ", ".join(
                    announcement[key]["announced_by"]
                )
            else:
                announcement[key]["announced_by"] = "🟢 " + ", ".join(
                    announcement[key]["announced_by"]
                )

    df = pd.DataFrame.from_dict(announcement, orient="index").astype(str)
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
            "tooltipField": "index",
            "headerName": "Address/Prefix",
            "cellRenderer": hyperlinkRenderer,
        },
        {
            "field": "announced_by",
            "tooltipField": "announced_by",
            "headerName": "Registered By",
            "headerTooltip": "🟢 If the object is registered in a single AS. 🔴 If the object is registered with more than one AS.",
        },
    ]

    addr_announcement_grid_return = AgGrid(
        df,
        key=f"{qp["query"]}_addr_announcement_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        theme="streamlit",
        height=325,
        allow_unsafe_jscode=True,
    )

    del df

    # Controls redirecting the search
    if (addr_announcement_grid_return.event_data != None) and (
        addr_announcement_grid_return.event_data["column"]["colId"] == "index"
    ):
        qp["query"] = addr_announcement_grid_return.event_data["value"]
        st.rerun()

    navigation_controls("route")


def present_asset_members(members, type):
    # Treats the case in which there are no results
    if (members == None) or (len(members) == 0):
        st.markdown("*No results were found for the given query*")
        return

    members = [{"ASN": asn} for asn in members]

    df = pd.DataFrame(members).astype(str)

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
            "field": "ASN",
            "tooltipField": "ASN",
            "headerName": "ASN",
            "cellRenderer": hyperlinkRenderer,
        },
    ]

    asset_members_grid_return = AgGrid(
        df,
        key=f"{qp["query"]}_{type}_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        theme="streamlit",
        height=325,
        allow_unsafe_jscode=True,
    )

    del df

    navigation_controls(f"{type}")


def present_addr_announced_by(announced_by):
    # Treats the case in which there are no results
    if (announced_by == None) or (len(announced_by) == 0):
        st.markdown("*No results were found for the given query*")
        return

    announced_by = [{"ASN": asn} for asn in announced_by]

    df = pd.DataFrame(announced_by).astype(str)

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
            "field": "ASN",
            "tooltipField": "ASN",
            "headerName": "ASN",
            "cellRenderer": hyperlinkRenderer,
        },
    ]

    addr_announced_by_grid_return = AgGrid(
        df,
        key=f"{qp["query"]}_addr_announced_by_grid",
        gridOptions=grid_options,
        update_on=["cellDoubleClicked"],
        theme="streamlit",
        height=325,
        allow_unsafe_jscode=True,
    )

    del df

    navigation_controls("announced_by")

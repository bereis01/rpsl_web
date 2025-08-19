# Parses a list of tags refering to import/export rules into colorful markdown badges
def parse_tags(tags, color="green"):
    result = ""
    for tag in tags:
        if isinstance(tag, list):
            aux = tag[0]
            for sub_tag in tag[1:]:
                aux += " " + sub_tag
            result += f":{color}-badge[" + aux + "] "
        else:
            result += f":{color}-badge[" + tag + "] "
    return result


# Parses a rules dataframe (import/export) into colorful markdown badges
def parse_rule_df(df):
    df["Type"] = df["Type"].apply(parse_tags, args=("gray",))
    df["Peer"] = df["Peer"].apply(parse_tags, args=("blue",))
    df["Filter"] = df["Filter"].apply(parse_tags, args=("orange",))
    df["Comments"] = df["Comments"].apply(parse_tags, args=("green",))
    return df


# Parses a dictionary of attributes
def parse_attributes(attributes):
    attributes_str = ""

    attributes_str += "**Name:** " + attributes["as-name"] + "\n\n"

    if "descr" in attributes.keys():
        attributes_str += "**Description:** " + attributes["descr"] + "\n\n"

    if "tech-c" in attributes.keys():
        attributes_str += "**Technical Contact:** " + attributes["tech-c"] + "\n\n"

    if "admin-c" in attributes.keys():
        attributes_str += (
            "**Administrative Contact:** " + attributes["admin-c"] + "\n\n"
        )

    if "mnt-by" in attributes.keys():
        attributes_str += "**Maintained By:** " + attributes["mnt-by"] + "\n\n"

    if "changed" in attributes.keys():
        attributes_str += "**Last Changed By:** " + attributes["changed"] + "\n\n"

    if "remarks" in attributes.keys():
        attributes_str += "**Remarks:**\n\n" + attributes["remarks"] + "\n\n"

    return attributes_str


# Parses a list of relationship objects
def parse_relationships(relationships):
    relationship_str = ""

    for relationship in relationships:
        sym = relationship["sym"]
        tor = relationship["tor"]
        peer = relationship["peer"]
        export_rule = relationship["export"]
        import_rule = relationship["import"]

        # Parses badges (symmetry, ...)
        if sym:
            relationship_str += ":green-badge[Symmetric] "
        else:
            relationship_str += ":red-badge[Asymmetric] "

        relationship_str += "\n\n"

        # Parses relationship type
        relationship_str += "Possible "
        match tor:
            case "Provider":
                relationship_str += ":red-background[**provider**] "
            case "Customer":
                relationship_str += ":red-background[**customer**] "
            case "Peer":
                relationship_str += ":red-background[**peer**] "
        relationship_str += "relationship with "

        # Parses peer description
        if peer["field"] == "Single" and peer["type"] == "Num":  # AS Number
            relationship_str += f":green-background[**AS{peer["value"]}**] "

        # Parses exchanged routes
        relationship_str += "over which it shares "
        if (
            export_rule["filter"]["type"] == "Any"
            and export_rule["filter"]["value"] == "Any"
        ):
            relationship_str += f":blue-background[**any route**] "
        elif export_rule["filter"]["type"] == "AsNum":
            relationship_str += f":blue-background[**the routes originated by AS{export_rule["filter"]["value"]}**] "
        elif export_rule["filter"]["type"] == "AsSet":
            relationship_str += f":blue-background[**the routes originated by any AS in AS set {export_rule["filter"]["value"]}**] "
        elif export_rule["filter"]["type"] == "RouteSet":
            relationship_str += f":blue-background[**the routes in the route set {export_rule["filter"]["value"]}**] "

        relationship_str += "and receives "
        if (
            import_rule["filter"]["type"] == "Any"
            and import_rule["filter"]["value"] == "Any"
        ):
            relationship_str += f":blue-background[**any route**] "
        elif import_rule["filter"]["type"] == "AsNum":
            relationship_str += f":blue-background[**the routes originated by AS{import_rule["filter"]["value"]}**] "
        elif import_rule["filter"]["type"] == "AsSet":
            relationship_str += f":blue-background[**the routes originated by any AS in AS set {import_rule["filter"]["value"]}**] "
        elif import_rule["filter"]["type"] == "RouteSet":
            relationship_str += f":blue-background[**the routes in the route set {import_rule["filter"]["value"]}**] "

        relationship_str += "\n"

        # Parses import routers if exists
        import_peer = import_rule["peering"]
        if "remote_router" in import_peer.keys():
            relationship_str += "- Imports routes from remote router of "
            if import_peer["remote_router"]["type"] == "Ip":
                relationship_str += (
                    f":gray-background[**IP {import_peer["remote_router"]["value"]}**] "
                )
            elif import_peer["remote_router"]["type"] == "InetRtrOrRtrSet":
                relationship_str += (
                    f":gray-background[**{import_peer["remote_router"]["value"]}**] "
                )

        if "local_router" in import_peer.keys():
            relationship_str += "- Imports routes at local router of "
            if import_peer["local_router"]["type"] == "Ip":
                relationship_str += (
                    f":gray-background[**IP {import_peer["local_router"]["value"]}**] "
                )
            elif import_peer["local_router"]["type"] == "InetRtrOrRtrSet":
                relationship_str += (
                    f":gray-background[**{import_peer["local_router"]["value"]}**] "
                )

        relationship_str += "\n"

        # Parses export routers if exists
        export_peer = export_rule["peering"]
        if "remote_router" in export_peer.keys():
            relationship_str += "- Exports routes at remote router of "
            if export_peer["remote_router"]["type"] == "Ip":
                relationship_str += (
                    f":gray-background[**IP {export_peer["remote_router"]["value"]}**] "
                )
            elif export_peer["remote_router"]["type"] == "InetRtrOrRtrSet":
                relationship_str += (
                    f":gray-background[**{export_peer["remote_router"]["value"]}**] "
                )

        if "local_router" in export_peer.keys():
            relationship_str += "- Exports routes from local router of "
            if export_peer["local_router"]["type"] == "Ip":
                relationship_str += (
                    f":gray-background[**IP {export_peer["local_router"]["value"]}**] "
                )
            elif export_peer["local_router"]["type"] == "InetRtrOrRtrSet":
                relationship_str += (
                    f":gray-background[**{export_peer["local_router"]["value"]}**] "
                )

        relationship_str += "\n\n"
        relationship_str += "---"
        relationship_str += "\n\n"

    return relationship_str


def parse_membership(membership, search: str = None):
    full_membership_str = ""
    for as_set, value in membership.items():
        members = value["members"]
        set_members = value["set_members"]

        membership_str = f":orange-background[**{as_set}**]\n"

        if members:
            membership_str += f"- **Members:** AS{members[0]}"
            for member in members[1:]:
                membership_str += f", AS{member}"

        membership_str += "\n"

        if set_members:
            membership_str += f"- **Set members:** {set_members[0]}"
            for set_member in set_members[1:]:
                membership_str += f", {set_member}"

        membership_str += "\n\n"

        if search:
            full_membership_str += membership_str if search in membership_str else ""
        else:
            full_membership_str += membership_str

    return full_membership_str


def parse_announcement(announcement, search: str = None):
    full_announcement_str = ""
    for route, value in announcement.items():
        announced_by = value["announced_by"]

        announcement_str = f":violet-background[**{route}**]\n"

        if announced_by:
            announcement_str += f"- **Announced by:** AS{announced_by[0]}"
            for asn in announced_by[1:]:
                announcement_str += f", AS{asn}"

        announcement_str += "\n\n"

        if search:
            full_announcement_str += (
                announcement_str if search in announcement_str else ""
            )
        else:
            full_announcement_str += announcement_str

    return full_announcement_str

import pandas as pd


# Parses a dictionary of attributes
def parse_attributes(attributes):
    if attributes == None:
        return "*No attributes to be shown*\n", "*No remarks to be shown*\n"

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

    remarks_str = "*No remarks to be shown*\n"
    if "remarks" in attributes.keys():
        remarks_str = attributes["remarks"]

    return attributes_str, remarks_str


# Parses a list of relationship objects
def parse_relationships(relationships):
    parsed_relationships = {}

    for key in relationships.keys():
        link = relationships[key].copy()

        link["bidirectional"] = (
            ":green-background[True]"
            if link["bidirectional"] == True
            else ":red-background[False]"
        )

        link["agreement"] = (
            ":green-background[True]"
            if link["agreement"] == True
            else ":red-background[False]"
        )

        link["reliability"] = float(link["reliability"])
        if link["reliability"] >= 0.66:
            link["reliability"] = "🟢 " + str(link["reliability"])[:4]
        elif link["reliability"] < 0.33:
            link["reliability"] = "🔴 " + str(link["reliability"])[:4]
        else:
            link["reliability"] = "🟡 " + str(link["reliability"])[:4]

        parsed_relationships[key] = link

    df = pd.DataFrame.from_dict(parsed_relationships, orient="index")
    df = df.rename(
        columns={
            "tor": "Relationship",
            "bidirectional": "Bidirectionality",
            "agreement": "Agreement",
            "reliability": "Reliability",
        }
    )
    return df


def parse_membership(membership, search: str = None):
    if membership == None:
        return "*No set membership information to be shown*\n"

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

        if search:
            full_membership_str += membership_str if search in membership_str else ""
        else:
            full_membership_str += membership_str

    return full_membership_str


def parse_announcement(announcement, search: str = None):
    if announcement == None:
        return "*No originated prefixes information to be shown*\n"

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

        if search:
            full_announcement_str += (
                announcement_str if search in announcement_str else ""
            )
        else:
            full_announcement_str += announcement_str

    return full_announcement_str

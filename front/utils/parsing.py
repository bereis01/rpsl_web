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


def parse_relationship(relationship):
    tor = relationship["tor"]
    peer = relationship["peer"]
    export_rule = relationship["export"]
    import_rule = relationship["import"]

    # Parses relationship type
    relationship_str = "Possible "
    match tor:
        case "Provider":
            relationship_str += ":red-background[**provider**] "
        case "Customer":
            relationship_str += ":red-background[**customer**] "
        case "Peer":
            relationship_str += ":red-background[**peer**] "
    relationship_str += "relationship with "

    # Parses peer description
    if (
        peer["remote_as"]["field"] == "Single" and peer["remote_as"]["type"] == "Num"
    ):  # AS Number
        relationship_str += f":green-background[**AS{peer["remote_as"]["value"]}**] "

    # Parses exchanged routes
    relationship_str += "over which it shares "
    if (
        export_rule["filter"]["type"] == "Any"
        and export_rule["filter"]["value"] == "Any"
    ):
        relationship_str += f":blue-background[**any route**] "
    elif export_rule["filter"]["type"] == "AsNum":
        relationship_str += (
            f":blue-background[**the routes originated by AS{export_rule["filter"]["value"]}**] "
        )
    elif export_rule["filter"]["type"] == "AsSet":
        relationship_str += f":blue-background[**the routes originated by any AS in AS set {export_rule["filter"]["value"]}**] "

    relationship_str += "and receives "
    if (
        import_rule["filter"]["type"] == "Any"
        and import_rule["filter"]["value"] == "Any"
    ):
        relationship_str += f":blue-background[**any route**] "
    elif import_rule["filter"]["type"] == "AsNum":
        relationship_str += (
            f":blue-background[**the routes originated by AS{import_rule["filter"]["value"]}**] "
        )
    elif import_rule["filter"]["type"] == "AsSet":
        relationship_str += f":blue-background[**the routes originated by any AS in AS set {import_rule["filter"]["value"]}**] "

    return relationship_str


def parse_relationships(df):
    relationships = df.apply(parse_relationship, axis=1).to_list()
    return " \n\n".join(relationships)

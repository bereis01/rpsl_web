# Parses a list of tags refering to import/export rules
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


# Parses a rules (import/export) dataframe
def parse_rule_df(df):
    df["Type"] = df["Type"].apply(parse_tags, args=("blue",))
    df["Peer"] = df["Peer"].apply(parse_tags, args=("green",))
    df["Filter"] = df["Filter"].apply(parse_tags, args=("orange",))
    df["Comments"] = df["Comments"].apply(parse_tags, args=("green",))
    return df

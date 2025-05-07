def generate_comment(rule):
    comment = []
    if len(rule["filter"]) == 1:
        if rule["filter"][0] == ["Any"]:
            comment.append("Possibly customer/provider relationship")
    return comment
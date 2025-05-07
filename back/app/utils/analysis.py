# Generates insightful comments based on a rule
def generate_comment(rule):
    # List of comments
    comment = []

    # Checks if is a simple "any" rule
    if len(rule["filter"]) == 1:
        if rule["filter"][0] == ["Any"]:
            comment.append("Possibly customer/provider relationship")

    return comment

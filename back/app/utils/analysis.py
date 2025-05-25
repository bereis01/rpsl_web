# Generates an analysis of the given import rule
# The analysis is a list of comments regarding the rule
def analyse_import_rule(type, peerings, filter):
    comments = []

    # Checks if it is a simple "any" rule
    if filter == ["Any"]:
        comments.append("Possibly customer/provider, provider/customer or peer/peer relationship")

    return comments


# Generates an analysis of the given export rule
# The analysis is a list of comments regarding the rule
def analyse_export_rule(type, peerings, filter):
    comments = []

    # Checks if it is a simple "any" rule
    if filter == ["Any"]:
        comments.append("Possibly provider/customer or peer/peer relationship")

    return comments

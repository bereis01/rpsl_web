import re


# Catches route set names
# A route name is a RPSL name preceded by "rs-"
def match_route_set_name(query):
    return re.fullmatch("([rR][sS]\\-[a-zA-Z0-9\\.\\-:;_]*[a-zA-Z0-9])", query)


# Catches as numbers
# An as number is a number with one or more digits form 0 to 9 preceded or not by "as"
def match_as_number(query):
    return re.fullmatch("([aA][sS][nN]?)?[\\s\\.\\-:;_]*([0-9]+)", query)


# Catches as set names
# An as set name is a RPSL name preceded by "as-"
def match_as_set_name(query):
    return re.fullmatch("([a-zA-Z][a-zA-Z0-9\\.\\-:;_]*[a-zA-Z0-9])", query)


# Catches address prefixes
# Address prefixes have the form X.X.X.X, where X is a number in the interval [0, 255]
# They can also be followed by /Y, where Y is a number in the interval [0, 32]
def match_address_prefix(query):
    return re.fullmatch(
        "([0-9][0-9]?[0-9]?\\.[0-9][0-9]?[0-9]?\\.[0-9][0-9]?[0-9]?\\.[0-9][0-9]?[0-9]?)(/[0-9][0-9]?)?",
        query,
    )


def process_query(query: str):
    # Removes white spaces from both ends
    query = query.strip()

    # Evaluates the query's type according to regular expressions
    query_matched = match_route_set_name(query)
    if query_matched:
        return "routeset", query_matched.string

    query_matched = match_as_number(query)
    if query_matched:
        return "asn", query_matched.groups()[1]

    query_matched = match_as_set_name(query)
    if query_matched:
        return "asset", query_matched.string

    # Replaces any "/" with "\\" in order to insert it as a parameter
    # into the backend endpoint address
    query_matched = match_address_prefix(query)
    if query_matched:
        return "prefix", query_matched.string.replace("/", "\\")

    return "invalid", None

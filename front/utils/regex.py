import re


def process_query(query: str):
    query_type = "invalid"
    processed_query = query

    # Catches as numbers
    match = re.fullmatch("\\s*([aA][sS][nN]?)?[\\s\\.\\-:;_]*([0-9]+)\\s*", query)
    if match:
        query_type = "asn"
        processed_query = match.groups()[1]
        return query_type, processed_query

    # Catches as names
    match = re.fullmatch("([a-zA-Z][a-zA-Z0-9\\.\\-:;_]*[a-zA-Z0-9])", query)
    if match:
        query_type = "asset"
        processed_query = match.groups()[0]
        return query_type, processed_query

    # Catches routes/prefixes
    match = re.fullmatch(
        "([0-9][0-9]?[0-9]?\\.[0-9][0-9]?[0-9]?\\.[0-9][0-9]?[0-9]?\\.[0-9][0-9]?[0-9]?)(/[0-9][0-9]?)?",
        query,
    )
    if match:
        query_type = "prefix"
        processed_query = match.groups()[0] + (
            match.groups()[1] if match.groups()[1] else ""
        )
        processed_query = processed_query.replace("/", "\\")
        return query_type, processed_query

    return "invalid", None

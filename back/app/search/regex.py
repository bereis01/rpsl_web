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

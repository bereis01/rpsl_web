# Gets the set of imported/exported objects for each asn
def process_exchanged_routes(rules):
    exchanged_routes = []

    for rule in rules:
        # Only extracts imported/exported objects
        # from the followingb types of objects
        if rule["filter"]["type"] == "AddrPrefixSet":
            for addr in rule["filter"]["value"]:
                exchanged_routes.append(addr["address_prefix"])
        elif rule["filter"]["type"] in [
            "Any",
            "PeerAS",
            "AsNum",
            "AsSet",
            "RouteSet",
            "FilterSet",
        ]:
            if rule["filter"]["value"] not in exchanged_routes:
                exchanged_routes.append(rule["filter"]["value"])

    return exchanged_routes

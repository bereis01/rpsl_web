# Gets the set of imported/exported objects for each asn
def process_exchanged_objects(rules):
    exchanged_objects = []

    for rule in rules:
        # Only extracts imported/exported objects
        # from the followingb types of objects
        if rule["filter"]["type"] == "AddrPrefixSet":
            for addr in rule["filter"]["value"]:
                exchanged_objects.append(addr["address_prefix"])
        elif rule["filter"]["type"] in [
            "Any",
            "PeerAS",
            "AsNum",
            "AsSet",
            "RouteSet",
            "FilterSet",
        ]:
            if rule["filter"]["value"] not in exchanged_objects:
                exchanged_objects.append(rule["filter"]["value"])

    return exchanged_objects

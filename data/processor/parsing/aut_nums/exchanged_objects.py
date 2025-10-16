import numpy as np


# Gets the set of imported/exported objects for each asn
def process_exchanged_objects(rules):
    exchanged_objects = []

    for rule in rules:
        # Filters the applicable types of objects
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
            exchanged_objects.append(rule["filter"]["value"])

    # Creates counts
    unique, count = np.unique(exchanged_objects, return_counts=True)
    exchanged_objects = {str(unique[i]): int(count[i]) for i in range(len(unique))}

    # Orders based on value
    exchanged_objects = dict(
        sorted(exchanged_objects.items(), key=lambda item: item[1], reverse=True)
    )

    return exchanged_objects

# Generates a dictionary in which each key is an AS/AS Set name
# and its value is the list of route_sets that include it
def process_members_inverted_as(route_sets):
    processed_inverted_as = {}

    for key in route_sets.keys():
        for member in route_sets[key]["members"]:
            # If the route_set member is an AS or AS Set,
            # adds the route_set to its list of route_sets
            if member["type"] == "as_set":
                if member["value"] in processed_inverted_as.keys():
                    processed_inverted_as[member["value"]].append(key)
                else:
                    processed_inverted_as[member["value"]] = [key]

    return processed_inverted_as


# Generates a dictionary in which each key is an address prefix
# and its value is the list of route_sets that include it
def process_members_inverted_addr(route_sets):
    processed_inverted_addr = {}

    for key in route_sets.keys():
        for member in route_sets[key]["members"]:
            # If the route_set member is an address,
            # adds the route_set to its list of route_sets
            if member["type"] == "address_prefix":
                if member["value"] in processed_inverted_addr.keys():
                    processed_inverted_addr[member["value"]].append(key)
                else:
                    processed_inverted_addr[member["value"]] = [key]

    return processed_inverted_addr


# Generates a dictionary in which each key is a route_set name
# and its value is the list of route_sets that include it
def process_members_inverted_rs(route_sets):
    processed_inverted_rs = {}

    for key in route_sets.keys():
        for member in route_sets[key]["members"]:
            # If the route_set member is an address,
            # adds the route_set to its list of route_sets
            if member["type"] == "route_set":
                if member["value"] in processed_inverted_rs.keys():
                    processed_inverted_rs[member["value"]].append(key)
                else:
                    processed_inverted_rs[member["value"]] = [key]

    return processed_inverted_rs

# Generates a dictionary in which each key is an AS name
# and its value is the list of route_sets that include it
def process_members_inverted_as(route_sets):
    processed_inverted_as = {}

    for key in route_sets.keys():
        for member in route_sets[key]["members"]:
            # If the route_set member is an AS,
            # adds the route_set to its list of route_sets
            if member["type"] == "AS":
                if member["name"] in processed_inverted_as.keys():
                    processed_inverted_as[member["name"]].append(key)
                else:
                    processed_inverted_as[member["name"]] = [key]

    return processed_inverted_as


# Generates a dictionary in which each key is an address prefix
# and its value is the list of route_sets that include it
def process_members_inverted_addr(route_sets):
    processed_inverted_addr = {}

    for key in route_sets.keys():
        for member in route_sets[key]["members"]:
            # If the route_set member is an address,
            # adds the route_set to its list of route_sets
            if member["type"] == "address":
                if member["address_prefix"] in processed_inverted_addr.keys():
                    processed_inverted_addr[member["address_prefix"]].append(key)
                else:
                    processed_inverted_addr[member["address_prefix"]] = [key]

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
                if member["name"] in processed_inverted_rs.keys():
                    processed_inverted_rs[member["name"]].append(key)
                else:
                    processed_inverted_rs[member["name"]] = [key]

    return processed_inverted_rs

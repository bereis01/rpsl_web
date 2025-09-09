from .members import process_members
from .inverted import process_inverted_as, process_inverted_addr, process_inverted_rs


def process_route_sets(route_sets, storage):
    # Extracts metadata
    route_sets_names = list(route_sets.keys())
    storage.set_key("metadata", "route_sets", route_sets_names)
    del route_sets_names

    # Processes each member of each route set
    for key in route_sets.keys():
        route_sets[key]["members"] = process_members(route_sets[key]["members"])

    # Inverts the route_sets object in terms of AS names and address prefixes
    inverted_as = process_inverted_as(route_sets)
    storage.set("rs-members_inverted_asn", inverted_as)
    del inverted_as

    inverted_addr = process_inverted_addr(route_sets)
    storage.set("rs-members_inverted_addr", inverted_addr)
    del inverted_addr

    inverted_rs = process_inverted_rs(route_sets)
    storage.set("rs-members_inverted_rs", inverted_rs)
    del inverted_rs

    # Writes the dictionary to a bucket
    storage.set("rs-members", route_sets)

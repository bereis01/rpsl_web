from storage import ObjStr
from .members import process_members
from .inverted import process_inverted_as, process_inverted_addr, process_inverted_rs


def process_route_sets(route_sets, output_path="./"):
    # Instantiates storage connection
    storage = ObjStr(output_path)

    # Processes each member of each route set
    for key in route_sets.keys():
        route_sets[key]["members"] = process_members(route_sets[key]["members"])

    # Inverts the route_sets object in terms of AS names and address prefixes
    inverted_as = process_inverted_as(route_sets)
    storage.set("route_sets_inverted_as", inverted_as)
    del inverted_as

    inverted_addr = process_inverted_addr(route_sets)
    storage.set("route_sets_inverted_addr", inverted_addr)
    del inverted_addr

    inverted_rs = process_inverted_rs(route_sets)
    storage.set("route_sets_inverted_rs", inverted_rs)
    del inverted_rs

    # Writes the dictionary to a bucket
    storage.set("route_sets", route_sets)

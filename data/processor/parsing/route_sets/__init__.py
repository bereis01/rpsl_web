from .members import process_members
from .members_inverted import (
    process_members_inverted_as,
    process_members_inverted_addr,
    process_members_inverted_rs,
)
from ..shared.attributes import process_attributes


def process_route_sets(route_sets, storage):
    # Extracts metadata
    route_sets_names = list(route_sets.keys())
    storage.set_key("metadata", "route_sets", route_sets_names)
    del route_sets_names

    # Aggregates the raw data
    attributes = {}
    for route_set in route_sets.keys():
        attributes[route_set] = process_attributes(route_sets[route_set]["body"])

    # Inverts the route_sets object in terms of AS names and address prefixes
    inverted_as = process_members_inverted_as(route_sets)
    storage.set("rs-members_inverted_asn", inverted_as)
    del inverted_as

    inverted_addr = process_members_inverted_addr(route_sets)
    storage.set("rs-members_inverted_addr", inverted_addr)
    del inverted_addr

    inverted_rs = process_members_inverted_rs(route_sets)
    storage.set("rs-members_inverted_rs", inverted_rs)
    del inverted_rs

    # Writes the dictionary to a bucket
    storage.set("rs-members", route_sets)
    storage.set("rs-attributes", attributes)

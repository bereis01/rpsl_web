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

    # Writes the dictionary to a bucket
    storage.set("rs-members", route_sets)
    storage.set("rs-attributes", attributes)

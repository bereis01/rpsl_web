from .membership import process_as_set_membership
from ..shared.attributes import process_attributes
from .members_inverted import process_members_inverted


def process_as_sets(as_sets, storage):
    # Processes alternative versions
    as_sets_names = list(as_sets.keys())
    members_inverted = process_members_inverted(as_sets)
    membership = process_as_set_membership(as_sets, members_inverted)

    # Aggregates the raw data
    attributes = {}
    as_members = {}
    set_members = {}
    for as_set in as_sets.keys():
        attributes[as_set] = process_attributes(as_sets[as_set]["body"])

        as_members[as_set] = as_sets[as_set]["members"]
        set_members[as_set] = as_sets[as_set]["set_members"]

    # Writes the results to each bucket
    storage.set_key("metadata", "as_sets", as_sets_names)
    storage.set("asset-attributes", attributes)
    storage.set("asset-members", as_sets)
    storage.set("asset-as_members", as_members)
    storage.set("asset-set_members", set_members)
    storage.set("asset-members_inverted", members_inverted)
    storage.set("asset-membership", membership)

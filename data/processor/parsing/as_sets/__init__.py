from .inverted import process_as_sets_inverted
from .membership import process_as_set_membership


def process_as_sets(as_sets, storage):
    # Processes alternative versions
    as_sets_names = list(as_sets.keys())
    as_sets_inverted = process_as_sets_inverted(as_sets)
    membership = process_as_set_membership(as_sets, as_sets_inverted)

    # Writes the results to each bucket
    storage.set_key("metadata", "as_sets", as_sets_names)
    storage.set("as-members", as_sets)
    storage.set("as-members_inverted", as_sets_inverted)
    storage.set("as-membership", membership)

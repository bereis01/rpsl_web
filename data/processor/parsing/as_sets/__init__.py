from ... import context
from shared.storage import ObjStr
from .inverted import process_as_sets_inverted
from .membership import process_as_set_membership


def process_as_sets(as_sets, output_path="./"):
    # Instantiates storage connection
    storage = ObjStr(output_path)

    # Processes alternative versions
    as_sets_names = list(as_sets.keys())
    as_sets_inverted = process_as_sets_inverted(as_sets)
    membership = process_as_set_membership(as_sets, as_sets_inverted)

    # Writes the results to each bucket
    storage.set_key("metadata", "as_sets", as_sets_names)
    storage.set("as_sets", as_sets)
    storage.set("as_sets_inverted", as_sets_inverted)
    storage.set("membership", membership)

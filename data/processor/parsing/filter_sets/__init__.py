from ... import context
from shared.storage import ObjStr


def process_filter_sets(filter_sets, output_path="./"):
    # Instantiates storage connection
    storage = ObjStr(output_path)

    # Writes the dictionary to a bucket
    storage.set("filter_sets", filter_sets)

from ... import context
from shared.storage import ObjStr


def process_peering_sets(peering_sets, output_path="./"):
    # Instantiates storage connection
    storage = ObjStr(output_path)

    # Writes the dictionary to a bucket
    storage.set("peering_sets", peering_sets)

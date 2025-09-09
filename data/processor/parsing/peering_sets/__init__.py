def process_peering_sets(peering_sets, storage):
    # Writes the dictionary to a bucket
    storage.set("ps-members", peering_sets)

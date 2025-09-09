def process_filter_sets(filter_sets, storage):
    # Writes the dictionary to a bucket
    storage.set("fs-members", filter_sets)

import pickle


def process_filter_sets(filter_sets, output_path="./"):
    # Writes the dictionary to a bucket
    filter_sets_output = open(output_path + "filter_sets", "wb")
    pickle.dump(filter_sets, filter_sets_output)
    filter_sets_output.close()

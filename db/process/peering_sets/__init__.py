import pickle


def process_peering_sets(peering_sets, output_path="./"):
    # Writes the dictionary to a bucket
    peering_sets_output = open(output_path + "peering_sets", "wb")
    pickle.dump(peering_sets, peering_sets_output)
    peering_sets_output.close()

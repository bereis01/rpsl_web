import pickle
from .inverted import process_as_sets_inverted


def process_as_sets(as_sets, output_path="./"):
    # Processes expanded version
    as_sets_inverted = process_as_sets_inverted(as_sets)

    # Writes as_sets to a bucket
    as_sets_output = open(output_path + "as_sets", "wb")
    pickle.dump(as_sets, as_sets_output)
    as_sets_output.close()

    # Writes as_sets_expanded to a bucket
    as_sets_inverted_output = open(output_path + "as_sets_inverted", "wb")
    pickle.dump(as_sets_inverted, as_sets_inverted_output)
    as_sets_inverted_output.close()

import pickle
from .inverted import process_as_sets_inverted
from .membership import process_as_set_membership


def process_as_sets(as_sets, output_path="./"):
    # Processes alternative versions
    as_sets_inverted = process_as_sets_inverted(as_sets)
    membership = process_as_set_membership(as_sets, as_sets_inverted)

    # Writes as_sets to a bucket
    as_sets_output = open(output_path + "as_sets", "wb")
    pickle.dump(as_sets, as_sets_output)
    as_sets_output.close()

    # Writes as_sets_expanded to a bucket
    as_sets_inverted_output = open(output_path + "as_sets_inverted", "wb")
    pickle.dump(as_sets_inverted, as_sets_inverted_output)
    as_sets_inverted_output.close()

    # Writes membership to a bucket
    membership_output = open(output_path + "membership", "wb")
    pickle.dump(membership, membership_output)
    membership_output.close()

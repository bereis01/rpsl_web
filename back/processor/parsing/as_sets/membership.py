def process_as_set_membership(as_sets, as_sets_inverted):
    # Each key is an asn
    membership = {}

    # Traverses all asns that are contained in an as set
    for asn in as_sets_inverted.keys():
        membership[asn] = {}

        # Each asn contains keys for the as sets it is a member of
        for as_set in as_sets_inverted[asn]:

            # The value is the list of other asns members of the set
            if as_set in as_sets.keys():
                membership[asn][as_set] = as_sets[as_set]

    return membership

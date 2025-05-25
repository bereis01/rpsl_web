def process_as_set_membership(as_sets, as_sets_inverted):
    # Each key is an asn
    membership = {}
    for asn in as_sets_inverted.keys():
        # Each asn contains keys for the as sets it is a member of
        membership[asn] = {}
        for as_set in as_sets_inverted[asn]:
            if as_set in as_sets.keys():
                # The value is the list of other asns members of the set
                membership[asn][as_set] = as_sets[as_set]

    return membership

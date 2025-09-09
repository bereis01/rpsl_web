def process_members_inverted(as_sets):
    # Retrieves all unique asn's in the members key of 'as_sets'
    members = []
    for key in as_sets.keys():
        members += as_sets[key]["members"]
    members = list(set(members))

    # Initializes the empty dictionary
    members_inverted = {asn: [] for asn in members}

    # Retrieves the as sets of which asn is a member
    for key in as_sets.keys():
        for asn in as_sets[key]["members"]:
            members_inverted[asn].append(key)

    return members_inverted

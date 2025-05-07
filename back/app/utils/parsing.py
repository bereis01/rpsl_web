import copy
from . import analysis


# Auxiliary function for traversing a dict as a tree
def process_tree_aux(tree, prefix, result):
    if isinstance(tree, dict):
        for key in tree.keys():
            prefix += [key]
            process_tree_aux(tree[key], prefix, result)
            prefix.pop()
    else:
        result.append((copy.copy(prefix), copy.copy(tree)))


# Processes import/export rules
def process_rules(tree):
    # Traverses the tree to get all unique tags and their rules
    prefix, result = [], []
    process_tree_aux(tree, prefix, result)

    # Multiply list entries to form individual records
    records = []
    for tags, rules in result:
        for rule in rules:
            for peer in rule["mp_peerings"]:
                # Processes peer/filter dict separetely
                processed_peer = process_peering_type(peer["mp_peering"])
                processed_filter = process_filter_type(rule["mp_filter"])
                # Generates comments based on the rule's structure
                comment = analysis.generate_comment(
                    {"tags": tags, "peer": processed_peer, "filter": processed_filter}
                )
                records.append((tags, processed_peer, processed_filter, comment))

    return records


# Processes peerings' type
def process_peering_type(tree):
    # Traverses the tree to get all unique tags and their elements
    prefix, result = [], []
    process_tree_aux(tree, prefix, result)

    # Formats the results into unique entries
    records = []
    for tags, peer in result:
        records.append(tags + [str(peer)])

    return records


# Processes filters' type
def process_filter_type(tree):
    # Traverses the tree to get all unique tags and their elements
    prefix, result = [], []
    process_tree_aux(tree, prefix, result)

    # Formats the results into unique entries
    records = []
    for tags, filter in result:
        if isinstance(filter, list):
            records.append(tags + [str(x) for x in filter])
        else:
            records.append(tags + [str(filter)])

    return records

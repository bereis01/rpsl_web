import copy


# Auxiliary function for process_tags
def process_tree_aux(tree, prefix, result):
    if isinstance(tree, dict):
        for key in tree.keys():
            prefix += [key]
            process_tree_aux(tree[key], prefix, result)
            prefix.pop()
    else:
        result.append((copy.copy(prefix), copy.copy(tree)))


# Processes import/export rules' type
def process_tags(tree):
    # Traverses the tree to get all unique tags and their rules
    prefix, result = [], []
    process_tree_aux(tree, prefix, result)

    # Multiply one by another to form records
    records = []
    for tags, rules in result:
        for rule in rules:
            records.append((tags, rule["mp_peerings"], rule["mp_filter"]))

    return records

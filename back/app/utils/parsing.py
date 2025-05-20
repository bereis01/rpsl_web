import copy
from . import analysis


# Auxiliary function for traversing a dict as a tree
# Stops at the first non-dict value
# Returns list of tuples (prefixes, value),
# where prefixes is a list of seen keys
def process_dict_as_tree(tree, prefix, result):
    if isinstance(tree, dict):
        for key in tree.keys():
            prefix += [key]
            process_dict_as_tree(tree[key], prefix, result)
            prefix.pop()
    else:
        result.append((copy.copy(prefix), copy.copy(tree)))


# Processes peering from import/export rule
# Converts the dictionary into a single string
def process_peering_from_import_export_rule(tree):
    # Traverses the tree to get all unique tags and their peers
    aux, peering_types = [], []
    process_dict_as_tree(tree, aux, peering_types)

    # Formats the results into a list of string values
    peerings = []
    for type, peering in peering_types:
        peerings.append((" ".join(type) + " " + str(peering)).strip())

    return peerings


def process_peering_from_import_rule_alt(tree):
    # Traverses the tree to get all unique tags and their peers
    aux, peering_types = [], []
    process_dict_as_tree(tree, aux, peering_types)

    # Formats the results into a list of string values
    peering = "FROM "
    for type, element in peering_types:
        if "remote_as" in type:
            peering += (
                "PEER [" + ((" ".join(type[2:]) + " " + str(element)).strip()) + "] "
            )
        elif "local_router" in type:
            peering += (
                "AT LOCAL ROUTER ["
                + ((" ".join(type[2:]) + " " + str(element)).strip())
                + "] "
            )
        elif "remote_router" in type:
            peering += (
                "FROM REMOTE ROUTER ["
                + ((" ".join(type[2:]) + " " + str(element)).strip())
                + "] "
            )
        elif "actions" in type:
            peering += (
                "TAKING ACTIONS ["
                + ((" ".join(type[2:]) + " " + str(element)).strip())
                + "] "
            )
        else:
            peering += "N/A [" + ((" ".join(type) + " " + str(element)).strip()) + "] "

    return peering.strip()


def process_peering_from_export_rule_alt(tree):
    # Traverses the tree to get all unique tags and their peers
    aux, peering_types = [], []
    process_dict_as_tree(tree, aux, peering_types)

    # Formats the results into a list of string values
    peering = "TO "
    for type, element in peering_types:
        if "remote_as" in type:
            peering += (
                "PEER [" + ((" ".join(type[2:]) + " " + str(element)).strip()) + "] "
            )
        elif "local_router" in type:
            peering += (
                "FROM LOCAL ROUTER ["
                + ((" ".join(type[2:]) + " " + str(element)).strip())
                + "] "
            )
        elif "remote_router" in type:
            peering += (
                "AT REMOTE ROUTER ["
                + ((" ".join(type[2:]) + " " + str(element)).strip())
                + "] "
            )
        elif "actions" in type:
            peering += (
                "TAKING ACTIONS ["
                + ((" ".join(type[2:]) + " " + str(element)).strip())
                + "] "
            )
        else:
            peering += "N/A [" + ((" ".join(type) + " " + str(element)).strip()) + "] "

    return peering.strip()


# Processes filter from import/export rule
# Converts the dictionary into a single string
def process_filter_from_import_export_rule(tree):
    # Traverses the tree to get all unique tags and their elements
    aux, filter_types = [], []
    process_dict_as_tree(tree, aux, filter_types)

    # Formats the results into a list of string values
    filters = []
    for type, filter in filter_types:
        if isinstance(filter, list):
            filters.append(
                (" ".join(type) + " " + " ".join([str(x) for x in filter])).strip()
            )
        else:
            filters.append((" ".join(type) + " " + str(filter)).strip())

    return filters


# Processes import/export rules
# Transforms the dictionary into a list of records, one for each rule
# Each record contains the columns 'type', 'peerings', 'filter' and 'comments'
def process_import_export_rules(tree, import_or_export=0):
    # Traverses the tree to get all unique tags and their rules
    aux, rule_types = [], []
    process_dict_as_tree(tree, aux, rule_types)

    # Multiply the type by the rules to get list of individual rules
    individual_rules = []
    for type, rules in rule_types:
        for rule in rules:
            # Processes the filter
            filter = process_filter_from_import_export_rule(rule["mp_filter"])

            if import_or_export == 0:
                # Processes the list of peers
                peerings = []
                for peering in rule["mp_peerings"]:
                    peerings.append(process_peering_from_import_rule_alt(peering))

                # Analyses the rule
                comments = analysis.analyse_import_rule(type, peerings, filter)
            else:
                # Processes the list of peers
                peerings = []
                for peering in rule["mp_peerings"]:
                    peerings.append(process_peering_from_export_rule_alt(peering))

                # Analyses the rule
                comments = analysis.analyse_export_rule(type, peerings, filter)

            # Appens the record
            individual_rules.append((type, peerings, filter, comments))

    return individual_rules

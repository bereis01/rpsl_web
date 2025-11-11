import pickle
from ..cleaning import match
from shared.storage import ObjStr

# Parameters
T_b = 5
T_r = 0.6


def process_relationships(store: ObjStr):
    # Expands as sets
    as_sets = store.get("asset-members")
    as_sets = expand_as_sets(as_sets)
    store.set_key("analysis", "as_sets", as_sets)

    # Pre-processes import and export rules
    imports = store.get("asn-imports")
    exports = store.get("asn-exports")
    aut_nums = pre_process_rules(imports, exports, as_sets)
    store.set_key("analysis", "aut_nums", aut_nums)

    # Applies heuristics
    ie_heuristic = apply_ie_heuristic(aut_nums)
    store.set_key("analysis", "ie_heuristic", ie_heuristic)

    set_heuristic = apply_set_heuristic(as_sets)
    store.set_key("analysis", "set_heuristic", set_heuristic)

    # Cleans some variables that are not necessary anymore
    del as_sets
    del aut_nums

    # Filtering unreliable data
    exchanged_objects = store.get("asn-exchanged_objects")
    ie_metadata, ie_heuristic_detailed = filter_unreliable_data(
        ie_heuristic, ie_heuristic, exchanged_objects
    )
    store.set_key("analysis", "ie_metadata", ie_metadata)
    store.set_key("analysis", "ie_heuristic_detailed", ie_heuristic_detailed)

    set_metadata, set_heuristic_detailed = filter_unreliable_data(
        set_heuristic, ie_heuristic, exchanged_objects
    )
    store.set_key("analysis", "set_metadata", set_metadata)
    store.set_key("analysis", "set_heuristic_detailed", set_heuristic_detailed)

    # Cleans some variables that are not necessary anymore
    del exchanged_objects
    del ie_heuristic
    del set_heuristic

    # Generating results per heuristic
    ie_heuristic_final = generate_final_results_per_heuristic(
        ie_metadata, ie_heuristic_detailed
    )
    store.set_key("analysis", "ie_heuristic_final", ie_heuristic_final)

    set_heuristic_final = generate_final_results_per_heuristic(
        set_metadata, set_heuristic_detailed
    )
    store.set_key("analysis", "set_heuristic_final", set_heuristic_final)

    # Cleans some variables that are not necessary anymore
    del ie_metadata
    del ie_heuristic_detailed
    del set_metadata
    del set_heuristic_detailed

    # Uniting results
    result = unite_heuristics(ie_heuristic_final, set_heuristic_final)
    del ie_heuristic_final
    del set_heuristic_final

    # Persisting the final result
    for key in list(result.keys()):
        store.set_key("analysis-relationships", str(key), result[key])
        result.pop(key, None)


def expand_as_sets(as_sets):
    # Removes unnecessary attributes from as_sets object
    for as_set in as_sets.keys():
        as_sets[as_set].pop("body", None)
        as_sets[as_set].pop("is_any", None)

    # Expands set members into as numbers
    for as_set in as_sets.keys():
        set_members = as_sets[as_set]["set_members"].copy()

        # Expands set members
        for set_member in set_members:
            if set_member not in as_sets.keys():
                continue

            # Extends the members list with new members
            as_sets[as_set]["members"] += as_sets[set_member]["members"]

            # Adds new as sets to the set members list
            for new_set_member in as_sets[set_member]["set_members"]:
                if new_set_member not in set_members:
                    set_members.append(new_set_member)

        # Removes duplicates
        as_sets[as_set]["members"] = list(set(as_sets[as_set]["members"]))

        # Cleans temp variables
        del set_members

    # Removes the now unused 'set_members' attribute
    # Reorganizes the data
    for as_set in as_sets.keys():
        as_sets[as_set].pop("set_members", None)
        as_sets[as_set] = as_sets[as_set]["members"]

    return as_sets


def pre_process_rules(imports, exports, as_sets):
    imports = process_rules_list(imports, as_sets)
    exports = process_rules_list(exports, as_sets)

    # Gets shared asns between imports and exports
    asns = list(set.intersection(set(imports.keys()), set(exports.keys())))

    # Unites import and export rules
    aut_nums = {}
    for asn in asns:
        aut_nums[asn] = []

        # Gets shared peers between imports and exports
        peers = list(
            set.intersection(set(imports[asn].keys()), set(exports[asn].keys()))
        )

        for peer in peers:
            aut_nums[asn].append(
                {
                    "peer": peer,
                    "import": imports[asn][peer],
                    "export": exports[asn][peer],
                }
            )

    return aut_nums


# Pre-processing applied to import and export rules
def process_rules_list(rules, as_sets):
    processed_rules = {}

    for asn in rules.keys():  # Imports and exports share the same keys
        processed_rules_list = {}

        for rule in rules[asn]:
            # Removes unnecessary keys
            rule.pop("version", None)
            rule.pop("cast", None)
            rule.pop("actions", None)

            # Extracts relevant variables
            peer = rule["peering"]["remote_as"]
            filter = rule["filter"]

            # Filters out only applicable rules
            if peer["type"] not in ["Num", "Set"]:
                continue
            if filter["type"] not in ["Any", "AsNum", "AsSet", "RouteSet"]:
                continue

            # Expands AS Sets into ASNs
            if peer["type"] == "Set":
                # Skips if the as set is not registered in the data
                if peer["value"] not in as_sets.keys():
                    continue

                for member in as_sets[peer["value"]]:
                    if member not in processed_rules_list.keys():
                        processed_rules_list[member] = [filter["value"]]
                    elif filter["value"] not in processed_rules_list[member]:
                        processed_rules_list[member].append(filter["value"])

            if peer["type"] == "Num":
                if peer["value"] not in processed_rules_list.keys():
                    processed_rules_list[peer["value"]] = [filter["value"]]
                elif filter["value"] not in processed_rules_list[peer["value"]]:
                    processed_rules_list[peer["value"]].append(filter["value"])

        processed_rules[asn] = processed_rules_list

    return processed_rules


def apply_ie_heuristic(aut_nums):
    ie_heuristic = {}

    # Pre-calculates the amount of any rules in each asn
    any_statements = {}
    for asn in aut_nums.keys():
        any_statements[asn] = 0
        for link in aut_nums[asn]:
            if "Any" in link["export"]:
                any_statements[asn] += 1

    for asn in aut_nums.keys():
        ie_heuristic[asn] = []

        for peer in aut_nums[asn]:
            # Customer
            if peer["import"] == ["Any"] and "Any" not in peer["export"]:
                ie_heuristic[asn].append(
                    (asn, peer["peer"], "Customer", peer["export"])
                )
                continue

            # Provider
            if "Any" not in peer["import"] and peer["export"] == ["Any"]:
                ie_heuristic[asn].append(
                    (asn, peer["peer"], "Provider", peer["import"])
                )

            # Peer
            if "Any" not in peer["import"] and "Any" not in peer["export"]:
                ie_heuristic[asn].append((asn, peer["peer"], "Peer", None))

            # Special case
            if peer["import"] == ["Any"] and peer["export"] == ["Any"]:

                # Counts any statements in host's exports
                host_count = any_statements[asn]

                # Counts any statements in peer's exports
                peer_count = 0
                if peer["peer"] in aut_nums.keys():
                    peer_count = any_statements[peer["peer"]]

                # The one with the most is the provider
                if host_count >= peer_count:
                    ie_heuristic[asn].append(
                        (asn, peer["peer"], "Provider", peer["import"])
                    )
                else:
                    ie_heuristic[asn].append(
                        (asn, peer["peer"], "Customer", peer["export"])
                    )

                pass

    return ie_heuristic


def apply_set_heuristic(as_sets):
    set_heuristic = {}
    for as_set_name in as_sets.keys():
        # Checks if the as set name follows the pattern ASN:ASSetName
        components = as_set_name.split(":")
        if len(components) != 2:
            continue
        firstComponentIsASN = match.match_as_num(components[0])
        secondComponentIsASSetName = match.match_as_set_name(components[1])
        if not (firstComponentIsASN and secondComponentIsASSetName):
            continue

        # Parses each component
        asn = components[0]
        if "as" in asn.lower():
            asn = asn[2:]
        asset = components[1].lower()

        # Defines the relationship indicator keywords
        p2c_keywords = ["downstream", "downlink", "customer", "client", "custs"]
        c2p_keywords = ["provider", "upstream", "uplink", "backbone"]
        p2p_keywords = ["peer"]

        # Evaluates the heuristic
        if any(keyword in asset for keyword in p2c_keywords):
            if as_set_name not in set_heuristic.keys():
                set_heuristic[as_set_name] = []
            for peer in as_sets[as_set_name]:
                set_heuristic[as_set_name].append((asn, peer, "Provider", None))
        elif any(keyword in asset for keyword in c2p_keywords):
            if as_set_name not in set_heuristic.keys():
                set_heuristic[as_set_name] = []
            for peer in as_sets[as_set_name]:
                set_heuristic[as_set_name].append((asn, peer, "Customer", None))
        elif any(keyword in asset for keyword in p2p_keywords):
            if as_set_name not in set_heuristic.keys():
                set_heuristic[as_set_name] = []
            for peer in as_sets[as_set_name]:
                set_heuristic[as_set_name].append((asn, peer, "Peer", None))

    return set_heuristic


def filter_unreliable_data(heuristic: dict, baseline: dict, exchanged_objects: dict):
    # Checks link bidirectionality and agreement
    metadata = {}
    heuristic_detailed = {}
    for key in heuristic.keys():
        metadata[key] = {"L": 0, "B": 0, "A": 0}
        heuristic_detailed[key] = []

        for link in heuristic[key]:
            host, peer, tor, x_obj = link
            bidirectional, agreement, representative = False, False, False

            # Counts the link
            metadata[key]["L"] += 1

            # Check if it is bidirectional
            if peer in baseline.keys():
                peer_peers = [peer_link[1] for peer_link in baseline[peer]]
                if host in peer_peers:
                    metadata[key]["B"] += 1
                    bidirectional = True

            # Check if it agrees with the other end
            if bidirectional:
                reverse_tor = [
                    peer_link[2] for peer_link in baseline[peer] if peer_link[1] == host
                ][0]
                if (
                    (tor == "Customer" and reverse_tor == "Provider")
                    or (tor == "Provider" and reverse_tor == "Customer")
                    or (tor == "Peer" and reverse_tor == "Peer")
                ):
                    metadata[key]["A"] += 1
                    agreement = True

            # Checks if the exchanged object is representative
            if (x_obj != None) and (host in exchanged_objects):
                if (tor == "Provider") and (
                    next(iter(exchanged_objects[host]["imports"])) in x_obj
                ):
                    representative = True
                elif (tor == "Customer") and (
                    next(iter(exchanged_objects[host]["exports"])) in x_obj
                ):
                    representative = True

            # Updates results
            heuristic_detailed[key].append(
                (host, peer, tor, bidirectional, agreement, representative)
            )

    # Calculates reliability score
    for key in metadata.keys():
        if metadata[key]["B"] > T_b:
            metadata[key]["r"] = metadata[key]["A"] / metadata[key]["B"]
        else:
            metadata[key]["r"] = 0

    """ # Filters the data
    for key in list(metadata.keys()):
        if metadata[key]["r"] < T_r:
            metadata.pop(key)
            heuristic_detailed.pop(key) """

    return metadata, heuristic_detailed


def generate_final_results_per_heuristic(metadata: dict, heuristic_detailed: dict):
    # Structures the final data structure
    heuristic_final = {}
    for key in heuristic_detailed.keys():
        for link in heuristic_detailed[key]:
            if link[0] not in heuristic_final.keys():
                heuristic_final[link[0]] = {}
            heuristic_final[link[0]][link[1]] = None
            if link[1] not in heuristic_final.keys():
                heuristic_final[link[1]] = {}
            heuristic_final[link[1]][link[0]] = None

    # Populates the final data structure
    for key in heuristic_detailed.keys():
        for link in heuristic_detailed[key]:
            host = link[0]
            peer = link[1]

            tor = link[2]
            opposite_tor = None
            match tor:
                case "Customer":
                    opposite_tor = "Provider"
                case "Provider":
                    opposite_tor = "Customer"
                case "Peer":
                    opposite_tor = "Peer"

            # The other end was not already added, if it exists
            if heuristic_final[host][peer] == None:
                heuristic_final[host][peer] = {
                    "tor": tor,
                    "bidirectional": link[3],
                    "agreement": link[4],
                    "reliability": metadata[key]["r"],
                    "representative": link[5],
                    "source": "internal",
                }
                heuristic_final[peer][host] = {
                    "tor": opposite_tor,
                    "bidirectional": link[3],
                    "agreement": link[4],
                    "reliability": metadata[key]["r"],
                    "representative": link[5],
                    "source": "external",
                }

            # The other end was already added, needs to reevaluate
            elif metadata[key]["r"] > heuristic_final[host][peer]["reliability"]:
                heuristic_final[host][peer] = {
                    "tor": tor,
                    "bidirectional": link[3],
                    "agreement": link[4],
                    "reliability": metadata[key]["r"],
                    "representative": link[5],
                    "source": "internal",
                }
                heuristic_final[peer][host] = {
                    "tor": opposite_tor,
                    "bidirectional": link[3],
                    "agreement": link[4],
                    "reliability": metadata[key]["r"],
                    "representative": link[5],
                    "source": "external",
                }

    return heuristic_final


def unite_heuristics(ie_heuristic_final: dict, set_heuristic_final: dict):
    # Organizing the data structure
    result = {}
    for host in ie_heuristic_final.keys():
        for peer in ie_heuristic_final[host].keys():
            if host not in result.keys():
                result[host] = {}
            result[host][peer] = None
            if peer not in result.keys():
                result[peer] = {}
            result[peer][host] = None
    for host in set_heuristic_final.keys():
        for peer in set_heuristic_final[host].keys():
            if host not in result.keys():
                result[host] = {}
            result[host][peer] = None
            if peer not in result.keys():
                result[peer] = {}
            result[peer][host] = None

    # Unites the heuristics
    for host in result.keys():
        for peer in result[host].keys():
            # Checks if it is classified by ie
            isClassifiedByIE = False
            if host in ie_heuristic_final.keys():
                if peer in ie_heuristic_final[host].keys():
                    isClassifiedByIE = True

            # Checks if it is classified by set
            isClassifiedBySet = False
            if host in set_heuristic_final.keys():
                if peer in set_heuristic_final[host].keys():
                    isClassifiedBySet = True

            # If classified by both, needs to resolve
            if isClassifiedByIE and isClassifiedBySet:
                # Case 1: Classifications are equal
                if (
                    ie_heuristic_final[host][peer]["tor"]
                    == set_heuristic_final[host][peer]["tor"]
                ):
                    result[host][peer] = ie_heuristic_final[host][peer]
                    result[host][peer]["reliability"] = 1.0

                # Case 2: Highest r
                elif (
                    ie_heuristic_final[host][peer]["reliability"]
                    != set_heuristic_final[host][peer]["reliability"]
                ):
                    if (
                        ie_heuristic_final[host][peer]["reliability"]
                        > set_heuristic_final[host][peer]["reliability"]
                    ):
                        result[host][peer] = ie_heuristic_final[host][peer]
                    else:
                        result[host][peer] = set_heuristic_final[host][peer]

                # Case 3: TODO Needs to keep bidirectionality data

                # Case 4: Default
                else:
                    result[host][peer] = ie_heuristic_final[host][peer]

            elif isClassifiedByIE:
                result[host][peer] = ie_heuristic_final[host][peer]
            else:
                result[host][peer] = set_heuristic_final[host][peer]

    return result

from .rules import process_rules


def process(data):
    """
    Works in place with respect to the parameter data.
    """
    # Restructure aut_nums key
    for asn in data["aut_nums"].keys():
        data["aut_nums"][asn]["imports"] = process_rules(
            data["aut_nums"][asn]["imports"]
        )
        data["aut_nums"][asn]["exports"] = process_rules(
            data["aut_nums"][asn]["exports"]
        )

    # Restructures the route_sets key
    for key in data["route_sets"].keys():
        route_set = data["route_sets"][key]
        for i in range(len(route_set["members"])):
            member = route_set["members"][i]
            member_type = list(member.keys())[0]
            match member_type:
                case "RSRange":
                    route_set["members"][i] = {
                        "type": member_type,
                        "value": member[member_type]["address_prefix"],
                        "op": member[member_type]["range_operator"],
                    }
                case "NameOp":
                    route_set["members"][i] = {
                        "type": member_type,
                        "value": member[member_type][0],
                        "op": member[member_type][1],
                    }

    # Restructure the as_routes key
    data["as_routes"] = {k: {"routes": v} for k, v in data["as_routes"].items()}

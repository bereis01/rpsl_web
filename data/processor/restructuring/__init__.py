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
                        "type": "address_prefix",
                        "value": member[member_type]["address_prefix"],
                        "operation": member[member_type]["range_operator"],
                    }
                case "NameOp":
                    if (member["NameOp"][0][0:3].lower() == "rs-") or (
                        member["NameOp"][0][0:5].lower() == "m#rs-"
                    ):
                        route_set["members"][i] = {
                            "type": "route_set",
                            "value": member[member_type][0],
                            "operation": member[member_type][1],
                        }
                    else:
                        route_set["members"][i] = {
                            "type": "as_set",  # AS or AS Set
                            "value": member[member_type][0],
                            "operation": member[member_type][1],
                        }

    # Restructure the as_routes key
    data["as_routes"] = {k: {"routes": v} for k, v in data["as_routes"].items()}

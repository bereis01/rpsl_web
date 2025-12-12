from . import match


def process(data):
    """
    Works in place with respect to the parameter data.
    """
    # Checks the 'aut_nums' object keys
    as_nums = list(data["aut_nums"].keys())
    for as_num in as_nums:
        if not match.match_as_num(as_num):
            data["aut_nums"].pop(as_num)

    # Checks the 'as_sets' object keys
    # Each key should be an as set name
    as_set_names = list(data["as_sets"].keys())
    for as_set_name in as_set_names:
        if not match.match_as_set_name(as_set_name):
            data["as_sets"].pop(as_set_name)

    # Checks the as_sets[key] 'members' object
    # Each member should be an asn
    as_set_names = list(data["as_sets"].keys())
    for as_set_name in as_set_names:
        members_names = data["as_sets"][as_set_name]["members"]
        for as_num in members_names[:]:
            if not match.match_as_num(as_num):
                data["as_sets"][as_set_name]["members"].remove(as_num)

    # Checks the as_sets[key] 'set_members' object
    # Each set member should be an as set name
    as_set_names = list(data["as_sets"].keys())
    for as_set_name in as_set_names:
        set_members_names = data["as_sets"][as_set_name]["set_members"]
        for set_member_name in set_members_names[:]:
            if not match.match_as_set_name(set_member_name):
                data["as_sets"][as_set_name]["set_members"].remove(set_member_name)

    # Checks the 'route_sets' object keys
    # Each key should be a route set name
    route_set_names = list(data["route_sets"].keys())
    for route_set_name in route_set_names:
        if not match.match_route_set_name(route_set_name):
            data["route_sets"].pop(route_set_name)

    # Checks the members of the route set
    # They should be either a route set or as set name, or an address prefix
    for key in data["route_sets"].keys():
        route_set = data["route_sets"][key]
        for member in route_set["members"][:]:
            match member["type"]:
                case "address_prefix":
                    if not match.match_ip_address(member["value"]):
                        route_set["members"].remove(member)
                case "route_set":
                    if not match.match_route_set_name(member["value"]):
                        route_set["members"].remove(member)
                case "as_set":  # AS or AS Set
                    if not (
                        match.match_as_num(member["value"])
                        or match.match_as_set_name(member["value"])
                    ):
                        route_set["members"].remove(member)

    # Checks the 'as_routes' object keys
    # Each key should be an as num
    as_nums = list(data["as_routes"].keys())
    for as_num in as_nums:
        if not match.match_as_num(as_num):
            data["as_routes"].pop(as_num)

    # Checks the as_routes[key] list of addresses
    # Each address should be a valid ipv4 or ipv6 address
    as_nums = list(data["as_routes"].keys())
    for as_num in as_nums:
        addresses = data["as_routes"][as_num]["routes"]
        for address in addresses[:]:
            if not match.match_ip_address(address):
                data["as_routes"][as_num].remove(address)

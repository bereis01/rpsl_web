from . import match


def process(data):
    # Checks the 'aut_nums' object keys
    for key in data["aut_nums"].keys():
        if not match.match_as_num(key):
            data["aut_nums"].pop(key)

    # Checks the 'as_sets' object keys
    as_set_names = list(data["as_sets"].keys())
    for as_set_name in as_set_names:
        if not match.match_as_set_name(as_set_name):
            data["as_sets"].pop(as_set_name)

    # Checks the as_sets[key] 'members' object
    as_set_names = list(data["as_sets"].keys())
    for as_set_name in as_set_names:
        members_names = data["as_sets"][as_set_name]["members"]
        for as_num in members_names:
            if not match.match_as_num(str(as_num)):
                data["as_sets"][as_set_name]["members"].remove(as_num)

    # Checks the as_sets[key] 'set_members' object
    as_set_names = list(data["as_sets"].keys())
    for as_set_name in as_set_names:
        set_members_names = data["as_sets"][as_set_name]["set_members"]
        for set_member_name in set_members_names:
            if not match.match_as_set_name(set_member_name):
                data["as_sets"][as_set_name]["set_members"].remove(set_member_name)

    # Checks the 'route_sets' object keys
    route_set_names = list(data["route_sets"].keys())
    for route_set_name in route_set_names:
        if not match.match_route_set_name(route_set_name):
            data["route_sets"].pop(route_set_name)

    # Checks the 'as_routes' object keys
    for key in data["as_routes"].keys():
        if not match.match_as_num(key):
            data["as_routes"].pop(key)

    # Checks the as_routes[key] list of addresses
    as_nums = list(data["as_routes"].keys())
    for as_num in as_nums:
        addresses = data["as_routes"][as_num]
        for address in addresses:
            if not match.match_ip_address(address):
                data["as_routes"][as_num].remove(address)

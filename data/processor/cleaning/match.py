import re


def match_as_num(asn: str):
    # Matches any number of 1 or more digits
    # preceded by "AS" or not
    return re.fullmatch("([aA][sS])?([0-9]+)", asn) != None


def match_rpsl_name(name: str):
    # RPSL names are made up of letters, digits, the character underscore "_",
    # and the character hyphen "-"; the first character of a name must be a
    # letter, and the last character of a name must be a letter or a digit
    return re.fullmatch("[a-zA-Z]([a-zA-Z0-9\\-_]*[a-zA-Z0-9])?", name) != None


def match_single_as_set_name(as_set: str):
    # AS set names are RPSL names that start with "as-"
    if as_set.lower()[0:3] != "as-":
        return False
    else:
        return match_rpsl_name(as_set)


def match_as_set_name(as_set: str):
    # AS set names can be hierarchical
    # Each component is evaluated individually
    components = as_set.split(":")

    # Makes the value false if any component is invalid
    # Components can be AS set names or AS numbers
    isNameValid = True
    for component in components:
        isComponentValid = match_single_as_set_name(component) or match_as_num(
            component
        )
        isNameValid = isNameValid and isComponentValid

    return isNameValid


def match_single_route_set_name(route_set: str):
    # Route set names are RPSL names that start with "rs-"
    if route_set.lower()[0:3] != "rs-":
        return False
    else:
        return match_rpsl_name(route_set)


def match_route_set_name(route_set: str):
    # Route set names can be hierarchical
    # Each component is evaluated individually
    components = route_set.split(":")

    # Makes the value false if any component is invalid
    # Components can be route set names or AS numbers
    isNameValid = True
    for component in components:
        isComponentValid = match_single_route_set_name(component) or match_as_num(
            component
        )
        isNameValid = isNameValid and isComponentValid

    return isNameValid


def match_ipv4_address(address: str):
    # IPv4 addressses are of the form 255.255.255.255/32
    return (
        re.fullmatch(
            "([0-9][0-9]?[0-9]?\\.[0-9][0-9]?[0-9]?\\.[0-9][0-9]?[0-9]?\\.[0-9][0-9]?[0-9]?)(/[0-9][0-9]?)?",
            address,
        )
        != None
    )


def match_ipv6_address(address: str):
    # IPv6 addressses are of the form 0000:0000:0000:0000/32
    return (
        re.fullmatch("([0-9a-fA-F]{0,4}:)*([0-9a-fA-F]{0,4})(/[0-9]{1,3})?", address)
        != None
    )


def match_ip_address(address: str):
    return match_ipv4_address(address) or match_ipv6_address(address)

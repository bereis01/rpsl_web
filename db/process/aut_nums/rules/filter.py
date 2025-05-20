def process_filter(filter):
    # Simplest case
    if filter in ["Any", "PeerAS"]:
        type = filter
        processed_filter = {"type": type, "value": type}
        return processed_filter

    # Catches abnormal cases
    if not isinstance(filter, dict) or len(filter.keys()) != 1:
        print(filter)
        raise Exception

    type = list(filter.keys())[0]

    if type in ["AsNum", "AsSet", "RouteSet"]:
        # Catches abnormal cases
        if not isinstance(filter[type], list) or len(filter[type]) != 2:
            print(filter)
            raise Exception

        value = filter[type][0]
        op = filter[type][1]

        # Catches abnormal cases
        if not isinstance(value, (str, int)) or not isinstance(op, (str, dict)):
            print(filter)
            raise Exception

        processed_filter = {"type": type, "value": value, "op": op}
        return processed_filter

    elif type in ["FilterSet", "AsPathRE", "Unknown"]:
        # Catches abnormal cases
        if not isinstance(filter[type], (str, int)):
            print(filter)
            raise Exception

        value = filter[type]

        processed_filter = {"type": type, "value": value}
        return processed_filter

    elif type in ["AddrPrefixSet"]:
        # Catches abnormal cases
        if not isinstance(filter[type], list):
            print(filter)
            raise Exception

        value = filter[type]

        processed_filter = {"type": type, "value": value}
        return processed_filter

    elif type in ["And", "Or"]:
        # Catches abnormal cases
        if not isinstance(filter[type], dict):
            print(filter)
            raise Exception

        processed_filter = {
            "type": type,
            "left": process_filter(filter[type]["left"]),
            "right": process_filter(filter[type]["right"]),
        }
        return processed_filter

    elif type in ["Not"]:
        # Catches abnormal cases
        if not isinstance(filter[type], (str, dict)):
            print(filter)
            raise Exception

        value = filter[type]

        if value == "Any":
            processed_filter = {"type": type, "value": value}
            return processed_filter
        else:
            processed_filter = {"type": type, "value": process_filter(filter[type])}
            return processed_filter

    elif type in ["Group"]:
        # Catches abnormal cases
        if not isinstance(filter[type], dict):
            print(filter)
            raise Exception

        value = filter[type]

        processed_filter = {"type": type, "value": process_filter(value)}
        return processed_filter

    elif type in ["Community"]:
        # Catches abnormal cases
        if not isinstance(filter[type], dict):
            print(filter)
            raise Exception

        value = filter[type]

        processed_filter = {"type": type, "value": value}
        return processed_filter

    else:  # Unkown case
        print(filter)
        raise Exception

def process_remote_as(remote_as):
    field, type, value = None, None, None

    # Catches abnormal cases
    if not isinstance(remote_as, dict) or len(remote_as.keys()) != 1:
        print(remote_as)
        raise Exception

    field = list(remote_as.keys())[0]

    if field in ["And", "Or", "Except"]:
        # Catches abnormal cases
        if not isinstance(remote_as[field], dict):
            print(remote_as)
            raise Exception

        processed_remote_as = {
            "field": "Operation",
            "type": field,
            "left": process_remote_as(remote_as[field]["left"]),
            "right": process_remote_as(remote_as[field]["right"]),
        }
        return processed_remote_as

    elif field in ["PeeringSet"]:
        # Catches abnormal cases
        if not isinstance(remote_as[field], str):
            print(remote_as)
            raise Exception

        value = remote_as[field]
        processed_remote_as = {
            "field": field,
            "type": field,
            "value": value,
        }
        return processed_remote_as

    elif field in ["Group"]:
        # Catches abnormal cases
        if not isinstance(remote_as[field], dict) or len(remote_as[field].keys()) != 1:
            print(remote_as)
            raise Exception

        type = list(remote_as[field].keys())[0]

        if type in ["And", "Or", "Except"]:
            # Catches abnormal cases
            if not isinstance(remote_as[field][type], dict):
                print(remote_as)
                raise Exception

            processed_remote_as = {
                "field": field,
                "type": type,
                "left": process_remote_as(remote_as[field][type]["left"]),
                "right": process_remote_as(remote_as[field][type]["right"]),
            }
            return processed_remote_as

        else:  # Unkown case
            print(remote_as)
            raise Exception

    elif field in ["Single"]:
        # Catches abnormal cases
        if not remote_as[field] == "Any" and (
            not isinstance(remote_as[field], dict) or len(remote_as[field].keys()) != 1
        ):
            print(remote_as)
            raise Exception

        # Exception
        if remote_as[field] == "Any":
            type = remote_as[field]
            processed_remote_as = {
                "field": field,
                "type": type,
                "value": type,
            }
            return processed_remote_as

        type = list(remote_as[field].keys())[0]

        if type in ["Num", "Set", "Invalid"]:
            # Catches abnormal cases
            if not isinstance(remote_as[field][type], str) and not isinstance(
                remote_as[field][type], int
            ):
                print(remote_as)
                raise Exception

            value = remote_as[field][type]
            processed_remote_as = {
                "field": field,
                "type": type,
                "value": value,
            }
            return processed_remote_as

        else:  # Unkown case
            print(remote_as)
            raise Exception

    else:  # Unkown case
        print(remote_as)
        raise Exception

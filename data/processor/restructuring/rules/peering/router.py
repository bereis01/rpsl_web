def process_router(remote_router):
    type, value = None, None

    # Catches abnormal cases
    if not isinstance(remote_router, dict) or len(remote_router.keys()) != 1:
        print(remote_router)
        raise Exception

    type = list(remote_router.keys())[0]

    if type in ["Ip", "InetRtrOrRtrSet"]:
        # Catches abnormal cases
        if not isinstance(remote_router[type], str):
            print(remote_router)
            raise Exception

        value = remote_router[type]

        processed_remote_router = {
            "type": type,
            "value": value,
        }
        return processed_remote_router

    elif type in ["And", "Or", "Except"]:
        # Catches abnormal cases
        if not isinstance(remote_router[type], dict):
            print(remote_router)
            raise Exception

        processed_remote_router = {
            "type": type,
            "left": process_router(remote_router[type]["left"]),
            "right": process_router(remote_router[type]["right"]),
        }
        return processed_remote_router

    else:  # Unkown case
        print(remote_router)
        raise Exception

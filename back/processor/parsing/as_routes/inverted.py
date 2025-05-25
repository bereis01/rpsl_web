def process_as_routes_inverted(as_routes):
    # Retrieves all unique routes in the 'routes' key of 'as_routes'
    routes = []
    for key in as_routes.keys():
        routes += as_routes[key]["routes"]
    routes = list(set(routes))

    # Initializes the empty dictionary
    as_routes_inverted = {route: {"announced_by": []} for route in routes}

    # Retrieves the asns that announce each route
    for key in as_routes.keys():
        for route in as_routes[key]["routes"]:
            as_routes_inverted[route]["announced_by"].append(key)

    return as_routes_inverted

def process_announced_by(as_routes):
    # Retrieves all unique routes in the 'routes' key of 'as_routes'
    routes = []
    for key in as_routes.keys():
        routes += as_routes[key]["routes"]
    routes = list(set(routes))

    # Initializes the empty dictionary
    announced_by = {route: {"announced_by": []} for route in routes}

    # Retrieves the asns that announce each route
    for key in as_routes.keys():
        for route in as_routes[key]["routes"]:
            announced_by[route]["announced_by"].append(key)

    return announced_by

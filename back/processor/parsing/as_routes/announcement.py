def process_announcement(as_routes, as_routes_inverted):
    # Each key is an asn
    announcement = {}
    for asn in as_routes.keys():
        # Each asn contains keys for the routes it announces
        announcement[asn] = {}
        for route in as_routes[asn]["routes"]:
            if route in as_routes_inverted.keys():
                # The value is the list of other asns that announce the same route
                announcement[asn][route] = as_routes_inverted[route]

    return announcement

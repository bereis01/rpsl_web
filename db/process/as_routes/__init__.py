import pickle


def process_as_routes(as_routes, output_path="./"):
    # Encapsulates the value into a dedicated object
    as_routes = {k: {"routes": v} for k, v in as_routes.items()}

    # Writes the dictionary to a bucket
    as_routes_output = open(output_path + "as_routes", "wb")
    pickle.dump(as_routes, as_routes_output)
    as_routes_output.close()

import pickle


def process_route_sets(route_sets, output_path="./"):
    # Writes the dictionary to a bucket
    route_sets_output = open(output_path + "route_sets", "wb")
    pickle.dump(route_sets, route_sets_output)
    route_sets_output.close()

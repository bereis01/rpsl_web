from storage import ObjStr


def process_route_sets(route_sets, output_path="./"):
    # Instantiates storage connection
    storage = ObjStr(output_path)

    # Writes the dictionary to a bucket
    storage.set("route_sets", route_sets)

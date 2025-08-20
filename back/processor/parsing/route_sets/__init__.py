from storage import ObjStr
from .members import process_members


def process_route_sets(route_sets, output_path="./"):
    # Instantiates storage connection
    storage = ObjStr(output_path)

    # Processes each member of each route set
    for key in route_sets.keys():
        route_sets[key]["members"] = process_members(route_sets[key]["members"])

    # Writes the dictionary to a bucket
    storage.set("route_sets", route_sets)

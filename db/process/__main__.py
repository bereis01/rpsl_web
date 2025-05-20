import json
from .aut_nums import process_aut_nums
from .as_sets import process_as_sets
from .route_sets import process_route_sets
from .peering_sets import process_peering_sets
from .filter_sets import process_filter_sets
from .as_routes import process_as_routes

output_path = "./data/"

# Reads the full data
f = open("./rpslyzer_output/full.json")
data = json.load(f)

""" # Processes the 'aut_nums' key
aut_nums = data["aut_nums"]
process_aut_nums(aut_nums, output_path) """

# Processes the 'as_sets' key
as_sets = data["as_sets"]
process_as_sets(as_sets, output_path)

""" # Processes the 'route_sets' key
route_sets = data["route_sets"]
process_route_sets(route_sets, output_path)

# Processes the 'peering_sets' key
peering_sets = data["peering_sets"]
process_peering_sets(peering_sets, output_path)

# Processes the 'filter_sets' key
filter_sets = data["filter_sets"]
process_filter_sets(filter_sets, output_path)

# Processes the 'as_routes' key
as_routes = data["as_routes"]
process_as_routes(as_routes, output_path) """

# Closes the file
f.close()

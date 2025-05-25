import json
from .aut_nums import process_aut_nums
from .as_sets import process_as_sets
from .route_sets import process_route_sets
from .peering_sets import process_peering_sets
from .filter_sets import process_filter_sets
from .as_routes import process_as_routes

output_path = "./data/"

# Reads the full data
# Converts all numeric data types to string
print("***STARTING***\n")
print("Reading input data...", end="", flush=True)

f = open("./rpslyzer_output/full.json")
data = json.load(
    f,
    parse_float=lambda x: str(x),
    parse_int=lambda x: str(x),
    parse_constant=lambda x: str(x),
)

print("DONE")

""" # Processes the 'aut_nums' key
print("Processing 'aut_nums'...", end="", flush=True)

aut_nums = data["aut_nums"]
process_aut_nums(aut_nums, output_path)

print("DONE")

# Processes the 'as_sets' key
print("Processing 'as_sets'...", end="", flush=True)

as_sets = data["as_sets"]
process_as_sets(as_sets, output_path)

print("DONE")

# Processes the 'route_sets' key
print("Processing 'route_sets'...", end="", flush=True)

route_sets = data["route_sets"]
process_route_sets(route_sets, output_path)

print("DONE")

# Processes the 'peering_sets' key
print("Processing 'peering_sets'...", end="", flush=True)

peering_sets = data["peering_sets"]
process_peering_sets(peering_sets, output_path)

print("DONE")

# Processes the 'filter_sets' key
print("Processing 'filter_sets'...", end="", flush=True)

filter_sets = data["filter_sets"]
process_filter_sets(filter_sets, output_path)

print("DONE") """

# Processes the 'as_routes' key
print("Processing 'as_routes'...", end="", flush=True)

as_routes = data["as_routes"]
process_as_routes(as_routes, output_path)

print("DONE")

# Closes the file
print("\n***FINISHING***")

f.close()

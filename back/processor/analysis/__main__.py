from storage import ObjStr
from .relationships import process_relationships

input_path = "./data/"
output_path = "./data/"
storage = ObjStr(input_path)

print("***STARTING***\n")

# Processes the 'aut_nums' key
print("Processing relationships...", end="", flush=True)

as_nums = storage.get("as_nums")
imports = storage.get("imports")
exports = storage.get("exports")
process_relationships(storage, as_nums, imports, exports)

print("DONE")

# Finishes
print("\n***FINISHING***")

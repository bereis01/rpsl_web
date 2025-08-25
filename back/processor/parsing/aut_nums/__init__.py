from storage import ObjStr
from .body import process_body
from .rules import process_rules
from .exchanged_routes import process_exchanged_routes


def process_aut_nums(aut_nums, output_path="./"):
    # Instantiates storage connection
    storage = ObjStr(output_path)

    # Initializes processing
    asns = []
    attributes = {}
    imports_obj = {}
    exports_obj = {}
    exchanged_routes = {}

    for asn in aut_nums.keys():
        # Saves the key
        asns.append(asn)
        exchanged_routes[asn] = {"imports": [], "exports": []}

        # Processes import key
        imports = aut_nums[asn].pop("imports", None)
        imports_obj[asn] = process_rules(imports)
        exchanged_routes[asn]["imports"] = process_exchanged_routes(imports_obj[asn])

        # Processes export key
        exports = aut_nums[asn].pop("exports", None)
        exports_obj[asn] = process_rules(exports)
        exchanged_routes[asn]["exports"] = process_exchanged_routes(exports_obj[asn])

        # Processes body
        attributes[asn] = process_body(aut_nums[asn]["body"])

    # Writes the results to each bucket
    storage.set_key("metadata", "as_nums", asns)
    storage.set("imports", imports_obj)
    storage.set("exports", exports_obj)
    storage.set("attributes", attributes)
    storage.set("exchanged_routes", exchanged_routes)

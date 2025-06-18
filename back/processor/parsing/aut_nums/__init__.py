from storage import ObjStr
from .rules import process_rules


def process_aut_nums(aut_nums, output_path="./"):
    # Instantiates storage connection
    storage = ObjStr(output_path)

    # Initializes processing
    asns = []
    imports_obj = {}
    exports_obj = {}

    for asn in aut_nums.keys():
        # Saves the key
        asns.append(asn)

        # Processes import key
        imports = aut_nums[asn].pop("imports", None)
        imports_obj[asn] = process_rules(imports)

        # Processes export key
        exports = aut_nums[asn].pop("exports", None)
        exports_obj[asn] = process_rules(exports)

    # Writes the results to each bucket
    storage.set_key("metadata", "as_nums", asns)
    storage.set("imports", imports_obj)
    storage.set("exports", exports_obj)

from .rules import process_rules
from ..shared.attributes import process_attributes
from .exchanged_objects import process_exchanged_objects


def process_aut_nums(aut_nums, storage):
    asns = []
    attributes = {}
    imports_obj = {}
    exports_obj = {}
    exchanged_objects = {}

    for asn in aut_nums.keys():
        # Saves the key
        asns.append(asn)
        exchanged_objects[asn] = {"imports": [], "exports": []}

        # Processes import attribute
        imports = aut_nums[asn].pop("imports", None)
        imports_obj[asn] = process_rules(imports)
        exchanged_objects[asn]["imports"] = process_exchanged_objects(imports_obj[asn])

        # Processes export attribute
        exports = aut_nums[asn].pop("exports", None)
        exports_obj[asn] = process_rules(exports)
        exchanged_objects[asn]["exports"] = process_exchanged_objects(exports_obj[asn])

        # Processes body attribute
        attributes[asn] = process_attributes(aut_nums[asn]["body"])

    # Writes the results to each bucket
    storage.set_key("metadata", "as_nums", asns)
    storage.set("asn-imports", imports_obj)
    storage.set("asn-exports", exports_obj)
    storage.set("asn-attributes", attributes)
    storage.set("asn-exchanged_objects", exchanged_objects)

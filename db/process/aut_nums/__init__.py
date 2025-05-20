import pickle
from .rules import process_rules


def process_aut_nums(aut_nums, output_path="./"):
    as_nums = []
    imports_obj = {}
    exports_obj = {}

    for asn in aut_nums.keys():
        # Saves the key
        as_nums.append(asn)

        # Processes import key
        imports = aut_nums[asn].pop("imports", None)
        imports_obj[asn] = process_rules(imports)

        # Processes export key
        exports = aut_nums[asn].pop("exports", None)
        exports_obj[asn] = process_rules(exports)

    # Writes the results to each bucket
    as_nums_output = open(output_path + "as_nums", "wb")
    pickle.dump(aut_nums, as_nums_output)
    as_nums_output.close()

    aut_nums_output = open(output_path + "aut_nums", "wb")
    pickle.dump(aut_nums, aut_nums_output)
    aut_nums_output.close()

    imports_output = open(output_path + "imports", "wb")
    pickle.dump(imports_obj, imports_output)
    imports_output.close()

    exports_output = open(output_path + "exports", "wb")
    pickle.dump(exports_obj, exports_output)
    exports_output.close()

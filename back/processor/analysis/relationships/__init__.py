from .import_export_heuristic import import_export_heuristic


def process_relationships(storage, as_nums, imports, exports):
    relationships = {}

    for asn in as_nums:
        relationships[asn] = import_export_heuristic(asn, imports[asn], exports[asn])

    storage.set("relationships", relationships)

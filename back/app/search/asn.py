from ..analysis.relationships import import_export_heuristic


def search_asn(asn: str, storage):
    # Gets basic info from aut_nums bucket
    aut_nums = storage.get("aut_nums", str(asn))

    # Gets import and export rules from respective buckets
    imports = storage.get("imports", str(asn))
    exports = storage.get("exports", str(asn))

    # Calculates relationships
    relationships = import_export_heuristic(asn, imports, exports)

    # Organizing data
    raw = {"aut_nums": aut_nums}
    analysis = {"relationships": relationships}
    sources = {"relationships": {"imports": imports, "exports": exports}}

    return {
        "raw": raw,
        "analysis": analysis,
        "sources": sources,
    }

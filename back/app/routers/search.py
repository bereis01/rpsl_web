from ..storage import ObjStr
from fastapi import APIRouter
from ..analysis.relationships.import_export_heuristic import import_export_heuristic

# Initializes router
router = APIRouter(prefix="/search")

# Initializes connection to storage
storage = ObjStr("../db/data/")


@router.get("/asn/{asn}")
def search_asn(asn: int):
    """
    Searches buckets for entries related to the given AS number.
    """
    # Gets basic info from aut_nums bucket
    aut_nums = storage.get("aut_nums", str(asn))

    # Gets import and export rules from respective buckets
    imports = storage.get("imports", str(asn))
    exports = storage.get("exports", str(asn))

    # Calculates relationships
    relationships = import_export_heuristic(asn, imports, exports)

    return {
        "aut_nums": aut_nums,
        "imports": imports,
        "exports": exports,
        "relationships": relationships,
    }

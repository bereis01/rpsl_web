from .. import search
from ..storage import ObjStr
from fastapi import APIRouter

# Initializes router
router = APIRouter()

# Initializes connection to storage
storage = ObjStr("../db/data/")


@router.get("/search")
def search_asn(query: str = ""):
    """
    Processes the query. Generates search results based on it.
    """
    # Processes the query
    query_type, processed_query = search.process_query(query)

    # Generates search results
    results = {}
    match query_type:
        case "asn":
            results = search.search_asn(processed_query, storage)

    return {"type": query_type, "results": results}

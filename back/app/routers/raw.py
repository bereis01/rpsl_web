from fastapi import APIRouter
from ..storage import ObjStr

# Initializes router
router = APIRouter()

# Initializes connection to storage
storage = ObjStr("../db/data/")


@router.get("/as_routes")
def fetch_as_routes_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the as_routes bucket.
    Implements pagination with query parameters.
    """
    # Retrieves the slice
    result = storage.get_slice("as_routes", skip, limit)

    return {"skip": skip, "limit": limit, "count": len(result.keys()), "data": result}


@router.get("/as_sets")
def fetch__as_sets_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the as_sets bucket.
    Implements pagination with query parameters.
    """
    # Retrieves the slice
    result = storage.get_slice("as_sets", skip, limit)

    return {"skip": skip, "limit": limit, "count": len(result.keys()), "data": result}


@router.get("/aut_nums")
def fetch_aut_nums_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the aut_nums bucket.
    Implements pagination with query parameters.
    """
    # Retrieves the slice
    result = storage.get_slice("aut_nums", skip, limit)

    return {"skip": skip, "limit": limit, "count": len(result.keys()), "data": result}


@router.get("/filter_sets")
def fetch_filter_sets_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the filter_sets bucket.
    Implements pagination with query parameters.
    """
    # Retrieves the slice
    result = storage.get_slice("filter_sets", skip, limit)

    return {"skip": skip, "limit": limit, "count": len(result.keys()), "data": result}


@router.get("/peering_sets")
def fetch_peering_sets_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the peering_sets bucket.
    Implements pagination with query parameters.
    """
    # Retrieves the slice
    result = storage.get_slice("peering_sets", skip, limit)

    return {"skip": skip, "limit": limit, "count": len(result.keys()), "data": result}


@router.get("/route_sets")
def fetch_route_sets_page(skip: int = 0, limit: int = 10):
    """
    Fetch entries from the route_sets bucket.
    Implements pagination with query parameters.
    """
    # Retrieves the slice
    result = storage.get_slice("route_sets", skip, limit)

    return {"skip": skip, "limit": limit, "count": len(result.keys()), "data": result}

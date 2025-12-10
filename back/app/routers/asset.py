import itertools
from fastapi import APIRouter, Request
from ..search import search_dict, search_list

# Initializes router
router = APIRouter(prefix="/asset")


@router.get("/{as_set}")
def check_asset_exist(request: Request, as_set: str):
    result = request.app.state.storage.get_key("metadata", "as_sets")

    if as_set in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/attributes/{as_set}")
def get_attributes(request: Request, as_set: str):
    result = request.app.state.storage.get("asset-attributes", as_set)

    return {"result": result}


@router.get("/members/{as_set}")
def get_members(request: Request, as_set: str):
    result = request.app.state.storage.get("asset-members", as_set)

    return {"result": result}


@router.get("/as_members/{as_set}")
def get_as_members(
    request: Request,
    as_set: str,
    skip: int = None,
    limit: int = None,
    search: str = None,
):
    result = request.app.state.storage.get("asset-as_members", as_set)

    # If nothing is found
    if result == None:
        return {"count": 0, "skip": 0, "limit": 0, "result": result}

    # Applies search
    result = search_list(result, search)

    if not skip:
        skip = 0
    if not limit:
        limit = len(result)

    return {
        "count": len(result),
        "skip": skip,
        "limit": limit,
        "result": result[skip : skip + limit],
    }


@router.get("/set_members/{as_set}")
def get_set_members(
    request: Request,
    as_set: str,
    skip: int = None,
    limit: int = None,
    search: str = None,
):
    result = request.app.state.storage.get("asset-set_members", as_set)

    # If nothing is found
    if result == None:
        return {"count": 0, "skip": 0, "limit": 0, "result": result}

    # Applies search
    result = search_list(result, search)

    if not skip:
        skip = 0
    if not limit:
        limit = len(result)

    return {
        "count": len(result),
        "skip": skip,
        "limit": limit,
        "result": result[skip : skip + limit],
    }


@router.get("/membership/{asn}")
def get_membership(
    request: Request, asn: str, skip: int = None, limit: int = None, search: str = None
):
    result = request.app.state.storage.get("asset-membership", asn)

    # If nothing is found
    if result == None:
        return {"count": 0, "skip": 0, "limit": 0, "result": result}

    # Applies search
    result = search_dict(result, search)

    # Applies paging
    if not skip:
        skip = 0
    if not limit:
        limit = len(result)

    return {
        "count": len(result),
        "skip": skip,
        "limit": limit,
        "result": dict(itertools.islice(result.items(), skip, skip + limit)),
    }

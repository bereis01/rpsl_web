import itertools
from fastapi import APIRouter, Request
from ..search import search_dict, search_list

# Initializes router
router = APIRouter(prefix="/addr")


@router.get("/{addr_prefix}")
def check_addr_prefix_exist(request: Request, addr_prefix: str):
    result = request.app.state.storage.get_key("metadata", "addr_prefixes")

    # / was codified as \\ in order to be inserted into the URL
    # Thus, all \\ occurrences are changed to /
    if addr_prefix.replace("\\", "/") in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/announced_by/{addr_prefix}")
def get_announced_by(
    request: Request,
    addr_prefix: str,
    skip: int = None,
    limit: int = None,
    search: str = None,
):
    # / was codified as \\ in order to be inserted into the URL
    # Thus, all \\ occurrences are changed to /
    result = request.app.state.storage.get(
        "addr-announced_by", addr_prefix.replace("\\", "/")
    )
    result = result["announced_by"]

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


@router.get("/announcement/{asn}")
def get_routes(
    request: Request, asn: str, skip: int = None, limit: int = None, search: str = None
):
    result = request.app.state.storage.get("addr-announcement", asn)

    # If nothing is found
    if result == None:
        return {"count": 0, "skip": 0, "limit": 0, "result": result}

    # Applies search
    if search:
        unfiltered_result = result
        result = {}
        for route in unfiltered_result.items():
            if search in str(route):
                result[route[0]] = route[1]

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

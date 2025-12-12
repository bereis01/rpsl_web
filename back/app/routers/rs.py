from fastapi import APIRouter, Request
from ..search import search_dict, search_list

# Initializes router
router = APIRouter(prefix="/rs")


@router.get("/{route_set}")
def check_rs_exists(request: Request, route_set: str):
    result = request.app.state.storage.get_key("metadata", "route_sets")

    if route_set in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/attributes/{route_set}")
def get_attributes(request: Request, route_set: str):
    result = request.app.state.storage.get("rs-attributes", route_set)

    return {"result": result}


@router.get("/members/{route_set}")
def get_members(
    request: Request,
    route_set: str,
    skip: int = None,
    limit: int = None,
    search: str = None,
):
    result = request.app.state.storage.get("rs-members", route_set)

    # If nothing is found
    if result == None:
        return {"count": 0, "skip": 0, "limit": 0, "result": result}

    # Minor fix
    result = result["members"]

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

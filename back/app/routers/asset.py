import itertools
from fastapi import APIRouter, Request

# Initializes router
router = APIRouter(prefix="/asset")


@router.get("/{as_set}")
def check_asset_exist(request: Request, as_set: str):
    result = request.app.state.storage.get_key("metadata", "as_sets")

    if as_set in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/members/{as_set}")
def get_members(request: Request, as_set: str):
    result = request.app.state.storage.get("asset-members", as_set)

    return {"result": result}


@router.get("/membership/{asn}")
def get_membership(
    request: Request, asn: str, skip: int = None, limit: int = None, search: str = None
):
    result = request.app.state.storage.get("asset-membership", asn)

    # If nothing is found
    if result == None:
        return {"result": result}

    # Applies search
    if search:
        unfiltered_result = result
        result = {}
        for membership in unfiltered_result.items():
            if search in str(membership):
                result[membership[0]] = membership[1]

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

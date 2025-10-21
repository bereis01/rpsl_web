import itertools
from fastapi import APIRouter, Request

# Initializes router
router = APIRouter(prefix="/asn")


@router.get("/{asn}")
def check_asn_exists(request: Request, asn: str):
    result = request.app.state.storage.get_key("metadata", "as_nums")

    if asn in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/attributes/{asn}")
def get_attributes(request: Request, asn: str):
    result = request.app.state.storage.get("asn-attributes", asn)

    return {"result": result}


@router.get("/exchanged_objects/{asn}")
def get_exchanged_objects(request: Request, asn: str):
    exchanged_objects = request.app.state.storage.get("asn-exchanged_objects", asn)

    # If nothing is found
    if exchanged_objects == None:
        return {"result": None}

    # Clips the result to 10 items
    for key in exchanged_objects.keys():
        others_count = 0
        while len(exchanged_objects[key]) > 9:
            sub_key = list(exchanged_objects[key].keys())[-1]
            others_count += exchanged_objects[key].pop(sub_key)
        if others_count > 0:
            exchanged_objects[key]["Others"] = others_count

    return {"result": exchanged_objects}


@router.get("/imports/{asn}")
def get_imports(request: Request, asn: str, skip: int = None, limit: int = None):
    result = request.app.state.storage.get("asn-imports", asn)

    # If nothing is found
    if result == None:
        return {"count": 0, "skip": 0, "limit": 0, "result": result}

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


@router.get("/exports/{asn}")
def get_exports(request: Request, asn: str, skip: int = None, limit: int = None):
    result = request.app.state.storage.get("asn-exports", asn)

    # If nothing is found
    if result == None:
        return {"count": 0, "skip": 0, "limit": 0, "result": result}

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


@router.get("/relationships/{asn}")
def get_relationships(
    request: Request, asn: str, skip: int = None, limit: int = None, search: str = None
):
    result = request.app.state.storage.get("analysis-relationships", asn)

    # If nothing is found
    if result == None:
        return {"count": 0, "skip": 0, "limit": 0, "result": result}

    # Applies search
    if search:
        unfiltered_result = result
        result = {}
        for key in unfiltered_result.keys():
            if search in (key + str(unfiltered_result[key])):
                result[key] = unfiltered_result[key]

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

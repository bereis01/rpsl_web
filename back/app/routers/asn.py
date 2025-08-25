import itertools
from fastapi import APIRouter, Request

# Initializes router
router = APIRouter(prefix="/asn")


@router.get("/{asn}")
def get_as_num_exist(request: Request, asn: str):
    result = request.app.state.storage.get_key("metadata", "as_nums")

    if asn in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/aut_num/{asn}")
def get_aut_num(request: Request, asn: str):
    result = request.app.state.storage.get("aut_nums", asn)

    return {"result": result}


@router.get("/attributes/{asn}")
def get_as_attributes(request: Request, asn: str):
    result = request.app.state.storage.get("attributes", asn)

    return {"result": result}


@router.get("/summary/{asn}")
def get_relationships_summary(request: Request, asn: str):
    simple_customer = request.app.state.storage.get(
        "relationships_simple_customer", asn
    )
    simple_provider = request.app.state.storage.get(
        "relationships_simple_provider", asn
    )

    # If nothing is found
    if (simple_customer == None) and (simple_provider == None):
        return {"result": None}

    return {
        "result": {
            "simple_customer": simple_customer,
            "simple_provider": simple_provider,
        }
    }


@router.get("/exch_routes/{asn}")
def get_exchanged_routes(request: Request, asn: str):
    exchanged_routes = request.app.state.storage.get("exchanged_routes", asn)

    # If nothing is found
    if exchanged_routes == None:
        return {"result": None}

    return {"result": exchanged_routes}


@router.get("/tor/{asn}")
def get_relationships(
    request: Request, asn: str, skip: int = None, limit: int = None, search: str = None
):
    result = request.app.state.storage.get("relationships", asn)

    # If nothing is found
    if result == None:
        return {"result": result}

    # Applies search
    if search:
        unfiltered_result = result
        result = []
        for relationship in unfiltered_result:
            if search in str(relationship):
                result.append(relationship)

    # Applies paging
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


@router.get("/imports/{asn}")
def get_imports(request: Request, asn: str, skip: int = None, limit: int = None):
    result = request.app.state.storage.get("imports", asn)

    # If nothing is found
    if result == None:
        return {"result": result}

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
    result = request.app.state.storage.get("exports", asn)

    # If nothing is found
    if result == None:
        return {"result": result}

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
def get_set_membership(
    request: Request, asn: str, skip: int = None, limit: int = None, search: str = None
):
    result = request.app.state.storage.get("membership", asn)

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


@router.get("/announcement/{asn}")
def get_routes(
    request: Request, asn: str, skip: int = None, limit: int = None, search: str = None
):
    result = request.app.state.storage.get("announcement", asn)

    # If nothing is found
    if result == None:
        return {"result": result}

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

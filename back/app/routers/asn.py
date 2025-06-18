import itertools
from storage import ObjStr
from fastapi import APIRouter

# Initializes router
router = APIRouter(prefix="/asn")

# Initializes connection to storage
storage = ObjStr("./data/")


@router.get("/{asn}")
def get_as_num_exist(asn: str):
    result = storage.get_key("metadata", "as_nums")

    if asn in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/aut_num/{asn}")
def get_aut_num(asn: str):
    result = storage.get("aut_nums", asn)

    return {"result": result}


@router.get("/summary/{asn}")
def get_relationships_summary(asn: str):
    simple_customer = storage.get("relationships_simple_customer", asn)
    simple_provider = storage.get("relationships_simple_provider", asn)

    # If nothing is found
    if (simple_customer == None) and (simple_provider == None):
        return {"result": None}

    return {
        "result": {
            "simple_customer": simple_customer,
            "simple_provider": simple_provider,
        }
    }


@router.get("/tor/{asn}")
def get_relationships(
    asn: str, skip: int = None, limit: int = None, search: str = None
):
    result = storage.get("relationships", asn)

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
def get_imports(asn: str, skip: int = None, limit: int = None):
    result = storage.get("imports", asn)

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
def get_exports(asn: str, skip: int = None, limit: int = None):
    result = storage.get("exports", asn)

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
    asn: str, skip: int = None, limit: int = None, search: str = None
):
    result = storage.get("membership", asn)

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
def get_routes(asn: str, skip: int = None, limit: int = None, search: str = None):
    result = storage.get("announcement", asn)

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

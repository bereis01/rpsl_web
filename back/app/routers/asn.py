import itertools
from storage import ObjStr
from fastapi import APIRouter

# Initializes router
router = APIRouter(prefix="/asn")

# Initializes connection to storage
storage = ObjStr("./data/")


@router.get("/aut_num/{asn}")
def get_aut_num(asn: str):
    result = storage.get("aut_nums", asn)

    return {"result": result}


@router.get("/tor/{asn}")
def get_relationships(
    asn: str, skip: int = None, limit: int = None, search: str = None
):
    result = storage.get("relationships", asn)

    # Applies search
    if search:
        for relationship in result:
            if search not in str(relationship):
                result = list(filter(lambda x: x != relationship, result))

    # Applies paging
    if (not skip) and (not limit):
        skip = 0
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

    if (not skip) and (not limit):
        skip = 0
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

    if (not skip) and (not limit):
        skip = 0
        limit = len(result)

    return {
        "count": len(result),
        "skip": skip,
        "limit": limit,
        "result": result[skip : skip + limit],
    }


@router.get("/membership/{asn}")
def get_set_membership(asn: str, skip: int = None, limit: int = None):
    result = storage.get("membership", asn)

    if (not skip) and (not limit):
        skip = 0
        limit = len(result)

    return {
        "count": len(result),
        "skip": skip,
        "limit": limit,
        "result": dict(itertools.islice(result.items(), skip, skip + limit)),
    }


@router.get("/routes/{asn}")
def get_routes(asn: str, skip: int = None, limit: int = None):
    result = storage.get("announcement", asn)

    if (not skip) and (not limit):
        skip = 0
        limit = len(result)

    return {
        "count": len(result),
        "skip": skip,
        "limit": limit,
        "result": dict(itertools.islice(result.items(), skip, skip + limit)),
    }

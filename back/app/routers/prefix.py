from storage import ObjStr
from fastapi import APIRouter

# Initializes router
router = APIRouter(prefix="/prefix")

# Initializes connection to storage
storage = ObjStr("./data/")


@router.get("/{prefix}")
def get_prefix_exist(prefix: str):
    result = storage.get_key("metadata", "prefixes")

    if prefix.replace("\\", "/") in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/announced_by/{prefix}")
def get_announced_by(prefix: str):
    result = storage.get("as_routes_inverted", prefix.replace("\\", "/"))

    return {"result": result}

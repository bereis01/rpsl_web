from storage import ObjStr
from fastapi import APIRouter

# Initializes router
router = APIRouter(prefix="/as_set")

# Initializes connection to storage
storage = ObjStr("./data/")


@router.get("/{as_set}")
def get_as_set_exist(as_set: str):
    result = storage.get_key("metadata", "as_sets")

    if as_set in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/as_set/{as_set}")
def get_as_set(as_set: str):
    result = storage.get("as_sets", as_set)

    return {"result": result}

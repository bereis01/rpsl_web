import itertools
from storage import ObjStr
from fastapi import APIRouter

# Initializes router
router = APIRouter(prefix="/as_set")

# Initializes connection to storage
storage = ObjStr("./data/")


@router.get("/{as_set}")
def get_as_set(as_set: str):
    result = storage.get("as_sets", as_set)

    return {"result": result}

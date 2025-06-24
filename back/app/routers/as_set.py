from fastapi import APIRouter, Request

# Initializes router
router = APIRouter(prefix="/as_set")


@router.get("/{as_set}")
def get_as_set_exist(request: Request, as_set: str):
    result = request.app.state.storage.get_key("metadata", "as_sets")

    if as_set in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/as_set/{as_set}")
def get_as_set(request: Request, as_set: str):
    result = request.app.state.storage.get("as_sets", as_set)

    return {"result": result}

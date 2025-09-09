from fastapi import APIRouter, Request

# Initializes router
router = APIRouter(prefix="/rs")


@router.get("/{route_set}")
def check_rs_exists(request: Request, route_set: str):
    result = request.app.state.storage.get_key("metadata", "route_sets")

    if route_set in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/members/{route_set}")
def get_members(request: Request, route_set: str):
    result = request.app.state.storage.get("rs-members", route_set)

    return {"result": result}

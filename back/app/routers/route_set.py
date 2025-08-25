from fastapi import APIRouter, Request

# Initializes router
router = APIRouter(prefix="/route_set")


@router.get("/{route_set}")
def route_set_exist(request: Request, route_set: str):
    result = request.app.state.storage.get_key("metadata", "route_sets")

    if route_set in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/route_set/{route_set}")
def get_route_set(request: Request, route_set: str):
    result = request.app.state.storage.get("route_sets", route_set)

    return {"result": result}

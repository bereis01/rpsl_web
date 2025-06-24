from fastapi import APIRouter, Request

# Initializes router
router = APIRouter(prefix="/prefix")


@router.get("/{prefix}")
def get_prefix_exist(request: Request, prefix: str):
    result = request.app.state.storage.get_key("metadata", "prefixes")

    if prefix.replace("\\", "/") in result:
        return {"result": True}
    else:
        return {"result": False}


@router.get("/announced_by/{prefix}")
def get_announced_by(request: Request, prefix: str):
    result = request.app.state.storage.get(
        "as_routes_inverted", prefix.replace("\\", "/")
    )

    return {"result": result}

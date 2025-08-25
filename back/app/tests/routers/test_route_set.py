from storage import ObjStr
from fastapi import FastAPI
from ...routers import route_set
from fastapi.testclient import TestClient

# Initializes app
app = FastAPI()

# Initializes connection to storage
app.state.storage = ObjStr("./data/")

# Includes all routers
app.include_router(route_set.router)

# Initializes test client
client = TestClient(app)


def test_get_route_set():
    response = client.get("/route_set/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]

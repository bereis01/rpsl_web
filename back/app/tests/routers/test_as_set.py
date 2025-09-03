from ... import context
from fastapi import FastAPI
from ...routers import as_set
from shared.storage import ObjStr
from fastapi.testclient import TestClient

# Initializes app
app = FastAPI()

# Initializes connection to storage
app.state.storage = ObjStr("../data/objects")

# Includes all routers
app.include_router(as_set.router)

# Initializes test client
client = TestClient(app)


def test_get_as_set():
    response = client.get("/as_set/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]

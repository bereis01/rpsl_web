from ... import context
from ...routers import rs
from fastapi import FastAPI
from shared.storage import ObjStr
from fastapi.testclient import TestClient

# Initializes app
app = FastAPI()

# Initializes connection to storage
app.state.storage = ObjStr("../data/objects")

# Includes all routers
app.include_router(rs.router)

# Initializes test client
client = TestClient(app)


def test_check_rs_exists():
    # Existent entry
    response = client.get("/rs/rs-Level3-transit")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == True

    # Non-existent entry
    response = client.get("/rs/none")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == False


def test_get_rs_members():
    response = client.get("/rs/members/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]

from ... import context
from fastapi import FastAPI
from ...routers import asset
from shared.storage import ObjStr
from fastapi.testclient import TestClient

# Initializes app
app = FastAPI()

# Initializes connection to storage
app.state.storage = ObjStr("../data/objects")

# Includes all routers
app.include_router(asset.router)

# Initializes test client
client = TestClient(app)


def test_check_asset_exists():
    # Existent entry
    response = client.get("/asset/AS-CUSTOMERS")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == True

    # Non-existent entry
    response = client.get("/asset/none")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == False


def test_get_asset_members():
    response = client.get("/asset/members/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]


def test_get_asset_membership():
    # Existent entry
    response = client.get("/asset/membership/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["count", "skip", "limit", "result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/asset/membership/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None

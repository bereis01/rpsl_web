from ... import context
from fastapi import FastAPI
from ...routers import addr
from shared.storage import ObjStr
from fastapi.testclient import TestClient

# Initializes app
app = FastAPI()

# Initializes connection to storage
app.state.storage = ObjStr("../data/objects")

# Includes all routers
app.include_router(addr.router)

# Initializes test client
client = TestClient(app)


def test_check_addr_exists():
    # Existent entry
    response = client.get("/addr/2.58.60.0\\22")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == True

    # Non-existent entry
    response = client.get("/addr/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == False


def test_get_addr_announced_by():
    response = client.get("/addr/announced_by/0")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]


def test_get_addr_announcement():
    # Existent entry
    response = client.get("/addr/announcement/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["count", "skip", "limit", "result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/addr/announcement/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None

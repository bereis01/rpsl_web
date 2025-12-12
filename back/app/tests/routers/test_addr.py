from ... import context
from fastapi import FastAPI
from ...routers import addr
from unittest.mock import Mock
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
    # Mocks calls to storage
    app.state.storage.get_key = Mock(return_value=["2.58.60.0/22"])

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
    # Mocks calls to storage
    app.state.storage.get = Mock(
        return_value={"announced_by": ["201813", "57916", "174"]}
    )

    # Existent entry
    response = client.get("/addr/announced_by/2.58.60.0\\22")

    assert response.status_code == 200
    assert "2.58.60.0/22" in app.state.storage.get.call_args[0]
    assert response.json()["result"] == ["201813", "57916", "174"]

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/addr/announced_by/0.0.0.0")

    assert response.status_code == 200
    assert "0.0.0.0" in app.state.storage.get.call_args[0]
    assert response.json()["result"] == None


def test_get_addr_announcement():
    # Mocks calls to storage
    app.state.storage.get = Mock(
        return_value={"2.58.60.0/22": {"announced_by": ["201813", "57916", "174"]}}
    )

    # Existent entry
    response = client.get("/addr/announcement/174")

    assert response.status_code == 200
    assert "174" in app.state.storage.get.call_args[0]
    assert response.json()["count"] == 1
    assert response.json()["result"] == {
        "2.58.60.0/22": {"announced_by": ["201813", "57916", "174"]}
    }

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/addr/announcement/-1")

    assert response.status_code == 200
    assert "-1" in app.state.storage.get.call_args[0]
    assert response.json()["result"] == None

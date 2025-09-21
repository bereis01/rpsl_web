from ... import context
from ...routers import rs
from fastapi import FastAPI
from unittest.mock import Mock
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
    # Mocks calls to storage
    app.state.storage.get_key = Mock(return_value=["rs-Level3-transit"])

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


def test_get_rs_attributes():
    # Mocks calls to storage
    app.state.storage.get = Mock(
        return_value={
            "descr": "Lorem Ipsum",
            "admin-c": "Lorem Ipsum",
            "tech-c": "Lorem Ipsum",
            "mnt-by": "Lorem Ipsum",
            "changed": "Lorem Ipsum",
            "source": "Lorem Ipsum",
        }
    )

    # Existent entry
    response = client.get("/rs/attributes/rs-peers")

    assert response.status_code == 200
    assert "rs-peers" in app.state.storage.get.call_args[0]
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] != None

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/rs/attributes/AS-CUSTOMERS")

    assert response.status_code == 200
    assert "AS-CUSTOMERS" in app.state.storage.get.call_args[0]
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


def test_get_rs_members():
    # Mocks calls to storage
    app.state.storage.get = Mock(
        return_value={
            "body": "Lorem Ipsum",
            "members": [
                {"type": "route_set", "name": "rs-Level3-transit-EU", "op": "NoOp"},
                {"type": "route_set", "name": "rs-Level3-transit-NA", "op": "NoOp"},
            ],
        }
    )

    # Existent entry
    response = client.get("/rs/members/rs-Level3-transit")

    assert response.status_code == 200
    assert "rs-Level3-transit" in app.state.storage.get.call_args[0]
    assert response.json()["result"] != None

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/rs/members/rs-no")

    assert response.status_code == 200
    assert "rs-no" in app.state.storage.get.call_args[0]
    assert response.json()["result"] == None

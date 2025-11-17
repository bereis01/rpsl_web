from ... import context
from ...routers import asn
from fastapi import FastAPI
from unittest.mock import Mock
from shared.storage import ObjStr
from fastapi.testclient import TestClient

# Initializes app
app = FastAPI()

# Initializes connection to storage
app.state.storage = ObjStr("../data/objects")

# Includes all routers
app.include_router(asn.router)

# Initializes test client
client = TestClient(app)


def test_check_asn_exists():
    # Mocks calls to storage
    app.state.storage.get_key = Mock(return_value=["174"])

    # Existent entry
    response = client.get("/asn/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == True

    # Non-existent entry
    response = client.get("/asn/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == False


def test_get_asn_attributes():
    # Mocks calls to storage
    app.state.storage.get = Mock(
        return_value={
            "as-name": "Lorem Ipsum",
            "descr": "Lorem Ipsum",
            "import": "Lorem Ipsum",
            "export": "Lorem Ipsum",
            "admin-c": "Lorem Ipsum",
            "tech-c": "Lorem Ipsum",
            "mnt-by": "Lorem Ipsum",
            "changed": "Lorem Ipsum",
            "source": "Lorem Ipsum",
        }
    )

    # Existent entry
    response = client.get("/asn/attributes/174")

    assert response.status_code == 200
    assert "174" in app.state.storage.get.call_args[0]
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] != None

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/asn/attributes/-1")

    assert response.status_code == 200
    assert "-1" in app.state.storage.get.call_args[0]
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


def test_get_asn_exchanged_objects():
    # Mocks calls to storage
    app.state.storage.get = Mock(return_value={"imports": ["Any"], "exports": ["Any"]})

    # Existent entry
    response = client.get("/asn/exchanged_objects/174")

    assert response.status_code == 200
    assert "174" in app.state.storage.get.call_args[0]
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] != None

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/asn/exchanged_objects/-1")

    assert response.status_code == 200
    assert "-1" in app.state.storage.get.call_args[0]
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


def test_get_asn_imports():
    # Mocks calls to storage
    app.state.storage.get = Mock(
        return_value=[
            {
                "version": "ipv4",
                "cast": "unicast",
                "peering": {
                    "remote_as": {"field": "Single", "type": "Any", "value": "Any"}
                },
                "actions": "None",
                "filter": {"type": "Any", "value": "Any"},
            }
        ]
    )

    # Existent entry
    response = client.get("/asn/imports/174")

    assert response.status_code == 200
    assert "174" in app.state.storage.get.call_args[0]
    assert response.json()["count"] == 1
    assert response.json()["result"] != None

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/asn/imports/-1")

    assert response.status_code == 200
    assert "-1" in app.state.storage.get.call_args[0]
    assert response.json()["count"] == 0
    assert response.json()["result"] == None


def test_get_asn_exports():
    # Mocks calls to storage
    app.state.storage.get = Mock(
        return_value=[
            {
                "version": "ipv4",
                "cast": "unicast",
                "peering": {
                    "remote_as": {"field": "Single", "type": "Any", "value": "Any"}
                },
                "actions": "None",
                "filter": {"type": "Any", "value": "Any"},
            }
        ]
    )

    # Existent entry
    response = client.get("/asn/exports/174")

    assert response.status_code == 200
    assert "174" in app.state.storage.get.call_args[0]
    assert response.json()["count"] == 1
    assert response.json()["result"] != None

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/asn/exports/-1")

    assert response.status_code == 200
    assert "-1" in app.state.storage.get.call_args[0]
    assert response.json()["count"] == 0
    assert response.json()["result"] == None


def test_get_asn_relationships():
    # Mocks calls to storage
    app.state.storage.get_key = Mock(return_value={})

    # Existent entry
    response = client.get("/asn/relationships/174")

    assert response.status_code == 200
    assert response.json()["result"] != None

    # Mocks calls to storage
    app.state.storage.get_key = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/asn/relationships/-1")

    assert response.status_code == 200
    assert response.json()["result"] == None

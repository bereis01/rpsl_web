from ... import context
from fastapi import FastAPI
from ...routers import asset
from unittest.mock import Mock
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
    # Mocks calls to storage
    app.state.storage.get_key = Mock(return_value=["AS-CUSTOMERS"])

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


def test_get_asset_attributes():
    # Mocks calls to storage
    app.state.storage.get = Mock(
        return_value={
            "descr": "Lorem Ipsum",
            "org": "Lorem Ipsum",
            "admin-c": "Lorem Ipsum",
            "tech-c": "Lorem Ipsum",
            "mnt-by": "Lorem Ipsum",
            "changed": "Lorem Ipsum",
            "source": "Lorem Ipsum",
        }
    )

    # Existent entry
    response = client.get("/asset/attributes/AS-CUSTOMERS")

    assert response.status_code == 200
    assert "AS-CUSTOMERS" in app.state.storage.get.call_args[0]
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] != None

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/asset/attributes/RS-ROUTES")

    assert response.status_code == 200
    assert "RS-ROUTES" in app.state.storage.get.call_args[0]
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


def test_get_asset_members():
    # Mocks calls to storage
    app.state.storage.get = Mock(
        return_value={
            "body": "Lorem Ipsum",
            "members": [],
            "set_members": [],
            "is_any": False,
        }
    )

    # Existent entry
    response = client.get("/asset/members/AS-CUSTOMERS")

    assert response.status_code == 200
    assert "AS-CUSTOMERS" in app.state.storage.get.call_args[0]
    assert response.json()["result"] != None

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/asset/members/AS-NOTCUSTOMERS")

    assert response.status_code == 200
    assert "AS-NOTCUSTOMERS" in app.state.storage.get.call_args[0]
    assert response.json()["result"] == None


def test_get_asset_membership():
    # Mocks calls to storage
    app.state.storage.get = Mock(
        return_value={
            "as-example-test": {
                "body": "Lorem Ipsum",
                "members": ["174", "194", "15169", "64400"],
                "set_members": [],
                "is_any": False,
            }
        }
    )

    # Existent entry
    response = client.get("/asset/membership/174")

    assert response.status_code == 200
    assert "174" in app.state.storage.get.call_args[0]
    assert response.json()["count"] == 1
    assert response.json()["result"] != None

    # Mocks calls to storage
    app.state.storage.get = Mock(return_value=None)

    # Non-existent entry
    response = client.get("/asset/membership/-1")

    assert response.status_code == 200
    assert "-1" in app.state.storage.get.call_args[0]
    assert response.json()["result"] == None

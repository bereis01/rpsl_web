from ... import context
from ...routers import asn
from fastapi import FastAPI
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
    # Existent entry
    response = client.get("/asn/attributes/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/asn/attributes/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


def test_get_asn_exchanged_objects():
    # Existent entry
    response = client.get("/asn/exchanged_objects/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/asn/exchanged_objects/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


def test_get_asn_imports():
    # Existent entry
    response = client.get("/asn/imports/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["count", "skip", "limit", "result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/asn/imports/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


def test_get_asn_exports():
    # Existent entry
    response = client.get("/asn/exports/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["count", "skip", "limit", "result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/asn/exports/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


def test_get_asn_summary():
    # Existent entry
    response = client.get("/asn/summary/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/asn/summary/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


def test_get_asn_tor():
    # Existent entry
    response = client.get("/asn/tor/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["count", "skip", "limit", "result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/asn/tor/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None

from ...routers import asn
from storage import ObjStr
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Initializes app
app = FastAPI()

# Initializes connection to storage
app.state.storage = ObjStr("./data/")

# Includes all routers
app.include_router(asn.router)

# Initializes test client
client = TestClient(app)


def test_get_asn():
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


def test_get_asn_aut_num():
    # Existent entry
    response = client.get("/asn/aut_num/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/asn/aut_num/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


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


def test_get_asn_membership():
    # Existent entry
    response = client.get("/asn/membership/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["count", "skip", "limit", "result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/asn/membership/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None


def test_get_asn_announcement():
    # Existent entry
    response = client.get("/asn/announcement/174")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["count", "skip", "limit", "result"]
    assert response.json()["result"] != None

    # Non-existent entry
    response = client.get("/asn/announcement/-1")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]
    assert response.json()["result"] == None

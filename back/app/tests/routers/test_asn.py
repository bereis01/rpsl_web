from ...routers import asn
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Initializes app
app = FastAPI()

# Includes all routers
app.include_router(asn.router)

# Initializes test client
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"msg": "Hello World"}

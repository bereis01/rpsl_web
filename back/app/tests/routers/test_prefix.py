from ...routers import prefix
from fastapi import FastAPI
from fastapi.testclient import TestClient

# Initializes app
app = FastAPI()

# Includes all routers
app.include_router(prefix.router)

# Initializes test client
client = TestClient(app)


def test_get_prefix_announced_by():
    response = client.get("/prefix/announced_by/0")

    assert response.status_code == 200
    assert list(response.json().keys()) == ["result"]

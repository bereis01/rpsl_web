import os
import requests

ENDPOINT_ROOT = f"http://{os.getenv("ENDPOINT_ROOT")}:8000/"


def get(route: str):
    return requests.get(ENDPOINT_ROOT + route)

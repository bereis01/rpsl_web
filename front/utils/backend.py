import requests

ROOT = "http://localhost:8000/"


def get(route: str):
    return requests.get(ROOT + route)

import requests

ROOT = "http://fastapi:8000/"


def get(route: str):
    return requests.get(ROOT + route)

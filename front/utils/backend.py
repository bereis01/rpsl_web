import requests

ROOT = "http://127.0.0.1:8000/"


def get(route: str):
    return requests.get(ROOT + route)

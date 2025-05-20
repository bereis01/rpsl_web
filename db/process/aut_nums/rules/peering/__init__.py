from .remote_as import process_remote_as
from .router import process_router


def process_peering(peering):
    processed_peering = {}

    # Processes each key ['remote_as', 'remote_router', 'local_router']
    for key in peering.keys():
        match key:
            case "remote_as":
                processed_peering[key] = process_remote_as(peering[key])
            case "remote_router":
                processed_peering[key] = process_router(peering[key])
            case "local_router":
                processed_peering[key] = process_router(peering[key])

    return processed_peering

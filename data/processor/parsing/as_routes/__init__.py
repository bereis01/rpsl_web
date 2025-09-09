from .announcement import process_announcement
from .inverted import process_as_routes_inverted


def process_as_routes(as_routes, storage):
    # Encapsulates the value into a dedicated object
    as_routes = {k: {"routes": v} for k, v in as_routes.items()}

    # Processes inverted version
    as_routes_inverted = process_as_routes_inverted(as_routes)
    prefixes = list(as_routes_inverted.keys())
    announcement = process_announcement(as_routes, as_routes_inverted)

    # Persists results
    storage.set_key("metadata", "addr_prefixes", prefixes)
    del prefixes
    storage.set("addr-announces", as_routes)
    del as_routes
    storage.set("addr-announced_by", as_routes_inverted)
    del as_routes_inverted
    storage.set("addr-announcement", announcement)
    del announcement

from .announcement import process_announcement
from .announced_by import process_announced_by


def process_as_routes(as_routes, storage):
    # Encapsulates the value into a dedicated object
    as_routes = {k: {"routes": v} for k, v in as_routes.items()}

    # Processes inverted version
    addr_prefixes = list(as_routes_inverted.keys())
    announced_by = process_announced_by(as_routes)
    announcement = process_announcement(as_routes, as_routes_inverted)

    # Persists results
    storage.set_key("metadata", "addr_prefixes", addr_prefixes)
    del prefixes
    storage.set("addr-announces", as_routes)
    del as_routes
    storage.set("addr-announced_by", announced_by)
    del as_routes_inverted
    storage.set("addr-announcement", announcement)
    del announcement

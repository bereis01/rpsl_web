from .announcement import process_announcement
from .announced_by import process_announced_by


def process_as_routes(as_routes, storage):
    # Encapsulates the value into a dedicated object
    as_routes = {k: {"routes": v} for k, v in as_routes.items()}

    # Processes inverted version
    announced_by = process_announced_by(as_routes)
    addr_prefixes = list(announced_by.keys())
    announcement = process_announcement(as_routes, announced_by)

    # Persists results
    storage.set_key("metadata", "addr_prefixes", addr_prefixes)
    del addr_prefixes
    storage.set("addr-announces", as_routes)
    del as_routes
    storage.set("addr-announced_by", announced_by)
    del announced_by
    storage.set("addr-announcement", announcement)
    del announcement

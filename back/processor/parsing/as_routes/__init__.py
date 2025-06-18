from storage import ObjStr
from .announcement import process_announcement
from .inverted import process_as_routes_inverted


def process_as_routes(as_routes, output_path="./"):
    # Instantiates storage connection
    storage = ObjStr(output_path)

    # Encapsulates the value into a dedicated object
    as_routes = {k: {"routes": v} for k, v in as_routes.items()}

    # Processes inverted version
    as_routes_inverted = process_as_routes_inverted(as_routes)
    prefixes = list(as_routes_inverted.keys())
    announcement = process_announcement(as_routes, as_routes_inverted)

    # Persists results
    storage.set_key("metadata", "prefixes", prefixes)
    del prefixes
    storage.set("as_routes", as_routes)
    del as_routes
    storage.set("as_routes_inverted", as_routes_inverted)
    del as_routes_inverted
    storage.set("announcement", announcement)
    del announcement

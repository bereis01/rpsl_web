import pickle
from .announcement import process_announcement
from .inverted import process_as_routes_inverted


def process_as_routes(as_routes, output_path="./"):
    # Encapsulates the value into a dedicated object
    as_routes = {k: {"routes": v} for k, v in as_routes.items()}

    # Processes inverted version
    as_routes_inverted = process_as_routes_inverted(as_routes)
    announcement = process_announcement(as_routes, as_routes_inverted)

    # Writes the dictionary to a bucket
    as_routes_output = open(output_path + "as_routes", "wb")
    pickle.dump(as_routes, as_routes_output)
    as_routes_output.close()
    del as_routes

    # Writes as_routes_inverted to a bucket
    as_routes_inverted_output = open(output_path + "as_routes_inverted", "wb")
    pickle.dump(as_routes_inverted, as_routes_inverted_output)
    as_routes_inverted_output.close()
    del as_routes_inverted

    # Writes announcement to a bucket
    announcement_output = open(output_path + "announcement", "wb")
    pickle.dump(announcement, announcement_output)
    announcement_output.close()
    del announcement_output

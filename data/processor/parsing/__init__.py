from .aut_nums import process_aut_nums
from .as_sets import process_as_sets
from .route_sets import process_route_sets
from .peering_sets import process_peering_sets
from .filter_sets import process_filter_sets
from .as_routes import process_as_routes


def process(key: str, data, storage):
    match key:
        case "aut_nums":
            process_aut_nums(data, storage)
        case "as_sets":
            process_as_sets(data, storage)
        case "route_sets":
            process_route_sets(data, storage)
        case "peering_sets":
            process_peering_sets(data, storage)
        case "filter_sets":
            process_filter_sets(data, storage)
        case "as_routes":
            process_as_routes(data, storage)

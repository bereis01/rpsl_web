from .symmetry import check_symmetry
from .categorize import categorize_relationship_complexity
from .import_export_heuristic import import_export_heuristic


def process_relationships(storage, as_nums, imports, exports):
    relationships = {}

    # Executes heuristics to retrieve types of possible relationships
    for asn in as_nums:
        relationships[asn] = import_export_heuristic(asn, imports[asn], exports[asn])
    relationships = check_symmetry(relationships)

    # Stores found relationships
    storage.set("relationships", relationships)

    # Further categorize them based on complexity
    simple_customer, simple_provider, complex = categorize_relationship_complexity(
        relationships
    )

    # Stores broke down relationships
    storage.set("relationships_simple_customer", simple_customer)
    storage.set("relationships_simple_provider", simple_provider)
    storage.set("relationships_complex", complex)

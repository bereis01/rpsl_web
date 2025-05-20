from .peering import process_peering
from .filter import process_filter
from .actions import *


def process_rules(rules):
    processed_rules = []

    # Flattens a cascated dictionary
    for version in rules.keys():
        for cast in rules[version].keys():
            for import_statement in rules[version][cast]:
                for peering in import_statement["mp_peerings"]:
                    processed_rules.append(
                        {
                            "version": version,
                            "cast": cast,
                            "peering": process_peering(peering["mp_peering"]),
                            "actions": (
                                peering["actions"]
                                if "actions" in peering.keys()
                                else None
                            ),
                            "filter": process_filter(import_statement["mp_filter"]),
                        }
                    )

    return processed_rules

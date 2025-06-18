def import_export_heuristic(asn, imports, exports):
    # Removes invariants
    processed_imports = []
    for import_rule in imports:
        processed_import_rule = {key: import_rule[key] for key in ["peering", "filter"]}
        if processed_import_rule not in processed_imports:
            processed_imports.append(processed_import_rule)

    processed_exports = []
    for export_rule in exports:
        processed_export_rule = {key: export_rule[key] for key in ["peering", "filter"]}
        if processed_export_rule not in processed_exports:
            processed_exports.append(processed_export_rule)

    # Creates a pairing list with import/export rules refering to the same peer
    pairs = []
    for import_rule in processed_imports:
        for export_rule in processed_exports:
            if (
                import_rule["peering"]["remote_as"]
                == export_rule["peering"]["remote_as"]
            ):
                pair = (import_rule["peering"]["remote_as"], import_rule, export_rule)
                pairs.append(pair)

    # Processes each pair following Zulan's et al import/export heuristic
    tors = []
    for peer, import_rule, export_rule in pairs:
        # Customer relationship with peer
        if (
            (
                peer["field"] == "Single" and peer["type"] == "Num"
            )  # If peer is an AS number
            and (
                import_rule["filter"]["type"] == "Any"
                and import_rule["filter"]["value"] == "Any"
            )  # If imports any route
            and (export_rule["filter"]["type"] in ["AsNum", "AsSet", "RouteSet"])
        ):  # If exports specified ASes
            tor = {
                "asn": asn,
                "peer": peer,
                "tor": "Customer",
                "import": import_rule,
                "export": export_rule,
            }
            tors.append(tor)

        # Provider relationship with peer
        elif (
            (
                peer["field"] == "Single" and peer["type"] == "Num"
            )  # If peer is an AS number
            and (
                import_rule["filter"]["type"] in ["AsNum", "AsSet", "RouteSet"]
            )  # If imports specified ASes
            and (
                export_rule["filter"]["type"] == "Any"
                and export_rule["filter"]["value"] == "Any"
            )
        ):  # If exports any route
            tor = {
                "asn": asn,
                "peer": peer,
                "tor": "Provider",
                "import": import_rule,
                "export": export_rule,
            }
            tors.append(tor)

        # Peer relationship with peer
        elif (
            (
                peer["field"] == "Single" and peer["type"] == "Num"
            )  # If peer is an AS number
            and (
                import_rule["filter"]["type"] in ["AsNum", "AsSet", "RouteSet"]
            )  # If imports specified ASes
            and (export_rule["filter"]["type"] in ["AsNum", "AsSet", "RouteSet"])
        ):  # If exports specified ASes
            tor = {
                "asn": asn,
                "peer": peer,
                "tor": "Peer",
                "import": import_rule,
                "export": export_rule,
            }
            tors.append(tor)

    return tors

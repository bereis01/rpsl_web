def import_export_heuristic(asn, imports, exports):
    # Creates a pairing list with import/export rules refering to the same peer
    pairs = []
    for import_rule in imports:
        for export_rule in exports:
            if (
                import_rule["peering"]["remote_as"]
                == export_rule["peering"]["remote_as"]
            ):
                pairs.append((import_rule["peering"], import_rule, export_rule))

    # Processes each pair following Zulan's et al import/export heuristic
    tors = []
    for peer, import_rule, export_rule in pairs:
        # Customer relationship with peer
        if (
            (
                peer["remote_as"]["field"] == "Single"
                and peer["remote_as"]["type"] == "Num"
            )  # If peer is an AS number
            and (
                import_rule["filter"]["type"] == "Any"
                and import_rule["filter"]["value"] == "Any"
            )  # If imports any route
            and (export_rule["filter"]["type"] in ["AsNum", "AsSet"])
        ):  # If exports specified ASes
            tors.append(
                {
                    "asn": asn,
                    "peer": peer,
                    "tor": "Customer",
                    "import": import_rule,
                    "export": export_rule,
                }
            )

        # Provider relationship with peer
        elif (
            (
                peer["remote_as"]["field"] == "Single"
                and peer["remote_as"]["type"] == "Num"
            )  # If peer is an AS number
            and (
                import_rule["filter"]["type"] in ["AsNum", "AsSet"]
            )  # If imports specified ASes
            and (
                export_rule["filter"]["type"] == "Any"
                and export_rule["filter"]["value"] == "Any"
            )
        ):  # If exports any route
            tors.append(
                {
                    "asn": asn,
                    "peer": peer,
                    "tor": "Provider",
                    "import": import_rule,
                    "export": export_rule,
                }
            )

        # Peer relationship with peer
        elif (
            (
                peer["remote_as"]["field"] == "Single"
                and peer["remote_as"]["type"] == "Num"
            )  # If peer is an AS number
            and (
                import_rule["filter"]["type"] in ["AsNum", "AsSet"]
            )  # If imports specified ASes
            and (export_rule["filter"]["type"] in ["AsNum", "AsSet"])
        ):  # If exports specified ASes
            tors.append(
                {
                    "asn": asn,
                    "peer": peer,
                    "tor": "Peer",
                    "import": import_rule,
                    "export": export_rule,
                }
            )

    return tors

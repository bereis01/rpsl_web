def process_members(members):
    # Processes each member of each route set
    processed_members = []
    for member in members:

        if list(member.keys())[0] == "NameOp":
            # Processes other route_set members
            if (member["NameOp"][0][0:3].lower() == "rs-") or (
                member["NameOp"][0][0:5].lower() == "m#rs-"
            ):
                processed_members.append(
                    {
                        "type": "route_set",
                        "name": member["NameOp"][0],
                        "op": member["NameOp"][1],
                    }
                )

            # Processes AS or AS set members
            else:
                processed_members.append(
                    {
                        "type": "AS",
                        "name": member["NameOp"][0],
                        "op": member["NameOp"][1],
                    }
                )

        # Processes address prefix members
        elif list(member.keys())[0] == "RSRange":
            processed_members.append(
                {
                    "type": "address",
                    "address_prefix": member["RSRange"]["address_prefix"],
                    "range_operator": member["RSRange"]["range_operator"],
                }
            )

    return processed_members

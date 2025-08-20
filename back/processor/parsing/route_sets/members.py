def process_members(members):
    # Processes each member of each route set
    processed_members = []
    for member in members:
        # Processes AS or AS set members
        if list(member.keys())[0] == "NameOp":
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

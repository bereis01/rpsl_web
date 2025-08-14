def process_body(body: str):
    # Splits into individual lines
    # Each one corresponds to a certain attribute
    attributes = body.split("\n")

    # Converts the attribute lines into a dict
    result = {}
    last_key = None
    for attribute in attributes:
        # Skips blank lines
        if attribute == "":
            continue

        # If starts with blank, pertains to last line
        if last_key != None and attribute[0] in [" ", "\t", "+"]:
            result[last_key] += "\n" + attribute[1:]
            continue

        attribute = attribute.split(":", maxsplit=1)

        # Catches weird situations
        if len(attribute) == 1:
            continue

        key, value = attribute
        result[key] = (
            value.strip() if key != last_key else result[key] + "\n" + value.strip()
        )  # Appends if the key is the same
        last_key = key

    return result

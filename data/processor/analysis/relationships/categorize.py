def categorize_relationship_complexity(relationships):
    simple_customer = {k: [] for k in relationships.keys()}
    simple_provider = {k: [] for k in relationships.keys()}
    complex_relationships = {k: [] for k in relationships.keys()}

    keys = list(relationships.keys())
    for asn in keys:
        tors = relationships.pop(asn)
        for tor in tors:
            # Simple relationship in which exports itself as customer
            if (
                (
                    tor["peer"]["field"] == "Single" and tor["peer"]["type"] == "Num"
                )  # It is an AS
                and (tor["tor"] == "Customer")  # It is a customer
                and (
                    tor["export"]["filter"]["value"] == tor["asn"]
                )  # It exports itself
            ):
                simple_customer[asn].append(tor["peer"]["value"])
            # Simple relationship in which imports the other AS as its provider
            elif (
                (
                    tor["peer"]["field"] == "Single" and tor["peer"]["type"] == "Num"
                )  # It is an AS
                and (tor["tor"] == "Provider")  # It is a provider
                and (
                    tor["import"]["filter"]["value"] == tor["peer"]["value"]
                )  # It imports itself
            ):
                simple_provider[asn].append(tor["peer"]["value"])
            # The rest is classified as 'complex'
            else:
                complex_relationships[asn].append(tor)
        simple_customer[asn] = list(set(simple_customer[asn]))
        simple_provider[asn] = list(set(simple_provider[asn]))
    return simple_customer, simple_provider, complex_relationships

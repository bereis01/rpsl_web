def check_symmetry(relationships):
    for asn in relationships.keys():

        # Traverses the relationships of each asn
        for relationship in relationships[asn]:
            relationship["sym"] = False

            # Relationship info
            tor = relationship["tor"]
            peer_asn = relationship["peer"]["value"]
            if peer_asn not in relationships.keys():
                continue  # Ignores in case there's no info about the peer
            peer_relationships = relationships[peer_asn]

            # Traverses the relationships of its peer
            for peer_relationship in peer_relationships:
                peer_tor = peer_relationship["tor"]

                # It it is symmetric, changes the value
                if (peer_relationship["peer"]["value"] == asn) and (
                    (tor == "Provider" and peer_tor == "Customer")
                    or (tor == "Customer" and peer_tor == "Provider")
                    or (tor == "Peer" and peer_tor == "Peer")
                ):
                    relationship["sym"] = True
                    break

    return relationships

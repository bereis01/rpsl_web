from ....analysis.relationships import categorize_relationship_complexity


simple_relationships = {
    "395127": [
        {
            "asn": "395127",
            "peer": {"field": "Single", "type": "Num", "value": "174"},
            "tor": "Customer",
            "import": {
                "peering": {
                    "remote_as": {"field": "Single", "type": "Num", "value": "174"}
                },
                "filter": {"type": "Any", "value": "Any"},
            },
            "export": {
                "peering": {
                    "remote_as": {"field": "Single", "type": "Num", "value": "174"}
                },
                "filter": {"type": "AsNum", "value": "395127", "op": "NoOp"},
            },
        },
        {
            "asn": "395127",
            "peer": {"field": "Single", "type": "Num", "value": "577"},
            "tor": "Provider",
            "import": {
                "peering": {
                    "remote_as": {"field": "Single", "type": "Num", "value": "577"}
                },
                "filter": {"type": "AsNum", "value": "577", "op": "NoOp"},
            },
            "export": {
                "peering": {
                    "remote_as": {"field": "Single", "type": "Num", "value": "577"}
                },
                "filter": {"type": "Any", "value": "Any"},
            },
        },
    ]
}


def test_categorize_relationships_by_complexity():
    keys = list(simple_relationships.keys())

    simple_customer, simple_provider, complex = categorize_relationship_complexity(
        simple_relationships
    )

    assert keys == list(simple_customer.keys())
    assert keys == list(simple_provider.keys())
    assert keys == list(complex.keys())

    assert simple_customer[keys[0]] == ["174"]
    assert simple_provider[keys[0]] == ["577"]
    assert complex[keys[0]] == []

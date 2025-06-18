from ....analysis.relationships import check_symmetry


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
    ],
    "174": [
        {
            "asn": "174",
            "peer": {"field": "Single", "type": "Num", "value": "395127"},
            "tor": "Provider",
            "import": {
                "peering": {
                    "remote_as": {"field": "Single", "type": "Num", "value": "395127"}
                },
                "filter": {"type": "AsNum", "value": "577", "op": "NoOp"},
            },
            "export": {
                "peering": {
                    "remote_as": {"field": "Single", "type": "Num", "value": "577"}
                },
                "filter": {"type": "Any", "value": "Any"},
            },
        }
    ],
}


def test_check_symmetry():
    simple_relationships = check_symmetry(simple_relationships)

    assert simple_relationships["395127"][0]["sym"] == True
    assert simple_relationships["395127"][1]["sym"] == False
    assert simple_relationships["174"][0]["sym"] == True

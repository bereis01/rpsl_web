from ....analysis.relationships import import_export_heuristic


asn = "395127"
imports = [
    {
        "version": "ipv4",
        "cast": "unicast",
        "peering": {"remote_as": {"field": "Single", "type": "Num", "value": "174"}},
        "actions": "None",
        "filter": {"type": "Any", "value": "Any"},
    },
    {
        "version": "ipv4",
        "cast": "unicast",
        "peering": {"remote_as": {"field": "Single", "type": "Num", "value": "577"}},
        "actions": "None",
        "filter": {"type": "AsNum", "value": "395127", "op": "NoOp"},
    },
]
exports = [
    {
        "version": "ipv4",
        "cast": "unicast",
        "peering": {"remote_as": {"field": "Single", "type": "Num", "value": "174"}},
        "actions": "None",
        "filter": {"type": "AsNum", "value": "395127", "op": "NoOp"},
    },
    {
        "version": "ipv4",
        "cast": "unicast",
        "peering": {"remote_as": {"field": "Single", "type": "Num", "value": "577"}},
        "actions": "None",
        "filter": {"type": "Any", "value": "Any"},
    },
]


def test_import_export_heuristic():
    result_simple = import_export_heuristic(asn, imports, exports)

    assert len(result_simple) == 2
    assert result_simple[0]["tor"] == "Customer"
    assert result_simple[1]["tor"] == "Provider"

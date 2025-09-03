from ....parsing.route_sets.members import process_members

route_set_members_example = [
    {
        "RSRange": {
            "address_prefix": "192.216.36.0/24",
            "range_operator": "NoOp",
        }
    },
    {"NameOp": ["AS19653:RS-ARIN", "NoOp"]},
    {"NameOp": ["rs-pingdash-v6-48", "NoOp"]},
    {"NameOp": ["RS-pingdash-v6-48", "NoOp"]},
]


def test_process_members():
    result = process_members(route_set_members_example)

    assert len(result) == 4
    assert result[0]["type"] == "address"
    assert result[1]["type"] == "AS"
    assert result[2]["type"] == "route_set"
    assert result[3]["type"] == "route_set"

from ....parsing.aut_nums.exchanged_objects import process_exchanged_objects

rules_example = [
    {
        "version": "ipv4",
        "cast": "unicast",
        "peering": {"remote_as": {"field": "Single", "type": "Num", "value": "26677"}},
        "actions": "None",
        "filter": {"type": "Any", "value": "Any"},
    },
    {
        "version": "ipv4",
        "cast": "unicast",
        "peering": {"remote_as": {"field": "Single", "type": "Num", "value": "3257"}},
        "actions": "None",
        "filter": {
            "type": "And",
            "left": {"type": "Any", "value": "Any"},
            "right": {
                "type": "Not",
                "value": {
                    "type": "AddrPrefixSet",
                    "value": [
                        {"address_prefix": "0.0.0.0/0", "range_operator": "NoOp"}
                    ],
                },
            },
        },
    },
    {
        "version": "ipv4",
        "cast": "unicast",
        "peering": {
            "remote_as": {
                "field": "Single",
                "type": "Set",
                "value": "AS266009:AS-CUSTOMERS",
            }
        },
        "actions": "None",
        "filter": {"type": "AsSet", "value": "AS266009:AS-CUSTOMERS", "op": "NoOp"},
    },
    {
        "version": "ipv4",
        "cast": "unicast",
        "peering": {
            "remote_as": {
                "field": "Single",
                "type": "Set",
                "value": "AS266009:AS-CUSTOMERS",
            }
        },
        "actions": "None",
        "filter": {"type": "AsSet", "value": "AS266009:AS-CUSTOMERS", "op": "NoOp"},
    },
]


def test_process_exchanged_objects():
    result = process_exchanged_objects(rules_example)

    assert len(result.keys()) == 2
    assert list(result.keys())[0] == "AS266009:AS-CUSTOMERS"
    assert list(result.keys())[1] == "Any"

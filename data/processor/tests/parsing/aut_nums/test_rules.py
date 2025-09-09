from ....parsing.aut_nums.rules import process_rules

imports_example = {
    "ipv4": {
        "unicast": [
            {
                "mp_peerings": [
                    {
                        "mp_peering": {"remote_as": {"Single": {"Num": 6939}}},
                        "actions": {"pref": "100"},
                    }
                ],
                "mp_filter": "Any",
            },
            {
                "mp_peerings": [
                    {
                        "mp_peering": {"remote_as": {"Single": {"Num": 55101}}},
                        "actions": {"pref": "300"},
                    }
                ],
                "mp_filter": {"AsNum": [55101, "NoOp"]},
            },
        ]
    },
    "ipv6": {
        "unicast": [
            {
                "mp_peerings": [
                    {
                        "mp_peering": {"remote_as": {"Single": {"Num": 6939}}},
                        "actions": {"pref": "100"},
                    }
                ],
                "mp_filter": "Any",
            },
            {
                "mp_peerings": [
                    {
                        "mp_peering": {"remote_as": {"Single": {"Num": 55101}}},
                        "actions": {"pref": "300"},
                    }
                ],
                "mp_filter": {"AsNum": [55101, "NoOp"]},
            },
        ]
    },
}

exports_example = {
    "ipv4": {
        "unicast": [
            {
                "mp_peerings": [{"mp_peering": {"remote_as": {"Single": "Any"}}}],
                "mp_filter": {
                    "And": {
                        "left": {"AsSet": ["AS-DAC-PEERS", "NoOp"]},
                        "right": {
                            "Not": {
                                "AddrPrefixSet": [
                                    {
                                        "address_prefix": "0.0.0.0/0",
                                        "range_operator": "NoOp",
                                    }
                                ]
                            }
                        },
                    }
                },
            }
        ]
    }
}


def test_process_rules():
    result_imports = process_rules(imports_example)

    assert len(result_imports) == 4
    assert list(result_imports[0].keys()) == [
        "version",
        "cast",
        "peering",
        "actions",
        "filter",
    ]

    result_exports = process_rules(exports_example)

    assert len(result_exports) == 1
    assert list(result_exports[0].keys()) == [
        "version",
        "cast",
        "peering",
        "actions",
        "filter",
    ]

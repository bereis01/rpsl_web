from ...aut_nums.rules.filter import process_filter


filter_simple = {"AsNum": [123, "NoOp"]}
filter_complex = {
    "And": {
        "left": "Any",
        "right": {
            "Not": {
                "AddrPrefixSet": [
                    {"address_prefix": "0.0.0.0/0", "range_operator": "NoOp"}
                ]
            }
        },
    }
}


def test_process_filter():
    result_simple = process_filter(filter_simple)

    assert result_simple == {"type": "AsNum", "value": 123, "op": "NoOp"}

    result_complex = process_filter(filter_complex)
    assert list(result_complex.keys()) == ["type", "left", "right"]

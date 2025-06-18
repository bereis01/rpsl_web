from ....parsing.as_sets.membership import process_as_set_membership


as_sets_simple = {
    "m#as-xipe1#SBMT": {
        "body": "",
        "members": ["204617"],
        "set_members": [],
        "is_any": False,
    }
}

as_sets_inverted_simple = {"204617": ["m#as-xipe1#SBMT"]}


def test_process_as_set_membership():
    result_simple = process_as_set_membership(as_sets_simple, as_sets_inverted_simple)

    assert result_simple == {
        "204617": {
            "m#as-xipe1#SBMT": {
                "body": "",
                "members": ["204617"],
                "set_members": [],
                "is_any": False,
            }
        }
    }

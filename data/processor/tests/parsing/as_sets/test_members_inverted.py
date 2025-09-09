from ....parsing.as_sets.members_inverted import process_members_inverted


as_sets_simple = {
    "m#as-xipe1#SBMT": {
        "body": "",
        "members": ["204617"],
        "set_members": [],
        "is_any": False,
    }
}


def test_process_members_inverted():
    result_simple = process_members_inverted(as_sets_simple)

    assert result_simple == {"204617": ["m#as-xipe1#SBMT"]}

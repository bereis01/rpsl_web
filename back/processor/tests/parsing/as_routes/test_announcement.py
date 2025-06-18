from ....parsing.as_routes.announcement import process_announcement


as_routes_simple = {"397898": {"routes": ["67.159.203.0/24", "2602:fccd::/36"]}}
as_routes_inverted_simple = {
    "67.159.203.0/24": {"announced_by": ["397898"]},
    "2602:fccd::/36": {"announced_by": ["397898"]},
}


def test_process_as_routes_inverted():
    result_simple = process_announcement(as_routes_simple, as_routes_inverted_simple)

    assert result_simple == {
        "397898": {
            "67.159.203.0/24": {"announced_by": ["397898"]},
            "2602:fccd::/36": {"announced_by": ["397898"]},
        }
    }

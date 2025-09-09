from ....parsing.as_routes.announced_by import process_announced_by


as_routes_simple = {"397898": {"routes": ["67.159.203.0/24", "2602:fccd::/36"]}}


def test_process_announced_by():
    result_simple = process_announced_by(as_routes_simple)

    assert len(result_simple) == 2
    assert result_simple == {
        "67.159.203.0/24": {"announced_by": ["397898"]},
        "2602:fccd::/36": {"announced_by": ["397898"]},
    }

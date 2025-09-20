from ...cleaning import match


def test_match_as_num():
    valid_input = "aS83912"
    invalid_input = "AS-8312a"

    assert match.match_as_num(valid_input) == True
    assert match.match_as_num(invalid_input) == False


def test_match_rpsl_name():
    valid_input = "Valid-name_123"
    invalid_input = "123-invalid-name-"

    assert match.match_rpsl_name(valid_input) == True
    assert match.match_rpsl_name(invalid_input) == False


def test_match_single_as_set_name():
    valid_input = "as-Valid-name_123"
    invalid_input = "123-invalid-name-"

    assert match.match_single_as_set_name(valid_input) == True
    assert match.match_single_as_set_name(invalid_input) == False


def test_match_as_set_name():
    valid_input = "AS123:AS-Set"
    invalid_input = "123:-invalid-name-"

    assert match.match_as_set_name(valid_input) == True
    assert match.match_as_set_name(invalid_input) == False


def test_match_single_route_set_name():
    valid_input = "rs-Valid-name_123"
    invalid_input = "123-invalid-name-"

    assert match.match_single_route_set_name(valid_input) == True
    assert match.match_single_route_set_name(invalid_input) == False


def test_match_route_set_name():
    valid_input = "AS123:rs-Set"
    invalid_input = "123:-invalid-name-"

    assert match.match_route_set_name(valid_input) == True
    assert match.match_route_set_name(invalid_input) == False


def test_match_ipv4_address():
    valid_input = "123.456.2.23/16"
    invalid_input = "123.4526.789.123/163"

    assert match.match_ipv4_address(valid_input) == True
    assert match.match_ipv4_address(invalid_input) == False


def test_match_ipv6_address():
    valid_input = "1234:abcd:2:23::/16"
    invalid_input = "12345:abch:2:23::/163"

    assert match.match_ipv6_address(valid_input) == True
    assert match.match_ipv6_address(invalid_input) == False

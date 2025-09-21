from utils.regex import process_query

asn_1 = "738129"
asn_2 = "AS:123"
asn_3 = "   aSn- 8321  "


def test_process_query_asn():
    result_1 = process_query(asn_1)

    assert result_1[0] == "asn"
    assert result_1[1] == "738129"

    result_2 = process_query(asn_2)

    assert result_2[0] == "asn"
    assert result_2[1] == "123"

    result_3 = process_query(asn_3)

    assert result_3[0] == "asn"
    assert result_3[1] == "8321"


as_set_1 = "tHiSISaTeSt;-0"
as_set_2 = "AS_SET:123"
as_set_3 = "a_____0"


def test_process_query_asset():
    result_1 = process_query(as_set_1)

    assert result_1[0] == "asset"
    assert result_1[1] == "tHiSISaTeSt;-0"

    result_2 = process_query(as_set_2)

    assert result_2[0] == "asset"
    assert result_2[1] == "AS_SET:123"

    result_3 = process_query(as_set_3)

    assert result_3[0] == "asset"
    assert result_3[1] == "a_____0"


prefix_1 = "255.255.255.255"
prefix_2 = "0.0.0.0"
prefix_3 = "192.168.0.1/12"


def test_process_query_prefix():
    result_1 = process_query(prefix_1)

    assert result_1[0] == "addr"
    assert result_1[1] == "255.255.255.255"

    result_2 = process_query(prefix_2)

    assert result_2[0] == "addr"
    assert result_2[1] == "0.0.0.0"

    result_3 = process_query(prefix_3)

    assert result_3[0] == "addr"
    assert result_3[1] == "192.168.0.1\\12"


route_set_1 = "rs-aaaaa9"
route_set_2 = "RS-123A"
route_set_3 = "rS-dmksa;_1"


def test_process_query_route_set():
    result_1 = process_query(route_set_1)

    assert result_1[0] == "rs"
    assert result_1[1] == "rs-aaaaa9"

    result_2 = process_query(route_set_2)

    assert result_2[0] == "rs"
    assert result_2[1] == "RS-123A"

    result_3 = process_query(route_set_3)

    assert result_3[0] == "rs"
    assert result_3[1] == "rS-dmksa;_1"


invalid_asn = "12389AS"
invalid_as_set = "123AS-SET:12A"
invalid_prefix = "1928.3281.2391.3921"
invalid_route_set = "rs-;"


def test_process_query_invalid():
    result_1 = process_query(invalid_asn)

    assert result_1[0] == "invalid"
    assert result_1[1] == None

    result_2 = process_query(invalid_as_set)

    assert result_2[0] == "invalid"
    assert result_2[1] == None

    result_3 = process_query(invalid_prefix)

    assert result_3[0] == "invalid"
    assert result_3[1] == None

    result_4 = process_query(invalid_route_set)

    assert result_4[0] == "invalid"
    assert result_4[1] == None

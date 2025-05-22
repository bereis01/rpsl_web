from ...search.regex import process_query

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

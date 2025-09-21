from ....parsing.shared.attributes import process_attributes

body_example = "as-name: FSNINC\ndescr: Full Service Networking\nmp-export: afi any.unicast to AS-ANY announce AS394599:AS-ALL\nadmin-c: RESCH2-ARIN\ntech-c: RESCH2-ARIN\nmnt-by: MAINT-AS394599\nchanged: chris.resch@fullservice.net 20230322\nsource: ALTDB\nsource: DBALT\n"


def test_process_attributes():
    result = process_attributes(body_example)

    assert len(list(result.keys())) == 8
    assert list(result.keys())[0] == "as-name"
    assert result["as-name"] == "FSNINC"
    assert result["source"] == "ALTDB\nDBALT"

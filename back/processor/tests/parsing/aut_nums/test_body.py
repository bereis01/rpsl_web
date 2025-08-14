from ....parsing.aut_nums.body import process_body

body_example = "as-name: FSNINC\ndescr: Full Service Networking\nmp-export: afi any.unicast to AS-ANY announce AS394599:AS-ALL\nadmin-c: RESCH2-ARIN\ntech-c: RESCH2-ARIN\nmnt-by: MAINT-AS394599\nchanged: chris.resch@fullservice.net 20230322\nsource: ALTDB\n"


def test_process_body():
    result = process_body(body_example)

    assert len(list(result.keys())) == 8
    assert list(result.keys())[0] == "as-name"
    assert result[list(result.keys())[0]] == "FSNINC"

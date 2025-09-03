from ....parsing.route_sets.inverted import (
    process_inverted_as,
    process_inverted_addr,
    process_inverted_rs,
)

route_sets_example = {
    "rs-peer-4-24-152-26": {
        "body": "descr: routes Level3 accepts from Citigroup (citibank4)\nmembers: 192.193.172.0/24,192.193.176.0/24,192.193.184.0/24,192.193.188.0/24,192.193.175.0/24\nremarks: Route data was migrated from former Genuity config.\nremarks: Please contact Genuity-migrations@Level3.net if\nremarks: you have any questions about this object.\nadmin-c: GM1-LEVEL3\ntech-c: GM1-LEVEL3\nmnt-by: GENUITY-MIGRATIONS\nchanged: Genuity-migrations@Level3.net 20040617\nsource: LEVEL3\n",
        "members": [
            {
                "type": "AS",
                "name": "AS123",
                "op": "NoOp",
            },
            {
                "type": "address",
                "address_prefix": "192.193.176.0/24",
                "range_operator": "NoOp",
            },
            {
                "type": "AS",
                "name": "AS456",
                "op": "NoOp",
            },
            {
                "type": "address",
                "address_prefix": "192.193.188.0/24",
                "range_operator": "NoOp",
            },
            {
                "type": "address",
                "address_prefix": "192.193.175.0/24",
                "range_operator": "NoOp",
            },
            {
                "type": "route_set",
                "name": "rs-pingdash-v6-48",
                "op": "NoOp",
            },
        ],
    },
    "rs-peer-4-24-152-30": {
        "body": "descr: routes Level3 accepts from DTCC - ESG End Cust (dtccny2)\nmembers: 207.45.41.0/24\nremarks: 2003/07/17-19:20:17 -Genuity Migration Tool-\nremarks: Route data was migrated from former Genuity config.\nremarks: Please contact Genuity-migrations@Level3.net if\nremarks: you have any questions about this object.\nadmin-c: GM1-LEVEL3\ntech-c: GM1-LEVEL3\nmnt-by: GENUITY-MIGRATIONS\nchanged: Genuity-migrations@Level3.net 20030717\nsource: LEVEL3\n",
        "members": [
            {
                "type": "address",
                "address_prefix": "207.45.41.0/24",
                "range_operator": "NoOp",
            },
            {
                "type": "route_set",
                "name": "RS-pingdash-v6-48",
                "op": "NoOp",
            },
        ],
    },
}


def test_process_inverted_as():
    result = process_inverted_as(route_sets_example)

    assert len(list(result.keys())) == 2
    assert list(result.keys())[0] == "AS123"
    assert result[list(result.keys())[1]] == ["rs-peer-4-24-152-26"]


def test_process_inverted_addr():
    result = process_inverted_addr(route_sets_example)

    assert len(list(result.keys())) == 4
    assert list(result.keys())[0] == "192.193.176.0/24"
    assert result[list(result.keys())[3]] == ["rs-peer-4-24-152-30"]


def test_process_inverted_rs():
    result = process_inverted_rs(route_sets_example)

    assert len(list(result.keys())) == 2
    assert list(result.keys())[0] == "rs-pingdash-v6-48"
    assert result[list(result.keys())[1]] == ["rs-peer-4-24-152-30"]

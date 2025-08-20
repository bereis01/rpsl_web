from utils.parsing import (
    parse_attributes,
    parse_relationships,
    parse_membership,
    parse_announcement,
)

attributes = {
    "as-name": "Level3",
    "descr": "Level 3 Communications",
    "admin-c": "LV3-LEVEL3",
    "tech-c": "LV3-LEVEL3",
    "mnt-by": "LEVEL3-MNT",
    "changed": "ipadmin@centurylink.com 20200611",
    "source": "LEVEL3",
}


def test_parse_attributes():
    parsed_text = parse_attributes(attributes)

    assert (
        parsed_text[0]
        == "**Name:** Level3\n\n**Description:** Level 3 Communications\n\n**Registered in:** LEVEL3\n\n**Technical contact:** LV3-LEVEL3\n\n**Administrative contact:** LV3-LEVEL3\n\n**Maintained by:** LEVEL3-MNT\n\n**Last changed by:** ipadmin@centurylink.com 20200611\n\n"
    )
    assert parsed_text[1] == "No remarks to be shown\n"


relationship = [
    {
        "asn": "3356",
        "peer": {"field": "Single", "type": "Num", "value": "3"},
        "tor": "Customer",
        "import": {
            "peering": {
                "remote_as": {"field": "Single", "type": "Num", "value": "3"},
                "remote_router": {"type": "Ip", "value": "4.24.88.50"},
            },
            "filter": {"type": "RouteSet", "value": "rs-peer-4-24-88-50", "op": "NoOp"},
        },
        "export": {
            "peering": {
                "remote_as": {"field": "Single", "type": "Num", "value": "3"},
                "remote_router": {"type": "Ip", "value": "4.78.140.10"},
            },
            "filter": {"type": "Any", "value": "Any"},
        },
        "sym": True,
    }
]


def test_parse_relationships():
    parsed_text = parse_relationships(relationship)

    assert (
        parsed_text
        == ":green-badge[Symmetric] \n\nPossible :red-background[**customer**] relationship with :green-background[**AS3**] over which it shares :blue-background[**any route**] and receives :blue-background[**the routes in the route set rs-peer-4-24-88-50**] \n- Imports routes from remote router of :gray-background[**IP 4.24.88.50**] \n- Exports routes at remote router of :gray-background[**IP 4.78.140.10**] \n\n---\n\n"
    )


membership = {
    "as-ebay-transit": {
        "body": "descr: transit\nmembers: AS3320, AS3356, AS209, AS701, AS1239, AS10911, AS3561, AS7911\nmnt-by: MAINT-AS11643\nchanged: lsabo@ebay.com 20070806\nsource: RADB\n",
        "members": ["209", "701", "1239", "3320", "3356", "3561", "7911", "10911"],
        "set_members": ["test123"],
        "is_any": False,
    }
}


def test_parse_membership():
    parsed_text = parse_membership(membership)

    assert (
        parsed_text
        == ":orange-background[**as-ebay-transit**]\n- **Members:** AS209, AS701, AS1239, AS3320, AS3356, AS3561, AS7911, AS10911\n- **Set members:** test123\n\n"
    )


announcement = {"4.0.0.0/8": {"announced_by": ["3356"]}}


def test_parse_announcement():
    parsed_text = parse_announcement(announcement)

    assert (
        parsed_text
        == ":violet-background[**4.0.0.0/8**]\n- **Announced by:** AS3356\n\n"
    )

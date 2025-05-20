from ...aut_nums.rules.peering.remote_as import process_remote_as
from ...aut_nums.rules.peering.router import process_router

remote_as_simple = {"Single": {"Num": 123}}


def test_process_remote_as():
    result_simple = process_remote_as(remote_as_simple)

    assert result_simple == {"field": "Single", "type": "Num", "value": 123}


router_simple = {"Ip": "123.456.789"}


def test_process_router():
    result_simple = process_router(router_simple)

    assert result_simple == {"type": "Ip", "value": "123.456.789"}

import pytest
from scripts.deploy_and_create import deploy_and_create
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account
from brownie import network


def test_can_create_simple_collectible():
    only_local()
    simple_collectible = deploy_and_create()
    assert simple_collectible.ownerOf(0) == get_account()


def only_local():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Can only test on local networks")

import time
import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from brownie import network


def test_i_can_create_advanced_collectible():
    only_remote()
    # Act
    _advanced_collectible, creating_tx = deploy_and_create()

    # wait for the randomness callback
    time.sleep(180)
    
    # Assert
    assert _advanced_collectible.tokenCounter() == 1


def only_remote():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Can only test on remote networks")

import pytest
from scripts.advanced_collectible.deploy_and_create import deploy_and_create
from scripts.utils import LOCAL_BLOCKCHAIN_ENVIRONMENTS, get_account, get_contract
from brownie import network


def test_can_create_advanced_collectible():
    # Arrange
    only_local()
    # Act
    advanced_collectible, creating_tx = deploy_and_create()
    # get the rng requestId from creating_tx
    requestId = creating_tx.events["requestedCollectible"]["requestId"]
    # callback rng
    rng = 721
    get_contract("vrf_coordinator").callBackWithRandomness(
        requestId, rng, advanced_collectible, {"from": get_account()}
    )
    
    # Assert
    assert advanced_collectible.ownerOf(0) == get_account()
    assert advanced_collectible.tokenCounter() == 1
    assert advanced_collectible.tokenIdToBreed(0) == rng % 3

def only_local():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("Can only test on local networks")

from brownie import Lottery, accounts, network, config, exceptions
import pytest
from web3.main import Web3
from scripts.deploy_lottery import deploy_lottery
from scripts.utils import (
    DECIMALS,
    ETH_USD_MOCK_VALUE,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
    get_account,
    fund_with_link,
    get_contract,
)

divider = ETH_USD_MOCK_VALUE / (10 ** DECIMALS)
expected_eth_entrance_fee = 50 / divider
expected_entrance_fee = Web3.toWei(expected_eth_entrance_fee, "ether")


def test_get_entrance_fee():
    only_in_local_network()

    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    # want to make sure entrance fee is what we expect (mock result)
    # mock returns 4,000 eth/usd
    # usd entry fee is 50
    # eth entrance fee is 50 / 4000 = 0.0125
    assert expected_entrance_fee == entrance_fee


def test_cant_enter_unless_started():
    only_in_local_network()

    # revert enter tx for a non-started lottery
    lottery = deploy_lottery()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": get_account(), "value": lottery.getEntranceFee()})


def test_can_enter_started_lottery():
    only_in_local_network()

    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    tx = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    tx.wait(1)
    assert lottery.players(0) == account


def test_can_end_lottery():
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    tx = lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    tx.wait(1)
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2


def test_can_pick_winner_correctly():
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=1), "value": lottery.getEntranceFee()})
    lottery.enter({"from": get_account(index=2), "value": lottery.getEntranceFee()})
    fund_with_link(lottery)
    # choose a winner
    # we need to pretend to be a chainlink node to call the random result function
    # end lottery starts the random number request. in there it receives the tx number
    # this tx number needs to be included in the random number response
    # we want to emit an event when the contract entered the calculating winner state
    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    # pretend to be the chainlink node, and make the callback function
    # winner index is 1 (8761 % 3)
    winner = get_account(index=1)
    starting_balance_of_account = winner.balance()
    balance_of_lottery = lottery.balance()
    get_contract("vrf_coordinator").callBackWithRandomness(
        request_id, 8761, lottery.address, {"from": account}
    )
    assert lottery.winner() == winner
    assert lottery.balance() == 0
    assert winner.balance() == starting_balance_of_account + balance_of_lottery


def only_in_local_network():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

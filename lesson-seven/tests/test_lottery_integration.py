import time
from brownie import Lottery, accounts, network, config
from web3 import Web3

from brownie import network
import pytest
from scripts.deploy_lottery import deploy_lottery
from scripts.utils import fund_with_link, get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def test_int_can_pick_winner():
    only_in_real_network()
    lottery = deploy_lottery()
    account = get_account()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 1000})
    lottery.enter({"from": account, "value": lottery.getEntranceFee() + 1000})
    fund_with_link(lottery)
    lottery.endLottery({"from": account})
    # wait for rng response. 60 is not enough
    time.sleep(180)
    assert lottery.winner() == account
    assert lottery.balance() == 0


def only_in_real_network():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip()

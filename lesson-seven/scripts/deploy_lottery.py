from scripts.utils import get_account, get_contract, fund_with_link
from brownie import Lottery, network, config
import time


def deploy_lottery():
    account = get_account()
    # returns either mock or real contract, depending on environment
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["vrf_fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Lottery deployed at {lottery.address}")

    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx = lottery.startLottery({"from": account})
    tx.wait(1)
    print(f"Lottery started")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx = lottery.enter({"from": account, "value": value})
    tx.wait(1)
    print(f"Entered lottery")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    # before we can end, we need some link in the contract
    tx = fund_with_link(lottery.address)
    tx.wait(1)

    # end the lottery
    ending_tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)

    # wait for the chainlink random to be returned from a node (few blocks)
    print(f"Lottery ending")
    time.sleep(60)
    print(f"Ended: {lottery.winner()} won the lottery")


def main():
    deploy_lottery()
    # usually only deploy in the script, and call this functions from the terminal
    start_lottery()
    enter_lottery()
    end_lottery()

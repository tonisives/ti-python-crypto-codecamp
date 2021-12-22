from brownie import interface, network, config
from scripts.utils import get_account


def main():
    get_weth()


def get_weth():
    """
    Mints WETH by depositing ETH.
    """
    # ABI: IWeth.sol
    # Address
    account = get_account()
    weth = interface.IWeth(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": 0.1 * 10 ** 18})
    tx.wait(1)
    # should get 0.1 WETH in return
    print(f"received 0.1 WETH")
    return tx

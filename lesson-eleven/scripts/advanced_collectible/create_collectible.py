from brownie import AdvancedCollectible, config, network

from scripts.utils import fund_with_link, get_account


def main():
    account = get_account()

    advanced_collectible = AdvancedCollectible[-1]
    fund_with_link(advanced_collectible.address, amount=0.1 * 10 ** 18)
    tx = advanced_collectible.createCollectible({"from": account})
    tx.wait(1)
    print("Collectible created")

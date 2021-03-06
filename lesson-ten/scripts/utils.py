from brownie import (
    accounts,
    network,
    config,
)

LOCAL_BLOCKCHAIN_ENVIRONMENTS = [
    "development",
    "ganache",
    "ganache-local",
    "mainnet-fork",
]


def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    if id:
        return accounts.load(id, password="test")
    if network.show_active() in config["networks"]:
        return accounts.add(config["wallets"]["from_key"])
    return None

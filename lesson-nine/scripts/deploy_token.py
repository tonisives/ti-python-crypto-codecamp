from web3 import Web3
from scripts.helpful_scripts import get_account
from brownie import OurToken

initial_supply = Web3.toWei(7000000, "ether")


def deploy_token():
    account = get_account()
    our_token = OurToken.deploy(initial_supply, {"from": account})
    print(our_token.name())


def main():
    deploy_token()

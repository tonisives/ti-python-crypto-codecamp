from brownie import FundMe
from scripts.utils import get_account


def fund():
    print("Funding")
    fund_me = FundMe[-1]
    account = get_account()
    # get the entrance fee in wei. send only that 50$
    entrance_fee = fund_me.getEntranceFee()
    print(f"Funding {account} with {entrance_fee}")
    fund_me.fund({"from": account, "value": entrance_fee})


def withdraw():
    print("Withdrawing")
    fund_me = FundMe[-1]
    account = get_account()
    fund_me.withdraw({"from": account})


def main():
    fund()
    withdraw()

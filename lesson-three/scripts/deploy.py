from brownie import accounts, network, FundMe, PriceConsumerV3
import os

def deploy_simple_storage():
    print("Deploying simple storage")
    account = get_account()
    
    fund_me = FundMe.deploy({"from": account})
    fund_tx = fund_me.fund({"from": account, "amount": 10000000000})
    fund_tx.wait(1)

    print(f"amount funded {fund_me.addressToAmountFunded(account)}")

    fund_tx = fund_me.fund({"from": account, "amount": 10000000000})
    fund_tx.wait(1)
    print(f"amount funded after second tx {fund_me.addressToAmountFunded(account)}")

def deploy_price_consumer():
    # kovan network
    account = accounts.add(os.getenv("PRIVATE_KEY"))
    price_consumer = PriceConsumerV3.deploy({"from": account})
    print(f"deployed price consumer {price_consumer}")
    print(f"eth price {price_consumer.getLatestPrice()}")

    print

def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    print("Hello!")
    # deploy_simple_storage()
    deploy_price_consumer()

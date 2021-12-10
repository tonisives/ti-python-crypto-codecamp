from brownie import accounts, network, FundMe, MockV3Aggregator, network, config
from scripts.utils import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from web3 import Web3


def deploy_fund_me():
    print("Deploying simple storage")
    account = get_account()

    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address

    # if on rinkeby, use 0x8A, otherwise deploy mocks
    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify"),
    )
    print(f"FundMe address: {fund_me.address}")

    # storage_factory = StorageFactory.deploy({"from": account})
    # # this makes the rpc shell error
    # new_contract = storage_factory.createSimpleStorageContract({"from": account})
    # new_contract.wait(1)

    # print(f"simple storage {storage_factory.simpleStorages(0)}")

    # store_tx = storage_factory.sfStoreFavoriteNumber(0, 42)
    # store_tx.wait(1)

    # stored_number = storage_factory.sfReadFavoriteNumber(0)
    # print(f"stored number: {stored_number}")


def main():
    print("Starting deployment")
    deploy_fund_me()

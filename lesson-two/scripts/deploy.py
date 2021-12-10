from brownie import accounts, network, StorageFactory


def deploy_simple_storage():
    print("Deploying simple storage")
    account = get_account()

    storage_factory = StorageFactory.deploy({"from": account})
    # this makes the rpc shell error
    new_contract = storage_factory.createSimpleStorageContract({"from": account})
    new_contract.wait(1)

    print(f"simple storage {storage_factory.simpleStorages(0)}")

    store_tx = storage_factory.sfStoreFavoriteNumber(0, 42)
    store_tx.wait(1)

    stored_number = storage_factory.sfReadFavoriteNumber(0)
    print(f"stored number: {stored_number}")


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    print("Hello!")
    deploy_simple_storage()

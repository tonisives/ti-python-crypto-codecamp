from brownie import accounts, SimpleStorage, network, config
import os

def deploy_simple_storage():
    print("Deploying simple storage")
    account = get_account()
    # account = accounts.load("test")
    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # print(account)
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print("Stored value: {}".format(stored_value))
    transaction = simple_storage.store(42, {"from": account})
    transaction.wait(1)  # wait for 1 block
    updated_stored_value = simple_storage.retrieve()
    print("Updated stored value: {}".format(updated_stored_value))


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def main():
    print("Hello!")
    project_id = os.getenv("WEB3_INFURA_PROJECT_ID")
    print(f"id {project_id} id")
    deploy_simple_storage()

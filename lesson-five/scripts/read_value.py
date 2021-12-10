from brownie import SimpleStorage, accounts, config

def read_contract():
    simple_storage = SimpleStorage[-1]
    # ABI - stored in SimpleStorage.json
    # Address saved in deployments folder
    print(simple_storage.retrieve())

def main():
    read_contract()
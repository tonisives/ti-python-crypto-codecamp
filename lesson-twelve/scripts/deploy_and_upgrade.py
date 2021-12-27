from scripts.utils import encode_function_data, get_account, upgrade
from brownie import (
    Contract,
    network,
    Box,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    BoxV2,
)


def main():
    account = get_account()
    print(f"Deploying box contract to {network.show_active()}")

    box = Box.deploy({"from": account}, publish_source=True)
    # error currently because BoxV2 has the increment function
    # print(box.increment())

    # Hook up proxy to our implementation
    # give a proxy admin. It could be multisig(safer) for defi protocols.
    proxy_admin = ProxyAdmin.deploy({"from": account}, publish_source=True)
    # proxies dont have constructors, so we choose initializer function
    # encode the initializer function
    # box.store is the function, 1 is the first parameter
    initializer = box.store, 1
    box_encoded_initializer_function = encode_function_data()

    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        # this could be us, but we use proxy admin
        proxy_admin.address,
        box_encoded_initializer_function,
        {"from": account, "gas_limit": 1000000},
        publish_source=True
    )

    print(f"Proxy deployed to: {proxy}. You can now upgrade to V2")

    # assign proxy address, abi of the box contract to the contract
    proxy_box = Contract.from_abi("Box", proxy.address, Box.abi)
    # call the box function from proxy address
    proxy_box.store(1, {"from": account}).wait(1)
    print(proxy_box.retrieve())

    # upgrade to v2
    box_v2 = BoxV2.deploy({"from": account}, publish_source=True)

    upgrade_tx = upgrade(account, proxy, box_v2.address, proxy_admin)
    print("Proxy has been upgraded")
    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    proxy_box.increment({"from": account}).wait(1)
    # will return 2, ecause in origial contract we already stored 1.
    print(proxy_box.retrieve())

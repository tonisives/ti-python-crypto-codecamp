import pytest
from scripts.utils import encode_function_data, get_account, upgrade
from brownie import (
    Box,
    Contract,
    ProxyAdmin,
    TransparentUpgradeableProxy,
    BoxV2,
    exceptions,
)


def test_proxy_upgrades():
    account = get_account()
    box = Box.deploy({"from": account})
    proxy_admin = ProxyAdmin.deploy({"from": account})
    box_encode_initializer_function = encode_function_data()
    proxy = TransparentUpgradeableProxy.deploy(
        box.address,
        proxy_admin.address,
        box_encode_initializer_function,
        {"from": account, "gas_limit": 1000000},
    )
    # we have tested that proxy works with Box in test_box_proxy
    # now we test that we can upgrade to BoxV2

    proxy_box = Contract.from_abi("BoxV2", proxy.address, BoxV2.abi)
    # currently proxy_box still uses box.address (from proxy.address)
    with pytest.raises(exceptions.VirtualMachineError):
        proxy_box.increment({"from": account})

    # upgrade proxy to boxv2
    box_v2 = BoxV2.deploy({"from": account})
    upgrade(account, proxy, box_v2, proxy_admin)
    proxy_box.increment({"from": account})
    assert proxy_box.retrieve() == 1

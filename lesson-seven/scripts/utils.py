from brownie import (
    accounts,
    network,
    config,
    interface,
    MockV3Aggregator,
    VRFCoordinatorMock,
    LinkToken,
    Contract,
)
from web3 import Web3

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork-dev"]

DECIMALS = 8
# 4000 + 8 decimals
ETH_USD_MOCK_VALUE = 400000000000

def get_account(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id, password="test")
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or network.show_active() in FORKED_LOCAL_ENVIRONMENTS
    ):
        # ganache accounts
        return accounts[0]
    # envrionment account
    return accounts.add(config["wallets"]["from_key"])


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    """
    Grab the contract addresses from the brownie config, if defined. otherwise
    will deploy a mock of that contract.

    Currently only supports the eth_usd_price_feed contract.

        Args:
            contract_name (str): name of the contract to deploy.
        Returns:
            The most recently deployed contract.
    """
    """
    address _priceFeedAddress,
    address _vrfCoordinator,
    address _link,
    uint256 _vrfFee,
    bytes32 _keyhashx
    """
    contract_type = contract_to_mock[contract_name]

    # check if we need to deploy a mock(local chain)
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        if len(contract_type) <= 0:
            deploy_mocks()

        contract = contract_type[-1]
    else:
        # TODO: why do you need a mock contract here? Lottery queries price feed contract my address
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )

    return contract



def deploy_mocks(decimals=DECIMALS, initial_value=ETH_USD_MOCK_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("mocks deployed")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):  # 0.1 LINK
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")

    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)

    print("fund with link")
    return tx

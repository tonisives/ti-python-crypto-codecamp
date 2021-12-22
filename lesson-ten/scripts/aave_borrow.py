from scripts.get_weth import get_weth
from scripts.utils import get_account

from brownie import config, network, interface

borrow_amount = 0.1 * 10 ** 18


def main():
    account = get_account()
    weth_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()

    # get AAVE lending pool
    lending_pool = get_lending_pool()
    # before we can deposit, need to approve WETH spending
    approve_erc20(borrow_amount, lending_pool.address, weth_address, account)
    # deposit to aave lending pool
    # address asset, uint256 amount, address onBehalfOf, uint16 referralCode
    print(f"Depositing {borrow_amount} to lending pool")
    tx = lending_pool.deposit(
        weth_address, borrow_amount, account, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited")

    # borrow according to positive health factor
    available_borrows_eth, total_debt_eth = get_borrowable_data(lending_pool, account)
    print("Borrowing DAI")
    # DAI in terms of ETH
    dai_eth_price_feed = config["networks"][network.show_active()]["dai_eth"]
    dai_eth_price = get_asset_price(dai_eth_price_feed)
    # borrowable eth > borrowable dai * 0.95
    amount_dai_to_borrow = (1 / dai_eth_price) * (available_borrows_eth * 0.95)
    print(f"borrowing {amount_dai_to_borrow} DAI")
    # borrow

    dai_address = config["networks"][network.show_active()]["dai_token"]
    tx = lending_pool.borrow(
        dai_address,
        amount_dai_to_borrow * 10 ** 18,
        2,
        0,
        account.address,
        {"from": account},
    )
    tx.wait(1)
    print("borrowed some DAI")
    get_borrowable_data(lending_pool, account)
    repay_all(amount_dai_to_borrow, lending_pool, account)


def repay_all(amount, lending_pool, account):
    print("Repaying")
    # approve DAI ERC20
    # approve_erc20(amount, spender, erc20_address, account):
    dai_token_address = config["networks"][network.show_active()]["dai_token"]

    approve_erc20(amount * 10 ** 18, lending_pool, dai_token_address, account)

    print(f"repaying {amount} DAI")
    tx = lending_pool.repay(
        dai_token_address, amount * 10 ** 18, 2, account.address, {"from": account}
    )
    tx.wait(1)
    print("Repayed")


def get_asset_price(asset_price_feed):
    # get price of asset
    price_feed = interface.AggregatorV3Interface(asset_price_feed)
    price = price_feed.latestRoundData()[1]
    # https://youtu.be/M576WGiDBdQ?t=34377
    converted_price = price / 10 ** 18
    print(f"dai/eth price: {converted_price}")
    return float(converted_price)


def get_borrowable_data(lending_pool, account):
    (
        totalCollateralETH,
        totalDebtETH,
        availableBorrowsETH,
        currentLiquidationThreshold,
        ltv,
        healthFactor,
    ) = lending_pool.getUserAccountData(account)

    available_borrows_eth = availableBorrowsETH / 10 ** 18
    total_collateral_eth = totalCollateralETH / 10 ** 18
    total_debt_eth = totalDebtETH / 10 ** 18
    print(f"available borrows: {available_borrows_eth}")
    print(f"total collateral: {total_collateral_eth}")
    print(f"total debt: {total_debt_eth}")
    return (float(available_borrows_eth), float(total_debt_eth))


def approve_erc20(amount, spender, erc20_address, account):
    print("approving ERC20 token")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from": account})
    tx.wait(1)
    print("Approved")
    return tx


def get_lending_pool():
    # LendingPool address can change. AdressesProvider will return the correct address.

    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()

    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

// SPDX-License-Identifier: UNLICENSE
pragma solidity ^0.6.6;

// import from chainlink contracts npm package
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

/**
 Allow any person to fund, but only the contract owner can withdraw.
*/
contract FundMe {
    using SafeMathChainlink for uint256;

    // uint256 is very big. normal int is 32
    mapping(address => uint256) public addressToAmountFunded;
    address[] public funders;

    address public owner;
    AggregatorV3Interface public priceFeed;

    constructor(address _priceFeed) public {
        // set the contract owner, so will only refund to owner
        priceFeed = AggregatorV3Interface(_priceFeed);
        owner = msg.sender;
    }

    function fund() public payable {
        // create a minimum value for the users to fund. set the minimum value in USD
        uint256 minimumUsd = 50 * 10**18;

        // check the truthedness of statement. if doesnt match, will revert tx
        require(
            getConversionRate(msg.value) >= minimumUsd,
            "Minimum fund amount is 50 usd."
        );

        // keep track of who sent us the funding
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender);
    }

    function withdraw() public payable onlyOwner {
        // withdraw all the money that has been transferred.
        msg.sender.transfer(address(this).balance);

        // probably could just loop all keys in the map....
        for (
            uint256 funderIndex = 0;
            funderIndex < funders.length;
            funderIndex++
        ) {
            address funder = funders[funderIndex];
            addressToAmountFunded[funder] = 0;
        }

        funders = new address[](0);
    }

    /**
    converts minimum 50usd fee to ether
     */
    function getEntranceFee() public view returns (uint256) {
        uint256 minimumUSD = 50 * 10**18;
        uint256 price = getPrice();
        uint256 precision = 1 * 10**18;
        return (minimumUSD * precision) / price;
    }

    modifier onlyOwner() {
        // require that owner is calling the method
        require(owner == msg.sender, "Only contract owner can withdraw.");
        _;
    }

    function getVersion() public view returns (uint256) {
        return priceFeed.version();
    }

    function getPrice() public view returns (uint256) {
        (, int256 answer, , , ) = priceFeed.latestRoundData();
        return uint256(answer * 10000000000);
    }

    // 1000000000 1 gwei
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUsd = (ethPrice * ethAmount) / 1000000000000000000;
        return ethAmountInUsd;
        // 0.000004471499325570
    }
}

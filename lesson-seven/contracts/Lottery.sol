// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";
import "@chainlink/contracts/src/v0.8/VRFConsumerBase.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract Lottery is VRFConsumerBase, Ownable {
    address payable[] public players;
    address payable public winner;
    uint256 public usdEntryFee;
    uint256 public random;

    enum LOTTERY_STATE {
        OPEN,
        CLOSED,
        CALCULATING_WINNER
    }
    LOTTERY_STATE public lottery_state;

    AggregatorV3Interface internal ethUsdPriceFeed;

    // random number generator
    uint256 public vrfFee;
    bytes32 public keyhash;

    constructor(
        address _priceFeedAddress,
        address _vrfCoordinator,
        address _link,
        uint256 _vrfFee,
        bytes32 _keyhash
    ) VRFConsumerBase(_vrfCoordinator, _link) {
        usdEntryFee = 50 * 10**18;
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSED;
        vrfFee = _vrfFee;
        keyhash = _keyhash;
    }

    function enter() public payable {
        require(lottery_state == LOTTERY_STATE.OPEN);
        require(
            msg.value >= getEntranceFee(),
            "Minimum 50$ entrance fee required"
        );
        // 50$ minimum
        players.push(payable(msg.sender));
    }

    function getEntranceFee() public view returns (uint256) {
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        // ethusd has 8 decimals, convert to wei (18 decimals)
        uint256 adjustedPrice = uint256(price) * 10**10;
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        // TODO: should use safemath or solidity 8+
        return costToEnter;
    }

    function startLottery() public onlyOwner {
        require(
            lottery_state == LOTTERY_STATE.CLOSED,
            "Lottery is already open"
        );
        lottery_state = LOTTERY_STATE.OPEN;
    }

    /**
    Choose a random winner
     */
    function endLottery() public onlyOwner {
        // need a number outside of blockchain
        lottery_state = LOTTERY_STATE.CALCULATING_WINNER;
        // first request the random number
        bytes32 requestId = requestRandomness(keyhash, vrfFee);
    }

    function fulfillRandomness(bytes32 requestId, uint256 _randomness)
        internal
        override
    {
        // internal - only VRF coordinator can call this function
        require(
            lottery_state == LOTTERY_STATE.CALCULATING_WINNER,
            "Lottery is ending"
        );
        require(_randomness > 0, "random not found");
        random = _randomness;
        uint256 indexOfWinner = _randomness % players.length;
        winner = players[indexOfWinner];
        winner.transfer(address(this).balance);
        // reset the lottery

        players = new address payable[](0);
        lottery_state = LOTTERY_STATE.CLOSED;
    }
}

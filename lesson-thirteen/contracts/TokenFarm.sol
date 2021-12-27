/**
 stake tokens
 unstake tokens
 issue token rewards
 add more tokens to be allowed to be staked
 getEthValue - value of tokens in ether
 */
// SPDX-License-Identifier: MIT
pragma solidity 0.8.0;

import "@openzeppelin/contracts/access/ownable.sol";

contract TokenFarm is Ownable {
    address[] public allowedTokens;

    function stakeTokens(uint256 _amount, address _token) public {
        // what tokens can they stake
        require(_amount > 0, "Amount must be more than 0");
        require(tokenIsAllowed(_token), "This token is not allowed to be staked");
        // how much can they stake
    }

    function addAllowedToken(address _token) public onlyOwner{
        allowedTokens.push(_token);
    }

    function tokenIsAllowed(address _token) public returns (bool) {
        // what tokens can they stake.
        for (uint256 allowedTokensIndex=0; allowedTokensIndex<allowedTokens.length;allowedTokensIndex++) {
            if (allowedTokens[allowedTokensIndex] == _token) {
                return true;
            }
        }

        return false;
    }
}

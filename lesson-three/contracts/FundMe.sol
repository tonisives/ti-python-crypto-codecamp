// SPDX-License-Identifier: UNLICENSE
pragma solidity >=0.6.6 <0.9.0;

contract FundMe {

    // uint256 is very big. normal int is 32
    mapping(address => uint256) public addressToAmountFunded;

    function fund() public payable {
        // we want to keep track of who sent us the funding
        addressToAmountFunded[msg.sender] += msg.value;

        // we want to create minimum value for the users to fund. set the minimum value in USD
        // get the conversion rate from USD to ETH

        // what is the ETH to USD conversion rate is?


    }

}
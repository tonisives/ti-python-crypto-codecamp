// SPDX-License-Identifier: MIT
// simple NFT

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    // give name and symbol

    constructor() public ERC721("Dogie", "DOG") {
        tokenCounter = 0;
    }

    // create a new NFT and assign it to the person who called the function

    function createCollectible() public returns (uint256) {
        // safemint adds count of tokens to addresses
        // safemint checks if tokenId has been used before or not
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        tokenCounter++;
        return newTokenId;
    }
}

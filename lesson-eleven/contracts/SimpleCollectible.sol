// SPDX-License-Identifier: MIT

/**
 simple NFT
 1. We didnt upload image to IPFS
 2. Why is IPFS decentralized?
 3. Anyone can mint an NFT here - it is not scarce or random
*/

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract SimpleCollectible is ERC721 {
    uint256 public tokenCounter;

    // give name and symbol

    constructor() public ERC721("Dogie", "DOG") {
        tokenCounter = 0;
    }

    // create a new NFT and assign it to the person who called the function

    function createCollectible(string memory tokenURI)
        public
        returns (uint256)
    {
        // safemint adds count of tokens to addresses
        // safemint checks if tokenId has been used before or not
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenURI);
        tokenCounter++;
        return newTokenId;
    }
}

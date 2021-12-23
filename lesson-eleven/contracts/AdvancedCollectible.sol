// SPDX-License-Identifier: MIT

/** 
    An NFT Contract where the tokenURI can be one of 3 different dogs.
    Randomly selected.
*/

pragma solidity 0.6.6;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@chainlink/contracts/src/v0.6/VRFConsumerBase.sol";

contract AdvancedCollectible is ERC721, VRFConsumerBase {
    // https://youtu.be/M576WGiDBdQ?t=37497
    uint256 public tokenCounter;
    bytes32 public keyHash;
    uint256 public fee;

    enum Breed {
        PUG,
        SHIBA_INU,
        ST_BERNARD
    }

    mapping(uint256 => Breed) public tokenIdToBreed;
    mapping(bytes32 => address) public requestIdToSender;

    // indexed keyword makes it easier to search for this event
    event requestedCollectible(bytes32 indexed requestId, address requester);
    event breedAssigned(uint256 indexed tokenId, Breed breed);

    constructor(
        address _vrfCoordinator,
        address _linkToken,
        bytes32 _keyHash,
        uint256 _fee
    )
        public
        VRFConsumerBase(_vrfCoordinator, _linkToken)
        ERC721("Dogie", "DOG")
    {
        tokenCounter = 0;
        keyHash = _keyHash;
        fee = _fee;
    }

    function createCollectible(string memory tokenURI)
        public
        returns (bytes32)
    {
        // create an event whenever we request one of these new dogs
        bytes32 requestId = requestRandomness(keyHash, fee);
        requestIdToSender[requestId] = msg.sender;
        emit requestedCollectible(requestId, msg.sender);
    }

    function fulfillRandomness(bytes32 requestId, uint256 randomNumber)
        internal
        override
    {
        Breed breed = Breed(randomNumber % 3);
        uint256 newTokenId = tokenCounter;
        tokenIdToBreed[newTokenId] = breed;
        emit breedAssigned(newTokenId, breed);

        address owner = requestIdToSender[requestId];
        _safeMint(owner, newTokenId);

        // TODO: make this function decide what the tokenURI is, so it is even more
        // decentralized
        tokenCounter++;
    }

    function setTokenURI(uint256 tokenId, string memory tokenURI) public {
        // owner of the nft can set a new tokenURI
        // we have on chain metadata (breed), now add the off chain metadata

        // predefined 3 tokenURIS for dogs

        // only the onwer(or someone approved) should be able to update the tokenURI
        // check that the owner of the tokenId is the sender
        require(
            _isApprovedOrOwner(_msgSender(), tokenId),
            "Only the owner can set the tokenURI"
        );

        _setTokenURI(tokenId, tokenURI);
    }
}

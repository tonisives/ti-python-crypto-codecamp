// SPDX-License-Identifier: UNLICENSED

pragma solidity ^0.6.0; // 0.6.0..x until 0.7(breaking changes there)

import "./SimpleStorage.sol";

contract StorageFactory {

    SimpleStorage[] public simpleStorages;

    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorages.push(simpleStorage);
    }

    function sfStoreFavoriteNumber(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        // address
        // ABI
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorages[_simpleStorageIndex]));
        simpleStorage.store(_simpleStorageNumber);
    }

    function sfReadFavoriteNumber(uint256 _simpleStorageIndex) public view returns(uint256) {
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorages[_simpleStorageIndex]));
        return simpleStorage.retrieve();
    }
}


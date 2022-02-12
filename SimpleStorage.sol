// SPDX-License-Identifier: MIT
pragma solidity >=0.6.0 <0.9.0;
pragma experimental ABIEncoderV2;

contract SimpleStorage {
    //this will get initialized to 0
    uint256 favoriteNumber;
    bool favoriteBool;

    struct People {
        uint256 favoriteNumber;
        string name;
    }

    string[] public peopleNames;
    uint256[] public peopleFavNumbers;

    People[] public people;
    mapping(string => uint256) public nameToFavoriteNumber;

    function store(uint256 _favoriteNumber) public returns (uint256){
        favoriteNumber = _favoriteNumber;
        return _favoriteNumber;
    }

    function retrieve() public view returns (uint256) {
        return favoriteNumber;
    }

    function addPerson(string memory _name, uint256 _favoriteNumber) public {
        people.push(People({favoriteNumber : _favoriteNumber, name : _name}));
        peopleNames.push(_name);
        peopleFavNumbers.push(_favoriteNumber);
        nameToFavoriteNumber[_name] = _favoriteNumber;
    }

    function getPeoples() public view returns (string[] memory, uint256[] memory) {
        return (peopleNames, peopleFavNumbers);
    }
}

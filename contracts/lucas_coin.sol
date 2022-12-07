// contracts/Box.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Lucas {

    string private _teste = "ola";

    function print() public view returns(string memory) {
        return _teste;
    }
   
}
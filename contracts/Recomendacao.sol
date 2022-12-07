// contracts/Box.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Recomendacao {

  struct Usuario {
    uint id;
    string listaPrevisao;
  }

  Usuario[] public ArrayUsuario;

  function novoUsuario(uint id, string calldata previsao) public{
    Usuario memory _novoUsuario;
    _novoUsuario.id = id;
    _novoUsuario.listaPrevisao = previsao;
    ArrayUsuario.push(_novoUsuario);
    return;
  }

  function deletarUsuario(uint id) public returns(bool boolean) {
    if(ArrayUsuario[id].id != 0 && bytes(ArrayUsuario[id].listaPrevisao).length > 0)
    {
        delete ArrayUsuario[id];
        return true;
    }
    else
    {
        return false;
    }
    
  }

  function getUsuario(uint id) public view returns(Usuario memory user) {
    return ArrayUsuario[id];
  }

  function numeroUsuarios() public view returns(uint entityCount) {
    return ArrayUsuario.length;
  }
}
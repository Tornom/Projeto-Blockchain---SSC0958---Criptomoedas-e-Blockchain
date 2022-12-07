import json
from web3 import Web3, HTTPProvider

blockchain_address = 'http://127.0.0.1:7545'

web3 = Web3(HTTPProvider(blockchain_address))
web3.eth.defaultAccount = web3.eth.accounts[0]

compiled_contract_path = 'build/contracts/Recomendacao.json'
deployed_contract_address = '0x27C916761a6c1806813Bcf7002C6f57bA8529Dd5'

with open(compiled_contract_path) as file:
    contract_json = json.load(file) 
    contract_abi = contract_json['abi'] 

contract = web3.eth.contract(address=deployed_contract_address, abi=contract_abi)

message = contract.functions.novoUsuario(1,'22199,Akame ga Kill!,TV,24,0,24,0000-00-00,0000-00-00,,4,,0.00,Completed,,0,,LOW,,0,0,1,default,0').transact()

print(message)

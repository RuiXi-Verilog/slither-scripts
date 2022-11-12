# Slither scripts

```
pip install pipenv --user
pipenv -python 3.10.8
pipenv install --dev
solc-select install 0.4.24 && solc-select use 0.4.24
pipenv run python erc20/erc20.py erc20/ERC20.sol ERC20
```

```
nvm use 16
npm install yarn
yarn add
# yarn add @openzeppelin/contracts@2.3.0
solc-select install 0.5.0 && solc-select use 0.5.0
pipenv run python erc20/erc20.py node_modules/@openzeppelin/contracts/token/ERC721/ERC721.sol ERC721
```

## Results

```
== ERC20 functions definition ==
[x] transfer (address, uint256) -> (bool)
[x] approve (address, uint256) -> (bool)
[x] transferFrom (address, address, uint256) -> (bool)
[x] allowance (address, address) -> (uint256)
[✓] balanceOf (address) -> (uint256)

== Custom modifiers ==
[✓] No custom modifiers in ERC20 functions

== ERC20 events ==
[✓] Transfer (address, address, uint256)
[✓] Approval (address, address, uint256)

== ERC20 getters ==
[x] totalSupply () -> (uint256)
[x] decimals () -> (uint8)
[x] symbol () -> (string)
[x] name () -> (string)

== Allowance frontrunning mitigation ==
[x] increaseAllowance (address, uint256) -> (bool)
[x] decreaseAllowance (address, uint256) -> (bool)

== Balance check in approve function ==
[✓] approve function should not check for sender's balance
```
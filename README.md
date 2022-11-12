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
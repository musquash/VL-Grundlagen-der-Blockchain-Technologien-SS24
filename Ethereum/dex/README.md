This repo contains a toy-dex implementation.

# Docs
https://ethresear.ch/t/improving-front-running-resistance-of-x-y-k-market-makers/1281

# Steps

- Copy the files into Remix
- Deploy the ERC20 contract (which provides the deployer with 1M TestTKN)
- Deploy the DEX contract (provide the ERC20 address on deployment)
- Call approve (dexAddr, 100000) on the ERC20 contract
- Call addLiquidity(100000) with 100000 wei value
- Swap as much as you like using swapETHToToken and swapTokenToETH
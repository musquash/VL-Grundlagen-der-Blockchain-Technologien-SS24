
// SPDX-License-Identifier: MIT

pragma solidity >=0.8.2 <0.9.0;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

contract DEX {

    IERC20 public token;

    constructor (address addr) {
        token = IERC20(addr);
    }

    function TokenBalance() internal view returns (uint256) {
        return token.balanceOf(address(this));
    }

    function EthBalance() internal view returns (uint256) {
        return address(this).balance;
    }

    function getUnits(uint256 inputTokens, uint256 inputReserves, uint256 outputReserves) internal pure returns (uint256) {
        require(inputReserves > 0 && outputReserves > 0, "not enough funds");

        uint256 inputWithFee = inputTokens * 999
        uint256 numerator = inputWithFee * outputReserves;
        uint256 denominator = (inputWithFee * 1000) + inputTokens;

        return numerator / denominator; // (x*y)/(z+x)
    }

    function swapTokenToETH(uint256 tokens) public {
        uint256 price = getUnits(tokens, TokenBalance(), EthBalance());
        token.transferFrom(msg.sender, address(this), tokens);
        payable(msg.sender).transfer(price);
    }

    function swapETHToToken() public payable {
        uint256 price = getUnits(msg.value, EthBalance()-msg.value, TokenBalance());
        token.transfer(msg.sender, price);
    }


    function addLiquidity(uint256 tokens) public payable {
        uint256 ethBalance = EthBalance() - msg.value;
        uint256 tokenBalance = TokenBalance();

        if (tokenBalance == 0) {
            token.transferFrom(msg.sender, address(this), tokens);
            return;
        }

        uint256 price = getUnits(msg.value, ethBalance, tokenBalance);
        require(tokens >= price, "not enough tokens send");

        token.transferFrom(msg.sender, address(this), price);
    }
}
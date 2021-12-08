// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;


import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";


contract FabricaDeCampanhas{

    address[] public campanhas;
    address dataFeedEther;

    constructor(address _dataFeedEther) {
        dataFeedEther = _dataFeedEther;
    }

    function criarCampanha(
        string memory _nome, 
        uint _investimentoMinimo, 
        uint _dataLimite
    ) public returns (Campanha){

        address beneficiario = msg.sender;

        Campanha novaCampanha = new Campanha(
            _nome, 
            beneficiario, 
            _investimentoMinimo, 
            _dataLimite, 
            dataFeedEther
        );

        campanhas.push(address(novaCampanha));

        return novaCampanha;
    }

    function buscarTodasAsCampanhas() public view returns (address[] memory){
        return campanhas;
    }
}

contract Campanha {

    AggregatorV3Interface public dataFeedEther;
    uint public financiamentoMinimo;
    uint public dataLimite;
    address public beneficiario;
    mapping(address => uint) public valorInvestidoPorCadaInvestidor;
    address[] public financiadores;
    string nomeCampanha;
    // Valor dolar considerado = 5,6 reais
    uint private valorDolar = 56 * 10**17;
    
    constructor(
        string memory _nomeCampanha, 
        address _beneficiario, 
        uint _investimentoMinimo, 
        uint _dataLimite, 
        address _dataFeedEther
    ) {
        dataFeedEther = AggregatorV3Interface(_dataFeedEther);
        nomeCampanha = _nomeCampanha;
        financiamentoMinimo = _investimentoMinimo * 10**18;
        dataLimite = _dataLimite;
        beneficiario = _beneficiario;
    }

    modifier somentebeneficiario() {
        require(msg.sender == beneficiario);
        _;
    }

    function buscarValorFinanciamentoMinimo() public view returns (uint){
        (uint precoEth, uint decimais) = buscarPrecoEth();

        uint financiamentoMinimoEmDolar = (financiamentoMinimo * 10**18) / valorDolar;
        return ((financiamentoMinimoEmDolar * 10**decimais) / precoEth) + 100;
    }

    function buscarFinanciadores() external view returns (address[] memory) {
        return financiadores;
    }

    function buscarTotalInvestido() external view returns (uint){
        return address(this).balance;
    }

    function buscarPrecoEth() public view returns (uint, uint) {
        // Buscando valor atual do Ether
        (, int256 precoEth, , , ) = dataFeedEther.latestRoundData();
        uint decimais = dataFeedEther.decimals();

        return (uint(precoEth), uint(decimais));
    }

    function converterEthParaReal(uint256 quantidadeDeEth) public view returns (uint256) {
        (uint256 precoEth, uint256 decimais) = buscarPrecoEth();

        uint256 quantidadeDeEthEmDolar = (precoEth * quantidadeDeEth) / 10**decimais;
        uint256 quantidadeEmReal = quantidadeDeEthEmDolar * valorDolar / 10**18;

        return quantidadeEmReal;
    }

    function financiar() public payable {
        require(converterEthParaReal(msg.value) >= financiamentoMinimo, "Valor minimo de investimento nao atingido.");

        if(valorInvestidoPorCadaInvestidor[msg.sender] == 0) {
            financiadores.push(msg.sender);
        }

        valorInvestidoPorCadaInvestidor[msg.sender] += msg.value;
    }

    function colherInvestimentos() public somentebeneficiario {
        require(block.timestamp >= dataLimite, "Data limite ainda nao atingida");

        payable(msg.sender).transfer(address(this).balance);
        for(uint indiceFinanciador ; indiceFinanciador < financiadores.length; indiceFinanciador++) {
            address financiador = financiadores[indiceFinanciador];
            valorInvestidoPorCadaInvestidor[financiador] = 0;
        }

        financiadores = new address[](0);
    }
}
    

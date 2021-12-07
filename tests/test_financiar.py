from datetime import datetime

import pytest
from brownie import Campanha, FabricaDeCampanhas, MockV3Aggregator, exceptions

from scripts.deploy import deploy_fabrica_de_campanhas
from scripts.helper import buscar_conta
from tests.decorators import pular_caso_rede_nao_local


@pular_caso_rede_nao_local
def test_financiar():
    conta = buscar_conta()

    campanha = test_criar_campanha()
    valor_a_financiar = campanha.buscarValorFinanciamentoMinimo()
    tx = campanha.financiar({"from": conta, "value": valor_a_financiar})
    tx.wait(1)

    financiadores = campanha.buscarFinanciadores()
    print(f"Financiadores: {financiadores}")

    assert campanha.valorInvestidoPorCadaInvestidor(conta.address) == valor_a_financiar


@pular_caso_rede_nao_local
def test_colher_investimentos():
    conta = buscar_conta()

    campanha = test_criar_campanha()

    valor_a_financiar = campanha.buscarValorFinanciamentoMinimo()
    tx = campanha.financiar({"from": conta, "value": valor_a_financiar})
    tx.wait(1)

    tx2 = campanha.colherInvestimentos({"from": conta})
    tx2.wait(1)
    assert campanha.valorInvestidoPorCadaInvestidor(conta.address) == 0


@pular_caso_rede_nao_local
def test_converter_eth_para_real():
    conta = buscar_conta()

    valor_minimo = 50  # reais
    campanha = test_criar_campanha()

    valor_financiamento_minimo = campanha.buscarValorFinanciamentoMinimo()

    valor_em_real = campanha.converterEthParaReal(valor_financiamento_minimo, {"from": conta})
    assert int(valor_em_real/(10**18)) == valor_minimo


@pular_caso_rede_nao_local
def test_valor_financiamento_minimo():
    def e18(num):
        return num * 10 ** 18

    campanha = test_criar_campanha()

    preco_eth, decimais = campanha.buscarPrecoEth()

    valor_financiamento_minimo = campanha.buscarValorFinanciamentoMinimo()
    print(valor_financiamento_minimo)
    valor_esperado = int((e18(50) * e18(1) / 5.6) / preco_eth) + 100

    assert valor_financiamento_minimo == valor_esperado


@pular_caso_rede_nao_local
def test_criar_campanha():
    conta = buscar_conta()
    fabrica = deploy_fabrica_de_campanhas()
    data_limite = datetime.now().timestamp()

    tx = fabrica.criarCampanha("Campanha 1", 50, data_limite, {"from": conta})
    tx.wait(1)

    campanha = Campanha.at(tx.return_value)

    assert campanha
    return campanha


@pular_caso_rede_nao_local
def test_colher_investimentos_usuario_inautorizado():
    conta = buscar_conta()
    campanha = test_criar_campanha()

    valor_a_financiar = campanha.buscarValorFinanciamentoMinimo()

    tx = campanha.financiar({"from": conta, "value": valor_a_financiar})
    tx.wait(1)

    conta_inautorazada = buscar_conta(1)

    with pytest.raises(exceptions.VirtualMachineError):
        campanha.colherInvestimentos({"from": conta_inautorazada})


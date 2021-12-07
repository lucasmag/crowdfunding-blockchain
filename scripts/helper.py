from brownie import (
    network,
    accounts,
    config,
    MockV3Aggregator,
    Contract,
)
from web3 import Web3

AMBIENTES_LOCAIS_DE_BLOCKCHAIN = ["development", "ganache"]


def buscar_conta(index=None, id=None):
    if index:
        return accounts[index]
    if network.show_active() in AMBIENTES_LOCAIS_DE_BLOCKCHAIN:
        return accounts[0]
    if id:
        return accounts.load(id)
    return accounts.add(config["wallets"]["from_key"])


def buscar_contrato_preco_moeda():
    """Esta função cria um mock do contrato, caso a rede seja local.
    Caso contrario, cria um contrato a partir do endereço definido no brownie-config.yaml para a rede corrente.
    """
    if network.show_active() in AMBIENTES_LOCAIS_DE_BLOCKCHAIN:
        if len(MockV3Aggregator) <= 0:
            criar_mock_preco_moeda()

        endereco_contrato = MockV3Aggregator[-1].address
    else:
        endereco_contrato = config["networks"][network.show_active()]["eth_usd_price_feed"]

    return endereco_contrato


def criar_mock_preco_moeda():
    DECIMAIS = 18
    VALOR_INICIAL = Web3.toWei(4000, "ether")  # 1 ETH == 4000 USD

    print(f"A rede atual é {network.show_active()}")
    conta = buscar_conta()

    print("Criando cópia da tabela de preços...")
    tabela_precos = MockV3Aggregator.deploy(DECIMAIS, VALOR_INICIAL, {"from": conta})
    print(f"Endereço contrato tabela de preços: {tabela_precos.address}")


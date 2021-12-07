from scripts.atualizar_frontend import atualizar_front_end
from scripts.helper import buscar_conta, buscar_contrato_preco_moeda
from brownie import FabricaDeCampanhas


def deploy_fabrica_de_campanhas(atualizar_front=False):
    conta = buscar_conta()
    endereco_contrato_preco_moeda = buscar_contrato_preco_moeda()
    fabrica = FabricaDeCampanhas.deploy(endereco_contrato_preco_moeda, {"from": conta})
    print(f"Fabrica de campanhas criada: {fabrica}")

    if atualizar_front:
        atualizar_front_end()

    return fabrica


def main():
    deploy_fabrica_de_campanhas(atualizar_front=True)

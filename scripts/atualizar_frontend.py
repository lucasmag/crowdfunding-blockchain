from os import path
import shutil
import json
import yaml


def copiar_pastas_para_frontend(src, dest):
    # Apaga pastas do destino, caso existam
    if path.exists(dest):
        shutil.rmtree(dest)

    shutil.copytree(src, dest)


def atualizar_front_end():
    copiar_pastas_para_frontend("./build", "./frontend/src/blockchain")

    with open("brownie-config.yaml", "r") as brownie_config:
        config_dict = yaml.load(brownie_config, Loader=yaml.FullLoader)

        with open("./frontend/src/brownie.config.json", "w") as brownie_config_json:
            json.dump(config_dict, brownie_config_json)

    print("Frontend atualizado.")


def main():
    atualizar_front_end()

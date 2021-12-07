from scripts.helper import AMBIENTES_LOCAIS_DE_BLOCKCHAIN
from brownie import network
import functools
import pytest


def pular_caso_rede_nao_local(func):
    @functools.wraps(func)
    def wrapper_skip_non_local(*args, **kwargs):
        if network.show_active() not in AMBIENTES_LOCAIS_DE_BLOCKCHAIN:
            pytest.skip()

        return func(*args, **kwargs)
    return wrapper_skip_non_local


def pular_caso_rede_local(func):
    @functools.wraps(func)
    def wrapper_skip_non_local(*args, **kwargs):
        if network.show_active() in AMBIENTES_LOCAIS_DE_BLOCKCHAIN:
            pytest.skip()

        return func(*args, **kwargs)
    return wrapper_skip_non_local

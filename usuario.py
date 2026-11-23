from hashlib import pbkdf2_hmac
from hmac import compare_digest
from os import urandom


def proteger_senha(senha):
    sal = urandom(16).hex()
    resumo = pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(sal), 600000)
    return sal + ":" + resumo.hex()


class Usuario:

    def __init__(self, nome, senha_hash):
        self.nome = nome
        self.__senha_hash = senha_hash

    @property
    def senha_hash(self):
        return self.__senha_hash

    def autenticar(self, senha):
        try:
            sal, resumo = self.__senha_hash.split(":")
            tentativa = pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(sal), 600000)
            return compare_digest(tentativa.hex(), resumo)
        except (ValueError, TypeError):
            return False

    def perfil(self):
        return "Usuário"

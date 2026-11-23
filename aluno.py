from usuario import Usuario


class Aluno(Usuario):

    def __init__(self, nome, ra, senha_hash, validar_nome=True):
        if validar_nome and not Aluno.nome_valido(nome):
            raise ValueError("Informe um nome com letras, sem números.")
        super().__init__(nome, senha_hash)

        if len(ra) != 12 or not ra.isascii() or not ra.isdigit():
            raise ValueError("O RA deve ter exatamente 12 números.")

        self.ra = ra

        self.perdas = []

    @staticmethod
    def nome_valido(nome):
        letras = nome.replace(" ", "").replace("-", "").replace("'", "").replace("’", "")
        return letras.isalpha()

    def perfil(self):
        return "Aluno"

    def informar_perda(self, nome, local, data, caracteristicas):
        perda = {"nome": nome, "local": local, "data": data,
                 "caracteristicas": caracteristicas, "situacao": "em aberto"}

        self.perdas.append(perda)

    def mostrar_perdas(self):
        if len(self.perdas) == 0:
            print("Nenhuma perda registrada.")

        for numero, perda in enumerate(self.perdas, start=1):
            print("Aviso:", numero, "| Situação:", perda.get("situacao", "em aberto"))

            print(perda["nome"], "|", perda["local"], "|", perda["data"])

            print("Características:", perda["caracteristicas"])

    def resolver_perda(self, numero):
        if numero < 1 or numero > len(self.perdas):
            raise ValueError("Número de aviso não encontrado nas suas perdas.")

        perda = self.perdas[numero - 1]

        if perda.get("situacao", "em aberto") == "resolvida":
            raise ValueError("Essa perda já está resolvida.")

        perda["situacao"] = "resolvida"

    def para_dicionario(self):
        return {"nome": self.nome, "ra": self.ra,
                "senha": self.senha_hash, "perdas": self.perdas}

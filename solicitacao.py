class Solicitacao:
    def __init__(self, codigo, aluno, item, local, data, caracteristicas,
                 situacao="em análise", resposta=""):
        if situacao not in ("em análise", "aprovado para retirada", "recusado", "entregue"):
            raise ValueError("Situação de pedido inválida.")
        self.codigo = codigo
        self.aluno = aluno
        self.item = item
        self.local = local
        self.data = data
        self.caracteristicas = caracteristicas
        self.__situacao = situacao
        self.resposta = resposta

    @property
    def situacao(self):
        return self.__situacao

    def aprovar(self, resposta):
        if self.situacao != "em análise":
            raise ValueError("Esse pedido já foi analisado.")
        self.item.reservar()
        self.__situacao = "aprovado para retirada"
        self.resposta = resposta

    def recusar(self, resposta):
        if self.situacao != "em análise":
            raise ValueError("Esse pedido já foi analisado.")
        self.__situacao = "recusado"
        self.resposta = resposta

    def entregar(self, ra):
        if self.situacao != "aprovado para retirada":
            raise ValueError("Esse pedido não está aprovado para retirada.")
        if self.aluno.ra != ra:
            raise ValueError("O RA não corresponde ao aluno autorizado.")
        self.item.devolver()
        self.__situacao = "entregue"

    def mostrar(self):
        print("Pedido:", self.codigo, "| Objeto:", self.item.nome)
        print("Local informado:", self.local, "| Data informada:", self.data)
        print("Características que você informou:", self.caracteristicas)
        print("Situação:", self.situacao)
        if self.situacao == "aprovado para retirada":
            print("Retire o objeto na sala de achados e perdidos.")
        if self.resposta != "":
            print("Resposta:", self.resposta)

    def para_dicionario(self):
        return {"codigo": self.codigo, "aluno": self.aluno.ra,
                "item": self.item.codigo, "local": self.local, "data": self.data,
                "caracteristicas": self.caracteristicas,
                "situacao": self.situacao, "resposta": self.resposta}

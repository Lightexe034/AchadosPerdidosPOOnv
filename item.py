class Item:
    def __init__(self, codigo, nome, local, data, caracteristicas,
                 situacao="disponível"):
        if situacao not in ("disponível", "aguardando retirada", "devolvido"):
            raise ValueError("Situação de objeto inválida.")
        self.codigo = codigo
        self.nome = nome
        self.local = local
        self.data = data
        self.caracteristicas = caracteristicas
        self.guardado = "Sala de achados e perdidos"
        self.__situacao = situacao

    @property
    def situacao(self):
        return self.__situacao

    def reservar(self):
        if self.__situacao != "disponível":
            raise ValueError("O objeto já está reservado ou devolvido.")
        self.__situacao = "aguardando retirada"

    def devolver(self):
        if self.__situacao != "aguardando retirada":
            raise ValueError("O objeto precisa estar reservado antes da entrega.")
        self.__situacao = "devolvido"

    def mostrar(self):
        print("Código:", self.codigo)
        print("Nome:", self.nome)

    def mostrar_detalhes(self):
        self.mostrar()
        print("Local:", self.local)
        print("Data:", self.data)
        print("Características reservadas:", self.caracteristicas)
        print("Guardado em:", self.guardado)
        print("Situação:", self.situacao)

    def para_dicionario(self):
        return {"codigo": self.codigo, "nome": self.nome, "local": self.local,
                "data": self.data, "caracteristicas": self.caracteristicas,
                "guardado": self.guardado, "situacao": self.situacao}

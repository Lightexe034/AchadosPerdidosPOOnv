from item import Item
from usuario import Usuario


class Responsavel(Usuario):
    def __init__(self, nome, codigo, senha_hash):
        super().__init__(nome, senha_hash)
        self.codigo = codigo
        self.itens = []

    def perfil(self):
        return "Responsável"

    def cadastrar_item(self, nome, local, data, caracteristicas):
        codigo = max((item.codigo for item in self.itens), default=0) + 1
        item = Item(codigo, nome, local, data, caracteristicas)
        self.itens.append(item)

    def analisar(self, pedido, aprovar, resposta, pedidos):
        if resposta.strip() == "":
            raise ValueError("Escreva uma resposta ao aluno.")
        if aprovar:
            pedido.aprovar(resposta)
            for outro in pedidos:
                if outro.item == pedido.item and outro.situacao == "em análise":
                    outro.recusar("Objeto reservado para outro pedido conferido.")
        else:
            pedido.recusar(resposta)
        print("Análise registrada.")

    def entregar(self, pedido, ra):
        pedido.entregar(ra)
        print("Entrega registrada para", pedido.aluno.nome)

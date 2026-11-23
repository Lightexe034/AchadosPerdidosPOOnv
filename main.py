import json
from pathlib import Path
from datetime import datetime, date
from aluno import Aluno
from responsavel import Responsavel
from solicitacao import Solicitacao
from item import Item
from usuario import proteger_senha


ARQUIVO = Path(__file__).with_name("dados.json")


def salvar(alunos, itens, pedidos):
    dados = {"alunos": [], "objetos": [], "pedidos": []}

    for aluno in alunos:
        dados["alunos"].append(aluno.para_dicionario())
    for item in itens:
        dados["objetos"].append(item.para_dicionario())
    for pedido in pedidos:
        dados["pedidos"].append(pedido.para_dicionario())

    temporario = ARQUIVO.with_suffix(".tmp")
    temporario.write_text(json.dumps(dados, ensure_ascii=False, indent=4), encoding="utf-8")
    temporario.replace(ARQUIVO)


def conferir_registro(registro, campos):
    if not isinstance(registro, dict):
        raise ValueError("Registro inválido no JSON.")
    for campo, tipo in campos.items():
        if type(registro.get(campo)) is not tipo:
            raise ValueError("Campo inválido no JSON: " + campo)
        if tipo is str and not registro[campo].strip():
            raise ValueError("Campo vazio no JSON: " + campo)
        if campo == "data":
            data_salva = datetime.strptime(registro[campo], "%d/%m/%Y").date()
            if data_salva > date.today():
                raise ValueError("Data futura no JSON.")


def conferir_dados(dados):
    conferir_registro(dados, {"alunos": list, "objetos": list, "pedidos": list})
    for aluno in dados["alunos"]:
        conferir_registro(aluno, {"nome": str, "ra": str, "senha": str, "perdas": list})
        for perda in aluno["perdas"]:
            conferir_registro(perda, {"nome": str, "local": str,
                                     "data": str, "caracteristicas": str})
            if perda.get("situacao", "em aberto") not in ("em aberto", "resolvida"):
                raise ValueError("Situação de perda inválida no JSON.")
    for item in dados["objetos"]:
        conferir_registro(item, {"codigo": int, "nome": str, "local": str,
                                "data": str, "caracteristicas": str, "situacao": str})
        if item["codigo"] < 1:
            raise ValueError("Código de objeto inválido no JSON.")
    for pedido in dados["pedidos"]:
        conferir_registro(pedido, {"codigo": int, "aluno": str, "item": int,
                                  "local": str, "data": str, "caracteristicas": str,
                                  "situacao": str})
        if pedido["codigo"] < 1 or not isinstance(pedido.get("resposta"), str):
            raise ValueError("Pedido inválido no JSON.")


def carregar():
    if not ARQUIVO.exists():
        return [], [], []

    try:
        dados = json.loads(ARQUIVO.read_text(encoding="utf-8-sig"))
        conferir_dados(dados)
        alunos = {}
        itens = {}
        pedidos = []

        for registro in dados["alunos"]:
            aluno = Aluno(registro["nome"], registro["ra"], registro["senha"], validar_nome=False)
            aluno.perdas = registro["perdas"]
            for perda in aluno.perdas:
                perda.setdefault("situacao", "em aberto")
            if aluno.ra in alunos:
                raise ValueError("RA duplicado no JSON.")
            alunos[aluno.ra] = aluno

        for registro in dados["objetos"]:
            item = Item(registro["codigo"], registro["nome"], registro["local"],
                        registro["data"], registro["caracteristicas"], registro["situacao"])
            if item.codigo in itens:
                raise ValueError("Código de objeto duplicado no JSON.")
            itens[item.codigo] = item

        for registro in dados["pedidos"]:
            pedido = Solicitacao(registro["codigo"], alunos[registro["aluno"]],
                                 itens[registro["item"]], registro["local"],
                                 registro["data"], registro["caracteristicas"],
                                 registro["situacao"], registro["resposta"])
            if any(outro.codigo == pedido.codigo for outro in pedidos):
                raise ValueError("Código de pedido duplicado no JSON.")
            if pedido.situacao == "em análise" and pedido.item.situacao != "disponível":
                raise ValueError("Pedido em análise para um objeto indisponível.")
            if pedido.situacao == "aprovado para retirada" and pedido.item.situacao != "aguardando retirada":
                raise ValueError("Reserva do pedido e do objeto não correspondem.")
            if pedido.situacao == "entregue" and pedido.item.situacao != "devolvido":
                raise ValueError("Entrega do pedido e do objeto não correspondem.")
            if pedido.situacao == "em análise" and any(
                    outro.aluno is pedido.aluno and outro.item is pedido.item and
                    outro.situacao == "em análise" for outro in pedidos):
                raise ValueError("Pedido em análise duplicado para o mesmo aluno e objeto.")
            pedidos.append(pedido)

        for item in itens.values():
            retiradas = [p for p in pedidos if p.item is item and
                         p.situacao in ("aprovado para retirada", "entregue")]
            if item.situacao != "disponível" and len(retiradas) != 1:
                raise ValueError("Objeto com retirada ausente ou duplicada.")
        return list(alunos.values()), list(itens.values()), pedidos
    except (OSError, ValueError, KeyError, TypeError):
        raise SystemExit("Não foi possível carregar dados.json. O arquivo foi preservado.")


def mostrar_titulo(titulo):
    print()
    print("=" * 48)
    print(titulo.center(48))
    print("=" * 48)


def escolher_opcao():
    print("=" * 48)
    return input("Escolha uma opção: ")


def receber_usuario(usuario):
    mostrar_titulo(usuario.perfil() + " - " + usuario.nome)


def ler_texto(pergunta):
    valor = input(pergunta).strip()
    while valor == "":
        print("Preencha este campo.")
        valor = input(pergunta).strip()
    return valor


def ler_ra():
    ra = ler_texto("RA (12 números): ")
    while len(ra) != 12 or not ra.isascii() or not ra.isdigit():
        print("O RA deve ter exatamente 12 números.")
        ra = ler_texto("RA: ")
    return ra


def ler_data():
    while True:
        valor = ler_texto("Data aproximada (DD/MM/AAAA): ")
        try:
            data = datetime.strptime(valor, "%d/%m/%Y").date()
            if data <= date.today():
                return data.strftime("%d/%m/%Y")
        except ValueError:
            pass
        print("Digite uma data válida que não esteja no futuro.")


def listar_objetos():
    encontrou = False
    for item in responsavel.itens:
        if item.situacao == "disponível":
            item.mostrar()
            encontrou = True
    if encontrou == False:
        print("Nenhum objeto encontrado disponível.")


def escolher_pedido():
    codigo = input("Código do pedido (0 para voltar): ")
    for pedido in pedidos:
        if str(pedido.codigo) == codigo:
            return pedido
    return None


def menu_aluno(aluno):
    opcao = ""
    while opcao != "0":
        mostrar_titulo("ALUNO: " + aluno.nome)
        print("1 - Objetos encontrados e guardados na faculdade")
        print("2 - Objetos que os alunos estão procurando")
        print("3 - Informar uma perda")
        print("4 - Ver minhas perdas")
        print("5 - Solicitar um objeto: pode ser meu")
        print("6 - Meus pedidos")
        print("7 - Marcar minha perda como resolvida")
        print("0 - Sair da conta")
        opcao = escolher_opcao()

        if opcao == "1":
            mostrar_titulo("OBJETOS GUARDADOS NA FACULDADE")
            listar_objetos()
        elif opcao == "2":
            mostrar_titulo("OBJETOS QUE OS ALUNOS PROCURAM")
            encontrou = False
            for estudante in alunos:
                for perda in estudante.perdas:
                    if perda.get("situacao", "em aberto") == "em aberto":
                        print("Nome:", perda["nome"], "| Local:", perda["local"], "| Data:", perda["data"])
                        encontrou = True
            if encontrou == False:
                print("Nenhuma perda em aberto registrada.")
        elif opcao == "3":
            mostrar_titulo("INFORMAR UMA PERDA")
            nome = ler_texto("O que perdeu? ")
            local = ler_texto("Onde perdeu? ")
            data = ler_data()
            caracteristicas = ler_texto("Características (cor, marca, detalhes): ")
            aluno.informar_perda(nome, local, data, caracteristicas)
            salvar(alunos, responsavel.itens, pedidos)
            print("Perda registrada para consulta do responsável.")
        elif opcao == "4":
            mostrar_titulo("MINHAS PERDAS")
            aluno.mostrar_perdas()
        elif opcao == "5":
            mostrar_titulo("SOLICITAR UM OBJETO")
            listar_objetos()
            codigo = input("Código do objeto (0 para voltar): ")
            escolhido = None
            for item in responsavel.itens:
                if str(item.codigo) == codigo and item.situacao == "disponível":
                    escolhido = item
            if escolhido == None:
                print("Nenhum objeto disponível selecionado.")
            else:
                repetido = False
                for pedido in pedidos:
                    if pedido.aluno == aluno and pedido.item == escolhido and pedido.situacao == "em análise":
                        repetido = True
                if repetido:
                    print("Você já tem um pedido em análise para esse objeto.")
                else:
                    local = ler_texto("Onde você perdeu o objeto? ")
                    data = ler_data()
                    caracteristicas = ler_texto("Descreva características que comprovem que é seu: ")
                    pedido = Solicitacao(max((p.codigo for p in pedidos), default=0) + 1, aluno, escolhido, local, data, caracteristicas)
                    pedidos.append(pedido)
                    salvar(alunos, responsavel.itens, pedidos)
                    print("Pedido enviado. Aguarde a análise do responsável.")
        elif opcao == "6":
            mostrar_titulo("MEUS PEDIDOS")
            encontrou = False
            for pedido in pedidos:
                if pedido.aluno == aluno:
                    pedido.mostrar()
                    encontrou = True
            if encontrou == False:
                print("Você ainda não fez pedidos.")
        elif opcao == "7":
            mostrar_titulo("RESOLVER MINHA PERDA")
            if len(aluno.perdas) == 0:
                print("Você ainda não registrou perdas.")
            else:
                aluno.mostrar_perdas()
                numero = input("Número do aviso resolvido (0 para voltar): ")
                if numero != "0":
                    if not numero.isascii() or not numero.isdigit():
                        print("Digite o número de um dos seus avisos.")
                    else:
                        try:
                            aluno.resolver_perda(int(numero))
                            salvar(alunos, responsavel.itens, pedidos)
                            print("Perda marcada como resolvida.")
                        except ValueError as erro:
                            print(erro)
        elif opcao != "0":
            print("Opção inválida.")


def menu_responsavel():
    opcao = ""
    while opcao != "0":
        mostrar_titulo("PAINEL DO RESPONSÁVEL")
        print("1 - Cadastrar objeto encontrado")
        print("2 - Consultar objetos e detalhes reservados")
        print("3 - Consultar perdas dos alunos")
        print("4 - Analisar pedidos")
        print("5 - Registrar entrega")
        print("0 - Sair da conta")
        opcao = escolher_opcao()

        if opcao == "1":
            mostrar_titulo("CADASTRAR OBJETO")
            nome = ler_texto("Nome genérico (ex.: garrafa, sem características): ")
            local = ler_texto("Local encontrado (reservado ao responsável): ")
            data = ler_data()
            caracteristicas = ler_texto("Características reservadas: ")
            responsavel.cadastrar_item(nome, local, data, caracteristicas)
            salvar(alunos, responsavel.itens, pedidos)
            print("Objeto cadastrado. Guardado na sala de achados e perdidos.")
        elif opcao == "2":
            if len(responsavel.itens) == 0:
                print("Nenhum objeto cadastrado.")
            for item in responsavel.itens:
                item.mostrar_detalhes()
        elif opcao == "3":
            encontrou = False
            for aluno in alunos:
                if len(aluno.perdas) > 0:
                    print("Aluno:", aluno.nome, "| RA:", aluno.ra)
                    aluno.mostrar_perdas()
                    encontrou = True
            if encontrou == False:
                print("Nenhuma perda registrada.")
        elif opcao == "4":
            mostrar_titulo("ANALISAR PEDIDOS")
            encontrou = False
            for pedido in pedidos:
                if pedido.situacao == "em análise":
                    pedido.mostrar()
                    print("Aluno:", pedido.aluno.nome, "| RA:", pedido.aluno.ra)
                    encontrou = True
            if encontrou == False:
                print("Nenhum pedido em análise.")
            else:
                pedido = escolher_pedido()
                if pedido == None or pedido.situacao != "em análise":
                    print("Nenhum pedido em análise selecionado.")
                else:
                    mostrar_titulo("DESCRIÇÃO DO ALUNO")
                    pedido.mostrar()
                    mostrar_titulo("REGISTRO RESERVADO DO OBJETO")
                    pedido.item.mostrar_detalhes()
                    print("Confira o local, a data e as características.")
                    decisao = input("1 - Aprovar / 2 - Recusar / 0 - Voltar: ")
                    if decisao == "1" or decisao == "2":
                        resposta = ler_texto("Motivo ou orientação de retirada, sem revelar detalhes reservados: ")
                        try:
                            responsavel.analisar(pedido, decisao == "1", resposta, pedidos)
                            salvar(alunos, responsavel.itens, pedidos)
                        except ValueError as erro:
                            print(erro)
                    elif decisao != "0":
                        print("Decisão inválida.")
        elif opcao == "5":
            mostrar_titulo("REGISTRAR ENTREGA")
            encontrou = False
            for pedido in pedidos:
                if pedido.situacao == "aprovado para retirada":
                    print("Pedido:", pedido.codigo, "|", pedido.item.nome,
                          "| Aluno:", pedido.aluno.nome, "| RA:", pedido.aluno.ra)
                    encontrou = True
            if encontrou == False:
                print("Nenhuma retirada aprovada.")
            else:
                pedido = escolher_pedido()
                if pedido == None or pedido.situacao != "aprovado para retirada":
                    print("Nenhuma retirada aprovada selecionada.")
                else:
                    print("Confira a identificação do aluno presencialmente.")
                    ra = ler_ra()
                    if input("O objeto foi entregue? (s/n): ").lower() == "s":
                        try:
                            responsavel.entregar(pedido, ra)
                            salvar(alunos, responsavel.itens, pedidos)
                        except ValueError as erro:
                            print(erro)
        elif opcao != "0":
            print("Opção inválida.")


responsavel = Responsavel("Secretaria", "12responsavel34", proteger_senha("1234"))
alunos = []
pedidos = []


def executar():
    global alunos, pedidos
    alunos, responsavel.itens, pedidos = carregar()
    opcao = ""
    while opcao != "0":
        mostrar_titulo("ACHADOS E PERDIDOS")
        print("1 - Entrar na conta")
        print("2 - Criar conta de aluno")
        print("0 - Encerrar")
        opcao = escolher_opcao()

        if opcao == "1":
            mostrar_titulo("ENTRAR NA CONTA")
            identificacao = ler_texto("RA ou código do responsável: ")
            senha = input("Senha: ")
            if identificacao == responsavel.codigo and responsavel.autenticar(senha):
                receber_usuario(responsavel)
                menu_responsavel()
            else:
                aluno_logado = None
                for aluno in alunos:
                    if aluno.ra == identificacao and aluno.autenticar(senha):
                        aluno_logado = aluno
                if aluno_logado == None:
                    print("Identificação ou senha incorretas.")
                else:
                    receber_usuario(aluno_logado)
                    menu_aluno(aluno_logado)
        elif opcao == "2":
            mostrar_titulo("CRIAR CONTA DE ALUNO")
            nome = ler_texto("Nome: ")
            while not Aluno.nome_valido(nome):
                print("Informe um nome com letras, sem números.")
                nome = ler_texto("Nome: ")
            ra = ler_ra()
            existe = False
            for aluno in alunos:
                if aluno.ra == ra:
                    existe = True
            if existe:
                print("RA já cadastrado.")
            else:
                senha = ler_texto("Crie sua senha: ")
                confirmacao = input("Confirme a senha: ")
                if senha != confirmacao:
                    print("Senhas diferentes. Cadastro não realizado.")
                else:
                    alunos.append(Aluno(nome, ra, proteger_senha(senha)))
                    salvar(alunos, responsavel.itens, pedidos)
                    print("Conta criada. Agora faça login.")
        elif opcao == "0":
            print("Programa encerrado.")
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    try:
        executar()
    except OSError as erro:
        print("Falha ao acessar dados.json:", erro)
        print("A operação não pôde ser gravada. Confira o arquivo antes de continuar.")
    except (KeyboardInterrupt, EOFError):
        print("\nPrograma encerrado.")

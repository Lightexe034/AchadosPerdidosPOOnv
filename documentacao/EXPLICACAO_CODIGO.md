# Como entender e explicar o código

Este guia acompanha os arquivos Python comentados do projeto. Os comentários explicam as instruções próximas deles. Os exemplos de fala abaixo podem ser adaptados às suas palavras durante a apresentação.

## 1. Comece explicando o problema

> Nosso projeto organiza os achados e perdidos da faculdade. O aluno informa o que perdeu e solicita um objeto encontrado. O responsável cadastra o que recebeu, confere as descrições e registra a entrega. Os registros ficam salvos em JSON para continuar disponíveis depois de fechar o programa.

Há três registros diferentes no atendimento. Um aviso de perda informa o que alguém está procurando. Um Item representa algo que já está com a faculdade. Uma Solicitacao registra o pedido de um aluno para receber um Item específico. O aviso de perda pode existir antes de qualquer objeto parecido chegar à secretaria.

## 2. Ordem de leitura

1. [usuario.py](../usuario.py) reúne os dados e a autenticação comuns.
2. [aluno.py](../aluno.py) mostra a herança e os avisos de perda.
3. [item.py](../item.py) mostra os atributos e as situações do objeto.
4. [solicitacao.py](../solicitacao.py) liga aluno e objeto e controla o pedido.
5. [responsavel.py](../responsavel.py) coordena cadastro, análise e entrega.
6. [main.py](../main.py) apresenta as telas, valida entradas e salva os dados.

O Python começa executando as instruções de main.py. A ordem acima serve para estudar os conceitos antes de acompanhar o menu.

## 3. Classe, objeto, atributo e método

```python
ana = Aluno("Ana", "001234567890", proteger_senha("senha-exemplo"))
```

- Aluno é a classe, que define os dados e comportamentos de uma conta de aluno.
- A chamada Aluno(...) cria uma instância, também chamada de objeto.
- ana é a variável que permite acessar esse objeto.
- ana.nome e ana.ra acessam atributos, que são os dados guardados nele.
- ana.informar_perda(...) chama um método, que executa uma ação daquele aluno.

> Usamos classes para reunir os dados e as ações de cada parte do sistema. A classe Aluno representa o tipo, e cada conta cadastrada é um objeto desse tipo.

## 4. O significado de self

```python
def __init__(self, nome, ra, senha_hash):
    super().__init__(nome, senha_hash)
    self.ra = ra
    self.perdas = []
```

O parâmetro nome recebe o valor passado na chamada. self representa a instância que está sendo preparada. Em self.ra = ra, o valor recebido em ra é colocado no atributo ra daquele aluno. A lista self.perdas pertence a esse mesmo aluno.

Se Ana e José forem cadastrados, cada um tem sua própria lista. Quando chamamos ana.informar_perda(...), o Python passa ana como self. Quando José chama o mesmo método, self representa José.

> self é o objeto que está executando o método. Ele permite acessar e alterar os atributos da conta ou registro correto.

O nome self é uma convenção do Python. Nas chamadas do programa, escrevemos aluno.mostrar_perdas(). O próprio Python fornece a referência do objeto para o primeiro parâmetro do método.

## 5. usuario.py

### Importações e proteção da senha

Os imports trazem funções da biblioteca padrão do Python. pbkdf2_hmac calcula um hash de senha, urandom gera bytes aleatórios e compare_digest compara o resultado na autenticação.

Em proteger_senha, urandom(16) gera um sal aleatório. hex transforma bytes em texto hexadecimal para salvar no JSON. O sal permite que duas contas com a mesma senha tenham registros de hash diferentes.

pbkdf2_hmac recebe o algoritmo sha256, a senha convertida para bytes com encode, o sal e 600000 repetições do cálculo. O retorno da função junta sal e hash com um separador de dois-pontos. O código não possui uma função para recuperar a senha original a partir desse registro.

> Antes de salvar a senha do aluno, calculamos um hash com um sal aleatório. No login, repetimos o cálculo com o sal salvo e comparamos os resultados.

### Usuario e o construtor

__init__ inicializa o objeto com nome e __senha_hash. O prefixo de dois sublinhados aplica a transformação de nomes do Python e evita alterações acidentais pelo acesso comum. Esse recurso participa do encapsulamento, mas quem pode alterar os arquivos do programa ainda controla a execução local.

### A propriedade senha_hash

@property permite consultar usuario.senha_hash como um atributo. A função retorna o hash interno para a gravação. Não existe um setter para atribuir outro valor pela propriedade.

> O encapsulamento controla a forma de acesso a um dado. O hash é guardado em um atributo privado, e a propriedade permite consultá-lo para salvar.

### autenticar

split(":") separa o sal do hash gravado. A senha digitada é calculada com o mesmo sal. compare_digest compara o hash calculado com o salvo e retorna True ou False. O try e o except ValueError tratam um formato inválido do registro da senha.

### perfil

Usuario define perfil e retorna Usuário. As classes Aluno e Responsavel têm versões próprias desse método. Essa organização permite demonstrar sobrescrita e polimorfismo no login.

## 6. aluno.py

### Herança e super

class Aluno(Usuario) declara que Aluno herda de Usuario. Assim, uma conta de aluno pode usar autenticar sem copiar seu código. super().__init__(nome, senha_hash) chama o construtor da classe base para preparar os atributos compartilhados na própria instância de Aluno.

O construtor também verifica o RA. len confere o tamanho, isascii restringe os caracteres ao conjunto usado para os dígitos comuns e isdigit verifica se todos são números. O RA permanece texto para preservar zeros no início. raise ValueError sinaliza que um valor recebido é inválido.

> Aluno herda nome e autenticação de Usuario e acrescenta RA e perdas. O super reaproveita a inicialização compartilhada.

### perfil

Retorna Aluno. É uma sobrescrita porque tem o mesmo nome do método da classe base e define o comportamento próprio dessa classe.

### informar_perda

Monta um dicionário com nome do objeto, local, data, características e situação em aberto. append acrescenta esse dicionário à lista self.perdas. Um aluno pode ter vários avisos.

### mostrar_perdas

Se len(self.perdas) for zero, mostra que não existem avisos. O for percorre a lista e enumerate(..., start=1) fornece um número a partir de 1 para cada aviso. A tela mostra o número, a situação e os dados do próprio aluno. get("situacao", "em aberto") oferece um valor padrão para registros antigos.

### resolver_perda

Recebe o número exibido na tela. Primeiro confere se está entre 1 e a quantidade de avisos. A expressão self.perdas[numero - 1] localiza o registro porque os índices da lista começam em zero. Se ele já estiver resolvido, gera ValueError. Caso contrário, altera a chave situacao para resolvida. O registro permanece no histórico.

> Resolver uma perda encerra um aviso da própria conta. A entrega de um objeto recebido é confirmada pelo responsável em outra etapa.

### para_dicionario

Retorna os dados que main.py gravará no JSON. A chave senha contém o hash. As perdas ficam dentro do aluno para manter a identificação de quem criou os avisos.

## 7. item.py

### Construtor e atributos

Item guarda código, nome, local, data, características, local de guarda e situação. O local de guarda é Sala de achados e perdidos. O parâmetro situacao começa como disponível, mas também recebe uma situação já salva quando carregamos o JSON. O construtor verifica se ela pertence às três opções aceitas.

### situacao, reservar e devolver

__situacao é consultado pela propriedade situacao. reservar exige que o item esteja disponível e muda para aguardando retirada. devolver exige uma reserva e muda para devolvido. Esses métodos concentram as regras que controlam a mudança de situação.

> O objeto controla suas próprias mudanças. Para reservar, ele precisa estar disponível. Para registrar a entrega, precisa estar aguardando retirada.

### mostrar e mostrar_detalhes

mostrar imprime código e nome para o aluno. mostrar_detalhes chama mostrar e acrescenta local, data, características, local de guarda e situação. O painel do responsável usa essa exibição completa. A distinção ajuda a conferir a descrição apresentada pelo aluno.

### para_dicionario

Prepara os dados de Item para gravação, incluindo a situação consultada pela propriedade.

## 8. solicitacao.py

### Relacionamentos

self.aluno = aluno e self.item = item guardam referências aos objetos já existentes. Por isso pedido.aluno.ra acessa o RA do solicitante e pedido.item.reservar() atua no objeto solicitado. O pedido também guarda o que o aluno informou sobre local, data e características.

> A solicitação faz a ligação entre quem pede e o objeto desejado. Ela tem sua própria situação e a resposta do responsável.

### aprovar

Exige que o pedido esteja em análise. Chama self.item.reservar(), que também valida a situação do item. Depois muda o pedido para aprovado para retirada e guarda a resposta. Se a reserva falhar, o método para antes de aprovar.

### recusar

Exige pedido em análise, muda sua situação para recusado e guarda o motivo. Não realiza uma entrega.

### entregar

Exige pedido aprovado e verifica se o RA informado corresponde ao aluno do pedido. Depois chama devolver no Item e muda o pedido para entregue. A comparação evita confirmar a retirada para outro RA.

### mostrar

Exibe os dados apresentados pelo solicitante, a situação e a resposta. Quando aprovado, orienta a retirada na sala de achados e perdidos.

### para_dicionario

No arquivo, o pedido guarda o RA do aluno e o código do item. Ao abrir novamente o programa, main.py usa esses identificadores para localizar os objetos reconstruídos e ligá-los ao pedido.

## 9. responsavel.py

### Construtor e perfil

Responsavel herda de Usuario, chama super para preparar nome e hash, acrescenta o código de acesso e começa com uma lista de itens. perfil retorna Responsável.

### cadastrar_item

max((item.codigo for item in self.itens), default=0) procura o maior código existente. A expressão entre parênteses fornece os códigos dos itens para max. Se não houver itens, default=0 oferece o valor inicial. Somar 1 gera o próximo código. O método cria o Item e o acrescenta à lista.

### analisar

Verifica se a resposta foi preenchida. O parâmetro aprovar recebe um booleano. Quando True, chama pedido.aprovar. Depois percorre os pedidos e recusa os outros que se referem ao mesmo Item e ainda estão em análise. Quando False, chama pedido.recusar.

> O responsável toma a decisão manual e o método coordena suas consequências. Aprovar reserva o objeto para um aluno e encerra os pedidos concorrentes.

### entregar

Chama pedido.entregar(ra). As verificações do pedido e do item acontecem nesses objetos. A mensagem de sucesso é exibida depois que a operação termina.

## 10. main.py e a gravação

### Importações e caminho do arquivo

json converte texto JSON em estruturas Python e faz a conversão de volta. Path trabalha com caminhos e arquivos. datetime e date validam datas. Os outros imports trazem as classes do projeto.

Path(__file__).with_name("dados.json") cria o caminho do JSON junto ao arquivo main.py. Assim, a localização dos dados depende da pasta do programa.

### salvar

Prepara um dicionário com três listas, alunos, objetos e pedidos. Cada for chama para_dicionario para acrescentar os registros. As perdas já estão dentro de cada aluno.

json.dumps transforma o dicionário em texto. ensure_ascii=False mantém os acentos legíveis, indent=4 organiza a apresentação, e encoding="utf-8" define a codificação na gravação. Primeiro é criado dados.tmp. replace substitui dados.json depois de terminar essa escrita.

> As classes preparam seus dados e a função salvar grava o estado atual. A escrita usa um arquivo temporário para preservar o JSON anterior caso a gravação inicial falhe.

### carregar

1. Se o arquivo ainda não existe, retorna três listas vazias.
2. read_text lê o texto e json.loads transforma o JSON em dicionários e listas.
3. Reconstrói os alunos e guarda cada um em um dicionário temporário cuja chave é o RA.
4. setdefault acrescenta em aberto aos avisos antigos que ainda não possuíam situação.
5. Reconstrói os itens e guarda cada um em outro dicionário, usando seu código como chave.
6. Reconstrói os pedidos, buscando alunos e itens nesses dicionários pelos identificadores do JSON.
7. values e list recuperam os objetos e os devolvem como três listas.

O except trata problemas de leitura, estrutura e valores inválidos. SystemExit interrompe a abertura e apresenta a mensagem para preservar o arquivo que precisa ser corrigido.

## 11. main.py e as funções de apoio

| Função | Explicação |
| --- | --- |
| mostrar_titulo | Imprime os separadores. "=" * 48 repete o símbolo 48 vezes, e center(48) centraliza o texto. |
| escolher_opcao | Mostra o separador e retorna o texto digitado em input. |
| receber_usuario | Chama usuario.perfil() e mostra o nome. A implementação depende de receber um Aluno ou um Responsavel. |
| ler_texto | Usa strip para remover espaços nas extremidades e while para perguntar novamente quando ficar vazio. |
| ler_ra | Verifica exatamente 12 dígitos e mantém o RA como texto. |
| ler_data | strptime converte a entrada DD/MM/AAAA em data, compara com hoje e strftime retorna o texto padronizado. ValueError trata datas impossíveis. |
| listar_objetos | Percorre responsavel.itens e mostra somente os itens disponíveis. A variável encontrou informa se houve algum resultado. |
| escolher_pedido | Compara o código digitado com os pedidos. str converte o código inteiro para texto. Retorna o pedido ou None. |

> Polimorfismo aparece em receber_usuario. A função faz a mesma chamada perfil() e obtém Aluno ou Responsável conforme a instância recebida.

## 12. main.py e o menu do aluno

menu_aluno recebe a conta autenticada. O while mantém o menu aberto até a opção 0. input retorna texto, então as opções são comparadas com números entre aspas. if e elif escolhem o bloco a executar.

| Opção | Caminho no código |
| --- | --- |
| 1 | Chama listar_objetos e Item.mostrar para exibir código e nome. |
| 2 | Percorre as perdas dos alunos e mostra apenas avisos em aberto, com os dados públicos do aviso. |
| 3 | Lê os campos, chama aluno.informar_perda e salva. |
| 4 | Chama aluno.mostrar_perdas para exibir seu histórico. |
| 5 | Localiza um item disponível pelo código, verifica pedido repetido, lê a descrição e cria Solicitacao. Acrescenta o pedido e salva. |
| 6 | Percorre os pedidos e mostra somente aqueles cujo aluno é o da conta conectada. |
| 7 | Valida o número informado, chama aluno.resolver_perda e salva. O except apresenta eventuais erros de validação. |
| 0 | Encerra o laço da conta e devolve o controle ao login. |

Na opção 5, escolhido = None indica que nenhum objeto válido foi localizado ainda. repetido = False começa uma verificação que passa a True se houver um pedido ativo do mesmo aluno para o mesmo item. O código novo do pedido usa a mesma lógica de maior código mais 1 do cadastro de Item.

Na opção 7, int(numero) converte o texto em inteiro depois de verificar que contém dígitos. Essa conversão permite usar o número para localizar um aviso na lista.

## 13. main.py e o menu do responsável

| Opção | Caminho no código |
| --- | --- |
| 1 | Coleta os dados reservados, chama responsavel.cadastrar_item e salva. |
| 2 | Percorre os itens e chama mostrar_detalhes. |
| 3 | Percorre os alunos com perdas e exibe a identificação e os avisos. |
| 4 | Lista pedidos em análise, recebe a seleção e mostra as duas descrições. Lê a decisão e a resposta, chama analisar e salva. |
| 5 | Lista pedidos aprovados, recebe a seleção, confere o RA e a confirmação da entrega, chama entregar e salva. |
| 0 | Volta ao login. |

decisao == "1" produz True se o responsável escolheu aprovar e False quando escolheu recusar. Esse booleano é passado para analisar. O bloco try permite apresentar um ValueError de regra de negócio e continuar no menu.

> O menu coleta entradas e mostra os resultados. A conferência manual é feita pelo responsável e as classes verificam as regras antes de mudar as situações.

## 14. A inicialização, o cadastro e o login

Antes de executar, o programa prepara a conta de demonstração do responsável com código 12responsavel34 e hash da senha 1234. As listas alunos e pedidos começam vazias. executar usa global alunos, pedidos para substituir essas listas pelos dados carregados, que também serão consultados nas outras funções dos menus.

A função executar carrega o JSON uma vez ao iniciar. O menu inicial permite entrar na conta, cadastrar um aluno ou encerrar.

No login, primeiro compara o código com o do responsável e chama autenticar. Se corresponder, abre seu painel. Caso contrário, percorre os alunos e procura o RA com senha válida. aluno_logado começa como None e recebe a conta encontrada. O acesso só é encaminhado para o menu após a autenticação.

No cadastro, o programa lê nome e RA, verifica se o RA já existe e solicita senha e confirmação. Se as duas forem iguais, protege a senha, cria o Aluno, adiciona à lista e salva. existe é uma variável booleana que registra o resultado da busca por duplicidade.

## 15. O bloco final

```python
if __name__ == "__main__":
    try:
        executar()
```

Quando você roda python main.py, o Python define __name__ como __main__ e entra nesse bloco. Quando outro arquivo importa main, as definições são carregadas e esse bloco não inicia o menu.

OSError representa uma falha de acesso ou gravação e gera uma mensagem. KeyboardInterrupt corresponde à interrupção por teclado, e EOFError ocorre se a entrada termina. O bloco final trata essas interrupções com uma mensagem de encerramento.

## 16. Símbolos e comandos que podem aparecer nas perguntas

| Código | Significado |
| --- | --- |
| = | Atribui um valor a uma variável ou atributo. |
| == e != | Comparam igualdade e diferença. |
| and e or | Combinam condições. |
| not | Inverte uma condição. |
| True e False | Valores booleanos, verdadeiro e falso. |
| None | Ausência de um objeto selecionado ou de um resultado. |
| [] | Lista. Guarda uma sequência de registros ou objetos. |
| {} | Dicionário. Guarda valores identificados por chaves. |
| def | Define uma função ou método. |
| return | Entrega o resultado ao trecho que chamou a função. |
| for | Percorre os elementos de uma coleção. |
| while | Repete um bloco enquanto a condição for verdadeira. |
| if, elif e else | Selecionam qual bloco executar conforme as condições. |
| try e except | Tentam uma operação e tratam o tipo de erro esperado. |
| raise | Sinaliza um erro para o trecho que chamou o método. |
| # | Inicia um comentário que serve para leitura e é ignorado na execução. |
| Recuo das linhas | Define os blocos que pertencem à função, à condição ou ao laço. |

## 17. Uma sequência para explicar a colaboração

> O aluno entra na conta e o menu cria um pedido ligado a ele e ao objeto escolhido. Quando o responsável aprova, o método analisar chama aprovar no pedido. O pedido chama reservar no Item. Depois, na retirada, entregar confere o RA e chama devolver no Item. O main grava as mudanças no JSON.

O fluxo de aprovação fica assim.

```text
menu_responsavel
  -> responsavel.analisar
     -> pedido.aprovar
        -> item.reservar
  -> salvar
```

Essa sequência demonstra a colaboração entre os objetos. Cada classe concentra as informações e ações que representa.

## 18. Perguntas de revisão

1. Qual é a diferença entre um aviso de perda e uma solicitação de retirada?
2. Se Ana e José chamam informar_perda, qual objeto self representa em cada chamada?
3. O que super reaproveita nos construtores das classes filhas?
4. Por que perfil é um exemplo de sobrescrita e receber_usuario demonstra polimorfismo?
5. Como @property e __situacao ajudam a controlar a alteração de estados?
6. Por que Item precisa estar reservado antes de ser devolvido?
7. Por que guardar o código do item e o RA do aluno no JSON?
8. Como o carregamento recupera os relacionamentos entre objetos?
9. O que acontece se a identificação ou a senha estiver incorreta?
10. Como marcar uma perda como resolvida afeta a lista pública e o histórico?

Pratique acompanhando uma ação real do menu e apontando a chamada no código. Use os exemplos de fala como apoio e explique as instruções com suas próprias palavras.


## Conferência do JSON antes de carregar

A revisão de 14/11/2026 acrescentou duas funções de conferência em main.py. conferir_registro recebe um registro e uma lista de campos com os tipos esperados. Ela verifica se o registro é um dicionário, se os campos obrigatórios existem e se possuem conteúdo do tipo correto. conferir_dados aplica essa verificação às listas de alunos, objetos e pedidos.

Durante o carregamento, o programa também recusa RAs ou códigos repetidos e verifica se a situação de cada pedido corresponde à do objeto. Um pedido aprovado exige um objeto aguardando retirada. Um pedido entregue exige um objeto devolvido. Um objeto reservado ou devolvido deve ter um único pedido de retirada correspondente.

Se o arquivo estiver inválido, o programa mostra a mensagem de carregamento e preserva o JSON. Essas verificações ajudam a evitar uma falha posterior nos menus. Contas antigas com nome numérico continuam preservadas, mas novos cadastros exigem um nome válido.

# Achados e Perdidos

Projeto didático de programação orientada a objetos em Python. O sistema roda no terminal e tem dois perfis. O aluno registra perdas e solicita objetos encontrados. O responsável cadastra os objetos recebidos, analisa os pedidos e registra as entregas.

## Como executar

Com o Python 3 instalado, abra o terminal na pasta **Poo** e execute:

```powershell
python main.py
```

O programa usa apenas a biblioteca padrão do Python. Digite o número da opção desejada e pressione Enter. Nos menus de aluno e responsável, **0** volta à tela inicial. Na tela inicial, **0** encerra o programa.

## Cadastro e login

| Perfil | Identificação | Senha |
| --- | --- | --- |
| Aluno | RA de exatamente 12 dígitos | Senha criada no cadastro |
| Responsável | `12responsavel34` | `1234` |

Para cadastrar um aluno, escolha **2 - Criar conta de aluno**. Informe nome, RA, senha e confirmação da senha. O RA precisa ser único e pode começar com zero. Depois, escolha **1 - Entrar na conta** e informe o RA e a senha.

O responsável usa a mesma opção **1 - Entrar na conta** com o código e a senha de demonstração da tabela. Essa conta já está definida em `main.py`.

## Para que serve o Achados e Perdidos

O sistema ajuda os estudantes a recuperar objetos perdidos na faculdade e organiza o trabalho de quem recebe e guarda os objetos encontrados. Ele registra quem está procurando algo, quais objetos chegaram à sala de achados e perdidos, os pedidos de retirada e as entregas realizadas.

Um guarda, um responsável da faculdade ou outra pessoa pode encontrar um objeto. Ao receber esse objeto, o responsável faz o cadastro no sistema. O estudante consulta a lista e apresenta informações para comprovar que o objeto pode ser seu. O responsável compara essas informações antes de autorizar a retirada.

### O que cada registro significa

| Registro | Significado | Exemplo |
| --- | --- | --- |
| Objeto encontrado | Item que já foi recebido e cadastrado pelo responsável. | Uma garrafa está guardada na sala de achados e perdidos. |
| Aviso de perda | Informação de um estudante sobre algo que ele perdeu. | José informa que perdeu uma garrafa na biblioteca. |
| Pedido de retirada | Solicitação de um estudante para receber um item encontrado específico. | José escolhe o código da garrafa e descreve suas características. |

O aviso de perda pode ser registrado antes de alguém encontrar o objeto. Quando um possível objeto aparece na lista, o estudante faz um pedido de retirada pela opção 5.

## Menu do aluno

### 1 — Objetos encontrados e guardados na faculdade

Use para procurar algo que possa ser seu entre os itens disponíveis que já estão com o responsável. A lista mostra somente **código e nome**. Local, data e características do objeto encontrado ficam reservados ao responsável para a conferência.

Ao reconhecer um possível objeto, anote o código e use a opção 5 para solicitar a retirada. Consultar a lista permite conhecer os itens disponíveis, e a solicitação registra o pedido que será analisado.

### 2 — Objetos que os alunos estão procurando

Mostra os avisos de perda em aberto dos estudantes, com nome do objeto, local e data informados por quem perdeu. Essa lista ajuda a divulgar o que está sendo procurado. As características detalhadas e o RA ficam nas consultas autorizadas.

Por exemplo, o aviso “Estojo, biblioteca, 10/11/2026” significa que um aluno informou essa perda. Se você encontrar um estojo, entregue ao responsável da faculdade para cadastro e conferência.

### 3 — Informar uma perda

Use assim que perceber que perdeu alguma coisa. Informe o nome do objeto, onde perdeu, a data aproximada e suas características, como cor, marca e algum detalhe particular.

O aviso aparece na opção 2 enquanto estiver em aberto. O responsável também consegue consultar sua descrição. Você pode registrar mais de uma perda.

### 4 — Ver minhas perdas

Mostra o histórico dos avisos registrados pela sua própria conta. Cada aviso tem um número, os dados que você informou e a situação **em aberto** ou **resolvida**.

Use para conferir o que registrou e identificar o número do aviso que deseja encerrar na opção 7.

### 5 — Solicitar um objeto: pode ser meu

Use quando houver na lista um objeto que você acredita ser seu. A tela mostra somente código e nome. Informe o código e depois descreva **onde perdeu, a data aproximada e as características** que conhece.

O responsável comparará sua descrição com o cadastro reservado do objeto encontrado. O pedido começa **em análise**. Uma solicitação repetida para o mesmo objeto enquanto seu pedido estiver em análise é recusada pelo sistema. Digite 0 na seleção do objeto para voltar ao menu.

### 6 — Meus pedidos

Mostra os pedidos de retirada feitos pela sua conta, a situação de cada um e a resposta do responsável.

| Situação | O que significa e o que fazer |
| --- | --- |
| Em análise | O pedido está aguardando a conferência do responsável. |
| Aprovado para retirada | A retirada foi autorizada. Leia a resposta e procure a sala de achados e perdidos com sua identificação. |
| Recusado | Leia o motivo informado pelo responsável. |
| Entregue | O responsável confirmou que o objeto foi entregue ao aluno aprovado. |

### 7 — Marcar minha perda como resolvida

Use depois de recuperar algo que você registrou como perdido. Isso também se aplica quando você encontra o objeto por conta própria, como dentro da mochila.

Escolha o número de um dos seus avisos. Ele passa para **resolvida**, sai da opção 2 e continua no histórico da opção 4. A situação fica salva no JSON. Só é possível resolver avisos da própria conta. Digite 0 para voltar sem selecionar um aviso.

Essa opção encerra o aviso de procura. A autorização de retirada e a entrega de um objeto cadastrado são registradas pelo responsável nas opções próprias do painel dele.

### 0 — Sair da conta

Volta à tela de login e permite que outra pessoa entre com a própria conta. As alterações já realizadas ficam salvas. Para encerrar o programa, escolha 0 também na tela inicial.

## Menu do responsável

### 1 — Cadastrar objeto encontrado

Use quando receber um objeto encontrado na faculdade. Informe um **nome genérico**, como “Garrafa”, além do local, data e características reais do objeto. O local de guarda fica definido como **Sala de achados e perdidos**.

Os estudantes veem somente código e nome. Preencha cor, marca, adesivos e outros detalhes no campo de características reservadas. O cadastro torna o objeto disponível para solicitações.

### 2 — Consultar objetos e detalhes reservados

Permite consultar os objetos recebidos, incluindo local, data, características, local de guarda e situação. Serve para controlar o que está disponível, reservado para retirada ou já devolvido.

### 3 — Consultar perdas dos alunos

Mostra os avisos de perda com nome e RA do estudante, descrição, local, data e situação. Ajuda o responsável a conhecer os objetos procurados e identificar possíveis correspondências com os itens recebidos. Os avisos resolvidos continuam disponíveis no histórico.

### 4 — Analisar pedidos

Use para conferir uma solicitação de retirada. Selecione o código de um pedido em análise. A tela apresenta a descrição do aluno e o registro reservado do objeto para comparar local, data e características.

- Escolha **1 para aprovar** quando a conferência indicar que o objeto corresponde ao pedido. Escreva a orientação de retirada. O objeto fica reservado para aquele aluno, e outros pedidos em análise para o mesmo item são recusados.
- Escolha **2 para recusar** quando as informações não corresponderem. Escreva o motivo para o aluno consultar.
- Escolha **0 para voltar** e deixar a análise para depois.

A decisão é tomada pelo responsável. Escreva respostas que orientem o estudante e mantenha as características usadas na conferência nos campos reservados.

### 5 — Registrar entrega

Use no momento da retirada presencial de um objeto com pedido aprovado. Selecione o pedido, confira a identificação do estudante, informe o RA e confirme que o objeto foi entregue.

O RA deve corresponder ao aluno autorizado. Após a confirmação, o pedido fica **entregue** e o objeto fica **devolvido**. Aprovar reserva o objeto para retirada. Registrar a entrega confirma que a pessoa efetivamente o recebeu.

### 0 — Sair da conta

Encerra o acesso ao painel e volta à tela de login. Os registros ficam salvos.

## Caminho completo de um atendimento

1. José percebe que perdeu uma garrafa e registra um aviso pela opção 3 do aluno.
2. Um guarda encontra uma garrafa e a entrega ao responsável da faculdade.
3. O responsável cadastra o objeto pela opção 1 do seu painel, com local, data e características.
4. José consulta a opção 1 do aluno e vê o código e o nome da garrafa.
5. José usa a opção 5, escolhe o código e informa onde, quando e quais características a garrafa tinha.
6. O responsável usa a opção 4, compara as informações e aprova a retirada se corresponderem.
7. José acompanha o resultado em Meus pedidos, opção 6, e vai à sala de achados e perdidos.
8. O responsável confere a identificação e registra a entrega pela opção 5 do painel.
9. José marca seu aviso de perda como resolvido pela opção 7. Ele permanece no histórico e sai da lista de objetos procurados.

Informe as datas no formato **DD/MM/AAAA**. O programa aceita datas válidas até o dia atual e salva as alterações no JSON.

## O que explicar na apresentação do projeto

Demonstrem o atendimento acima pelos menus e expliquem por que cada etapa existe. O sistema precisa distinguir o aviso de quem perdeu algo, o cadastro de um objeto recebido e o pedido de quem quer retirá-lo. Mostrem também uma entrada inválida, uma recusa e a recuperação dos dados ao fechar e abrir o programa.

| Parte demonstrada | Código e conceito para explicar |
| --- | --- |
| Cadastro e login | Aluno e Responsavel herdam de Usuario. A autenticação é compartilhada e o método perfil tem uma implementação em cada classe filha. |
| Registro de perda | Aluno guarda seus próprios avisos na lista perdas. self identifica o aluno que está executando o método. |
| Cadastro de objeto | Responsavel cria um objeto Item e o adiciona à sua lista. |
| Solicitação | Solicitacao guarda referências ao Aluno e ao Item envolvidos no pedido. |
| Aprovação e entrega | Os métodos verificam as regras e alteram as situações encapsuladas dos pedidos e itens. |
| Encerramento do aviso | Aluno.resolver_perda muda a situação de um aviso da própria conta e preserva o histórico. |
| Reabertura do programa | salvar e carregar em main.py gravam e recuperam registros e relacionamentos no dados.json. |

Cada integrante deve conseguir acompanhar esse caminho e explicar as classes, o self, os construtores, a herança, o encapsulamento e os relacionamentos. O [guia de classes](documentacao/CLASSES.md) detalha esses conceitos, e o [roteiro de testes](documentacao/TESTES.md) orienta a demonstração e o registro de evidências.

## Onde os dados ficam salvos

O programa cria o arquivo `dados.json` na pasta **Poo** ao gravar o primeiro registro. O arquivo guarda os alunos, as perdas de cada aluno, os objetos encontrados e os pedidos com suas situações e respostas. Cada pedido usa o RA do aluno e o código do objeto para restabelecer essa ligação ao abrir o programa.

Os dados são carregados automaticamente ao iniciar `main.py` e gravados a cada alteração. As senhas dos alunos são armazenadas como hashes. Os detalhes reservados ficam disponíveis no painel do responsável e também constam no arquivo local.

## Arquivos e classes

| Arquivo | Responsabilidade |
| --- | --- |
| [usuario.py](usuario.py) | Classe base Usuario, com autenticação e senha encapsulada. |
| [main.py](main.py) | Inicia o programa, valida entradas, apresenta os menus e lê e grava o JSON. |
| [aluno.py](aluno.py) | A classe `Aluno` herda Usuario e guarda nome, RA, senha protegida e avisos de perda. |
| [item.py](item.py) | A classe `Item` representa um objeto encontrado e sua situação. |
| [responsavel.py](responsavel.py) | A classe `Responsavel` herda Usuario, cadastra objetos, decide pedidos e registra entregas. |
| [solicitacao.py](solicitacao.py) | A classe `Solicitacao` liga um aluno a um objeto e guarda o andamento do pedido. |
| `dados.json` | Guarda os registros entre execuções. |

Por exemplo, em `self.nome = nome`, `self` representa o objeto que está sendo criado. Assim, cada aluno tem seu próprio nome e sua própria lista de perdas. Uma solicitação usa `self.aluno` e `self.item` para relacionar quem pediu com o objeto solicitado.


## Material para o barema

- [CLASSES.md](documentacao/CLASSES.md) contém o diagrama e a explicação de herança, encapsulamento, sobrescrita, polimorfismo e relacionamentos.
- [TESTES.md](documentacao/TESTES.md) contém um roteiro de testes pelos próprios menus, com resultados esperados e orientações para registrar evidências.


## Organização das pastas

- A raiz contém main.py, as classes e dados.json. Execute o programa com python main.py.
- documentacao contém o diagrama de classes e o roteiro de apresentação e testes.

Uma perda pode estar **em aberto** ou **resolvida**. A opção 7 altera somente um aviso da conta conectada. Resolver um aviso não aprova pedidos nem registra a entrega de um objeto. Avisos antigos sem situação são carregados como em aberto.

## Guia para estudar e explicar o código

Os arquivos Python têm comentários explicativos. O [guia completo do código](documentacao/EXPLICACAO_CODIGO.md) explica os comandos, cada classe, as funções dos menus, o JSON e exemplos de fala para a apresentação.

# Roteiro de testes pelos menus

Execute python main.py e siga os passos abaixo. Use dados de exemplo. Para registrar as evidências, tire capturas do terminal com os resultados e apresente os fluxos ao professor. O barema aceita testes ou roteiro de testes com evidências.

## Sequência para demonstrar

| Etapa | Ação | Resultado esperado |
| --- | --- | --- |
| 1 | Cadastre um aluno. Tente um nome com números e depois um nome com letras. Tente um RA curto e depois informe um RA de 12 números. | O programa recusa o nome numérico e o RA curto e aceita os dados válidos. |
| 2 | Tente entrar com senha errada e depois com a correta. | Só a senha correta permite entrar. |
| 3 | Entre como responsável usando código 12responsavel34 e senha 1234. Cadastre uma garrafa com local, data e características. | O objeto aparece no painel com os detalhes. |
| 4 | Entre como aluno e abra as opções 1 e 5. | As listas mostram apenas código e nome do objeto. |
| 5 | Na opção 3 do aluno, registre uma perda. Confira as opções 2 e 4. | O aviso aparece na lista de procurados e no histórico do aluno. |
| 6 | Use a opção 5 para pedir a garrafa. Informe onde e quando perdeu e suas características. Tente repetir o pedido. | O primeiro pedido fica em análise e a duplicidade é recusada. |
| 7 | No painel do responsável, use a opção 4 e compare as descrições. Aprove com uma orientação de retirada. | O pedido fica aprovado e o objeto fica reservado. |
| 8 | Entre como aluno e abra Meus pedidos. | A aprovação e a orientação de retirada aparecem. |
| 9 | Encerre e abra o programa novamente. | As contas, perdas, objetos e pedidos continuam salvos. |
| 10 | No painel do responsável, registre a entrega. Primeiro tente outro RA, depois informe o RA aprovado. | O RA errado é recusado. Com o RA certo, o pedido fica entregue e o objeto devolvido. |
| 11 | Na conta do aluno, use a opção 7 para resolver a perda registrada. | Ela sai da opção 2 e continua na opção 4 como resolvida, inclusive após reabrir. |
| 12 | Faça um segundo exemplo e recuse o pedido com um motivo. | O aluno vê a resposta e o objeto continua disponível. |

## Evidências do grupo

Depois de realizar a sequência, registrem a data, quem executou e o resultado observado. Guardem as capturas para mostrar ao professor. Preencham os resultados com o que foi verificado pelo grupo.

## O que cada integrante deve saber explicar

- A função de cada classe.
- O significado de self e __init__.
- A herança de Usuario em Aluno e Responsavel.
- A sobrescrita de perfil e seu uso em receber_usuario.
- A proteção da senha e das situações com atributos privados e propriedades.
- O relacionamento entre aluno, item e solicitação.
- A gravação e a leitura do dados.json.

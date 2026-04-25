# cantina-Fatec-2026
# Sistema de Cantina – Projeto FATEC
## Estrutura do Projeto

- main.py → ponto de entrada do sistema
- sistema.py → regras de negócio (vendas e relatórios)
- estoque.py → controle de estoque com lista encadeada (FIFO)
- modelos.py → classes do sistema (Produto, Lote, Pagamento, Consumo)

## Conceitos Utilizados

- Programação Orientada a Objetos (POO)
- Estrutura de Dados: Lista Encadeada
- FIFO (First In, First Out)
- Persistência com pickle

## Funcionalidades

- Cadastro de produtos em lote
- Controle de estoque
- Venda de produtos
- Relatórios de vendas e lucro
- Alerta de produtos próximos do vencimento

 ## Bibliotecas utilizadas

O sistema foi desenvolvido utilizando bibliotecas padrão da linguagem Python e uma biblioteca externa para melhoria da visualização no terminal.

Bibliotecas padrão do Python
datetime
Utilizada para manipulação de datas e horários, sendo aplicada no controle de validade dos produtos e no registro das operações do sistema.
pickle
Utilizada para serialização de dados, permitindo salvar e recuperar o estado do sistema em arquivos, garantindo persistência das informações entre execuções.
Biblioteca externa
tabulate
Utilizada para exibição de dados em formato de tabela no terminal, proporcionando melhor organização e legibilidade das informações de estoque e relatórios.
Instalação da dependência externa

Para instalar a biblioteca necessária:

pip install tabulate

import pickle
import random
from datetime import datetime, date
from faker import Faker
from tabulate import tabulate


# =========================
# MODELOS
# =========================

class Produto:
    def __init__(self, nome, preco_compra, preco_venda):
        self.nome = nome
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda


class Pagamento:
    def __init__(self, nome_pagador, categoria, curso, valor_pago):
        self.nome_pagador = nome_pagador
        self.categoria = categoria
        self.curso = curso
        self.valor_pago = valor_pago
        self.data_hora = datetime.now()


class Consumo:
    def __init__(self, nome_consumidor, produto, quantidade, valor_total):
        self.nome_consumidor = nome_consumidor
        self.produto = produto
        self.quantidade = quantidade
        self.valor_total = valor_total
        self.data = datetime.now()


# =========================
# NÓS LISTA ENCADEADA
# =========================

class Lote:
    def __init__(self, id_lote, produto, data_compra, data_validade, quantidade):
        self.id_lote = id_lote
        self.produto = produto
        self.data_compra = data_compra
        self.data_validade = data_validade
        self.quantidade = quantidade
        self.proximo = None


class RegistroPagamento:
    def __init__(self, id_transacao, pagamento):
        self.id_transacao = id_transacao
        self.pagamento = pagamento
        self.proximo = None


class RegistroConsumo:
    def __init__(self, id_consumo, consumo):
        self.id_consumo = id_consumo
        self.consumo = consumo
        self.proximo = None


# =========================
# ESTOQUE
# =========================

class Estoque:

    def __init__(self):
        self.inicio = None
        self._contador_lotes = 0

    def proximo_id(self):
        self._contador_lotes += 1
        return self._contador_lotes

    def adicionar_lote(self, novo_lote):

        if self.inicio is None:
            self.inicio = novo_lote
            return

        atual = self.inicio

        while atual.proximo:
            atual = atual.proximo

        atual.proximo = novo_lote

    def baixar_estoque(self, nome_produto, qtd):

        restante = qtd
        atual = self.inicio

        while atual and restante > 0:

            if atual.produto.nome == nome_produto:

                if atual.quantidade >= restante:
                    atual.quantidade -= restante
                    restante = 0
                else:
                    restante -= atual.quantidade
                    atual.quantidade = 0

            atual = atual.proximo

        return restante == 0

    def get_saldo(self, nome_produto):

        total = 0
        atual = self.inicio

        while atual:

            if atual.produto.nome == nome_produto:
                total += atual.quantidade

            atual = atual.proximo

        return total

    def listar_estoque(self):

        atual = self.inicio
        tabela = []

        while atual:

            tabela.append([
                atual.id_lote,
                atual.produto.nome,
                atual.quantidade,
                atual.data_validade
            ])

            atual = atual.proximo

        print("\n===== ESTOQUE =====")

        print(tabulate(
            tabela,
            headers=["Lote", "Produto", "Qtd", "Validade"],
            tablefmt="grid"
        ))

    def listar_produtos_disponiveis(self):

        vistos = {}
        atual = self.inicio

        while atual:

            nome = atual.produto.nome

            if nome not in vistos and self.get_saldo(nome) > 0:
                vistos[nome] = atual.produto

            atual = atual.proximo

        return list(vistos.values())


# =========================
# SISTEMA
# =========================

class SistemaCantina:

    def __init__(self, estoque):

        self.estoque = estoque
        self.historico_pagamentos = None
        self.historico_consumos = None

        self.cont_pgto = 0
        self.cont_consumo = 0

    def realizar_venda(self, nome, categoria, curso, produto, qtd):

        if not self.estoque.baixar_estoque(produto.nome, qtd):
            print("Estoque insuficiente.")
            return

        valor_total = produto.preco_venda * qtd

        self.cont_pgto += 1
        pagamento = Pagamento(nome, categoria, curso, valor_total)

        reg = RegistroPagamento(self.cont_pgto, pagamento)
        reg.proximo = self.historico_pagamentos
        self.historico_pagamentos = reg

        self.cont_consumo += 1
        consumo = Consumo(nome, produto, qtd, valor_total)

        regc = RegistroConsumo(self.cont_consumo, consumo)
        regc.proximo = self.historico_consumos
        self.historico_consumos = regc

        print("\nVenda registrada!")

    def relatorio_vendas(self):

        atual = self.historico_pagamentos

        while atual:
            p = atual.pagamento
            print(atual.id_transacao, p.nome_pagador, p.valor_pago)
            atual = atual.proximo


# =========================
# PERSISTÊNCIA
# =========================

ARQUIVO_DADOS = "cantina.pkl"

def salvar_dados(sistema):

    with open(ARQUIVO_DADOS, "wb") as f:
        pickle.dump(sistema, f)


def carregar_dados():

    try:
        with open(ARQUIVO_DADOS, "rb") as f:
            return pickle.load(f)
    except:
        return None


# =========================
# ESTOQUE PADRÃO
# =========================

def sistema_padrao():

    estoque = Estoque()

    produtos = [

        Produto("Hitt Nuts",1.5,3),
        Produto("Pão de Mel",1.8,3),
        Produto("Bala Bon",0.8,1.5),
        Produto("Paçoca",0.8,1.5),
        Produto("Trento",1.5,3),
        Produto("KitKat",2.5,4),
        Produto("Amendoim Japonês",1.5,3),
        Produto("Chips",2.5,4.5),
        Produto("Salgadinho",2,3.5),

        Produto("Coca-Cola Lata",3.5,5),
        Produto("Guaraná Lata",3.5,5),
        Produto("Fanta Lata",3.5,5),
        Produto("Água Mineral",1.5,3),
        Produto("H2O",3.5,5.5),
        Produto("Energético",5,8)

    ]

    for p in produtos:

        estoque.adicionar_lote(
            Lote(estoque.proximo_id(),p,date.today(),date(2026,12,31),50)
        )

    return SistemaCantina(estoque)


# =========================
# MENU
# =========================

def menu():

    print("\n===== CANTINA FATEC =====")
    print("1 Venda")
    print("2 Estoque")
    print("3 Relatório vendas")
    print("6 Reiniciar sistema")
    print("0 Sair")

    return input("Opção: ")


# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":

    sistema = carregar_dados()

    if sistema is None:
        sistema = sistema_padrao()

    while True:

        op = menu()

        if op == "1":

            nome = input("Nome: ")

            produtos = sistema.estoque.listar_produtos_disponiveis()

            for i,p in enumerate(produtos):
                print(i+1,p.nome)

            escolha = int(input("Produto: ")) - 1

            qtd = int(input("Quantidade: "))

            sistema.realizar_venda(
                nome,"Aluno","IA",
                produtos[escolha],
                qtd
            )

        elif op == "2":

            sistema.estoque.listar_estoque()

        elif op == "3":

            sistema.relatorio_vendas()

        elif op == "6":

            sistema = sistema_padrao()
            salvar_dados(sistema)
            print("Sistema reiniciado.")

        elif op == "0":

            salvar_dados(sistema)
            break1
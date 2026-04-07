import pickle
import random
from datetime import datetime, date
from faker import Faker
from tabulate import tabulate


# =========================
# MODELOS
# =========================

# =========================
# Classe Produto (ENCAPSULADA)
# =========================

class Produto:

    def __init__(self, nome, preco_compra, preco_venda):

        # ATRIBUTOS PRIVADOS (encapsulamento)
        self._nome = nome
        self._preco_compra = preco_compra
        self._preco_venda = preco_venda


    # =========================
    # GETTER nome
    # =========================
    @property
    def nome(self):
        return self._nome


    # =========================
    # GETTER preco_compra
    # =========================
    @property
    def preco_compra(self):
        return self._preco_compra


    # =========================
    # GETTER preco_venda
    # =========================
    @property
    def preco_venda(self):
        return self._preco_venda


    # =========================
    # SETTER preco_venda
    # =========================
    @preco_venda.setter
    def preco_venda(self, valor):

        if valor > 0:
            self._preco_venda = valor
        else:
            print("Preço de venda inválido!")


    # =========================
    # MÉTODO EXTRA (DIFERENCIAL)
    # =========================
    def calcular_lucro(self):
        return self._preco_venda - self._preco_compra


    # =========================
    # REPRESENTAÇÃO (BONITO NO PRINT)
    # =========================
    def __str__(self):
        return f"{self._nome} | Venda: R$ {self._preco_venda:.2f}"


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

# =========================
# Classe Estoque (LISTA ENCADEADA + FIFO)
# =========================
class Estoque:

    def __init__(self):
        # início da lista encadeada
        self.inicio = None
        self._contador_lotes = 0

    def proximo_id(self):
        self._contador_lotes += 1
        return self._contador_lotes
    # =========================
    # ADICIONAR LOTE (INSERÇÃO)
    # =========================
    def adicionar_lote(self, novo_lote):

        # Se lista vazia OU validade menor → entra no início
        if self.inicio is None or novo_lote.data_validade < self.inicio.data_validade:
            novo_lote.proximo = self.inicio
            self.inicio = novo_lote
            return

        atual = self.inicio

        # percorre a lista encadeada
        # AQUI ESTAMOS ANDANDO NOS NÓS
        while atual.proximo and atual.proximo.data_validade < novo_lote.data_validade:
            atual = atual.proximo

        # liga o novo nó na lista
        novo_lote.proximo = atual.proximo
        atual.proximo = novo_lote

    # =========================
    # BAIXAR ESTOQUE (FIFO)
    # =========================
    def baixar_estoque(self, nome_produto, qtd):

        # verifica saldo antes
        if self.get_saldo(nome_produto) < qtd:
            return False

        restante = qtd
        atual = self.inicio

        # percorre lista encadeada
        # AQUI COMEÇA O FIFO (primeiro que entra sai primeiro)
        while atual and restante > 0:

            if atual.produto.nome == nome_produto:

                if atual.quantidade >= restante:
                    atual.quantidade -= restante
                    restante = 0
                else:
                    restante -= atual.quantidade
                    atual.quantidade = 0

            # vai para o próximo nó
            atual = atual.proximo

        return True

    # =========================
    # SALDO TOTAL DO PRODUTO
    # =========================
    def get_saldo(self, nome_produto):

        total = 0
        atual = self.inicio

        # percorre todos os nós
        while atual:

            if atual.produto.nome == nome_produto:
                total += atual.quantidade

            atual = atual.proximo

        return total

    # =========================
    # LISTAR ESTOQUE
    # =========================
    def listar_estoque(self):

        print("\n===== ESTOQUE =====")

        atual = self.inicio

        if atual is None:
            print("Estoque vazio.")
            return

        while atual is not None:
            print(
                f"Lote {atual.id_lote} | Produto: {atual.produto.nome} | "
                f"Qtd: {atual.quantidade} | Validade: {atual.data_validade}"
            )
            atual = atual.proximo

    # =========================
    # LISTAR PRODUTOS DISPONÍVEIS
    # =========================
    def listar_produtos_disponiveis(self):

        produtos_vistos = {}
        atual = self.inicio

        while atual is not None:
            if atual.quantidade > 0 and atual.produto.nome not in produtos_vistos:
                produtos_vistos[atual.produto.nome] = atual.produto
            atual = atual.proximo

        return list(produtos_vistos.values())
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
            break
        
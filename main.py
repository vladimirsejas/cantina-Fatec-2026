import pickle
import random
from datetime import datetime, date
from faker import Faker
from tabulate import tabulate

ARQUIVO_DADOS = "cantina.pkl"

# =============================
# CLASSES
# =============================

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


# =============================
# NÓS LISTA ENCADEADA
# =============================

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


# =============================
# ESTOQUE
# =============================

class Estoque:

    def __init__(self):

        self.inicio = None
        self._contador_lotes = 0


    def proximo_id(self):

        self._contador_lotes += 1
        return self._contador_lotes


    def adicionar_lote(self, novo_lote):

        if self.inicio is None or novo_lote.data_validade < self.inicio.data_validade:

            novo_lote.proximo = self.inicio
            self.inicio = novo_lote
            return

        atual = self.inicio

        while atual.proximo and atual.proximo.data_validade < novo_lote.data_validade:

            atual = atual.proximo

        novo_lote.proximo = atual.proximo
        atual.proximo = novo_lote


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

        if tabela:

            print(tabulate(
                tabela,
                headers=["Lote", "Produto", "Qtd", "Validade"],
                tablefmt="grid"
            ))

        else:

            print("Estoque vazio.")


    def get_saldo(self, nome_prod):

        total = 0
        atual = self.inicio

        while atual:

            if atual.produto.nome == nome_prod:
                total += atual.quantidade

            atual = atual.proximo

        return total


    def baixar_estoque(self, nome_prod, qtd):

        if self.get_saldo(nome_prod) < qtd:
            return False

        restante = qtd
        atual = self.inicio

        while atual and restante > 0:

            if atual.produto.nome == nome_prod:

                if atual.quantidade >= restante:

                    atual.quantidade -= restante
                    restante = 0

                else:

                    restante -= atual.quantidade
                    atual.quantidade = 0

            atual = atual.proximo

        return True


    def editar_quantidade(self, id_lote, nova):

        atual = self.inicio

        while atual:

            if atual.id_lote == id_lote:

                atual.quantidade = nova
                print("Quantidade atualizada.")
                return

            atual = atual.proximo

        print("Lote não encontrado.")


# =============================
# SISTEMA
# =============================

class SistemaCantina:

    def __init__(self, estoque):

        self.estoque = estoque
        self.historico_pagamentos = None
        self.historico_consumos = None
        self.contador_pgto = 0
        self.contador_consumo = 0


    def realizar_venda(self, nome, categoria, curso, produto, qtd):

        if not self.estoque.baixar_estoque(produto, qtd):
            print("Estoque insuficiente.")
            return

        preco = self.buscar_preco(produto)
        total = preco * qtd

        self.contador_pgto += 1
        pg = Pagamento(nome, categoria, curso, total)
        reg = RegistroPagamento(self.contador_pgto, pg)

        reg.proximo = self.historico_pagamentos
        self.historico_pagamentos = reg

        self.contador_consumo += 1
        cons = Consumo(nome, Produto(produto,0,preco), qtd, total)
        regc = RegistroConsumo(self.contador_consumo, cons)

        regc.proximo = self.historico_consumos
        self.historico_consumos = regc

        print("Venda realizada.")


    def buscar_preco(self, nome):

        atual = self.estoque.inicio

        while atual:

            if atual.produto.nome == nome:
                return atual.produto.preco_venda

            atual = atual.proximo

        return 0


    def relatorio_vendas(self):

        atual = self.historico_pagamentos

        while atual:

            p = atual.pagamento

            print(
                atual.id_transacao,
                p.nome_pagador,
                p.valor_pago,
                p.data_hora
            )

            atual = atual.proximo


    def relatorio_consumo(self):

        atual = self.historico_consumos

        while atual:

            c = atual.consumo

            print(
                atual.id_consumo,
                c.nome_consumidor,
                c.produto.nome,
                c.quantidade
            )

            atual = atual.proximo


# =============================
# PERSISTÊNCIA
# =============================

def salvar_dados(sistema):

    with open(ARQUIVO_DADOS,"wb") as f:

        pickle.dump(sistema,f)

    print("Dados salvos.")


def carregar_dados():

    try:

        with open(ARQUIVO_DADOS,"rb") as f:

            return pickle.load(f)

    except:

        return None


# =============================
# MENU
# =============================

def menu():

    print("\n===== CANTINA FATEC =====")

    print("1 Venda")
    print("2 Estoque")
    print("3 Relatório vendas")
    print("4 Relatório consumo")
    print("5 Faker vendas")
    print("0 Sair")

    return input("Opção: ")


# =============================
# INICIALIZAÇÃO
# =============================

def sistema_padrao():

    estoque = Estoque()

    p1 = Produto("Hitt Nuts",1.5,3)
    p2 = Produto("Pão de Mel",1.8,3)
    p3 = Produto("Bala Bon",0.8,1.5)

    estoque.adicionar_lote(Lote(1,p1,date.today(),date(2026,12,31),50))
    estoque.adicionar_lote(Lote(2,p2,date.today(),date(2026,10,1),30))
    estoque.adicionar_lote(Lote(3,p3,date.today(),date(2026,9,1),60))

    return SistemaCantina(estoque)


# =============================
# MAIN
# =============================

if __name__ == "__main__":

    sistema = carregar_dados()

    if sistema is None:

        sistema = sistema_padrao()

    while True:

        op = menu()

        if op == "1":

            nome = input("Nome: ")
            cat = input("Categoria: ")
            curso = input("Curso: ")
            prod = input("Produto: ")
            qtd = int(input("Qtd: "))

            sistema.realizar_venda(nome,cat,curso,prod,qtd)

        elif op == "2":

            sistema.estoque.listar_estoque()

        elif op == "3":

            sistema.relatorio_vendas()

        elif op == "4":

            sistema.relatorio_consumo()

        elif op == "5":

            fake = Faker("pt_BR")

            for _ in range(5):

                sistema.realizar_venda(
                    fake.name(),
                    random.choice(["Aluno","Professor"]),
                    random.choice(["IA","ESG"]),
                    random.choice(["Hitt Nuts","Pão de Mel","Bala Bon"]),
                    1
                )

        elif op == "0":

            salvar_dados(sistema)
            break
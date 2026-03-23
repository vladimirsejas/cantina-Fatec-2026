import pickle
import random
from datetime import datetime, date
from faker import Faker


# =============================================================================
# CLASSES DE MODELO
# =============================================================================

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


# =============================================================================
# NÓS DAS LISTAS ENCADEADAS
# =============================================================================

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

    def __str__(self):
        return (
            f"Consumo ID: {self.id_consumo} | "
            f"{self.consumo.nome_consumidor} | "
            f"{self.consumo.quantidade}x {self.consumo.produto.nome} | "
            f"R$ {self.consumo.valor_total:.2f}"
        )


# =============================================================================
# CONTROLE DE ESTOQUE
# =============================================================================

class Estoque:

    def __init__(self):
        self.inicio = None


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


    def baixar_estoque(self, nome_produto, qtd):

        if self.get_saldo(nome_produto) < qtd:
            return False

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

        return True


    def get_saldo(self, nome_produto):

        total = 0
        atual = self.inicio

        while atual:

            if atual.produto.nome == nome_produto:
                total += atual.quantidade

            atual = atual.proximo

        return total


# =============================================================================
# SISTEMA PRINCIPAL
# =============================================================================

class SistemaCantina:

    def __init__(self, estoque):

        self.estoque = estoque
        self.historico_pagamentos = None
        self.historico_consumos = None
        self.contador_pgto = 0
        self.contador_consumo = 0


    def realizar_venda(self, nome, categoria, curso, nome_prod, qtd):

        if self.estoque.baixar_estoque(nome_prod, qtd):

            produto = self._buscar_produto(nome_prod)

            valor_total = produto.preco_venda * qtd

            # pagamento
            self.contador_pgto += 1
            pgto = Pagamento(nome, categoria, curso, valor_total)

            reg_pgto = RegistroPagamento(self.contador_pgto, pgto)
            reg_pgto.proximo = self.historico_pagamentos
            self.historico_pagamentos = reg_pgto

            # consumo
            self.contador_consumo += 1
            cons = Consumo(nome, produto, qtd, valor_total)

            reg_cons = RegistroConsumo(self.contador_consumo, cons)
            reg_cons.proximo = self.historico_consumos
            self.historico_consumos = reg_cons

            return True

        return False


    def _buscar_produto(self, nome):

        atual = self.estoque.inicio

        while atual:

            if atual.produto.nome == nome:
                return atual.produto

            atual = atual.proximo

        return None


    # =========================
    # RELATÓRIO DE VENDAS
    # =========================
    def relatorio_vendas(self):

        print("\n===== RELATÓRIO DE VENDAS =====")

        atual = self.historico_pagamentos

        total = 0

        while atual:

            pg = atual.pagamento

            print(
                f"{pg.nome_pagador} | {pg.categoria} | "
                f"{pg.curso} | R$ {pg.valor_pago:.2f}"
            )

            total += pg.valor_pago

            atual = atual.proximo

        print("-----------------------------")
        print(f"TOTAL DE VENDAS: R$ {total:.2f}")


    # =========================
    # RELATÓRIO DE CONSUMO
    # =========================
    def relatorio_consumo(self):

        print("\n===== RELATÓRIO DE CONSUMO =====")

        atual = self.historico_consumos

        while atual:

            consumo = atual.consumo

            print(
                f"{consumo.nome_consumidor} | "
                f"{consumo.quantidade}x {consumo.produto.nome} | "
                f"R$ {consumo.valor_total:.2f}"
            )

            atual = atual.proximo


# =============================================================================
# PERSISTÊNCIA COM PICKLE
# =============================================================================

def salvar_dados(sistema, arquivo="cantina.pkl"):

    with open(arquivo, "wb") as f:
        pickle.dump(sistema, f)

    print("\nDados salvos com sucesso.")


def carregar_dados(arquivo="cantina.pkl"):

    try:
        with open(arquivo, "rb") as f:
            return pickle.load(f)

    except FileNotFoundError:
        return None


# =============================================================================
# GERAÇÃO AUTOMÁTICA COM FAKER
# =============================================================================

def popular_com_faker(sistema, qtd_vendas=15):

    fake = Faker("pt_BR")

    produtos = ["Hitt Nuts", "Pão de Mel"]

    print(f"\nGerando {qtd_vendas} vendas automáticas...")

    for _ in range(qtd_vendas):

        nome = fake.name()

        categoria = random.choice(["Aluno", "Professor", "Servidor"])

        curso = random.choice(["IA", "ESG"])

        produto = random.choice(produtos)

        sistema.realizar_venda(nome, categoria, curso, produto, 1)

        print(f"{nome} comprou {produto}")


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":

    sistema = carregar_dados()

    if sistema is None:

        print("Iniciando novo sistema...")

        estoque = Estoque()
        sistema = SistemaCantina(estoque)

        hitt = Produto("Hitt Nuts", 1.50, 3.00)
        pao = Produto("Pão de Mel", 1.80, 3.00)

        estoque.adicionar_lote(Lote(1, hitt, date.today(), date(2026, 12, 31), 50))
        estoque.adicionar_lote(Lote(2, pao, date.today(), date(2026, 6, 15), 30))

        popular_com_faker(sistema, 15)

    else:

        print("Sistema carregado do arquivo cantina.pkl")


    sistema.relatorio_vendas()
    sistema.relatorio_consumo()

    salvar_dados(sistema)

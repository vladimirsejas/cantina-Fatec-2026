from estoque import Produto, Lote, Estoque
from controlepgto import Pagamento, RegistroPagamento, ControlePagamentos
from datetime import datetime, date


class Consumo:
    def __init__(self, nome_consumidor, produto, quantidade, valor_total):
        self.nome_consumidor = nome_consumidor
        self.produto = produto
        self.quantidade = quantidade
        self.valor_total = valor_total
        self.data = datetime.now()


class RegistroConsumo:
    def __init__(self, id_consumo, consumo):
        self.id_consumo = id_consumo
        self.consumo = consumo
        self.proximo = None

    def __str__(self):
        return (
            f"{self.consumo.nome_consumidor} | "
            f"{self.consumo.quantidade}x {self.consumo.produto.nome} | "
            f"R$ {self.consumo.valor_total:.2f}"
        )


class ControleConsumo:

    def __init__(self):
        self.inicio = None
        self.contador = 0

    def registrar_consumo(self, consumo):

        self.contador += 1

        novo = RegistroConsumo(self.contador, consumo)

        if self.inicio is None:
            self.inicio = novo
            return

        atual = self.inicio

        while atual.proximo:
            atual = atual.proximo

        atual.proximo = novo

    def listar_consumos(self):

        atual = self.inicio

        print("\n===== CONSUMOS =====")

        while atual:
            print(atual)
            atual = atual.proximo


class SistemaCantina:

    def __init__(self):

        self.estoque = Estoque()
        self.pagamentos = ControlePagamentos()
        self.consumos = ControleConsumo()


    def buscar_produto(self, nome):

        atual = self.estoque.inicio

        while atual:

            if atual.produto.nome == nome:
                return atual.produto

            atual = atual.proximo

        return None


    def realizar_venda(self, nome_cliente, categoria, curso, nome_produto, quantidade):

        produto = self.buscar_produto(nome_produto)

        if produto is None:
            print("Produto não encontrado.")
            return

        if not self.estoque.vender_produto(nome_produto, quantidade):
            # mensagem já é exibida em vender_produto
            return

        valor_total = produto.preco_venda * quantidade

        pagamento = Pagamento(nome_cliente, categoria, curso, valor_total)

        registro = RegistroPagamento(
            self.pagamentos.contar_pagamentos() + 1,
            pagamento
        )

        self.pagamentos.registrar_pagamento(registro)

        consumo = Consumo(nome_cliente, produto, quantidade, valor_total)

        self.consumos.registrar_consumo(consumo)

        print(f"\nVenda realizada: {quantidade}x {nome_produto} para {nome_cliente}")


# =========================
# SIMULAÇÃO
# =========================

if __name__ == "__main__":

    sistema = SistemaCantina()

    hittnuts = Produto("Hitt Nuts", 1.50, 3.00)

    lote1 = Lote(1, hittnuts, date(2026,3,1), date(2026,4,1), 10)
    lote2 = Lote(2, hittnuts, date(2026,3,10), date(2026,5,1), 20)

    sistema.estoque.adicionar_lote(lote1)
    sistema.estoque.adicionar_lote(lote2)

    sistema.estoque.listar_estoque()

    sistema.realizar_venda("Vladi", "Aluno", "IA", "Hitt Nuts", 5)

    sistema.pagamentos.listar_pagamentos()
    sistema.consumos.listar_consumos()
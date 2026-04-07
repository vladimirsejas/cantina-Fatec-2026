from datetime import datetime, date
from controlepgto import ControlePagamentos

# =========================
# Classe Produto
# =========================
class Produto:
    def __init__(self, nome, preco_compra, preco_venda):
        self.nome = nome
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda


# =========================
# Classe Pagamento
# =========================
class Pagamento:
    def __init__(self, nome_pagador, categoria, curso, valor_pago):
        self.nome_pagador = nome_pagador
        self.categoria = categoria
        self.curso = curso
        self.valor_pago = valor_pago
        self.data_hora = datetime.now()


# =========================
# Classe Consumo
# =========================
class Consumo:
    def __init__(self, nome_consumidor, produto, quantidade, valor_total):
        self.nome_consumidor = nome_consumidor
        self.produto = produto
        self.quantidade = quantidade
        self.valor_total = valor_total
        self.data = datetime.now()


# =========================
# Nó da lista encadeada - Lote
# =========================
class Lote:
    def __init__(self, id_lote, produto, data_compra, data_validade, quantidade):
        self.id_lote = id_lote
        self.produto = produto
        self.data_compra = data_compra
        self.data_validade = data_validade
        self.quantidade = quantidade
        self.proximo = None


# =========================
# Nó da lista encadeada - Pagamento
# =========================
class RegistroPagamento:
    def __init__(self, id_transacao, pagamento):
        self.id_transacao = id_transacao
        self.pagamento = pagamento
        self.proximo = None


# =========================
# Nó da lista encadeada - Consumo
# =========================
class RegistroConsumo:
    def __init__(self, id_consumo, consumo):
        self.id_consumo = id_consumo
        self.consumo = consumo
        self.proximo = None

    def __str__(self):
        return (
            f"Consumo {self.id_consumo} | "
            f"Consumidor: {self.consumo.nome_consumidor} | "
            f"Produto: {self.consumo.produto.nome} | "
            f"Qtd: {self.consumo.quantidade} | "
            f"Valor: R$ {self.consumo.valor_total:.2f}"
        )


# =========================
# Classe Estoque
# =========================
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


    def baixar_estoque(self, nome_produto, qtd_desejada):

        if self.get_saldo(nome_produto) < qtd_desejada:
            return False

        restante = qtd_desejada
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


# =========================
# Sistema Cantina
# =========================
class SistemaCantina:

    def __init__(self, estoque):

        self.estoque = estoque
        
        from controlepgto import ControlePagamentos
        
        self.pagamentos = ControlePagamentos()
        self.historico_pagamentos = None
        self.historico_consumos = None

        self.cont_pgto = 0
        self.cont_consumo = 0


    def realizar_venda(self, nome, categoria, curso, nome_prod, qtd):

        if self.estoque.baixar_estoque(nome_prod, qtd):

            produto = self._buscar_produto(nome_prod)

            valor_total = produto.preco_venda * qtd

            # pagamento
            self.cont_pgto += 1
            pagamento = Pagamento(nome, categoria, curso, valor_total)
            reg_pgto = RegistroPagamento(self.cont_pgto, pagamento)

            reg_pgto.proximo = self.historico_pagamentos
            self.historico_pagamentos = reg_pgto

            # consumo
            self.cont_consumo += 1
            consumo = Consumo(nome, produto, qtd, valor_total)
            reg_cons = RegistroConsumo(self.cont_consumo, consumo)

            reg_cons.proximo = self.historico_consumos
            self.historico_consumos = reg_cons

            print(f"Venda registrada: {qtd}x {nome_prod} para {nome} - Total R${valor_total:.2f}")

        else:

            print("Estoque insuficiente.")


    def _buscar_produto(self, nome):

        atual = self.estoque.inicio

        while atual:

            if atual.produto.nome == nome:
                return atual.produto

            atual = atual.proximo

        return None


    def listar_consumos(self):

        atual = self.historico_consumos

        print("\n===== CONSUMOS =====")

        while atual:

            print(atual)

            p = atual.consumo

            print(
                f"ID: {atual.id_consumo} | "
                f"Nome: {p.nome_consumidor} | "
                f"Produto: {p.produto.nome} | "
                f"Qtd: {p.quantidade} | "
                f"Total: R$ {p.valor_total:.2f} | "
                f"Data: {p.data}"
            )

            atual = atual.proximo



# =========================
# Simulação
# =========================
if __name__ == "__main__":

    estoque = Estoque()
    sistema = SistemaCantina(estoque)

    hittnuts = Produto("Hitt Nuts", 1.50, 3.00)

    lote1 = Lote(1, hittnuts, date(2026,3,1), date(2026,4,1), 10)
    lote2 = Lote(2, hittnuts, date(2026,3,10), date(2026,5,1), 20)

    estoque.adicionar_lote(lote1)
    estoque.adicionar_lote(lote2)

    sistema.realizar_venda("Vladi", "Aluno", "IA", "Hitt Nuts", 5)

    print("\nSaldo restante:", estoque.get_saldo("Hitt Nuts"))

    sistema.listar_consumos()

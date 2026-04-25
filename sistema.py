from tabulate import tabulate
from modelos import Pagamento, Consumo, RegistroPagamento, RegistroConsumo


# =========================
# Classe SistemaCantina
# =========================

class SistemaCantina:

    def __init__(self, estoque):

        self.estoque = estoque

        # listas encadeadas de histórico
        self.historico_pagamentos = None
        self.historico_consumos = None

        # contadores de ID
        self._cont_pgto = 0
        self._cont_consumo = 0

    # -------------------------------------------------------
    # VENDA: baixa estoque e registra pagamento + consumo
    # -------------------------------------------------------
    def realizar_venda(self, nome, categoria, curso, produto, qtd):

        if not self.estoque.baixar_estoque(produto.nome, qtd):
            print("Estoque insuficiente para realizar a venda.")
            return False

        valor_total = produto.preco_venda * qtd

        # --- registro de pagamento ---
        self._cont_pgto += 1
        pagamento = Pagamento(nome, categoria, curso, valor_total)
        reg_pgto = RegistroPagamento(self._cont_pgto, pagamento)
        reg_pgto.proximo = self.historico_pagamentos
        self.historico_pagamentos = reg_pgto

        # --- registro de consumo ---
        self._cont_consumo += 1
        consumo = Consumo(nome, produto, qtd, valor_total)
        reg_cons = RegistroConsumo(self._cont_consumo, consumo)
        reg_cons.proximo = self.historico_consumos
        self.historico_consumos = reg_cons

        print(f"\nVenda registrada: {qtd}x {produto.nome} para {nome} — Total R$ {valor_total:.2f}")
        return True

    # -------------------------------------------------------
    # RELATÓRIO: vendas (pagamentos)
    # -------------------------------------------------------
    def relatorio_vendas(self):

        print("\n===== RELATÓRIO DE VENDAS =====")

        if self.historico_pagamentos is None:
            print("Nenhuma venda registrada.")
            return

        linhas = []
        total = 0
        atual = self.historico_pagamentos

        while atual:
            p = atual.pagamento
            linhas.append([
                atual.id_transacao,
                p.nome_pagador,
                p.categoria,
                p.curso,
                f"R$ {p.valor_pago:.2f}",
                p.data_hora.strftime("%d/%m/%Y %H:%M"),
            ])
            total += p.valor_pago
            atual = atual.proximo

        print(tabulate(
            linhas,
            headers=["#", "Nome", "Categoria", "Curso", "Valor", "Data/Hora"],
            tablefmt="rounded_outline"
        ))
        print(f"\nTotal arrecadado: R$ {total:.2f}  |  Vendas: {len(linhas)}")

    # -------------------------------------------------------
    # RELATÓRIO: consumos por produto
    # -------------------------------------------------------
    def relatorio_consumos(self):

        print("\n===== RELATÓRIO DE CONSUMOS =====")

        if self.historico_consumos is None:
            print("Nenhum consumo registrado.")
            return

        linhas = []
        atual = self.historico_consumos

        while atual:
            c = atual.consumo
            linhas.append([
                atual.id_consumo,
                c.nome_consumidor,
                c.produto.nome,
                c.quantidade,
                f"R$ {c.valor_total:.2f}",
                c.data.strftime("%d/%m/%Y %H:%M"),
            ])
            atual = atual.proximo

        print(tabulate(
            linhas,
            headers=["#", "Consumidor", "Produto", "Qtd", "Total", "Data/Hora"],
            tablefmt="rounded_outline"
        ))

    # -------------------------------------------------------
    # RELATÓRIO: lucro por produto vendido
    # -------------------------------------------------------
    def relatorio_lucro(self):

        print("\n===== RELATÓRIO DE LUCRO POR PRODUTO =====")

        if self.historico_consumos is None:
            print("Nenhum consumo registrado.")
            return

        lucros = {}  # {nome_produto: [qtd_total, receita, lucro]}
        atual = self.historico_consumos

        while atual:
            c = atual.consumo
            nome = c.produto.nome
            lucro_unit = c.produto.calcular_lucro()

            if nome not in lucros:
                lucros[nome] = [0, 0.0, 0.0]

            lucros[nome][0] += c.quantidade
            lucros[nome][1] += c.valor_total
            lucros[nome][2] += lucro_unit * c.quantidade

            atual = atual.proximo

        linhas = []
        for nome, (qtd, receita, lucro) in lucros.items():
            linhas.append([nome, qtd, f"R$ {receita:.2f}", f"R$ {lucro:.2f}"])

        # ordena por lucro decrescente
        linhas.sort(key=lambda x: float(x[3].replace("R$ ", "")), reverse=True)

        print(tabulate(
            linhas,
            headers=["Produto", "Qtd vendida", "Receita", "Lucro"],
            tablefmt="rounded_outline"
        ))

        lucro_total = sum(float(l[3].replace("R$ ", "")) for l in linhas)
        print(f"\nLucro total: R$ {lucro_total:.2f}")
  from datetime import date
from tabulate import tabulate
from modelos import Lote


# =========================
# Classe Estoque (lista encadeada com FIFO)
# =========================

class Estoque:

    def __init__(self):
        self.inicio = None          # cabeça da lista encadeada
        self._contador_lotes = 0    # gerador de IDs únicos

    # -------------------------------------------------------
    # UTILITÁRIO: próximo ID de lote
    # -------------------------------------------------------
    def proximo_id(self):
        self._contador_lotes += 1
        return self._contador_lotes

    # -------------------------------------------------------
    # INSERÇÃO: mantém lista ordenada por data de validade
    # (lotes que vencem primeiro ficam no início → FIFO)
    # -------------------------------------------------------
    def adicionar_lote(self, novo_lote):

        # lista vazia OU novo lote vence antes do primeiro
        if self.inicio is None or novo_lote.data_validade < self.inicio.data_validade:
            novo_lote.proximo = self.inicio
            self.inicio = novo_lote
            return

        # percorre até achar a posição certa
        atual = self.inicio
        while atual.proximo and atual.proximo.data_validade <= novo_lote.data_validade:
            atual = atual.proximo

        # encadeia o novo nó
        novo_lote.proximo = atual.proximo
        atual.proximo = novo_lote

    # -------------------------------------------------------
    # FIFO: baixa estoque consumindo os lotes mais antigos
    # -------------------------------------------------------
    def baixar_estoque(self, nome_produto, qtd):

        if self.get_saldo(nome_produto) < qtd:
            return False

        restante = qtd
        atual = self.inicio

        while atual and restante > 0:
            if atual.produto.nome == nome_produto and atual.quantidade > 0:
                if atual.quantidade >= restante:
                    atual.quantidade -= restante
                    restante = 0
                else:
                    restante -= atual.quantidade
                    atual.quantidade = 0
            atual = atual.proximo

        return True

    # -------------------------------------------------------
    # SALDO: total disponível de um produto
    # -------------------------------------------------------
    def get_saldo(self, nome_produto):

        total = 0
        atual = self.inicio

        while atual:
            if atual.produto.nome == nome_produto:
                total += atual.quantidade
            atual = atual.proximo

        return total

    # -------------------------------------------------------
    # EDITAR: atualiza quantidade de um lote pelo ID
    # -------------------------------------------------------
    def editar_quantidade(self, id_lote, nova_quantidade):

        if nova_quantidade < 0:
            print("Quantidade inválida.")
            return

        atual = self.inicio
        while atual:
            if atual.id_lote == id_lote:
                atual.quantidade = nova_quantidade
                print(f"Lote {id_lote} atualizado para {nova_quantidade} unidades.")
                return
            atual = atual.proximo

        print(f"Lote {id_lote} não encontrado.")

    # -------------------------------------------------------
    # LISTAGEM: todos os lotes com tabulate
    # -------------------------------------------------------
    def listar_estoque(self):

        linhas = []
        atual = self.inicio

        while atual:
            dias = atual.dias_para_vencer()
            status = "VENCIDO" if atual.esta_vencido() else (
                "⚠ VENCENDO" if dias <= 7 else "OK"
            )
            linhas.append([
                atual.id_lote,
                atual.produto.nome,
                atual.quantidade,
                atual.data_validade.strftime("%d/%m/%Y"),
                f"{dias}d",
                status,
                f"R$ {atual.produto.preco_venda:.2f}",
            ])
            atual = atual.proximo

        if not linhas:
            print("Estoque vazio.")
            return

        print("\n" + tabulate(
            linhas,
            headers=["Lote", "Produto", "Qtd", "Validade", "Vence em", "Status", "Preço venda"],
            tablefmt="rounded_outline"
        ))

    # -------------------------------------------------------
    # ALERTA: produtos que vencem nos próximos N dias
    # -------------------------------------------------------
    def alertar_vencendo(self, dias=7):

        linhas = []
        atual = self.inicio

        while atual:
            d = atual.dias_para_vencer()
            if 0 <= d <= dias and atual.quantidade > 0:
                linhas.append([
                    atual.id_lote,
                    atual.produto.nome,
                    atual.quantidade,
                    atual.data_validade.strftime("%d/%m/%Y"),
                    f"{d}d",
                ])
            atual = atual.proximo

        if not linhas:
            print(f"\nNenhum produto vencendo nos próximos {dias} dias.")
            return

        print(f"\n⚠  PRODUTOS VENCENDO EM ATÉ {dias} DIAS:")
        print(tabulate(
            linhas,
            headers=["Lote", "Produto", "Qtd", "Validade", "Faltam"],
            tablefmt="rounded_outline"
        ))

    # -------------------------------------------------------
    # LISTAGEM: produtos com saldo > 0 (para menu de venda)
    # -------------------------------------------------------
    def listar_produtos_disponiveis(self):

        vistos = {}
        atual = self.inicio

        while atual:
            if atual.quantidade > 0 and atual.produto.nome not in vistos:
                vistos[atual.produto.nome] = atual.produto
            atual = atual.proximo

        return list(vistos.values())
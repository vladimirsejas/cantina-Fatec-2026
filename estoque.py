from datetime import datetime, timedelta
from tabulate import tabulate

class Estoque:
    def __init__(self):
        self.inicio = None

    def alertar_vencendo(self, dias=7):
        """
        Percorre a lista encadeada e exibe produtos com validade 
        entre a data atual e o limite de dias informado.
        """
        hoje = datetime.now()
        limite = hoje + timedelta(days=dias)
        linhas = []
        atual = self.inicio

        while atual:
            # Garante que a validade seja tratada como objeto datetime para comparação
            validade_prod = atual.produto.validade
            if isinstance(validade_prod, str):
                try:
                    validade_prod = datetime.strptime(validade_prod, "%d/%m/%Y")
                except ValueError:
                    # Caso a data esteja em outro formato ou inválida, pula o nó
                    atual = atual.proximo
                    continue

            # Verifica se está dentro do intervalo (Vence hoje ou até a data limite)
            if hoje.date() <= validade_prod.date() <= limite.date():
                faltam = (validade_prod.date() - hoje.date()).days
                
                # Tradução de dias para uma mensagem mais amigável
                status_vencimento = f"{faltam} dias" if faltam > 0 else "Vence hoje!"
                if faltam < 0: status_vencimento = "Vencido!"

                linhas.append([
                    atual.id_lote,
                    atual.produto.nome,
                    atual.quantidade,
                    validade_prod.strftime("%d/%m/%Y"),
                    status_vencimento
                ])
            
            atual = atual.proximo

        if not linhas:
            print(f"\n[!] Nenhum produto vencendo nos próximos {dias} dias.")
            return

        print(f"\n>>> ALERTA: PRODUTOS VENCENDO EM ATÉ {dias} DIAS:")
        print(tabulate(
            linhas,
            headers=["Lote", "Produto", "Qtd", "Validade", "Status"],
            tablefmt="rounded_outline"
        ))

    def listar_produtos_disponiveis(self):
        """
        Retorna uma lista de produtos únicos que possuem saldo em estoque.
        """
        vistos = {}
        atual = self.inicio

        while atual:
            if atual.quantidade > 0 and atual.produto.nome not in vistos:
                vistos[atual.produto.nome] = atual.produto
            atual = atual.proximo

        return list(vistos.values())
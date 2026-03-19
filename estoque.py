from datetime import date

# =========================
# Classe Produto
# =========================
class Produto:
    def __init__(self, nome, preco_compra, preco_venda):
        self.nome = nome
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda


# =========================
# Classe Lote (Nó da Lista Encadeada)
# =========================
class Lote:
    def __init__(self, id_lote, produto, data_compra, data_validade, quantidade):
        self.id_lote = id_lote
        self.produto = produto
        self.data_compra = data_compra
        self.data_validade = data_validade
        self.quantidade = quantidade
        self.proximo = None  # ponteiro para o próximo lote

    def __str__(self):
        return (
            f"Lote {self.id_lote} | Produto: {self.produto.nome} | "
            f"Qtd: {self.quantidade} | Validade: {self.data_validade}"
        )


# =========================
# Classe Estoque (Lista Encadeada)
# =========================
class Estoque:
    def __init__(self):
        self.inicio = None  # cabeça da lista

    # inserir lote mantendo ordem por validade
    def adicionar_lote(self, novo_lote):

        if self.inicio is None or novo_lote.data_validade < self.inicio.data_validade:
            novo_lote.proximo = self.inicio
            self.inicio = novo_lote
            return

        atual = self.inicio

        while (
            atual.proximo is not None
            and atual.proximo.data_validade < novo_lote.data_validade
        ):
            atual = atual.proximo

        novo_lote.proximo = atual.proximo
        atual.proximo = novo_lote

    # editar quantidade de um lote
    def editar_quantidade(self, id_lote, nova_quantidade):

        atual = self.inicio

        while atual is not None:

            if atual.id_lote == id_lote:
                atual.quantidade = nova_quantidade
                print("Quantidade atualizada.")
                return

            atual = atual.proximo

        print("Lote não encontrado.")

    # vender produto (prioriza lotes mais antigos)
    def vender_produto(self, nome_produto, quantidade):

        atual = self.inicio

        while atual is not None and quantidade > 0:

            if atual.produto.nome == nome_produto and atual.quantidade > 0:

                if atual.quantidade >= quantidade:
                    atual.quantidade -= quantidade
                    quantidade = 0

                else:
                    quantidade -= atual.quantidade
                    atual.quantidade = 0

            atual = atual.proximo

        if quantidade == 0:
            print("Venda realizada.")
        else:
            print("Estoque insuficiente.")

    # listar estoque
    def listar_estoque(self):

        print("\n===== ESTOQUE =====")

        atual = self.inicio

        while atual is not None:
            print(atual)
            atual = atual.proximo


# =========================
# Simulação do sistema
# =========================
if __name__ == "__main__":

    # produtos
    hittnuts = Produto("Hitt Nuts", 1.50, 3.00)
    pao_mel = Produto("Pão de Mel", 1.80, 3.00)

    # lotes
    lote1 = Lote(
        1,
        hittnuts,
        date(2026, 3, 10),
        date(2026, 5, 1),
        50
    )

    lote2 = Lote(
        2,
        pao_mel,
        date(2026, 3, 12),
        date(2026, 4, 15),
        20
    )

    lote3 = Lote(
        3,
        hittnuts,
        date(2026, 3, 15),
        date(2026, 4, 20),
        30
    )

    # criar estoque
    estoque = Estoque()

    # adicionar lotes
    estoque.adicionar_lote(lote1)
    estoque.adicionar_lote(lote2)
    estoque.adicionar_lote(lote3)

    # mostrar estoque
    estoque.listar_estoque()

    # editar quantidade
    estoque.editar_quantidade(1, 48)

    # simular venda
    estoque.vender_produto("Hitt Nuts", 5)

    # mostrar estoque atualizado
    estoque.listar_estoque()

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

        self.proximo = None


    def __str__(self):

        return (
            f"Lote {self.id_lote} | "
            f"Produto: {self.produto.nome} | "
            f"Qtd: {self.quantidade} | "
            f"Validade: {self.data_validade}"
        )


# =========================
# Classe Estoque (Lista Encadeada)
# =========================
class Estoque:

    def __init__(self):

        self.inicio = None


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
                print(f"Lote {id_lote}: quantidade atualizada para {nova_quantidade}.")
                return

            atual = atual.proximo


        print("Lote não encontrado.")


    # vender produto
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
# SIMULAÇÃO DO SISTEMA
# =========================
if __name__ == "__main__":


    # =========================
    # PRODUTOS
    # =========================

    hittnuts = Produto("Hitt Nuts", 1.50, 3.00)
    pao_mel = Produto("Pão de Mel", 1.80, 3.00)
    balabon = Produto("Bala Bon", 0.80, 1.50)
    pacoca = Produto("Paçoca", 0.80, 1.50)
    trento = Produto("Trento", 1.50, 3.00)
    kitkat = Produto("KitKat", 2.50, 4.00)

    amendoim = Produto("Amendoim Japonês", 1.50, 3.00)
    chips = Produto("Chips", 2.50, 4.50)
    salgadinho = Produto("Salgadinho", 2.00, 3.50)

    coca = Produto("Coca-Cola Lata", 3.50, 5.00)
    guarana = Produto("Guaraná Lata", 3.50, 5.00)
    fanta = Produto("Fanta Lata", 3.50, 5.00)

    agua = Produto("Água Mineral", 1.50, 3.00)
    h2o = Produto("H2O", 3.50, 5.50)
    energetico = Produto("Energético", 5.00, 8.00)


    # =========================
    # LOTES
    # =========================

    lote1 = Lote(1, hittnuts, date(2026,3,10), date(2026,5,1), 50)
    lote2 = Lote(2, pao_mel, date(2026,3,12), date(2026,4,15), 20)
    lote3 = Lote(3, hittnuts, date(2026,3,15), date(2026,4,20), 30)
    lote4 = Lote(4, balabon, date(2026,3,18), date(2026,7,1), 60)

    lote5 = Lote(5, pacoca, date(2026,3,10), date(2026,6,1), 40)
    lote6 = Lote(6, trento, date(2026,3,10), date(2026,6,1), 30)
    lote7 = Lote(7, kitkat, date(2026,3,10), date(2026,6,1), 25)

    lote8 = Lote(8, amendoim, date(2026,3,10), date(2026,6,1), 35)
    lote9 = Lote(9, chips, date(2026,3,10), date(2026,6,1), 20)
    lote10 = Lote(10, salgadinho, date(2026,3,10), date(2026,6,1), 20)

    lote11 = Lote(11, coca, date(2026,3,10), date(2026,6,1), 40)
    lote12 = Lote(12, guarana, date(2026,3,10), date(2026,6,1), 30)
    lote13 = Lote(13, fanta, date(2026,3,10), date(2026,6,1), 25)

    lote14 = Lote(14, agua, date(2026,3,10), date(2026,6,1), 50)
    lote15 = Lote(15, h2o, date(2026,3,10), date(2026,6,1), 20)
    lote16 = Lote(16, energetico, date(2026,3,10), date(2026,6,1), 15)


    # =========================
    # CRIAR ESTOQUE
    # =========================

    estoque = Estoque()

    estoque.adicionar_lote(lote1)
    estoque.adicionar_lote(lote2)
    estoque.adicionar_lote(lote3)
    estoque.adicionar_lote(lote4)

    estoque.adicionar_lote(lote5)
    estoque.adicionar_lote(lote6)
    estoque.adicionar_lote(lote7)

    estoque.adicionar_lote(lote8)
    estoque.adicionar_lote(lote9)
    estoque.adicionar_lote(lote10)

    estoque.adicionar_lote(lote11)
    estoque.adicionar_lote(lote12)
    estoque.adicionar_lote(lote13)

    estoque.adicionar_lote(lote14)
    estoque.adicionar_lote(lote15)
    estoque.adicionar_lote(lote16)


    # =========================
    # MOSTRAR ESTOQUE
    # =========================

    estoque.listar_estoque()
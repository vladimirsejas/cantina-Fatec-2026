from datetime import date, datetime

# =========================
# Classe Produto
# =========================
class Produto:
    def __init__(self, nome, preco_compra, preco_venda):
        self.nome = nome
        self.preco_compra = preco_compra
        self.preco_venda = preco_venda

# =========================
# Classe Lote (Nó da Lista Encadeada de Estoque)
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
            f"Lote {self.id_lote} | Produto: {self.produto.nome} | "
            f"Qtd: {self.quantidade} | Validade: {self.data_validade}"
        )

# =========================
# Classe Pagamento (Dados do Pagamento)
# =========================
class Pagamento:
    def __init__(self, nome, categoria, curso, valor):
        self.nome = nome
        self.categoria = categoria
        self.curso = curso
        self.valor = valor
        self.data_hora = datetime.now()

# =========================
# Classe RegistroPagamento (Nó da Lista Encadeada de Pagamentos)
# =========================
class RegistroPagamento:
    def __init__(self, pagamento):
        self.pagamento = pagamento
        self.proximo = None

# =========================
# Classe ControlePagamentos (Lista Encadeada)
# =========================
class ControlePagamentos:
    def __init__(self):
        self.inicio = None

    def registrar_pagamento(self, pagamento):
        novo_registro = RegistroPagamento(pagamento)
        if self.inicio is None:
            self.inicio = novo_registro
            return
        
        atual = self.inicio
        while atual.proximo is not None:
            atual = atual.proximo
        atual.proximo = novo_registro

    def listar_pagamentos(self):
        print("\n===== HISTÓRICO DE PAGAMENTOS PIX =====")
        atual = self.inicio
        while atual is not None:
            p = atual.pagamento
            print(f"Nome: {p.nome} | Categoria: {p.categoria} | "
                  f"Curso: {p.curso} | Valor: R$ {p.valor:.2f} | "
                  f"Data: {p.data_hora.strftime('%d/%m/%Y %H:%M')}")
            atual = atual.proximo

# =========================
# Classe Estoque (Lista Encadeada)
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
        while (atual.proximo is not None and 
               atual.proximo.data_validade < novo_lote.data_validade):
            atual = atual.proximo

        novo_lote.proximo = atual.proximo
        atual.proximo = novo_lote

    def editar_quantidade(self, id_lote, nova_quantidade):
        atual = self.inicio
        while atual is not None:
            if atual.id_lote == id_lote:
                atual.quantidade = nova_quantidade
                print(f"Lote {id_lote}: Quantidade atualizada para {nova_quantidade}.")
                return
            atual = atual.proximo
        print("Lote não encontrado.")

    def vender_produto(self, nome_produto, quantidade):
        atual = self.inicio
        venda_possivel = False
        qtd_necessaria = quantidade

        while atual is not None and qtd_necessaria > 0:
            if atual.produto.nome == nome_produto and atual.quantidade > 0:
                if atual.quantidade >= qtd_necessaria:
                    atual.quantidade -= qtd_necessaria
                    qtd_necessaria = 0
                else:
                    qtd_necessaria -= atual.quantidade
                    atual.quantidade = 0
            atual = atual.proximo

        if qtd_necessaria == 0:
            print(f"Venda de {quantidade} unidades de {nome_produto} realizada.")
            return True
        else:
            print(f"Estoque insuficiente para {nome_produto}.")
            return False

    def listar_estoque(self):
        print("\n===== STATUS ATUAL DO ESTOQUE =====")
        atual = self.inicio
        while atual is not None:
            print(atual)
            atual = atual.proximo

# =========================
# Simulação Integrada
# =========================
if __name__ == "__main__":
    # Inicialização das Estruturas
    estoque = Estoque()
    controle_pix = ControlePagamentos()

    # Produtos
    hittnuts = Produto("Hitt Nuts", 1.50, 3.00)
    pao_mel = Produto("Pão de Mel", 1.80, 3.00)
    balabon = Produto("Bala Bon", 0.80, 1.50)

    # Lotes (Simetria com os dados reais observados) [cite: 22, 23, 24]
    estoque.adicionar_lote(Lote(1, hittnuts, date(2026, 3, 10), date(2026, 5, 1), 50))
    estoque.adicionar_lote(Lote(2, pao_mel, date(2026, 3, 12), date(2026, 4, 15), 20))
    estoque.adicionar_lote(Lote(3, hittnuts, date(2026, 3, 15), date(2026, 4, 20), 30))
    estoque.adicionar_lote(Lote(4, balabon, date(2026, 3, 18), date(2026, 7, 1), 60))

    estoque.listar_estoque()

    # Simulação de Venda e Pagamento [cite: 231]
    if estoque.vender_produto("Hitt Nuts", 5):
        pag = Pagamento("Vladimir Sejas", "Aluno", "IA", 15.00) # 5 x 3.00
        controle_pix.registrar_pagamento(pag)

    if estoque.vender_produto("Pão de Mel", 3):
        pag = Pagamento("Maria Silva", "Aluno", "ESG", 9.00) # 3 x 3.00
        controle_pix.registrar_pagamento(pag)

    # Relatórios Finais [cite: 236]
    estoque.listar_estoque()
    controle_pix.listar_pagamentos()

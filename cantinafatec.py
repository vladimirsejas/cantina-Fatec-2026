import pickle
import random
from datetime import datetime, date
from faker import Faker
from tabulate import tabulate


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


# =============================================================================
# CONTROLE DE ESTOQUE
# =============================================================================

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

    def editar_quantidade(self, id_lote, nova_quantidade):
        atual = self.inicio
        while atual:
            if atual.id_lote == id_lote:
                atual.quantidade = nova_quantidade
                print(f"Lote {id_lote}: quantidade atualizada para {nova_quantidade}.")
                return
            atual = atual.proximo
        print("Lote não encontrado.")

    def listar_estoque(self):
        atual = self.inicio
        tabela = []
        while atual:
            tabela.append([
                atual.id_lote,
                atual.produto.nome,
                f"R$ {atual.produto.preco_venda:.2f}",
                atual.quantidade,
                atual.data_validade
            ])
            atual = atual.proximo

        if tabela:
            print("\n===== ESTOQUE =====")
            print(tabulate(
                tabela,
                headers=["Lote", "Produto", "Preço Venda", "Qtd", "Validade"],
                tablefmt="grid"
            ))
        else:
            print("\nEstoque vazio.")

    def listar_produtos_disponiveis(self):
        """Retorna lista de produtos únicos com saldo > 0."""
        vistos = {}
        atual = self.inicio
        while atual:
            nome = atual.produto.nome
            if nome not in vistos and self.get_saldo(nome) > 0:
                vistos[nome] = atual.produto
            atual = atual.proximo
        return list(vistos.values())


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

    def realizar_venda(self, nome, categoria, curso, produto, qtd):
        if not self.estoque.baixar_estoque(produto.nome, qtd):
            print("Estoque insuficiente.")
            return False

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

        print(f"\nVenda registrada: {qtd}x {produto.nome} para {nome} — Total: R$ {valor_total:.2f}")
        return True

    def relatorio_vendas(self):
        print("\n===== RELATÓRIO DE VENDAS =====")
        atual = self.historico_pagamentos
        tabela = []
        total = 0

        while atual:
            pg = atual.pagamento
            tabela.append([
                atual.id_transacao,
                pg.nome_pagador,
                pg.categoria,
                pg.curso,
                f"R$ {pg.valor_pago:.2f}",
                pg.data_hora.strftime("%d/%m/%Y %H:%M")
            ])
            total += pg.valor_pago
            atual = atual.proximo

        if tabela:
            print(tabulate(
                tabela,
                headers=["#", "Nome", "Categoria", "Curso", "Valor", "Data/Hora"],
                tablefmt="grid"
            ))
            print(f"\nTOTAL DE VENDAS: R$ {total:.2f}")
        else:
            print("Nenhuma venda registrada.")

    def relatorio_consumo(self):
        print("\n===== RELATÓRIO DE CONSUMO =====")
        atual = self.historico_consumos
        tabela = []

        while atual:
            consumo = atual.consumo
            tabela.append([
                atual.id_consumo,
                consumo.nome_consumidor,
                consumo.produto.nome,
                consumo.quantidade,
                f"R$ {consumo.valor_total:.2f}",
                consumo.data.strftime("%d/%m/%Y %H:%M")
            ])
            atual = atual.proximo

        if tabela:
            print(tabulate(
                tabela,
                headers=["#", "Consumidor", "Produto", "Qtd", "Valor", "Data/Hora"],
                tablefmt="grid"
            ))
        else:
            print("Nenhum consumo registrado.")


# =============================================================================
# PERSISTÊNCIA
# =============================================================================

ARQUIVO_DADOS = "cantina.pkl"

def salvar_dados(sistema):
    with open(ARQUIVO_DADOS, "wb") as f:
        pickle.dump(sistema, f)
    print("\nDados salvos com sucesso.")

def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


# =============================================================================
# INICIALIZAÇÃO PADRÃO
# =============================================================================

def sistema_padrao():
    estoque = Estoque()

    p1 = Produto("Hitt Nuts", 1.50, 3.00)
    p2 = Produto("Pão de Mel", 1.80, 3.00)
    p3 = Produto("Bala Bon", 0.80, 1.50)

    estoque.adicionar_lote(Lote(estoque.proximo_id(), p1, date.today(), date(2026, 12, 31), 50))
    estoque.adicionar_lote(Lote(estoque.proximo_id(), p2, date.today(), date(2026, 10,  1), 30))
    estoque.adicionar_lote(Lote(estoque.proximo_id(), p3, date.today(), date(2026,  9,  1), 60))

    return SistemaCantina(estoque)


# =============================================================================
# FAKER
# =============================================================================

def popular_com_faker(sistema, qtd_vendas=5):
    fake = Faker("pt_BR")
    produtos = sistema.estoque.listar_produtos_disponiveis()

    if not produtos:
        print("Sem produtos disponíveis no estoque.")
        return

    print(f"\nGerando {qtd_vendas} vendas automáticas...")
    for _ in range(qtd_vendas):
        produto = random.choice(produtos)
        sistema.realizar_venda(
            fake.name(),
            random.choice(["Aluno", "Professor", "Servidor"]),
            random.choice(["IA", "ESG"]),
            produto,
            1
        )


# =============================================================================
# HELPERS DE INPUT
# =============================================================================

def escolher_opcao(titulo, opcoes):
    """Exibe uma lista numerada e retorna o índice escolhido (0-based)."""
    print(f"\n{titulo}")
    for i, op in enumerate(opcoes, 1):
        print(f"  {i}. {op}")
    while True:
        try:
            escolha = int(input("Escolha: "))
            if 1 <= escolha <= len(opcoes):
                return escolha - 1
        except ValueError:
            pass
        print(f"Opção inválida. Digite um número entre 1 e {len(opcoes)}.")


# =============================================================================
# MENU
# =============================================================================

def menu():
    print("\n╔══════════════════════════╗")
    print("║     CANTINA FATEC        ║")
    print("╠══════════════════════════╣")
    print("║  1. Realizar venda       ║")
    print("║  2. Ver estoque          ║")
    print("║  3. Relatório de vendas  ║")
    print("║  4. Relatório de consumo ║")
    print("║  5. Gerar vendas (Faker) ║")
    print("║  0. Sair                 ║")
    print("╚══════════════════════════╝")
    return input("Opção: ").strip()


# =============================================================================
# FLUXO DE VENDA INTERATIVO
# =============================================================================

def fluxo_venda(sistema):
    produtos = sistema.estoque.listar_produtos_disponiveis()

    if not produtos:
        print("\nSem produtos disponíveis no estoque no momento.")
        return

    # --- nome ---
    nome = input("\nNome do cliente: ").strip()
    if not nome:
        print("Nome inválido.")
        return

    # --- categoria ---
    categorias = ["Aluno", "Professor", "Servidor"]
    idx_cat = escolher_opcao("Categoria:", categorias)
    categoria = categorias[idx_cat]

    # --- curso ---
    cursos = ["IA", "ESG", "Outro"]
    idx_curso = escolher_opcao("Curso:", cursos)
    curso = cursos[idx_curso]

    # --- produto (com saldo e preço exibidos) ---
    opcoes_prod = [
        f"{p.nome}  |  Saldo: {sistema.estoque.get_saldo(p.nome)}  |  R$ {p.preco_venda:.2f}"
        for p in produtos
    ]
    idx_prod = escolher_opcao("Produto:", opcoes_prod)
    produto = produtos[idx_prod]

    # --- quantidade ---
    saldo = sistema.estoque.get_saldo(produto.nome)
    while True:
        try:
            qtd = int(input(f"Quantidade (máx {saldo}): "))
            if 1 <= qtd <= saldo:
                break
        except ValueError:
            pass
        print(f"Quantidade inválida. Digite entre 1 e {saldo}.")

    sistema.realizar_venda(nome, categoria, curso, produto, qtd)


# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":

    sistema = carregar_dados()

    if sistema is None:
        print("Nenhum dado encontrado. Iniciando sistema novo...")
        sistema = sistema_padrao()
    else:
        print("Sistema carregado de cantina.pkl")

    while True:
        op = menu()

        if op == "1":
            fluxo_venda(sistema)

        elif op == "2":
            sistema.estoque.listar_estoque()

        elif op == "3":
            sistema.relatorio_vendas()

        elif op == "4":
            sistema.relatorio_consumo()

        elif op == "5":
            try:
                n = int(input("Quantas vendas gerar? (padrão 5): ") or "5")
            except ValueError:
                n = 5
            popular_com_faker(sistema, n)

        elif op == "0":
            salvar_dados(sistema)
            print("Até logo!")
            break

        else:
            print("Opção inválida.")
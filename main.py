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

    def __str__(self):
        return (
            f"Lote {self.id_lote} | Produto: {self.produto.nome} | "
            f"Qtd: {self.quantidade} | Validade: {self.data_validade}"
        )


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

    def _proximo_id(self):
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

    def listar_estoque(self):
        print("\n===== ESTOQUE =====")
        tabela = []
        atual = self.inicio
        while atual:
            tabela.append([
                atual.id_lote,
                atual.produto.nome,
                atual.quantidade,
                f"R$ {atual.produto.preco_venda:.2f}",
                atual.data_validade
            ])
            atual = atual.proximo

        if tabela:
            print(tabulate(
                tabela,
                headers=["Lote", "Produto", "Qtd", "Preço Venda", "Validade"],
                tablefmt="grid"
            ))
        else:
            print("Estoque vazio.")

    def editar_quantidade(self, id_lote, nova_quantidade):
        atual = self.inicio
        while atual:
            if atual.id_lote == id_lote:
                atual.quantidade = nova_quantidade
                print(f"Lote {id_lote}: quantidade atualizada para {nova_quantidade}.")
                return True
            atual = atual.proximo
        print("Lote não encontrado.")
        return False

    def listar_produtos_disponiveis(self):
        produtos = {}
        atual = self.inicio
        while atual:
            nome = atual.produto.nome
            if nome not in produtos:
                produtos[nome] = {
                    "produto": atual.produto,
                    "saldo": 0
                }
            produtos[nome]["saldo"] += atual.quantidade
            atual = atual.proximo
        return produtos


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

            self.contador_pgto += 1
            pgto = Pagamento(nome, categoria, curso, valor_total)
            reg_pgto = RegistroPagamento(self.contador_pgto, pgto)
            reg_pgto.proximo = self.historico_pagamentos
            self.historico_pagamentos = reg_pgto

            self.contador_consumo += 1
            cons = Consumo(nome, produto, qtd, valor_total)
            reg_cons = RegistroConsumo(self.contador_consumo, cons)
            reg_cons.proximo = self.historico_consumos
            self.historico_consumos = reg_cons

            return True, valor_total

        return False, 0

    def _buscar_produto(self, nome):
        atual = self.estoque.inicio
        while atual:
            if atual.produto.nome == nome:
                return atual.produto
            atual = atual.proximo
        return None

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
                headers=["ID", "Nome", "Categoria", "Curso", "Valor", "Data/Hora"],
                tablefmt="grid"
            ))
            print(f"\nTOTAL DE VENDAS: R$ {total:.2f}")
            print(f"Quantidade de vendas: {self.contador_pgto}")
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
                headers=["ID", "Consumidor", "Produto", "Qtd", "Valor", "Data/Hora"],
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
    print("\n✔ Dados salvos com sucesso.")


def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


# =============================================================================
# INICIALIZAÇÃO COM DADOS PADRÃO
# =============================================================================

def inicializar_sistema():
    estoque = Estoque()
    sistema = SistemaCantina(estoque)

    hitt = Produto("Hitt Nuts", 1.50, 3.00)
    pao  = Produto("Pão de Mel", 1.80, 3.00)
    bala = Produto("Bala Bon",   0.80, 1.50)

    estoque.adicionar_lote(Lote(1, hitt, date.today(), date(2026, 12, 31), 50))
    estoque.adicionar_lote(Lote(2, pao,  date.today(), date(2026,  6, 15), 30))
    estoque.adicionar_lote(Lote(3, bala, date.today(), date(2026,  8, 20), 60))

    return sistema


# =============================================================================
# FAKER
# =============================================================================

def popular_com_faker(sistema, qtd_vendas=10):
    fake = Faker("pt_BR")
    produtos_disp = list(sistema.estoque.listar_produtos_disponiveis().keys())

    if not produtos_disp:
        print("Sem produtos no estoque para gerar vendas.")
        return

    geradas = 0
    for _ in range(qtd_vendas):
        nome      = fake.name()
        categoria = random.choice(["Aluno", "Professor", "Servidor"])
        curso     = random.choice(["IA", "ESG", "Logística"])
        produto   = random.choice(produtos_disp)
        ok, _     = sistema.realizar_venda(nome, categoria, curso, produto, 1)
        if ok:
            geradas += 1

    print(f"\n✔ {geradas} vendas automáticas geradas com sucesso.")


# =============================================================================
# HELPERS DE INPUT
# =============================================================================

def input_int(prompt, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(prompt))
            if minimo is not None and valor < minimo:
                print(f"  Digite um valor >= {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"  Digite um valor <= {maximo}.")
                continue
            return valor
        except ValueError:
            print("  Entrada inválida. Digite um número inteiro.")


def input_float(prompt, minimo=0.0):
    while True:
        try:
            valor = float(input(prompt))
            if valor < minimo:
                print(f"  Digite um valor >= {minimo}.")
                continue
            return valor
        except ValueError:
            print("  Entrada inválida. Digite um número.")


def escolher_opcao(opcoes):
    """Recebe lista de strings e retorna o índice escolhido (base 0)."""
    for i, op in enumerate(opcoes, 1):
        print(f"  [{i}] {op}")
    return input_int("  Escolha: ", 1, len(opcoes)) - 1


# =============================================================================
# SUBMENUS
# =============================================================================

def menu_nova_venda(sistema):
    print("\n--- NOVA VENDA ---")

    produtos = sistema.estoque.listar_produtos_disponiveis()
    if not produtos:
        print("Estoque vazio. Cadastre lotes antes de realizar vendas.")
        return

    # exibe produtos disponíveis
    nomes = list(produtos.keys())
    print("\nProdutos disponíveis:")
    for i, nome in enumerate(nomes, 1):
        saldo = produtos[nome]["saldo"]
        preco = produtos[nome]["produto"].preco_venda
        print(f"  [{i}] {nome} — Saldo: {saldo} | Preço: R$ {preco:.2f}")

    idx_prod = input_int("\n  Escolha o produto (número): ", 1, len(nomes)) - 1
    nome_prod = nomes[idx_prod]

    saldo_max = produtos[nome_prod]["saldo"]
    qtd = input_int(f"  Quantidade (máx {saldo_max}): ", 1, saldo_max)

    nome_comprador = input("  Nome do comprador: ").strip() or "Anônimo"

    print("\n  Categoria:")
    categorias = ["Aluno", "Professor", "Servidor"]
    idx_cat = escolher_opcao(categorias)
    categoria = categorias[idx_cat]

    print("\n  Curso:")
    cursos = ["IA", "ESG", "Logística", "Outro"]
    idx_cur = escolher_opcao(cursos)
    curso = cursos[idx_cur]

    ok, valor = sistema.realizar_venda(nome_comprador, categoria, curso, nome_prod, qtd)
    if ok:
        print(f"\n✔ Venda realizada! {qtd}x {nome_prod} para {nome_comprador} — Total: R$ {valor:.2f}")
    else:
        print("\n✘ Estoque insuficiente. Venda não realizada.")


def menu_estoque(sistema):
    while True:
        print("\n--- GESTÃO DE ESTOQUE ---")
        print("  [1] Listar estoque")
        print("  [2] Adicionar novo lote")
        print("  [3] Editar quantidade de lote")
        print("  [4] Consultar saldo por produto")
        print("  [0] Voltar")

        op = input_int("\n  Opção: ", 0, 4)

        if op == 0:
            break

        elif op == 1:
            sistema.estoque.listar_estoque()

        elif op == 2:
            print("\n  --- Novo Lote ---")
            nome_prod    = input("  Nome do produto: ").strip()
            preco_compra = input_float("  Preço de compra (R$): ")
            preco_venda  = input_float("  Preço de venda  (R$): ")
            qtd          = input_int("  Quantidade: ", 1)

            print("  Data de validade:")
            ano  = input_int("    Ano  (ex: 2026): ", 2000, 2099)
            mes  = input_int("    Mês  (1-12): ", 1, 12)
            dia  = input_int("    Dia  (1-31): ", 1, 31)

            try:
                validade = date(ano, mes, dia)
            except ValueError:
                print("  Data inválida.")
                continue

            produto = Produto(nome_prod, preco_compra, preco_venda)
            novo_id = sistema.estoque._proximo_id()
            lote    = Lote(novo_id, produto, date.today(), validade, qtd)
            sistema.estoque.adicionar_lote(lote)
            print(f"\n✔ Lote {novo_id} adicionado: {qtd}x {nome_prod} (validade {validade}).")

        elif op == 3:
            sistema.estoque.listar_estoque()
            id_lote = input_int("\n  ID do lote a editar: ", 1)
            nova_qtd = input_int("  Nova quantidade: ", 0)
            sistema.estoque.editar_quantidade(id_lote, nova_qtd)

        elif op == 4:
            nome_prod = input("  Nome do produto: ").strip()
            saldo = sistema.estoque.get_saldo(nome_prod)
            print(f"\n  Saldo de '{nome_prod}': {saldo} unidades")


def menu_relatorios(sistema):
    while True:
        print("\n--- RELATÓRIOS ---")
        print("  [1] Relatório de vendas")
        print("  [2] Relatório de consumo")
        print("  [0] Voltar")

        op = input_int("\n  Opção: ", 0, 2)

        if op == 0:
            break
        elif op == 1:
            sistema.relatorio_vendas()
        elif op == 2:
            sistema.relatorio_consumo()


def menu_faker(sistema):
    print("\n--- GERAR VENDAS AUTOMÁTICAS (FAKER) ---")
    qtd = input_int("  Quantas vendas deseja gerar? ", 1, 500)
    popular_com_faker(sistema, qtd)


# =============================================================================
# MENU PRINCIPAL
# =============================================================================

def menu_principal(sistema):
    while True:
        print("\n" + "=" * 45)
        print("      🛒  SISTEMA CANTINA FATEC  🛒")
        print("=" * 45)
        print("  [1] Realizar venda")
        print("  [2] Gestão de estoque")
        print("  [3] Relatórios")
        print("  [4] Gerar vendas automáticas (Faker)")
        print("  [5] Salvar dados")
        print("  [0] Sair (salva automaticamente)")
        print("=" * 45)

        op = input_int("\n  Opção: ", 0, 5)

        if op == 0:
            salvar_dados(sistema)
            print("\nAté logo! 👋\n")
            break
        elif op == 1:
            menu_nova_venda(sistema)
        elif op == 2:
            menu_estoque(sistema)
        elif op == 3:
            menu_relatorios(sistema)
        elif op == 4:
            menu_faker(sistema)
        elif op == 5:
            salvar_dados(sistema)


# =============================================================================
# PONTO DE ENTRADA
# =============================================================================

if __name__ == "__main__":
    print("\nCarregando sistema...")

    sistema = carregar_dados()

    if sistema is None:
        print("Nenhum dado encontrado. Iniciando sistema com dados padrão...")
        sistema = inicializar_sistema()
    else:
        print(f"✔ Dados carregados de '{ARQUIVO_DADOS}'.")

    menu_principal(sistema)
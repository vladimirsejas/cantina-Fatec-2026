   import pickle
from datetime import date

from modelos import Produto, Lote
from estoque import Estoque
from sistema import SistemaCantina


# =========================
# PERSISTÊNCIA
# =========================

ARQUIVO_DADOS = "cantina.pkl"


def salvar_dados(sistema):
    with open(ARQUIVO_DADOS, "wb") as f:
        pickle.dump(sistema, f)
    print("Dados salvos.")


def carregar_dados():
    try:
        with open(ARQUIVO_DADOS, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return None


# =========================
# ESTOQUE PADRÃO
# =========================

def sistema_padrao():

    estoque = Estoque()

    produtos = [
        Produto("Hitt Nuts",        1.50, 3.00),
        Produto("Pão de Mel",       1.80, 3.00),
        Produto("Bala Bon",         0.80, 1.50),
        Produto("Paçoca",           0.80, 1.50),
        Produto("Trento",           1.50, 3.00),
        Produto("KitKat",           2.50, 4.00),
        Produto("Amendoim Japonês", 1.50, 3.00),
        Produto("Chips",            2.50, 4.50),
        Produto("Salgadinho",       2.00, 3.50),
        Produto("Coca-Cola Lata",   3.50, 5.00),
        Produto("Guaraná Lata",     3.50, 5.00),
        Produto("Fanta Lata",       3.50, 5.00),
        Produto("Água Mineral",     1.50, 3.00),
        Produto("H2O",              3.50, 5.50),
        Produto("Energético",       5.00, 8.00),
    ]

    for p in produtos:
        estoque.adicionar_lote(
            Lote(estoque.proximo_id(), p, date.today(), date(2026, 12, 31), 50)
        )

    return SistemaCantina(estoque)


# =========================
# LEITURA SEGURA DE INPUT
# =========================

def ler_inteiro(mensagem, minimo=None, maximo=None):
    while True:
        try:
            valor = int(input(mensagem))
            if minimo is not None and valor < minimo:
                print(f"Digite um valor maior ou igual a {minimo}.")
                continue
            if maximo is not None and valor > maximo:
                print(f"Digite um valor menor ou igual a {maximo}.")
                continue
            return valor
        except ValueError:
            print("Entrada inválida. Digite um número inteiro.")


# =========================
# MENU
# =========================

def menu():
    print("\n" + "=" * 36)
    print("       CANTINA FATEC")
    print("=" * 36)
    print("  1  Realizar venda")
    print("  2  Ver estoque")
    print("  3  Alerta de vencimento")
    print("  4  Relatório de vendas")
    print("  5  Relatório de consumos")
    print("  6  Relatório de lucro")
    print("  7  Editar quantidade de lote")
    print("  8  Reiniciar sistema")
    print("  0  Sair")
    print("=" * 36)
    return input("  Opção: ").strip()


# =========================
# EXECUÇÃO PRINCIPAL
# =========================

if __name__ == "__main__":

    sistema = carregar_dados()

    if sistema is None:
        print("Nenhum dado encontrado. Iniciando sistema padrão.")
        sistema = sistema_padrao()

    while True:
        op = menu()

        if op == "1":
            nome = input("\nNome do cliente: ").strip()
            if not nome:
                print("Nome inválido.")
                continue

            produtos = sistema.estoque.listar_produtos_disponiveis()
            if not produtos:
                print("Sem produtos disponíveis.")
                continue

            print("\nProdutos disponíveis:")
            for i, p in enumerate(produtos, 1):
                saldo = sistema.estoque.get_saldo(p.nome)
                print(f"  {i}. {p.nome} — R$ {p.preco_venda:.2f} (estoque: {saldo})")

            escolha = ler_inteiro("Escolha o produto (número): ", 1, len(produtos)) - 1
            qtd = ler_inteiro("Quantidade: ", 1)

            sistema.realizar_venda(
                nome, "Aluno", "IA",
                produtos[escolha], qtd
            )

        elif op == "2":
            sistema.estoque.listar_estoque()

        elif op == "3":
            dias = ler_inteiro("Alertar produtos que vencem em quantos dias? ", 1)
            sistema.estoque.alertar_vencendo(dias)

        elif op == "4":
            sistema.relatorio_vendas()

        elif op == "5":
            sistema.relatorio_consumos()

        elif op == "6":
            sistema.relatorio_lucro()

        elif op == "7":
            sistema.estoque.listar_estoque()
            id_lote = ler_inteiro("\nID do lote a editar: ", 1)
            nova_qtd = ler_inteiro("Nova quantidade: ", 0)
            sistema.estoque.editar_quantidade(id_lote, nova_qtd)

        elif op == "8":
            confirma = input("Tem certeza? Isso apaga todos os dados. (s/n): ")
            if confirma.lower() == "s":
                sistema = sistema_padrao()
                salvar_dados(sistema)
                print("Sistema reiniciado.")

        elif op == "0":
            salvar_dados(sistema)
            print("Até logo!")
            break

        else:
            print("Opção inválida.")
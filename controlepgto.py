from datetime import datetime


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
# Classe RegistroPagamento (Nó da Lista Encadeada)
# =========================
class RegistroPagamento:

    def __init__(self, id_transacao, pagamento):

        self.id_transacao = id_transacao
        self.pagamento = pagamento
        self.proximo = None  # ponteiro para o próximo registro

    def __str__(self):

        return (
            f"Transação {self.id_transacao} | "
            f"Pagador: {self.pagamento.nome_pagador} | "
            f"Categoria: {self.pagamento.categoria} | "
            f"Curso: {self.pagamento.curso} | "
            f"Valor: R$ {self.pagamento.valor_pago:.2f} | "
            f"Data/Hora: {self.pagamento.data_hora}"
        )


# =========================
# Classe ControlePagamentos (Lista Encadeada)
# =========================
class ControlePagamentos:

    def __init__(self):

        self.inicio = None  # cabeça da lista


    def registrar_pagamento(self, novo_registro):

        if self.inicio is None:
            self.inicio = novo_registro
            return

        atual = self.inicio

        while atual.proximo is not None:
            atual = atual.proximo

        atual.proximo = novo_registro


    def listar_pagamentos(self):

        print("\n===== PAGAMENTOS REGISTRADOS =====")

        atual = self.inicio
        total = 0

        while atual is not None:

            print(atual)
            total += atual.pagamento.valor_pago
            atual = atual.proximo

        print("-----------------------------")
        print(f"Total arrecadado: R$ {total:.2f}")
        print(f"Quantidade de pagamentos: {self.contar_pagamentos()}")

    def contar_pagamentos(self):

        atual = self.inicio
        contador = 0

        while atual is not None:
            contador += 1
            atual = atual.proximo

        return contador


# =========================
# Simulação
# =========================
if __name__ == "__main__":

    controle = ControlePagamentos()

    p1 = Pagamento("Vladimir Sejas", "Aluno", "IA", 3.00)
    p2 = Pagamento("Maria Silva", "Aluno", "ESG", 1.50)
    p3 = Pagamento("Professor João", "Professor", "IA", 3.00)

    r1 = RegistroPagamento(1, p1)
    r2 = RegistroPagamento(2, p2)
    r3 = RegistroPagamento(3, p3)

    controle.registrar_pagamento(r1)
    controle.registrar_pagamento(r2)
    controle.registrar_pagamento(r3)

    controle.listar_pagamentos()

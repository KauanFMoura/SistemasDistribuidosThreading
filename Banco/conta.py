import threading

class Conta():
    def __init__(self, numero: int, saldo: int):
        self.numero = numero
        self.saldo = saldo
        self.conta = threading.Condition()

    def depositar(self, valor, transferencia=False):
        with self.conta:
            self.saldo += valor
            if not transferencia:
                print(f'Depósito de R$ {valor} realizado com sucesso na conta {self.numero}. '
                      f'Saldo atual: R$ {self.saldo}')
            else:
                print(f'Conta 1 recebeu transferência de R$ {valor}. Saldo atual: R$ {self.saldo}')
            self.conta.notify()

    def sacar(self, valor):
        with self.conta:
            if self.saldo >= valor:
                self.saldo -= valor
                print(f'Saque de R$ {valor} realizado com sucesso na conta {self.numero}. '
                      f'Saldo atual: R$ {self.saldo}')
            else:
                print(f'Saldo insuficiente para saque de R$ {valor} na conta {self.numero}. '
                      f'Saldo atual: R$ {self.saldo}')

            self.conta.notify()

    def transferir(self, valor, conta_destino):
        with self.conta:
            if self.saldo >= valor:
                self.saldo -= valor
                conta_destino.depositar(valor, True)
                print(f'Transferência de R$ {valor} realizada com sucesso na conta {self.numero} '
                      f'para a conta {conta_destino.numero}. Saldo atual: R$ {self.saldo}')
            else:
                print(f'Saldo insuficiente para transferência de R$ {valor} na conta {self.numero} '
                      f'para a conta {conta_destino.numero}. Saldo atual: R$ {self.saldo}')

            self.conta.notify()

    def credito_juros(self, juros):
        with self.conta:
            self.saldo += juros
            print(f'Crédito de juros de R$ {juros} realizado com sucesso na conta {self.numero}. '
                  f'Saldo atual: R$ {self.saldo}')
            self.conta.notify()

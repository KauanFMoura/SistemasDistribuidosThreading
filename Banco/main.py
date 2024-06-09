import threading
import random
from conta import Conta

def realizar_deposito(conta, valor):
    conta.depositar(valor)

def realizar_saque(conta, valor):
    conta.sacar(valor)

def realizar_transferencia(conta_origem, conta_destino, valor):
    conta_origem.transferir(valor, conta_destino)

def realizar_credito_juros(conta, juros):
    conta.credito_juros(juros)

if __name__ == '__main__':

    conta1 = Conta(1, 100)
    conta2 = Conta(2, 200)

    acoes = [
        lambda: realizar_deposito(conta1, random.randint(10, 500)),
        lambda: realizar_saque(conta1, random.randint(10, 500)),
        lambda: realizar_transferencia(conta1, conta2, random.randint(10, 500)),
        lambda: realizar_credito_juros(conta1, random.randint(1, 50)),
        lambda: realizar_deposito(conta2, random.randint(10, 500)),
        lambda: realizar_saque(conta2, random.randint(10, 500)),
        lambda: realizar_transferencia(conta2, conta1, random.randint(10, 500)),
        lambda: realizar_credito_juros(conta2, random.randint(1, 50))
    ]

    for _ in range(30):
        thread = threading.Thread(target=random.choice(acoes))
        thread.start()

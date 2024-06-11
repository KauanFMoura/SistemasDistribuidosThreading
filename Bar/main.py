import threading
import time
import random
from bartender import Bartender
from bar import Bar
from garcom import Garcom
from cliente import Cliente

if __name__ == '__main__':

    clientes_no_bar = 6
    limite_atendimentos_garcom = 3
    rodadas_disponiveis = 20
    garcoes_disponiveis = 1

    bar = Bar('Bar do Zé', rodadas_disponiveis, clientes_no_bar)
    bartender = Bartender()
    garcoes = [Garcom(f'Garçom {i}', limite_atendimentos_garcom, bar, bartender) for i in range(garcoes_disponiveis)]
    clientes = [Cliente(i, bar) for i in range(clientes_no_bar)]
    bar.clientes_nao_atendidos = clientes

    bar.start()
    for garcom in garcoes:
        garcom.start()

    for cliente in clientes:
        print(f'Cliente {cliente.numero} entrou no bar', flush=True)
        cliente.start()
        time.sleep(random.randint(0, 2))

    bar.join()

    for garcom in garcoes:
        with garcom.garcom:
            garcom.garcom.notify()
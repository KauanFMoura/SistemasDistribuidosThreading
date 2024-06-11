import threading
import time
import random
from bartender import Bartender
from bar import Bar
from garcom import Garcom
from cliente import Cliente


if __name__ == '__main__':

    clientes_no_bar = 20
    limite_atendimentos_garcom = 3
    rodadas_disponiveis = 20
    garcoes_disponiveis = 3
    livre = threading.Condition()

    bar = Bar('Bar do Zé', rodadas_disponiveis)
    bartender = Bartender()
    garcoes = [Garcom(f'Garçom {i}', limite_atendimentos_garcom, bar, bartender, livre) for i in range(garcoes_disponiveis)]
    clientes = [Cliente(i, bar, garcoes, livre) for i in range(clientes_no_bar)]

    bar.start()
    for garcom in garcoes:
        garcom.start()

    for cliente in clientes:
        cliente.start()
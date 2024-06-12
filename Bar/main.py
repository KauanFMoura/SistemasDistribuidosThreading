import threading
import time

from Bar.bar import Bar
from Bar.bartender import Bartender
from Bar.garcom import Garcom
from Bar.cliente import Cliente
from Bar.query import Query

if __name__ == '__main__':
    n_clientes = 10
    n_garcoms = 3
    rodadas = 5
    limite_atendimentos = 3

    query = Query()
    bar = Bar(n_clientes, rodadas, query)
    bartender = Bartender(bar, [], query)
    garcoms = [Garcom(i, bar, limite_atendimentos, bartender, query) for i in range(n_garcoms)]
    clientes = [Cliente(i, bar, garcoms, query) for i in range(n_clientes)]

    bar.start()
    query.start()

    for garcom in garcoms:
        garcom.start()

    for cliente in clientes:
        cliente.start()

    bar.join()

    for garcom in garcoms:
        with garcom.garcom:
            garcom.garcom.notify()
        garcom.join()

    for cliente in clientes:
        cliente.join()

    time.sleep(3)
    query.stop()
    print('\033[41mBar fechado\033[0m')


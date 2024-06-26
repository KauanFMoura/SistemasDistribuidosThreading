from threading import Thread, Semaphore
from pedidos import Pedidos
from produtor import Produtor
from consumidor import Consumidor

if __name__ == '__main__':
    limite_estoque = 3
    qntd_produtores = 20
    qntd_consumidores = 5
    limite_producao = 20

    pedidos = Pedidos(limite_estoque, limite_producao)

    produtores = [Produtor(i, pedidos) for i in range(qntd_produtores)]
    consumidores = [Consumidor(i, pedidos) for i in range(qntd_consumidores)]

    for produtor in produtores:
        produtor.start()

    for consumidor in consumidores:
        consumidor.start()

    for produtor in produtores:
        produtor.join()

    pedidos.finalizar_producao()

    for consumidor in consumidores:
        consumidor.join()

    print(f'Total Pedidos produzidos: {pedidos.quantidade_produzida}')
    print(f'Total Pedidos consumidos: {pedidos.quantidade_consumida}')
from produtor import Produtor
from consumidor import Consumidor
from pedidos import Pedidos
import threading

if __name__ == '__main__':
    limite_estoque = 10
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

    print(f'Total Comida produzida: {pedidos.quantidade_produzida}')
    print(f'Total Comida consumida: {pedidos.quantidade_consumida}')

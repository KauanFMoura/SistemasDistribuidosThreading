import threading
import time
import random

class Pedidos():
    def __init__(self, limite_pedidos, limite_produtos):
        self.lista_pedidos = []
        self.limite_pedidos = limite_pedidos
        self.limite_produtos = limite_produtos
        self.quantidade_produzida = 0
        self.quantidade_consumida = 0
        self.em_producao = True
        self.pedido = threading.Semaphore(1)
        self.semaforo_consumo = threading.Semaphore(0)
        self.semaforo_producao = threading.Semaphore(limite_pedidos)

    def produzir(self, produtor_id):
        self.semaforo_producao.acquire()
        with self.pedido:
            if not self.em_producao or self.quantidade_produzida >= self.limite_produtos:
                self.semaforo_producao.release()
                return
            self.lista_pedidos.append(1)  # Adiciona um pedido
            self.quantidade_produzida += 1
            print(f'Produtor {produtor_id} produziu um pedido. Total produzido: {self.quantidade_produzida} -'
                  f' Total em estoque: {len(self.lista_pedidos)}')
        self.semaforo_consumo.release()

    def consumir(self, consumidor_id):
        self.semaforo_consumo.acquire()
        with self.pedido:
            if not self.lista_pedidos and not self.em_producao:
                self.semaforo_consumo.release()  # Libera o semáforo para outros consumidores
                return False  # Indica que o consumidor deve parar
            if self.lista_pedidos:
                self.lista_pedidos.pop(0)  # Remove um pedido
                self.quantidade_consumida += 1
                print(f'Consumidor {consumidor_id} consumiu um pedido. Total consumido: {self.quantidade_consumida} - '
                      f'Total em estoque: {len(self.lista_pedidos)}')
                self.semaforo_producao.release()
        return True

    def finalizar_producao(self):
        with self.pedido:
            self.em_producao = False
            # Libera o semáforo de consumo o suficiente para acordar todos os consumidores
            for _ in range(len(self.lista_pedidos) + threading.active_count()):
                self.semaforo_consumo.release()
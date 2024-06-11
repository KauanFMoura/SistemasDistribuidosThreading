import threading
import time
import random

class Pedidos:
    def __init__(self, limite_pedidos, limite_produtos):
        self.pedidos_list = []
        self.limite_pedidos = limite_pedidos
        self.limite_produtos = limite_produtos
        self.quantidade_produzida = 0
        self.quantidade_consumida = 0
        self.produzindo = True
        self.mutex = threading.Semaphore(1)
        self.semaforo_consumo = threading.Semaphore(0)
        self.semaforo_producao = threading.Semaphore(limite_pedidos)

    def produzir(self, produtor_id):
        self.semaforo_producao.acquire()
        with self.mutex:
            if not self.produzindo or self.quantidade_produzida >= self.limite_produtos:
                self.semaforo_producao.release()
                return
            self.pedidos_list.append(1)  # Adiciona um pedido
            self.quantidade_produzida += 1
            print(f'Produtor {produtor_id} produziu um pedido. Total produzido: {self.quantidade_produzida} -'
                  f' Total em estoque: {len(self.pedidos_list)}')
        self.semaforo_consumo.release()

    def consumir(self, consumidor_id):
        self.semaforo_consumo.acquire()
        with self.mutex:
            if not self.pedidos_list and not self.produzindo:
                self.semaforo_consumo.release()  # Libera o semáforo para outros consumidores
                return False  # Indica que o consumidor deve parar
            if self.pedidos_list:
                self.pedidos_list.pop(0)  # Remove um pedido
                self.quantidade_consumida += 1
                print(f'Consumidor {consumidor_id} consumiu um pedido. Total consumido: {self.quantidade_consumida} - '
                      f'Total em estoque: {len(self.pedidos_list)}')
                self.semaforo_producao.release()
        return True

    def finalizar_producao(self):
        with self.mutex:
            self.produzindo = False
            # Libera o semáforo de consumo o suficiente para acordar todos os consumidores
            for _ in range(len(self.pedidos_list) + threading.active_count()):
                self.semaforo_consumo.release()


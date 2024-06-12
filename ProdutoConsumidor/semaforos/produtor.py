import threading
import time
import random
class Produtor(threading.Thread):
    def __init__(self, numero, pedidos):
        super().__init__()
        self.numero = numero
        self.pedidos = pedidos

    def run(self):
        while True:
            with self.pedidos.pedido:
                if self.pedidos.quantidade_produzida >= self.pedidos.limite_produtos:
                    break
            self.pedidos.produzir(self.numero)
            time.sleep(random.uniform(0.1, 0.5))  # Simula o tempo de produção
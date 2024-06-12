import threading
import time
import random
class Consumidor(threading.Thread):
    def __init__(self, numero, pedidos):
        super().__init__()
        self.numero = numero
        self.pedidos = pedidos

    def run(self):
        while True:
            with self.pedidos.pedido:
                if not self.pedidos.em_producao and len(self.pedidos.lista_pedidos) == 0:
                    break
            self.pedidos.consumir(self.numero)
            time.sleep(random.uniform(0.1, 0.5))  # Simula o tempo de consumo

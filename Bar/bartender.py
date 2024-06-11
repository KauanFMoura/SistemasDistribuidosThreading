import threading
import time
class Bartender(threading.Thread):

    def __init__(self):
        super().__init__()
        self.bartender = threading.Condition()
        self.ocupado = False
        self.clientes_atendidos = 0

    def preparar_pedidos(self, garcom):
        with self.bartender:
            self.ocupado = True
            print(f'Bartender preparando pedido para {garcom.nome}')
            time.sleep(2)
            print(f'Bartender terminou pedido para {garcom.nome}')
            self.ocupado = False
            self.bartender.notify()
import threading
import time
class Bartender(threading.Thread):

    def __init__(self):
        super().__init__()
        self.bartender = threading.Condition()
        self.ocupado = False
        self.clientes_atendidos = 0

    def preparar_pedidos(self, garcom):
        self.ocupado = True
        print(f'Bartender preparando pedido para {garcom.nome}', flush=True)
        time.sleep(2)
        print(f'Bartender terminou pedido para {garcom.nome}', flush=True)
        self.ocupado = False
        self.bartender.notify_all()
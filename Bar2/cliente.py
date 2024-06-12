import threading
import time
import random

class Cliente(threading.Thread):

    def __init__(self, numero, bar, garcoms):
        super().__init__()
        self.numero = numero
        self.satisfeito = False
        self.bar = bar
        self.garcoms = garcoms
        self.garcom_atendendo = None

    def fazer_pedido(self):
        for garcom in self.garcoms:
            with garcom.garcom:
                with self.bar.bar:
                    if len(garcom.pedidos) < garcom.limite_atendimentos and self.bar.aberto:
                        self.garcom_atendendo = garcom
                        garcom.pedidos.append(self)
                        print(f'Cliente {self.numero} fez pedido para garçom {garcom.numero}')
                        garcom.garcom.notify_all()
                        return True

        return False

    def esperar_pedido(self):
        with self.garcom_atendendo.garcom:
            while self in self.garcom_atendendo.pedidos:
                print(f'Cliente {self.numero} esperando pedido')
                self.garcom_atendendo.garcom.wait()

            self.garcom_atendendo.garcom.notify_all()

    def comer_pedido(self):
        print(f'Cliente {self.numero} está comendo', flush=True)
        time.sleep(random.randint(1, 5))

        if random.choice([True, False]):
            print(f'Cliente {self.numero} está satisfeito', flush=True)
            self.satisfeito = True
            with self.bar.bar:
                self.bar.clientes_satisfeitos += 1
                self.bar.bar.notify_all()
        else:
            print(f'Cliente {self.numero} não está satisfeito', flush=True)

    def run(self):
        print(f'Cliente {self.numero} chegou no bar')
        while self.bar.aberto and not self.satisfeito:
            if self.fazer_pedido():
                self.esperar_pedido()
                self.comer_pedido()

        print(f'Cliente {self.numero} saiu do bar')
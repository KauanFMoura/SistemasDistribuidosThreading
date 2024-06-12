import threading
import time
import random


class Cliente(threading.Thread):
    def __init__(self, numero, bar, garcoms, query):
        super().__init__()
        self.numero = numero
        self.satisfeito = False
        self.bar = bar
        self.garcoms = garcoms
        self.garcom_atendendo = None
        self.query = query

    def fazer_pedido(self):
        for garcom in self.garcoms:
            with garcom.garcom:
                if len(garcom.pedidos) < garcom.limite_atendimentos and self.bar.aberto:
                    self.garcom_atendendo = garcom
                    garcom.pedidos.append(self)
                    self.query.add_query(f'\033[36mCliente {self.numero} fez pedido para garçom {garcom.numero}\033[0m')
                    garcom.garcom.notify()
                    return True
        return False

    def esperar_pedido(self):
        with self.garcom_atendendo.garcom:
            while self in self.garcom_atendendo.pedidos:
                self.query.add_query(f'\033[33mCliente {self.numero} esperando pedido\033[0m')
                self.garcom_atendendo.garcom.wait()

    def comer_pedido(self):
        self.query.add_query(f'\033[35mCliente {self.numero} está comendo\033[0m')
        time.sleep(random.randint(1, 5))

        if random.choice([True, False]):
            self.query.add_query(f'\033[38;5;22mCliente {self.numero} está satisfeito\033[0m')
            self.satisfeito = True
            with self.bar.bar:
                self.bar.clientes_satisfeitos += 1
                self.bar.bar.notify_all()
        else:
            self.query.add_query(f'\033[38;5;208mCliente {self.numero} não está satisfeito\033[0m')

    def run(self):
        self.query.add_query(f'\033[32mCliente {self.numero} chegou no bar\033[0m')
        while self.bar.aberto and not self.satisfeito:
            if self.fazer_pedido():
                self.esperar_pedido()
                self.comer_pedido()

        self.query.add_query(f'\033[31mCliente {self.numero} saiu do bar\033[0m')

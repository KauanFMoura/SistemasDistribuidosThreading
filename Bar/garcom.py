import threading
import time


class Garcom(threading.Thread):

    def __init__(self, nome, limite_atendimentos, bar, bartender):
        super().__init__()
        self.garcom = threading.Condition()
        self.garcom_pedidos = threading.Condition()
        self.nome = nome
        self.limite_atendimentos = limite_atendimentos
        self.pedidos = []
        self.bar = bar
        self.bartender = bartender

    def recebe_pedidos(self):
        with self.garcom:
            while len(self.pedidos) < self.limite_atendimentos and len(self.bar.clientes_nao_atendidos) != 0:
                self.garcom.wait()

            if len(self.pedidos) == 0:
                return False

            self.bar.remove_garcom_disponivel(self)
            print(f'Garçom {self.nome} recebeu todos pedidos possiveis para essa rodada', flush=True)
            self.garcom.notify()
            return True

    def registrar_pedido(self, cliente):
        self.pedidos.append(cliente)
        self.bar.cliente_atendido(cliente)
        print(f'Cliente {cliente.numero} fez pedido para {self.nome}', flush=True)
        print(len(self.pedidos))

        self.garcom.notify()

    def levar_pedido(self):
        with self.bartender.bartender:
            while self.bartender.ocupado:
                self.bartender.bartender.wait()

            print(f'Garçom {self.nome} levou os pedidos para o Bartender', flush=True)
            self.bartender.preparar_pedidos(self)
            self.bartender.bartender.notify()

    def entregar_pedido(self):
        with self.garcom_pedidos:
            for cliente in self.pedidos:
                cliente.pedido_entregue = True
                time.sleep(1)

            self.pedidos = []

    def run(self):
        while self.bar.aberto:
            with self.garcom:
                self.bar.add_garcom_disponivel(self)
                self.garcom.notify()

            if self.recebe_pedidos():
                self.levar_pedido()
                self.entregar_pedido()
                self.bar.rodada()
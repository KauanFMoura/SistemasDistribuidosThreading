import threading
import time


class Garcom(threading.Thread):

    def __init__(self, nome, limite_atendimentos, bar, bartender, livre):
        super().__init__()
        self.garcom = threading.Condition()
        self.garcom_pedidos = threading.Condition()
        self.nome = nome
        self.limite_atendimentos = limite_atendimentos
        self.pedidos = []
        self.bar = bar
        self.bartender = bartender
        self.livre = livre

    def recebe_pedidos(self):
        with self.garcom:
            while len(self.pedidos) < self.limite_atendimentos and not self.bar.clientes_nao_atendidos:
                self.garcom.wait()

            print(f'Garçom {self.nome} recebeu todos pedidos possiveis para essa rodada')
            self.garcom.notify()

    def registrar_pedido(self, cliente):
        with self.garcom:
            self.pedidos.append(cliente)
            self.bar.cliente_atendido(cliente)  # Remove o cliente da lista de clientes não atendidos
            print(f'Cliente {cliente.numero} fez pedido para {self.nome}')
            self.garcom.notify()

    def levar_pedido(self):
        with self.bartender.bartender:
            while self.bartender.ocupado:
                self.bartender.bartender.wait()

        print(f'Garçom {self.nome} levou os pedidos para o Bartender')
        self.bartender.preparar_pedidos(self)

    def entregar_pedido(self):
        with self.garcom_pedidos:
            for cliente in self.pedidos:
                self.pedidos.remove(cliente)
                self.garcom_pedidos.notify()
                time.sleep(1)

            print(f'Garçom {self.nome} entregou Todos os seus pedidos!')
    def liberar_garcom(self):
        with self.livre:
            self.livre.notify()
    def run(self):
        while self.bar.aberto:
            self.recebe_pedidos()
            self.levar_pedido()
            self.entregar_pedido()
            self.bar.rodada()
            self.liberar_garcom()
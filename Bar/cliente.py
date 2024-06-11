import threading
import time
import random


class Cliente(threading.Thread):
    def __init__(self, numero, bar, garcoes, livre):
        super().__init__()
        self.numero = numero
        self.bar = bar
        self.garcoes = garcoes
        self.garcom_atendendo = None
        self.satisfeito = False
        self.livre = livre
        self.pedido_registrado = False
        self.pedido_recebido = False

    def fazer_pedido(self):
        while not self.pedido_registrado:
            with self.livre:
                for garcom in self.garcoes:
                    with garcom.garcom:
                        if len(garcom.pedidos) < garcom.limite_atendimentos:
                            self.garcom_atendendo = garcom
                            garcom.registrar_pedido(self)
                            self.pedido_registrado = True
                            break

                if not self.pedido_registrado:
                    print(f"Cliente {self.numero} está aguardando um garçom disponível.")
                    self.livre.wait()  # Aguarda notificação de garçom disponível

    def esperar_pedido(self):
        with self.garcom_atendendo.garcom_pedidos:
            while self in self.garcom_atendendo.pedidos:
                self.garcom_atendendo.garcom_pedidos.wait()
                print(f'Cliente {self.numero} está esperando pedido')

    def receber_pedido(self):
        print(f'Cliente {self.numero} recebeu pedido')

    def comer_pedido(self):
        print(f'Cliente {self.numero} está comendo')
        time.sleep(random.randint(1, 5))  # Cliente come por um tempo aleatório

        if random.choice([True, False]):  # Cliente pode ficar satisfeito ou não
            print(f'Cliente {self.numero} está satisfeito')
            self.satisfeito = True  # Cliente está satisfeito

    def run(self):
        while self.bar.aberto and not self.satisfeito:
            self.pedido_registrado = False
            self.garcom_atendendo = None
            self.bar.clientes_nao_atendido(self)  # Adiciona o cliente à lista de clientes não atendidos
            self.fazer_pedido()
            self.esperar_pedido()
            self.receber_pedido()
            self.comer_pedido()

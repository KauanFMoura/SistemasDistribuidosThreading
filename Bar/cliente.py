import threading
import time
import random


class Cliente(threading.Thread):
    def __init__(self, numero, bar):
        super().__init__()
        self.numero = numero
        self.bar = bar
        self.satisfeito = False
        self.pedido_entregue = False

    def fazer_pedido(self):
        with self.bar.bar:
            while len(self.bar.garcoes_disponiveis) == 0:
                print(f'Cliente {self.numero} está esperando garçom', flush=True)
                self.bar.bar.wait()

            garcom = random.choice(self.bar.garcoes_disponiveis)
            with garcom.garcom:
                if len(garcom.pedidos) == garcom.limite_atendimentos:
                    garcom.garcom.wait()

                garcom.registrar_pedido(self)
                garcom.garcom.notify()

            self.bar.bar.notify_all()

    def esperar_pedido(self):
        print(f'Cliente {self.numero} está esperando pedido', flush=True)
        while not self.pedido_entregue:
            time.sleep(0.1)

    def receber_pedido(self):
        print(f'Cliente {self.numero} recebeu pedido', flush=True)

    def comer_pedido(self):
        print(f'Cliente {self.numero} está comendo', flush=True)
        time.sleep(random.randint(1, 5))  # Cliente come por um tempo aleatório

        if random.choice([True, False]):  # Cliente pode ficar satisfeito ou não
            print(f'Cliente {self.numero} está satisfeito', flush=True)

            self.satisfeito = True  # Cliente está satisfeito
            self.bar.cliente_satisfeito()  # Adiciona o cliente à lista de clientes satisfeitos
        else:
            self.pedido_entregue = False
            print(f'Cliente {self.numero} não está satisfeito', flush=True)

    def run(self):
        print(f'Cliente {self.numero} entrou no bar', flush=True)
        while self.bar.aberto and not self.satisfeito:
            self.bar.clientes_nao_atendidos.append(self)
            self.fazer_pedido()
            self.esperar_pedido()
            self.receber_pedido()
            self.comer_pedido()


import threading


class Garcom(threading.Thread):
    def __init__(self, numero, bar, limite_atendimentos, bartender, query):
        super().__init__()
        self.numero = numero
        self.garcom = threading.Condition()
        self.bar = bar
        self.pedidos = []
        self.limite_atendimentos = limite_atendimentos
        self.bartender = bartender
        self.query = query

    def recebe_pedidos(self):
        with self.garcom:
            while len(self.pedidos) == 0 and self.bar.aberto:
                self.garcom.wait()

            if not self.bar.aberto or len(self.pedidos) == 0:
                return False

            self.query.add_query(f'\033[43mGarçom {self.numero} recebeu todos pedidos possiveis para essa rodada\033[0m')
            return True

    def levar_pedido(self):
        self.bartender.fazer_bebida(self)

    def entregar_pedido(self):
        with self.garcom:
            while self.pedidos:
                cliente = self.pedidos.pop(0)
                self.query.add_query(f'\033[38;5;82mGarçom {self.numero} entregando pedido para cliente {cliente.numero}\033[0m')
                with cliente.garcom_atendendo.garcom:
                    cliente.garcom_atendendo.garcom.notify_all()
            self.garcom.notify_all()

    def rodada(self):
        with self.bar.bar:
            self.bar.rodadas -= 1
            self.query.add_query(f'\033[44mGarçom {self.numero} terminou rodada - {self.bar.rodadas} rodadas restantes\033[0m')
            self.bar.bar.notify_all()

    def run(self):
        while self.bar.aberto:
            if self.recebe_pedidos():
                self.levar_pedido()
                self.entregar_pedido()
                self.rodada()
        self.query.add_query(f'\033[31mGarçom {self.numero} saiu do bar\033[0m')

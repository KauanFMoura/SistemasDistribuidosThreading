import threading


class Garcom(threading.Thread):
    def __init__(self, numero, bar, limite_atendimentos, bartender):
        super().__init__()
        self.numero = numero
        self.garcom = threading.Condition()
        self.bar = bar
        self.pedidos = []
        self.limite_atendimentos = limite_atendimentos
        self.bartender = bartender

    def recebe_pedidos(self):
        with self.garcom:
            while len(self.pedidos) == 0 and self.bar.aberto:
                self.garcom.wait()

            if not self.bar.aberto or len(self.pedidos) == 0:
                return False

            print(f'Garçom {self.numero} recebeu todos pedidos possiveis para essa rodada')
            return True

    def levar_pedido(self):
        self.bartender.fazer_bebida(self)

    def entregar_pedido(self):
        with self.garcom:
            while self.pedidos:
                cliente = self.pedidos.pop(0)
                print(f'Garçom {self.numero} entregando pedido para cliente {cliente.numero}')
                with cliente.garcom_atendendo.garcom:
                    cliente.garcom_atendendo.garcom.notify_all()
            self.garcom.notify_all()

    def rodada(self):
        with self.bar.bar:
            self.bar.rodadas -= 1
            print(f'Garçom {self.numero} terminou rodada - {self.bar.rodadas} rodadas restantes')
            self.bar.bar.notify_all()

    def run(self):
        while self.bar.aberto:
            if self.recebe_pedidos():
                self.levar_pedido()
                self.entregar_pedido()
                self.rodada()
        print(f'Garçom {self.numero} saiu do bar')

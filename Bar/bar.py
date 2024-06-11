import threading
import time


class Bar(threading.Thread):

    def __init__(self, nome: str, rodadas_disponiveis: int, numero_clientes_bar: int):
        super().__init__()
        self.nome = nome
        self.aberto = True
        self.rodadas_disponiveis = rodadas_disponiveis
        self.rodadas_realizadas = 0
        self.bar = threading.Condition()
        self.garcoes_disponiveis = []
        self.clientes_nao_atendidos = []
        self.numero_clientes_bar = numero_clientes_bar
        self.clientes_satisfeitos = 0

    def add_garcom_disponivel(self, garcom):
        with self.bar:
            self.garcoes_disponiveis.append(garcom)
            self.bar.notify_all()

    def remove_garcom_disponivel(self, garcom):
        self.garcoes_disponiveis.remove(garcom)

    def fechar(self):
        with self.bar:  # Garante que não haverá leitura suja
            while self.rodadas_disponiveis > 0 and self.clientes_satisfeitos != self.numero_clientes_bar:  # Enquanto houver rodadas disponíveis espera
                self.bar.wait()

            self.aberto = False  # Fecha o bar
            print('Bar fechado', flush=True)

    def clientes_nao_atendido(self, cliente):
        with self.bar:
            self.clientes_nao_atendidos.append(cliente)
            self.bar.notify()

    def cliente_atendido(self, cliente):
        with self.bar:
            self.clientes_nao_atendidos.remove(cliente)
            self.bar.notify()

    def cliente_satisfeito(self):
        with self.bar:
            self.clientes_satisfeitos += 1
            self.bar.notify()

    def rodada(self):
        with self.bar:
            self.rodadas_realizadas += 1
            print(f'Rodada {self.rodadas_realizadas} finalizada', flush=True)
            self.rodadas_disponiveis -= 1
            print(f'Rodadas disponíveis: {self.rodadas_disponiveis}', flush=True)
            self.bar.notify()

    def run(self):
        while self.aberto:
            self.fechar()

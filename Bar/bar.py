import threading
import time


class Bar(threading.Thread):

    def __init__(self, nome: str, rodadas_disponiveis: int):
        super().__init__()
        self.nome = nome
        self.aberto = True
        self.rodadas_disponiveis = rodadas_disponiveis
        self.rodadas_realizadas = 0
        self.bar = threading.Condition()
        self.clientes_nao_atendidos = []

    def fechar(self):
        with self.bar:  # Garante que não haverá leitura suja
            while self.rodadas_disponiveis > 0 or self.clientes_nao_atendidos:  # Enquanto houver rodadas disponíveis espera
                self.bar.wait()

            self.aberto = False  # Fecha o bar

    def clientes_nao_atendido(self, cliente):
        with self.bar:
            self.clientes_nao_atendidos.append(cliente)
            self.bar.notify()

    def cliente_atendido(self, cliente):
        with self.bar:
            self.clientes_nao_atendidos.remove(cliente)
            self.bar.notify()

    def rodada(self):
        with self.bar:
            self.rodadas_realizadas += 1
            print(f'Rodada {self.rodadas_realizadas} finalizada')
            self.rodadas_disponiveis -= 1
            print(f'Rodadas disponíveis: {self.rodadas_disponiveis}')
            self.bar.notify()
    def run(self):
        self.fechar()

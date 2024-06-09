import threading
import random
from time import sleep
from barbearia import Barbearia

class Barbeiro(threading.Thread):

    def __init__(self, dormindo: bool, barbearia: Barbearia, cor: str, reset='\033[0m'):
        super().__init__()
        self.dormindo = dormindo
        self.barbearia = barbearia
        self.ocupado = False
        self.barbeiro = threading.Condition()
        self.cor = cor
        self.reset = reset

    def acordar(self):
        if self.dormindo:
            self.dormindo = False

    def dormir(self):
        with self.barbearia.cadeiras:
            if self.barbearia.ocup_cadeiras == 0 and not self.ocupado:
                self.dormindo = True
                print(self.cor + "Barbeiro dormindo." + self.reset)
                self.barbearia.cadeiras.wait()

    def cortar_cabelo(self, nome_cliente: str, cor: str, reset: str):
        self.ocupado = True
        print(cor + f"{nome_cliente} está cortando cabelo." + reset)
        sleep(random.randint(1, 3))
        print(cor + f"{nome_cliente} terminou de cortar cabelo." + reset)
        self.ocupado = False
        self.barbeiro.notify()

    def run(self):
        while True:
            self.dormir()

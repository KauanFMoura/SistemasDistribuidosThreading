import threading
from barbeiro import Barbeiro
from barbearia import Barbearia
class cliente(threading.Thread):

    def __init__(self, nome: str, barbearia: Barbearia, barbeiro: Barbeiro, cor: str, reset='\033[0m'):
        super().__init__()
        self.nome = nome
        self.barbearia = barbearia
        self.barbeiro = barbeiro
        self.cor = cor
        self.reset = reset

    def sentar_cadeira(self):
        if self.barbearia.ocupar_cadeira():
            if self.barbeiro.dormindo:
                print(self.cor + 'cliente acordou barbeiro.' + self.reset)
                self.barbeiro.acordar()

            print(self.cor + f"{self.nome} sendou numa cadeira." + self.reset)
            self.esperar_barbeiro()
        else:
            print(self.cor + f"{self.nome} não conseguiu cortar cabelo, barbearia lotada." + self.reset)

    def esperar_barbeiro(self):
        with self.barbeiro.barbeiro:
            while self.barbeiro.ocupado:
                self.barbeiro.barbeiro.wait()

            self.barbearia.desocupar_cadeira()
            self.barbeiro.cortar_cabelo(self.nome, self.cor, self.reset)

    def run(self):
        self.sentar_cadeira()

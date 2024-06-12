import threading
import time
from mesa import Mesa
class Filosofo(threading.Thread):

    def __init__(self, nome, cor, garfo_esquerda, garfo_direita, pos_garf_esq, pos_garf_dir, mesa, reset='\033[0m'):
        super().__init__()
        self.nome = nome
        self.cor = cor
        self.reset = reset
        self.garfo_esquerda = garfo_esquerda
        self.garfo_direita = garfo_direita
        self.pos_garf_esq = pos_garf_esq
        self.pos_garf_dir = pos_garf_dir
        self.mesa = mesa

    def comer(self):
        with self.mesa.tigela_central:
            if self.mesa.tamanho_arroz == 0:
                exit()
            self.mesa.tamanho_arroz -= 1
            print(self.cor + f"{self.nome} pegou um punhado de arroz. Restam {self.mesa.tamanho_arroz} punhados." + self.reset)
            self.mesa.tigela_central.notify()

        print(self.cor + f"{self.nome} está comendo." + self.reset)
        time.sleep(1)
        print(self.cor + f"{self.nome} terminou de comer." + self.reset)

    def tentar_comer(self):
        if self.garfo_esquerda.acquire(False):
            if self.garfo_direita.acquire(False): # Tenta pegar o garfo direito manualmente
                try:
                    self.comer()
                finally:
                    self.garfo_direita.release()
                    self.garfo_esquerda.release()
            else:
                print(self.cor + f"{self.nome} não conseguiu pegar o garfo direito na posição {self.pos_garf_dir}." + self.reset)
                self.garfo_esquerda.release()
        else:
            print(self.cor + f"{self.nome} não conseguiu pegar o garfo esquerdo na posição {self.pos_garf_esq}." + self.reset)

        self.meditar()

    def meditar(self):
        print(self.cor + f"{self.nome} está meditando." + self.reset)
        time.sleep(2)

    def run(self):
        while True:
            self.tentar_comer()

import threading
import random
import time

class Roleta(threading.Thread):

    def __init__(self, contador, numero):
        super().__init__()
        self.numero = numero
        self.contador_central = contador

    def entrar(self, n_pessoas):
        with self.contador_central.contador:
            if not self.contador_central.aberto:
                print("Tentativa de entrada quando o contador está fechado. Nenhuma pessoa entrou.")
                exit()

            if self.contador_central.total_contador + n_pessoas > self.contador_central.limit:
                n_pessoas_que_podem_entrar = self.contador_central.limit - self.contador_central.total_contador
                if n_pessoas_que_podem_entrar > 0:
                    self.contador_central.total_contador += n_pessoas_que_podem_entrar
                    print(f'Entraram {n_pessoas_que_podem_entrar} pessoas pela Roleta {self.numero}. Total de pessoas: {self.contador_central.total_contador}')
                    self.contador_central.fechar()
            else:
                self.contador_central.total_contador += n_pessoas
                print(f'Entraram {n_pessoas} pessoas pela Roleta {self.numero}. Total de pessoas: {self.contador_central.total_contador}')
                self.contador_central.contador.notify()

    def run(self):
        while True:
            n_pessoas = random.randint(1, 10)
            self.entrar(n_pessoas)
            time.sleep(random.randint(1, 3))

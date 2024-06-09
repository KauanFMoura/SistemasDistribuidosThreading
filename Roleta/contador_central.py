import threading

class contadorCentral(threading.Thread):

    def __init__(self, limit: int):
        super().__init__()
        self.limit = limit
        self.contador = threading.Condition()
        self.total_contador = 0
        self.aberto = True

    def fechar(self):
        self.aberto = False
        print("Limite Atingido! Não é mais possível entrar.")

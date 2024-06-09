import threading

class Mesa(threading.Thread):

    def __init__(self, tamanho_arroz):
        super().__init__()
        self.garfos = [threading.Lock() for _ in range(5)]
        self.tigela_central = threading.Condition()
        self.tamanho_arroz = tamanho_arroz


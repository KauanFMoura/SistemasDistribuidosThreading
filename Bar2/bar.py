import threading
class Bar(threading.Thread):

    def __init__(self, n_clientes, rodadas):
        super().__init__()
        self.bar = threading.Condition()
        self.aberto = True
        self.rodadas = rodadas
        self.clientes_satisfeitos = 0
        self.clientes_total = n_clientes

    def fechar(self):
        with self.bar:
            while self.rodadas > 0 and self.clientes_satisfeitos < self.clientes_total:
                self.bar.wait()

            self.aberto = False
            print("Bar fechado")
            self.bar.notify_all()

    def run(self):
        self.fechar()

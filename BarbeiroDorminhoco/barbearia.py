import threading
class Barbearia(threading.Thread):

    def __init__(self, cadeiras: int):
        super().__init__()
        self.limit_cadeiras = cadeiras
        self.ocup_cadeiras = 0
        self.cadeiras = threading.Condition()

    def ocupar_cadeira(self):
        with self.cadeiras:
            if self.ocup_cadeiras < self.limit_cadeiras:
                self.ocup_cadeiras += 1
                self.cadeiras.notify()
                return True
            
            return False

    def desocupar_cadeira(self):
        with self.cadeiras:
            self.ocup_cadeiras -= 1
            self.cadeiras.notify()

    def fechar(self):
        with self.cadeiras:
            if self.ocup_cadeiras == 0:
                print("Barbearia fechada.")
                exit()


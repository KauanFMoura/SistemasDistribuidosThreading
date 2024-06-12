import threading
import time
import random

class Bartender:
    def __init__(self, bar, garcons):
        self.bartender = threading.Condition()

    def fazer_bebida(self, garcom):
        with self.bartender:
            print(f'Bartender fazendo bebida para garçom {garcom.numero}')
            time.sleep(random.randint(1, 5))
            print(f'Bartender terminou bebida para garçom {garcom.numero}')
            with garcom.garcom:
                garcom.garcom.notify_all()

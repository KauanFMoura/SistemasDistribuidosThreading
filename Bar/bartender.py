import threading
import time
import random


class Bartender:
    def __init__(self, bar, garcons, query):
        self.query = query
        self.bartender = threading.Condition()

    def fazer_bebida(self, garcom):
        with self.bartender:
            self.query.add_query(f'Bartender fazendo bebida para garçom {garcom.numero}')
            time.sleep(random.randint(1, 5))
            self.query.add_query(f'Bartender terminou bebida para garçom {garcom.numero}')
            with garcom.garcom:
                garcom.garcom.notify_all()

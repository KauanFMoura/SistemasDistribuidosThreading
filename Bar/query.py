import threading
import time


class Query(threading.Thread):
    def __init__(self, bar):
        super().__init__()
        self.querys = []
        self.bar = bar
        self.semaphore = threading.Semaphore(1)

    def run(self):
        while self.bar.aberto or len(self.querys) > 0:
            with self.semaphore:
                if self.querys:
                    for query in self.querys:
                        print(query)
                    self.querys.clear()
            time.sleep(0.5)

    def add_query(self, query):
        with self.semaphore:
            self.querys.append(query)

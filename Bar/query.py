import threading
import time


class Query(threading.Thread):
    def __init__(self):
        super().__init__()
        self.querys = []
        self.semaphore = threading.Semaphore(1)
        self.rodando = True

    def run(self):
        while self.rodando:
            with self.semaphore:
                if self.querys:
                    self.querys = sorted(self.querys, key=lambda x: x["time"])
                    for query in self.querys:
                        print(query['msg'])
                    self.querys.clear()
            time.sleep(0.5)

    def stop(self):
        self.rodando = False

    def add_query(self, query, horario_requisitado):
        with self.semaphore:
            self.querys.append({
                'msg': query,
                'time': horario_requisitado
            })

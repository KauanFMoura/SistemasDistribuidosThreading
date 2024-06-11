import threading

class Pedidos:
    def __init__(self, limite_pedidos, limite_produtos):
        self.pedidos_list = []
        self.pedidos = threading.Condition()
        self.limite_pedidos = limite_pedidos
        self.limite_produtos = limite_produtos
        self.quantidade_produzida = 0
        self.quantidade_consumida = 0
        self.produzindo = True

    def produzir(self, produtor_id):
        with self.pedidos:
            while len(self.pedidos_list) == self.limite_pedidos and self.produzindo:
                self.pedidos.wait()

            if not self.produzindo or self.quantidade_produzida >= self.limite_produtos:
                return

            self.pedidos_list.append(1)  # Adiciona um pedido
            self.quantidade_produzida += 1
            print(f'Produtor {produtor_id} produziu um pedido. Total produzido: {self.quantidade_produzida} - '
                  f'Total em estoque: {len(self.pedidos_list)}')
            self.pedidos.notify_all()

    def consumir(self, consumidor_id):
        with self.pedidos:
            while len(self.pedidos_list) == 0 and self.produzindo:
                self.pedidos.wait()

            if len(self.pedidos_list) == 0:
                return

            self.pedidos_list.pop(0)  # Remove um pedido
            self.quantidade_consumida += 1
            print(f'Consumidor {consumidor_id} consumiu um pedido. Total consumido: {self.quantidade_consumida} - '
                  f'Total em estoque: {len(self.pedidos_list)}')
            self.pedidos.notify_all()

    def finalizar_producao(self):
        with self.pedidos:
            self.produzindo = False
            self.pedidos.notify_all()

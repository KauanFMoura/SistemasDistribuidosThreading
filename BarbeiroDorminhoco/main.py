import random
from cliente import cliente
from barbeiro import Barbeiro
from barbearia import Barbearia
from cores import cores
from time import sleep
import names

if '__main__' == __name__:

    barbearia = Barbearia(3)
    cadeiras = barbearia.cadeiras
    barbeiro = Barbeiro(True, barbearia, cores.VERMELHO, cores.RESET)
    barbeiro.start()

    all_cores = [cores.VERDE, cores.AMARELO, cores.AZUL, cores.ROXO, cores.CIANO, cores.BRANCO, cores.CINZA_CLARO,
             cores.VERDE_CLARO, cores.AMARELO_CLARO, cores.AZUL_CLARO, cores.ROXO_CLARO, cores.CIANO_CLARO,
             cores.BRANCO_BRILHANTE, cores.PRETO, cores.ROSA, cores.LARANJA, cores.VERDE_AMARELO, cores.AMARELO_VERDE,
             cores.VERDE_AZUL, cores.AZUL_VERMELHO, cores.MARROM, cores.ROSA_CLARO]

    clientes = []
    for i in range(15):
        nome = names.get_full_name('pt')
        cor = all_cores[i]
        cliente(nome, barbearia, barbeiro, cor).start()
        sleep(random.randint(0, 2))

    for cliente in clientes:
        cliente.join()

    with barbeiro.barbeiro:
        while barbeiro.ocupado:
            barbeiro.barbeiro.wait()
        barbearia.fechar()
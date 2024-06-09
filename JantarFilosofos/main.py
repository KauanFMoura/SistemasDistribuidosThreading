import threading
import sys
from filosofo import Filosofo
from cores import cores
from mesa import Mesa

if __name__ == '__main__':

    mesa = Mesa(5)
    all_cores = [cores.VERDE, cores.AMARELO, cores.AZUL, cores.ROXO, cores.CIANO]
    nomes = ["Aristóteles (0f1)", "Platão (1f2)", "Sócrates (2f3)", "Descartes (3f4)", "Kant (4f0)"]
    filosofos = [Filosofo(nomes[i], all_cores[i], mesa.garfos[i], mesa.garfos[(i + 1) % 5], i, ((i+1) % 5), mesa) for i in range(5)]

    for filosofo in filosofos:
        filosofo.start()

    while True:
        if mesa.tamanho_arroz == 0:
            print("Acabou o Arroz da Tigela Central!")
            break
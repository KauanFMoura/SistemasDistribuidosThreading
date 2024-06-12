from roleta import Roleta
from contador_central import contadorCentral

if __name__ == "__main__":

    limit_pessoas = 100
    n_roletas = 5

    contador = contadorCentral(limit_pessoas)
    roletas = [Roleta(contador, i) for i in range(1, n_roletas+1)]

    for roleta in roletas:
        roleta.start()

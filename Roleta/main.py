from roleta import Roleta
from contador_central import contadorCentral

if __name__ == "__main__":

    limit_pessoas = 1000
    n_roletas = 5

    contador = contadorCentral(limit_pessoas)
    roletas = [Roleta(contador) for i in range(n_roletas)]

    for roleta in roletas:
        roleta.start()

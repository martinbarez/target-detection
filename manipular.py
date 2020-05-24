from difflib import SequenceMatcher
import numpy

#para llevar el contador aquí escondido en vez de fuera
class contar:
    def __init__(self):
        self.bits = 0

    def truncar(self, X):
        bit = 56

        #trunco
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                X[i][j] = X[i][j] // 1

        #que todos los elementos cumplan ambas condiciones
        while True and bit > 0 and all(
            j <  (2 << (bit-1)) and
            j > -(2 << (bit-1))
                  for i in X
                  for j in i):
            bit = bit - 1


        self.bits = max(bit, self.bits)
        return bit

def comparar(fijo, flotante):
    #añado índices
    fijo = list(enumerate(fijo))
    flotante = list(enumerate(flotante))

    #ordeno
    fijo.sort(key=lambda tup: tup[1], reverse=True)
    flotante.sort(key=lambda tup: tup[1], reverse=True)

    #me quedo con el 5%
    #fijo = fijo [: len(fijo)//20]
    #flotante = flotante[: len(flotante)//20]

    #elimino valores
    fijo = [x[0] for x in fijo]
    flotante = [x[0] for x in flotante]

    #comparo índices
    sm = SequenceMatcher(None, fijo, flotante)

    return sm.ratio()

#para llevar el contador aquí escondido en vez de fuera
class contar:
    def __init__(self):
        self.bits = 0

    #tengo que renombrar esto, porque hace de todo menos truncar
    def truncar(self, X):
        bit = 56

        #trunco
        for i in range(X.shape[0]):
            for j in range(X.shape[1]):
                X[i][j] = X[i][j] // 1

        #cuento los bits necesarios
        #cuando todos los elementos cumplen ambas condiciones
        while False and bit > 0 and all(
            j <  (2 << (bit-1)) and
            j > -(2 << (bit-1))
                  for i in X
                  for j in i):
            bit = bit - 1


        self.bits = max(bit, self.bits)
        return bit
def contar(X, habilitar=True):
    bit = 64
    #cuento los bits necesarios
    #cuando todos los elementos cumplen ambas condiciones
    if (X.ndim == 2):
        while habilitar and bit > 0 and all(
            j <  (2 << (bit-1)) and
            j > -(2 << (bit-1))
                    for i in X
                    for j in i):
            bit = bit - 1
    elif (X.ndim == 1):
        while habilitar and bit > 0 and all(
            i <  (2 << (bit-1))
                    for i in X):
            bit = bit - 1
    else:
        while habilitar and bit > 0 and X < (2 << (bit-1)) and X > -(2 << (bit-1)):
            bit = bit - 1

    return bit

def shift(X, bits):
    X = X * pow(2, bits)
    return X

def clamp(X, bits):
    X = X * pow(2, 64 - bits)
    X = X // pow(2, 64 - bits)
    return X
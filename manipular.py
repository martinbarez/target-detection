import numpy as np

def contar(X, habilitar=True):
    bit = 64
    #cuento los bits necesarios
    #cuando todos los elementos cumplen ambas condiciones
    if (X.ndim == 2):
        while habilitar and bit > 0 and all(
            j <  (2 << (bit-1)) and
            j >= -(2 << (bit)-1)
                    for i in X
                    for j in i):
            bit = bit - 1
    elif (X.ndim == 1):
        while habilitar and bit > 0 and all(
            i <  (2 << (bit-1)) and
            i >= -(2 << (bit)-1)
                    for i in X):
            bit = bit - 1
    elif (X.ndim == 0):
        while habilitar and bit > 0 and X < (2 << (bit-1)) and X >= -(2 << (bit)-1):
            bit = bit - 1

    return bit+2

def shift(X, bits):
    X = np.int64(X * pow(2, bits))
    return X

def clamp(X, bits):
    orig = np.int64(X)
    if(bits >= 64): return orig
    X = np.int64(X * pow(2, 64 - bits))
    X = X // pow(2, 64 - bits)
    if (orig != X).any():
        print("Some precision lost by clamping")
    return X
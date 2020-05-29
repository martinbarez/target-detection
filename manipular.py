def contar(X):
    bit = 64
    #cuento los bits necesarios
    #cuando todos los elementos cumplen ambas condiciones
    while False and bit > 0 and all(
        j <  (2 << (bit-1)) and
        j > -(2 << (bit-1))
                for i in X
                for j in i):
        bit = bit - 1

    return bit
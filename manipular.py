def contar(X, habilitar):
    bit = 64
    #cuento los bits necesarios
    #cuando todos los elementos cumplen ambas condiciones
    while habilitar and bit > 0 and all(
        j <  (2 << (bit-1)) and
        j > -(2 << (bit-1))
                for i in X
                for j in i):
        bit = bit - 1

    return bit

def contar_num(n, habilitar):
    bit = 64
    while habilitar and bit > 0 and n < (2 << (bit-1)) and n > -(2 << (bit-1)):
        bit = bit - 1

    return bit
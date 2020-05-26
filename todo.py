import spectral.io.envi as envi
import numpy as np
from operaciones import media, deviacion, covarianza, valores_rx
from inversa import inversa
from manipular import comparar
np.set_printoptions(suppress=True, linewidth=210)


#Valores predefinidos
X = np.array([[209, 246, 108, 174, 71, 113, 182, 246, 229, 209, 91, 98, 146, 43, 59, 28, 67, 223, 103, 232, 200, 148, 167, 176, 125, 165, 160, 58, 232, 155, 22, 61],
    [232, 248, 235, 194, 12, 98, 194, 88, 246, 63, 213, 146, 121, 155, 234, 247, 205, 149, 20, 242, 100, 16, 188, 47, 112, 97, 151, 44, 251, 183, 68, 118],
    [33, 41, 203, 191, 25, 196, 71, 150, 141, 238, 150, 20, 4, 68, 40, 2, 111, 141, 62, 126, 62, 61, 166, 95, 115, 208, 54, 59, 113, 57, 206, 247],
    [234, 249, 246, 101, 211, 204, 175, 58, 36, 90, 141, 14, 87, 168, 212, 199, 234, 38, 32, 126, 104, 91, 116, 161, 79, 137, 78, 112, 29, 31, 8, 140],
    [162, 246, 168, 168, 178, 48, 168, 193, 39, 51, 235, 136, 42, 177, 138, 210, 47, 219, 48, 87, 25, 211, 141, 200, 131, 90, 121, 80, 67, 76, 238, 134],
    [25, 125, 10, 44, 82, 126, 42, 66, 66, 65, 74, 200, 204, 192, 256, 223, 68, 160, 62, 231, 34, 4, 76, 21, 131, 241, 60, 237, 105, 82, 187, 60],
    [72, 205, 218, 181, 244, 115, 31, 130, 216, 158, 194, 240, 80, 116, 21, 22, 38, 90, 107, 95, 242, 12, 191, 238, 210, 225, 217, 111, 153, 109, 126, 126],
    [141, 37, 240, 9, 9, 166, 128, 179, 66, 122, 193, 34, 136, 22, 114, 103, 35, 132, 13, 29, 245, 44, 49, 199, 204, 141, 50, 48, 68, 131, 149, 160]])


#Valores aleatorios
N = 169  # bandas
M = 64*64  # pixeles
X = np.random.randint(low=0, high=256, size=(N, M))


#Una imagen de verdad
img = envi.open('hydice.hdr').load()
X = np.reshape(img, (img.shape[0] * img.shape[1], img.shape[2]))
X = np.transpose(X) #para que cada banda sea una fila

#Lo transformo a float para realizar todas las operaciones
X = X.astype(np.float64)

#Las operaciones previas
m_aux = media(X)
d_aux = deviacion(X, m_aux)
c_aux = covarianza(X, d_aux)

#Calculo en flotante para poder comparar luego
inversa_flotante = np.linalg.inv(c_aux)
rx_flotante = valores_rx(X.shape[1], inversa_flotante, d_aux)

if True:
    inversa_fija, bits = inversa(c_aux, *[13, 38])

    rx_fijo = valores_rx(X.shape[1], inversa_fija, d_aux)
    ratio = comparar(rx_fijo, rx_flotante)

else:
    n_vars = 2
    reset = False
    new = True
    values = [16, 16]
    valid = [True]*n_vars
    bits_antes = 64
    ratio_antes = 0

    while reset or any(valid):
        inversa_fija, bits = inversa(c_aux, *values)
        rx_fijo = valores_rx(X.shape[1], inversa_fija, d_aux)
        ratio = comparar(rx_fijo, rx_flotante)

        print(values)
        print(bits, "bits,", "ratio:", ratio, '\n')

        if ratio >= ratio_antes and bits_antes >= bits:
            bits_antes = bits
            ratio_antes = ratio
            if new:
                reset = True
            for i in range(n_vars):
                if values[i] == 0:
                    valid[i] = False
                if valid[i]:
                    values[i] = values[i] - 1
                    new = True
                    break
            if reset and not any(valid):
                reset = False
                valid = [True]*n_vars
        else:
            new = False
            for i in range(n_vars):
                if valid[i]:
                    values[i] = values[i] + 1
                    valid[i] = False
                    break
    print(values)
    ratio = ratio_antes




#Imprimo resultados
print("El bit más significativo está en la posición:", bits)
print("Similitud con resultado correcto:", ratio)

print("Fin")

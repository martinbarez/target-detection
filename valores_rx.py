import numpy as np
import logging
import sys

from manipular import contar, contar_num


def valores_rx(n_pixeles, inversa, deviacion):
    rx = np.zeros(n_pixeles, inversa.dtype)
    n_bandas = inversa.shape[0]

    if inversa.dtype == np.float64 or inversa.dtype == np.float32:

        for i in range(n_pixeles):
            resta = deviacion[i]
            t = np.transpose(resta)
            inter_res = np.matmul(t, inversa)
            rx[i] = np.matmul(inter_res, resta)

    elif inversa.dtype == np.int64 or inversa.dtype == np.int32:

        for i in range(n_pixeles):
            resta = deviacion[i]
            inter_res = np.zeros(n_bandas, np.float64)
            for j in range(n_bandas):
                mult = resta[j] * inversa[j]
                inter_res += mult
            sum = 0
            for j in range(n_bandas):
                sum += inter_res[j] * resta[j]
            rx[i] = sum

    else:
        print("Something bad happened in valores_rx")

    return rx

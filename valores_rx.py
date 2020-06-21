import numpy as np
import logging
import sys

from manipular import contar, contar_num


def valores_rx(n_pixeles, inversa, deviacion, dev_up=0, inter_up=0):
    rx = np.zeros(n_pixeles, inversa.dtype)
    n_bandas = inversa.shape[0]

    if inversa.dtype == np.float64 or inversa.dtype == np.float32:

        for i in range(n_pixeles):
            resta = deviacion[i]
            t = np.transpose(resta)
            inter_res = np.matmul(t, inversa)
            rx[i] = np.matmul(inter_res, resta)

    elif inversa.dtype == np.int64 or inversa.dtype == np.int32:
        deviacion = deviacion * pow(2, dev_up)
        deviacion = deviacion // 1
        for i in range(n_pixeles):
            resta = deviacion[i].astype(inversa.dtype)
            inter_res = np.zeros(n_bandas, inversa.dtype)
            for j in range(n_bandas):
                mult = resta[j] * inversa[j]
                inter_res += mult 
            # this leaves inter_res with 35 significant bits
            inter_res = inter_res * pow(2, inter_up)
            inter_res = inter_res // pow(2, 64 - 35)
            sum = 0
            for j in range(n_bandas):
                sum += inter_res[j] * resta[j]
            rx[i] = sum

    else:
        print("Something bad happened in valores_rx")

    return rx

import numpy as np
import logging
import sys

from manipular import contar, shift, clamp


def valores_rx(n_pixeles, inversa, deviacion, dev_up=0, inter_up=0):
    rx = np.zeros(n_pixeles, inversa.dtype)
    n_bandas = inversa.shape[0]

    if inversa.dtype == np.float64:

        for i in range(n_pixeles):
            resta = deviacion[i]
            t = np.transpose(resta)
            inter_res = np.matmul(t, inversa)
            rx[i] = np.matmul(inter_res, resta)

    elif inversa.dtype == np.int64:
        deviacion = shift(deviacion, dev_up)
        deviacion = clamp(deviacion, 25)
        inversa = clamp(inversa, 35)
        for i in range(n_pixeles):
            resta = deviacion[i].astype(inversa.dtype)
            inter_res = np.zeros(n_bandas, inversa.dtype)
            for j in range(n_bandas):
                mult = shift(inversa[j] * resta[j], -5)
                inter_res += clamp(mult, 48)
            inter_res = shift(inter_res, inter_up)
            inter_res = clamp(inter_res, 35)
            sum = 0
            for j in range(n_bandas):
                sum += clamp(shift(inter_res[j] * resta[j], -5), 48)
            rx[i] = clamp(sum, 64)

    else:
        raise Exception

    return rx

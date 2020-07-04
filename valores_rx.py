import numpy as np
import logging
import sys

from manipular import contar, shift, clamp
import rx_package as rx


def valores_rx(n_pixeles, inversa, deviacion, dev_up=0, inter_down=0):
    valores = np.zeros(n_pixeles, inversa.dtype)
    n_bandas = inversa.shape[0]

    if inversa.dtype == np.float64:

        for i in range(n_pixeles):
            resta = deviacion[i]
            t = np.transpose(resta)
            inter_res = np.matmul(t, inversa)
            valores[i] = np.matmul(inter_res, resta)

    elif inversa.dtype == np.int64:
        deviacion = shift(deviacion, dev_up)
        deviacion = clamp(deviacion, rx.mult_st_mul_a_precision)
        inversa = clamp(inversa, rx.mult_st_mul_b_precision)
        for i in range(n_pixeles):
            resta = deviacion[i].astype(inversa.dtype)
            inter_res = np.zeros(n_bandas, inversa.dtype)
            for j in range(n_bandas):
                mult = shift(resta[j] * inversa[j], 0)
                inter_res += clamp(mult, rx.mult_st_accum_in_precision)
            inter_res = clamp(inter_res, rx.mult_st_accum_out_precision)
            inter_res = shift(inter_res, inter_down)
            sum = 0
            for j in range(n_bandas):
                sum += clamp(shift(resta[j] * inter_res[j], 0), rx.mult_nd_accum_in_precision)
            valores[i] = clamp(sum, rx.mult_nd_accum_out_precision)

    else:
        raise Exception

    return valores

import numpy as np
import logging
import sys

import rx_package as rx
from manipular import contar, shift, clamp



def inversa(cov, cov_in, inv_in, div_up, div_bc, div_dg, count_en):
    n_bandas = cov.shape[0]
    inv = np.zeros([n_bandas, n_bandas], np.int64)

    if count_en:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

    #lo inicializo como identidad
    for i in range(n_bandas):
        inv[i][i] = 1

    cov = shift(cov, cov_in)
    inv = shift(inv, inv_in)
    logging.info("Covarianza:")
    c = contar(cov, count_en)
    logging.info(c)
    logging.debug(cov)
    logging.info("Inversa:")
    c = contar(inv, count_en)
    logging.info(c)
    logging.debug(inv)
    cov = clamp(cov, rx.ram_precision)
    inv = clamp(inv, rx.ram_precision)

    max_bits = 0
    #forward elimination to build an upper triangular matrix
    for i in range(n_bandas):
        # if zero
        if (cov[i][i] == 0):
            for j in range(i, n_bandas):
                if (cov[j][j] != 0):
                    cov[[i, j]] = cov[[j, i]]
                    inv[[i, j]] = inv[[j, i]]
                    print("swapped", i, j)
        assert cov[i][i] != 0, "Matrix is singular"

        for j in range(i + 1, n_bandas):
            div = cov[j][i] / cov[i][i]
            div = shift(div, div_up)
            c = contar(div, count_en)
            max_bits = max(max_bits, c)
            div = clamp(div, rx.quotient_precision)
            inv[j] = inv[j] - clamp(shift(inv[i] * div, -div_up), rx.gauss_sub_b_precision)
            cov[j] = cov[j] - clamp(shift(cov[i] * div, -div_up), rx.gauss_sub_b_precision)


    logging.info("Division:")
    logging.info(max_bits)
    logging.info("Covarianza:")
    c = contar(cov, count_en)
    logging.info(c)
    logging.debug(cov)
    logging.info("Inversa:")
    c = contar(inv, count_en)
    logging.info(c)
    logging.debug(inv)
    cov = clamp(cov, rx.ram_precision)
    inv = clamp(inv, rx.ram_precision)

    max_bits = 0
    #backward elimination to build a diagonal matrix
    for i in range(n_bandas-1, 0, -1):
        for j in range(i-1, -1, -1):
            div = cov[j][i] / cov[i][i]
            div = shift(div, div_bc)
            c = contar(div, count_en)
            max_bits = max(max_bits, c)
            div = clamp(div, rx.quotient_precision)
            inv[j] = inv[j] - clamp(shift(inv[i] * div, -div_bc), rx.gauss_sub_b_precision)
            cov[j] = cov[j] - clamp(shift(cov[i] * div, -div_bc), rx.gauss_sub_b_precision)

    logging.info("Division:")
    logging.info(max_bits)
    logging.info("Covarianza:")
    c = contar(cov, count_en)
    logging.info(c)
    logging.debug(cov)
    logging.info("Inversa:")
    c = contar(inv, count_en)
    logging.info(c)
    logging.debug(inv)
    cov = clamp(cov, rx.ram_precision)
    inv = clamp(inv, rx.ram_precision)

    #last division to build identity [i][i]/[i][i]
    for i in range(n_bandas):
        inv[i] = shift(inv[i] / cov[i][i], div_dg)

    clamp(inv, rx.quotient_precision)

    return inv.astype(np.int64), contar(inv, count_en)

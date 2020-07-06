import numpy as np
import logging
import sys

import rx_package as rx
from manipular import contar, shift, clamp



def inversa(cov, count_en):
    n_bandas = cov.shape[0]
    inv = np.zeros([n_bandas, n_bandas], np.int64)

    if count_en:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

    #lo inicializo como identidad
    for i in range(n_bandas):
        inv[i][i] = 1

    cov = shift(cov, rx.cov_up)
    inv = shift(inv, rx.inv_up)
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
            div = shift(cov[j][i] / cov[i][i], rx.forw)
            c = contar(div, count_en)
            max_bits = max(max_bits, c)
            div = clamp(div, rx.quotient_precision)
            inv[j] = inv[j] - clamp(shift(inv[i] * div, -rx.forw), rx.gauss_sub_b_precision)
            cov[j] = cov[j] - clamp(shift(cov[i] * div, -rx.forw), rx.gauss_sub_b_precision)


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
            div = shift(cov[j][i] / cov[i][i], rx.back)
            c = contar(div, count_en)
            max_bits = max(max_bits, c)
            div = clamp(div, rx.quotient_precision)
            inv[j] = inv[j] - clamp(shift(inv[i] * div, -rx.back), rx.gauss_sub_b_precision)
            cov[j] = cov[j] - clamp(shift(cov[i] * div, -rx.back), rx.gauss_sub_b_precision)

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
        div = shift(1, rx.diag_up) // cov[i][i]
        div = clamp(div, rx.quotient_precision)
        inv[i] = clamp(shift(inv[i] * div, -rx.diag_dw), rx.ram_precision)


    return inv.astype(np.int64), contar(inv, count_en)

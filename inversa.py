import numpy as np
import logging
import sys

from manipular import contar



def inversa(cov, cov_in, inv_in, div_up, div_bc, div_dg, count_en):
    n_bandas = cov.shape[0]
    inv = np.zeros([n_bandas, n_bandas], cov.dtype)
    max_bits = 0

    if count_en:
        logging.basicConfig(stream=sys.stderr, level=logging.INFO)
    else:
        logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

    #lo inicializo como identidad
    for i in range(n_bandas):
        inv[i][i] = 1

    cov = cov * pow(2, cov_in) //1
    inv = inv * pow(2, inv_in) //1
    logging.info("Covarianza:")
    c = contar(cov, count_en)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(cov)
    logging.info("Inversa:")
    c = contar(inv, count_en)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(inv)

    #forward elimination to build an upper triangular matrix
    for i in range(n_bandas):
        # if zero
        if (cov[i][i] == 0):
            for j in range(i, n_bandas):
                if (cov[j][j] != 0):
                    cov[[i, j]] = cov[[j, i]]
                    inv[[i, j]] = inv[[j, i]]
                    print("swapped", i, j)
        assert cov[i][i] is not 0, "Matrix is singular"

        for j in range(i + 1, n_bandas):
            div = cov[j][i] / cov[i][i]
            div = div*pow(2, div_up)
            div = div // 1
            inv[j] = inv[j] - inv[i] * div * pow(2, -div_up) //1
            cov[j] = cov[j] - cov[i] * div * pow(2, -div_up) //1

    logging.info("Covarianza:")
    c = contar(cov, count_en)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(cov)
    logging.info("Inversa:")
    c = contar(inv, count_en)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(inv)

    #backward elimination to build a diagonal matrix
    for i in range(n_bandas-1, 0, -1):
        for j in range(i-1, -1, -1):
            div = cov[j][i] / cov[i][i]
            div = div*pow(2, div_bc)
            div = div // 1
            inv[j] = inv[j] - inv[i] * div * pow(2, -div_bc) //1
            cov[j] = cov[j] - cov[i] * div * pow(2, -div_bc) //1

    logging.info("Covarianza:")
    c = contar(cov, count_en)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(cov)
    logging.info("Inversa:")
    c = contar(inv, count_en)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(inv)

    #last division to build identity [i][i]/[i][i]
    for i in range(n_bandas):
        inv[i] = (inv[i] / cov[i][i])* pow(2, div_dg) //1

    max_bits = max(max_bits, contar(inv, count_en))

    return inv, max_bits

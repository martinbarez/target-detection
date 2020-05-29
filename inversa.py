import numpy as np
import logging
import sys

from manipular import contar

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)


def inversa(cov, cov_in, inv_in):
    n_bandas = cov.shape[0]
    inv = np.zeros([n_bandas, n_bandas], cov.dtype)
    max_bits = 0

    #lo inicializo como identidad
    for i in range(n_bandas):
        inv[i][i] = 1

    cov = cov * pow(2, cov_in)
    inv = inv * pow(2, inv_in)
    logging.info("Covarianza:")
    c = contar(cov)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(cov)
    logging.info("Inversa:")
    c = contar(inv)
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
            inv[j] = (inv[j] - inv[i] * (cov[j][i] / cov[i][i]))
            cov[j] = (cov[j] - cov[i] * (cov[j][i] / cov[i][i]))

    logging.info("Covarianza:")
    c = contar(cov)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(cov)
    logging.info("Inversa:")
    c = contar(inv)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(inv)

    #backward elimination to build a diagonal matrix
    for i in range(n_bandas-1, 0, -1):
        for j in range(i-1, -1, -1):
            inv[j] = (inv[j] - inv[i] * (cov[j][i] / cov[i][i]))
            cov[j] = (cov[j] - cov[i] * (cov[j][i] / cov[i][i]))

    logging.info("Covarianza:")
    c = contar(cov)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(cov)
    logging.info("Inversa:")
    c = contar(inv)
    max_bits = max(max_bits, c)
    logging.info(c)
    logging.debug(inv)

    #last division to build identity [i][i]/[i][i]
    for i in range(n_bandas):
        inv[i] = (inv[i] * (1 / cov[i][i]))

    inv = inv // 1
    max_bits = max(max_bits, contar(inv))

    return inv, max_bits

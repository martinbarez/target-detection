import numpy as np
import logging
import sys

from manipular import contar

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

def inversa(cov, cov_in, cov_up=0, cov_bc=0, cov_dg=0, inv_in=0, inv_up=0, inv_bc=0, inv_dg=0):
    n_bandas = cov.shape[0]
    inv = np.zeros([n_bandas, n_bandas], cov.dtype)

    c = contar()

    #lo inicializo como identidad
    for i in range(n_bandas):
        inv[i][i]=1

    logging.info("Covarianza:")
    logging.info(cov)
    cov = cov * pow(2, cov_in)
    inv = inv * pow(2, inv_in)
    c.truncar(cov)
    logging.info("Covarianza:")
    logging.info(cov)

    #forward elimination to build an upper triangular matrix
    for i in range (n_bandas):
        # if zero
        if (cov[i][i]==0):
            for j in range(i, n_bandas):
                if (cov[j][j]!=0):
                    cov[[i, j]] = cov[[j, i]]
                    inv[[i, j]] = inv[[j, i]]
                    print("swapped", i, j)
        assert cov[i][i] is not 0, "Matrix is singular"

        for j in range(i + 1, n_bandas):
            inv[j] = (inv[j] - inv[i] * (cov[j][i] / cov[i][i]))
            cov[j] = (cov[j] - cov[i] * (cov[j][i] / cov[i][i]))

    logging.info("")
    logging.info("Covarianza:")
    logging.info(cov)
    logging.info("Inversa:")
    logging.info(inv)
    cov = cov * pow(2, cov_up)
    inv = inv * pow(2, inv_up)
    c.truncar(cov)
    c.truncar(inv)
    logging.info("Covarianza:")
    logging.info(cov)
    logging.info("Inversa:")
    logging.info(inv)


    #backward elimination to build a diagonal matrix
    for i in range(n_bandas-1, 0, -1):
        for j in range(i-1, -1, -1):
            inv[j] = (inv[j] - inv[i] * (cov[j][i] / cov[i][i]))
            cov[j] = (cov[j] - cov[i] * (cov[j][i] / cov[i][i]))

    logging.info("")
    logging.info("Covarianza:")
    logging.info(cov)
    logging.info("Inversa:")
    logging.info(inv)
    cov = cov * pow(2, cov_bc)
    inv = inv * pow(2, inv_bc)
    c.truncar(cov)
    c.truncar(inv)
    logging.info("Covarianza:")
    logging.info(cov)
    logging.info("Inversa:")
    logging.info(inv)


    #last division to build identity [i][i]/[i][i]
    for i in range(n_bandas):
        inv[i] = (inv[i] * (1 / cov[i][i]))

    logging.info("")
    logging.info("Inversa:")
    logging.info(inv)
    inv = inv * pow(2, inv_dg*cov_dg)
    c.truncar(inv)
    logging.info("Inversa:")
    logging.info(inv)

    return inv, c.bits

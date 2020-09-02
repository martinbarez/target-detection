import numpy as np

from manipular import clamp
import rx_package as rx

def media(X):
    return np.mean(X, axis=1)


def deviacion(X, media_bandas):
    Xt = np.transpose(X.copy())

    #A cada toma le resto la media de su banda
    return Xt-media_bandas


def covarianza(X, deviacion):
    #Transpongo
    devt = np.transpose(deviacion)
    #Mutiplico
    otra = np.matmul(devt, deviacion)

    #divido por algo fijo, pero que si puedo tomar algo de error mejor desplazo
    n_pixeles = X.shape[1]
    #covarianza = otra/(n_pixeles-1)
    covarianza = otra/(n_pixeles)

    return covarianza

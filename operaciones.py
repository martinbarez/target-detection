import numpy as np

def media(X):
    return np.mean(X, axis=1)


def deviacion(X, media_bandas):
    Xt = np.transpose(X.copy())

    #A cada toma le resto la media de su banda
    deviacion = (Xt-media_bandas)
    return deviacion


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

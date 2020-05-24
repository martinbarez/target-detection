import numpy

def media(X):
    return numpy.mean(X, axis=1)


def deviacion(X, media_bandas):
    Xt = numpy.transpose(X.copy())

    #A cada toma le resto la media de su banda
    deviacion = (Xt-media_bandas)
    return deviacion


def covarianza(X, deviacion):
    #Transpongo
    devt = numpy.transpose(deviacion)
	#Mutiplico
    otra = numpy.matmul(devt, deviacion)

    #divido por algo fijo, pero que si puedo tomar algo de error mejor desplazo
    n_pixeles = X.shape[1]
    #covarianza = otra/(n_pixeles-1)
    covarianza = otra/(n_pixeles)

    return covarianza

def valores_rx(n_pixeles, inversa, deviacion):
	rx = numpy.zeros(n_pixeles, numpy.float32)
	for i in range(n_pixeles):
		resta = deviacion[i]
		t = numpy.transpose(resta)
		rx[i] = numpy.matmul(t, numpy.matmul(inversa, resta))
	return rx

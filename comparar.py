import numpy as np
from matplotlib import pyplot as plt
from math import sqrt

#spectral angle mapping
#https://earth.esa.int/documents/973910/1002056/CK2.pdf/861e7d6e-dbcf-4209-a29a-e283cc0e67d6
def angle_compare(X, target_coord, ref_coord, threshhold = 10):
    #all bands for a pixel
    target = X[:,target_coord]
    reference = X[:,ref_coord]

    target_sum = np.sum(pow(target, 2))
    reference_sum = np.sum(pow(reference, 2))

    denominator = pow(target_sum, 1/2) * pow(reference_sum, 1/2)

    numerator = np.sum(target*reference)

    angle_rad = np.arccos(numerator/denominator)

    angle = angle_rad * 180 / np.pi

    return angle < threshhold


#if the coords are next to each other (up, down, right, left, including diagonals)
def spatial_compare(X, target_coord, ref_coord, threshhold = 1):
    for i in range(threshhold+1):
      if abs(target_coord-abs(sqrt(X.shape[1])*i-ref_coord)) <= threshhold or abs(target_coord-abs(sqrt(X.shape[1])*i+ref_coord)) <= threshhold:
        return True
    return False

#que porcentaje de los elementos han sido encontrados hasta ese mismo momento en ambas listas
#Es decir, si encuentro lo mismo todo el rato, el ratio es 1, en el
#momento en el que hay algo diferente, baja, pero si me lo encuentro en el
#siguiente elemento vuelve a subir. Y si solo había dos elementos permutados
#vuelve a saltar a 1
def grafico(fijo, flotante):
    graf = []
    for i in range(1, len(fijo)):
        found = sum(1 for e in fijo[:i] if e in flotante[:i])
        ratio = found/i
        graf.append(ratio)

    plt.xlabel("Nº de elementos")
    plt.ylabel("Ratio de elementos hallados/totales")
    plt.axis([0, len(fijo), 0, 1])
    plt.plot(graf)

#ordeno los resultados en dos listas y me quedo con cantidad de elementos
def ordenar_resultados(rx_fijo, rx_flotante, cantidad=0):
    #añado índices
    fijo = list(enumerate(rx_fijo))
    flotante = list(enumerate(rx_flotante))

    #ordeno
    fijo.sort(key=lambda tup: tup[1], reverse=True)
    flotante.sort(key=lambda tup: tup[1], reverse=True)

    #recorto
    if cantidad > 0:
      fijo = fijo[:cantidad]
      flotante = flotante[: len(fijo)]

    #elimino valores
    fijo = [x[0] for x in fijo]
    flotante = [x[0] for x in flotante]

    return fijo, flotante
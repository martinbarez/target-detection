import spectral.io.envi as envi
import numpy as np
from manipular import clamp
from operaciones import media, deviacion, covarianza
from inversa import inversa
from valores_rx import valores_rx
from comparar import *
from testbench import gen_testbench
import rx_package as rx

img = envi.open('hydice.hdr').load()
#para cortar la imagen
#img = img[10:20, 10:20, 0:55]
X = np.reshape(img, (img.shape[0] * img.shape[1], img.shape[2]))
X = np.transpose(X) #para que cada banda sea una fila
N = img.shape[2]
M = img.shape[0] * img.shape[1]

#Lo transformo a float para realizar todas las operaciones
X = X.astype(np.float64)

#Las operaciones previas
m_aux = media(X)
d_aux = deviacion(X, m_aux)
c_aux = covarianza(X, d_aux)

c_aux = clamp(c_aux, rx.precision)

#Calculo en flotante para poder comparar luego
inversa_flotante = np.linalg.inv(c_aux)
rx_flotante = valores_rx(X.shape[1], inversa_flotante, d_aux)

inversa_fija, bits = inversa(c_aux, False)
rx_fijo = valores_rx(X.shape[1], inversa_fija, d_aux)

res_ordenados = coords(rx_fijo, rx_flotante, 30)


if True:
    from matplotlib import pyplot as plt
    simple_results = analyze(X, res_ordenados[0], res_ordenados[1], simple_compare, -1)
    spatial_results = analyze(X, res_ordenados[0], res_ordenados[1], spatial_compare, 1)
    angle_results = analyze(X, res_ordenados[0], res_ordenados[1], angle_compare, 3)

    simple_ratios = []
    spatial_ratios = []
    angle_ratios = []

    for i in range(1, len(simple_results)):
        ratio = simple_results[i]/i
        simple_ratios.append(ratio)

    for i in range(1, len(spatial_results)):
        ratio = spatial_results[i]/i
        spatial_ratios.append(ratio)

    for i in range(1, len(angle_results)):
        ratio = angle_results[i]/i
        angle_ratios.append(ratio)

    plt.xlabel("Number of elements")
    plt.ylabel("Ratio between found/total")
    plt.axis([0, len(res_ordenados[0]), 0, 1.1])

    plt.plot(simple_ratios, 'r--')
    plt.plot(spatial_ratios, 'g-.')
    plt.plot(angle_ratios, 'b:')

    plt.savefig("name.png")

if False:
    with open('results_hydice_truth.txt', 'w') as file:
        for i in range(0, M):
            file.write(str(res_ordenados[1][i])+'\n')

    with open('results_hydice_simul.txt', 'w') as file:
        for i in range(0, M):
            file.write(str(res_ordenados[0][i])+'\n')

if False:
    gen_testbench(m_aux, c_aux, X, res_ordenados[1])

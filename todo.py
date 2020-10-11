import spectral.io.envi as envi
import numpy as np
from manipular import clamp, shift
from operaciones import media, deviacion, covarianza
from inversa import inversa
from valores_rx import valores_rx
from comparar import *
from testbench import gen_testbench
import rx_package as rx

s = "hydice"
img = envi.open('hydice.hdr').load()

#rearrange so each band is a row
X = np.reshape(img, (img.shape[0] * img.shape[1], img.shape[2]))
X = np.transpose(X)
X = X.astype(np.float64)

N = img.shape[2]
M = img.shape[0] * img.shape[1]

#Calc the reference in floating point
inverse_reference = np.linalg.inv(np.cov(X))
reference_rx = valores_rx(X.shape[1], inverse_reference, deviacion(X, media(X)))

#Calc the data how it is going to get written on the FIFOS
scale = 12
mean_fifo = clamp(shift(media(X), scale), rx.precision)
elements_fifo = clamp(shift(X, scale), rx.precision)
covariance_fifo = clamp(shift(np.cov(X), rx.read_cov), rx.precision)

#Simulate the FPGA
mean_fifo = clamp(mean_fifo, rx.mean_sub_a_precision)
elements_fifo = clamp(elements_fifo, rx.mean_sub_b_precision)
deviation_fpga = clamp(deviacion(elements_fifo, mean_fifo), rx.mean_sub_s_precision)

target_inverse, bits = inversa(covariance_fifo, False)
target_rx = valores_rx(X.shape[1], target_inverse, deviation_fpga)

#Analyze results
target_res, reference_res = coords(target_rx, reference_rx, 30)

from difflib import SequenceMatcher
print(SequenceMatcher(None, target_res, reference_res).ratio())

if True:
    from matplotlib import pyplot as plt

    simple_results = analyze(X, target_res, reference_res, simple_compare, -1)
    spatial_results = analyze(X, target_res, reference_res, spatial_compare, 1)
    angle_results = analyze(X, target_res, reference_res, angle_compare, 10)

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


    plt.figure(figsize=(6, 6))
    plt.xlabel("Number of elements")
    plt.ylabel("Ratio between found/total")
    plt.axis([0, len(target_res), -0.005, 1.005])

    plt.plot(simple_ratios, 'r--', label="equality")
    plt.plot(spatial_ratios, 'g-.', label="neighbour")
    plt.plot(angle_ratios, 'b:', label="spectral similarity")
    plt.legend(loc='lower right', frameon=True)

    plt.savefig(s+".png")
    plt.clf()

    plt.figure(figsize=(img.shape[1]/10, img.shape[0]/10))
    plt.tight_layout()
    ref_x = []
    ref_y = []
    for e in reference_res:
      ref_x.append(e%img.shape[1])
      ref_y.append(-e//img.shape[1])
    plt.scatter(ref_x, ref_y, marker="x", c='blue')
    plt.axis([0, img.shape[1], -img.shape[0], 0])
    plt.savefig(s+"_ref.png")
    plt.clf()

    target_x = []
    target_y = []
    for e in target_res:
      target_x.append(e%img.shape[1])
      target_y.append(-e//img.shape[1])
    plt.scatter(target_x, target_y, marker="+", c='red')
    plt.axis([0, img.shape[1], -img.shape[0], 0])
    plt.savefig(s+"_tar.png")
    plt.clf()

if False:
    with open('results_hydice_truth.txt', 'w') as file:
        for i in range(0, M):
            file.write(str(reference_res[i])+'\n')

    with open('results_hydice_simul.txt', 'w') as file:
        for i in range(0, M):
            file.write(str(target_res[i])+'\n')

if False:
    gen_testbench(mean_fifo, covariance_fifo, X, target_res)

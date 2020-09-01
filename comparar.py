import numpy as np
from math import sqrt

#spectral angle mapping
#https://earth.esa.int/documents/973910/1002056/CK2.pdf/861e7d6e-dbcf-4209-a29a-e283cc0e67d6
def angle_compare(X, target_coord, ref_coord, threshold = 10):
    if target_coord == ref_coord: #the limited floating point precision could make this to fail
        return True

    #all bands for a pixel
    target = X[:,target_coord]
    reference = X[:,ref_coord]

    target_sum = np.sum(pow(target, 2))
    reference_sum = np.sum(pow(reference, 2))

    denominator = pow(target_sum, 1/2) * pow(reference_sum, 1/2)

    numerator = np.sum(target*reference)

    angle_rad = np.arccos(numerator/denominator)

    angle = angle_rad * 180 / np.pi

    return angle < threshold


#if the coords are next to each other (up, down, right, left, including diagonals)
def spatial_compare(X, target_coord, ref_coord, threshold = 1):
    size = sqrt(X.shape[1])
    target_coord = (target_coord%size, target_coord/size)
    ref_coord = (ref_coord%size, ref_coord/size)
    if target_coord[0]>= ref_coord[0]-threshold and target_coord[0] <= ref_coord[0]+threshold:
        if target_coord[1]>= ref_coord[1]-threshold and target_coord[1] <= ref_coord[1]+threshold:
            return True
    return False

def simple_compare(X, target_coord, ref_coord, threshold = -1):
    return target_coord == ref_coord

def analyze(X, target, reference, compare_func, threshold):
    result = []
    found = []
    for i in range(len(target)):  #to graph different x
        found.append(False)
        for j in range(i+1):
            if found[j] is False:  #update every coord not found till current one
                for k in range(j+1):  #compare updating coord with all past reference coords
                    if compare_func(X, target[j], reference[k], threshold):
                        found[j] = True

        result.append(sum(1 for e in found[:i] if e))  #count found coords
    return result

#get coords from list of rx_values
def coords(target_values, reference_values, size=0):
    #add indices
    target = list(enumerate(target_values))
    reference = list(enumerate(reference_values))

    #order
    target.sort(key=lambda tup: tup[1], reverse=True)
    reference.sort(key=lambda tup: tup[1], reverse=True)

    #cut
    if size > 0:
      target = target[:size]
      reference = reference[: len(target)]

    #remove values
    target = [x[0] for x in target]
    reference = [x[0] for x in reference]

    return target, reference
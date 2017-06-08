# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:03:13 2017

@author: Gus
"""

import numpy as np
from newportTLS import TLS
from jazSpect import Spect
import matplotlib.pyplot as plt

filterW = 1

newp = TLS()

newp.filterW(filterW)

int_time = 1000

jaz = Spect(int_time = int_time)

steps = 200
minimum = 350
maximum = 800
# Build an array of the test frequencies
test_lam = np.array(range(steps+1))
test_lam = test_lam*(maximum-minimum)/steps+minimum

maxima = np.array([])
TLS_lam = np.array([])

doubles = []

#_ = newp.set_lambda(minimum)  
#_ = newp.query("INFO?")

for lam in test_lam:
    _ = newp.set_lambda(lam)
    TLS_lam = np.append(TLS_lam, newp.get_lambda())
    intens = jaz.get_intensities()
    lamDouble = jaz.get_double_peak(intens)
    if lamDouble is None:
        doubles.append(False)
        maxima = np.append(maxima, jaz.get_maximum(intens))
    else:
        doubles.append(True)
        maxima = np.append(maxima, lamDouble[2])

plt.figure(figsize = (9, 7))
plt.plot(TLS_lam, maxima)
plt.ylabel('wavelength measured')
plt.xlabel('wavelength nominal')

plt.figure(figsize = (9, 7))
plt.plot(TLS_lam, doubles)
plt.ylabel('double peak')
plt.xlabel('wavelength nominal')

#title = "Intensity Spectrum\n"
#if lam is not None:
#    title += "Nominal wavelength (nm): "+str(lam)+". "
#if int_time is not None:
#    title += "Integration time (ms): "+str(int_time)+". "
#if filterW is not None:
#    title += "Filter setting: "+str(filterW)+". "
#    
#plt.suptitle(title)

plt.figure(figsize = (9, 7))
plt.plot(test_lam, test_lam-maxima)
plt.ylabel('wavelength error')
plt.xlabel('wavelength nominal')

plt.show()

jaz.close()

newp.close()
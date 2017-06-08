# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:03:13 2017

@author: Gus
"""

import numpy as np
from newportTLS import TLS
from jazSpect import Spect
import matplotlib.pyplot as plt
from scipy.stats import norm

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
fwhm = np.array([])

for lam in test_lam:
    _ = newp.set_lambda(lam)
    TLS_lam = np.append(TLS_lam, newp.get_lambda())
    intens = jaz.get_intensities()
    
    noise = np.median(intens)
    intens = intens-noise
    
    p0 = [10000, lam, 10]
    coeff = jaz.fit_norm(intens,p0)
    
    maxima = np.append(maxima, coeff[1])
    fwhm = np.append(fwhm, coeff[2]*2.35)

plt.figure(figsize = (9, 7))
plt.plot(TLS_lam, maxima)
plt.ylabel('wavelength measured')
plt.xlabel('wavelength nominal')

plt.figure(figsize = (9, 7))
plt.plot(TLS_lam, fwhm)
plt.ylabel('FWHM')
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
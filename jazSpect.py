# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import seabreeze.spectrometers as sb
import numpy as np

# Find the spectrometer, there is only one
devices = sb.list_devices()
print(devices)
spec = sb.Spectrometer(devices[0])
spec.integration_time_micros(1500) # This is the minimum
spec.minimum_integration_time_micros
specData = spec.spectrum()
index_max = np.argmax(specData[1])
lam_max = specData[0][index_max]
print("maximum wavelength: ", lam_max)
plt.figure()
plt.plot(specData[0], specData[1])
plt.show()

plt.figure()
plt.plot(specData[0][index_max-50:index_max+50], specData[1][index_max-50:index_max+50])
plt.show()

# Remove the noise at all wavelengths using median.
med = np.median(specData[1])
specData[1] = specData[1]-med

# Find the average data point by bisecting data.
integ = sum(specData[1])
halfint = integ/2
csum = 0
for x in range(len(specData[1])):
    csum = csum+specData[1][x]
    if csum > halfint:
        print("data average wavelength: ", specData[0][x])
        break

spec.close()
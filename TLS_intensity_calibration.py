# -*- coding: utf-8 -*-
"""
Created on Wed May 10 15:51:52 2017

@author: Gus
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:03:13 2017

@author: Gus
"""

import numpy as np
from newportTLS import TLS
import matplotlib.pyplot as plt
from keysight import Keysight
from photodiode_calibration import diodeCal
import os

"""
Settings
"""

filterW = 1 # Wheel 1 is no filter

# wavelengths
steps = 650
minimum = 350
maximum = 1000

# range of SMU. Resolution is approximately 0.5*10^-6 of maximum
max_amps = 2e-7

save_file = True

file_suffix = "bare"

"""
Code
"""

newp = TLS()

keys = Keysight()
keys.set_range(max_amps) # experiment with different ranges for best performance.
keys.set_output_voltage(5) # Bit of an arbitrary choice. Shouldn't matter much.

newp.filterW(filterW)

# Build an array of the test frequencies
test_lam = np.array(range(steps+1))
test_lam = test_lam*(maximum-minimum)/steps+minimum

TLS_lam = np.array([])
curr_av = np.array([])
average_points = 2
aper_time = 0.05
# keys.set_aper(aper_time)

for lam in test_lam:
    _ = newp.set_lambda(lam)
    TLS_lam = np.append(TLS_lam, newp.get_lambda())
    
#    curr_points = np.array([])
#    for ind in range(average_points):
#        curr = keys.get_current()
#        curr_points = np.append(curr_points, curr)
#    
#    curr_av = np.append(curr_av, np.mean(curr_points))
    curr_av = np.append(curr_av, keys.get_current())
    
newp.set_lambda(550) #reset it to something we can see.

plt.figure(figsize = (9, 7))
plt.plot(TLS_lam, curr_av)
plt.ylabel('current')
plt.xlabel('wavelength (nm)')

pd_cal = diodeCal().func
watts = np.divide(curr_av, pd_cal(TLS_lam))

plt.figure(figsize = (9,7))
plt.plot(TLS_lam, watts)
plt.ylabel('power (W)')
plt.xlabel('wavelength (nm)')

aper_time = keys.get_aper()
hc = 1.98644568e-16 # J nm
photon_J = hc/TLS_lam
absorbed_J = aper_time*watts
photons = np.divide(absorbed_J, photon_J)

plt.figure(figsize = (9,7))
plt.plot(TLS_lam, photons)
plt.plot(TLS_lam, np.sqrt(photons))
plt.ylabel('photons')
plt.xlabel('wavelength (nm)')

plt.show()

print(max(watts))

temp = keys.get_temperature()
print("Temperature: "+str(temp))

if save_file:
    file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
    file_path = file_base+"/TLS_intensity_"+file_suffix+"%s.txt"
    number = 1
    while os.path.exists(file_path % number):
        number += 1
        
    f = open(file_path % number, "wb")
    
    head = "wavelength_nm, curr_A, power_W, Temperature = %s" % temp
    np.savetxt(f, (TLS_lam, curr_av, watts), header = head, delimiter = "\t") 
    
    f.close()
    
    data = np.loadtxt(file_path % number, unpack=True)
    lambda_nm = data[:,0] 
    curr_A = data[:,1]
    power_W = data[:,0]

keys.close()
newp.close()
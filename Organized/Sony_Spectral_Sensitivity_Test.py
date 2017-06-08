# -*- coding: utf-8 -*-
"""
Created on Tue May 16 10:45:55 2017

@author: Gus
"""

import numpy as np
from newportTLS import TLS
import matplotlib.pyplot as plt
from FTDI_cam import sensor
from TLS_Calibration import TLS_Cal
import os

"""
Settings
"""

filterW = 1 # Wheel 1 is no filter

# wavelengths
steps = 100
minimum = 350
maximum = 1000

integ_ms = 50

save_file = False

file_suffix = "TLSdiffuser"

"""
Code
"""

newp = TLS()

sens = sensor(port = "COM6")

try:    
    newp.filterW(filterW)
    
    # Initialize sensor
    sens.set_aper(integ_ms)
    sens.set_reps(1)
    sens.command("E1")
    
    # Build an array of the test frequencies
    test_lam = np.array(range(steps+1))
    test_lam = test_lam*(maximum-minimum)/steps+minimum
    
    TLS_lam = np.array([])
    level_av = np.array([])
    
    for lam in test_lam:
        _ = newp.set_lambda(lam)
        TLS_lam = np.append(TLS_lam, newp.get_lambda())
        
        """ Read sensor """
        array = sens.get_spect()

        av_level = np.mean(array[800:1100])
        
        level_av = np.append(level_av, av_level)
        
    newp.set_lambda(550) #reset it to something we can see.
    
    plt.figure(figsize = (9, 7))
    plt.plot(TLS_lam, level_av)
    plt.ylabel('sensor level')
    plt.xlabel('wavelength (nm)')
    
    power_func = TLS_Cal().power_func
    sensitivity = np.divide(level_av, power_func(TLS_lam))
    
    plt.figure(figsize = (9,7))
    plt.plot(TLS_lam, sensitivity)
    plt.ylabel('adjusted sensitivity (W)')
    plt.xlabel('wavelength (nm)')
    
    if save_file:
        file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
        file_path = file_base+"/Sony_spectrum_"+file_suffix+"%s.txt"
        number = 1
        while os.path.exists(file_path % number):
            number += 1
            
        f = open(file_path % number, "wb")
        
        head = "wavelength_nm, sensor_level, sensitivity"
        np.savetxt(f, (TLS_lam, level_av, sensitivity), header = head, delimiter = "\t") 
        
        f.close()
        
        data = np.loadtxt(file_path % number, unpack=True)
        lambda_nm = data[:,0] 
        curr_A = data[:,1]
        power_W = data[:,0]
        
except Exception as e:
    sens.close()
    newp.close()
    raise e
    
sens.close()
newp.close()
# -*- coding: utf-8 -*-
"""
Created on Tue May 23 10:24:30 2017

Used to find the correspondence between input voltage and output power of the ULS

@author: Gus
"""

import numpy as np
import matplotlib.pyplot as plt
from keysight import Keysight
from labjackU3LV import Labjack
#from photodiode_calibration import diodeCal
import time
import os

"""
Settings
"""

# voltages
steps = 44
minimum = 0.1
maximum = 4.5

sleeptime = 3

# range of SMU. Resolution is approximately 0.5*10^-6 of maximum
max_amps = 2e-8

save_file = False

file_suffix = "bare"

"""
Code
"""

keys = Keysight()
dac = Labjack()

try:    
    keys.set_range(max_amps) # experiment with different ranges for best performance.
    keys.set_output_voltage(5) # Bit of an arbitrary choice. Shouldn't matter much.
    keys.set_aper(0.1)

    # Build an array of the test frequencies
    test_volt = np.array(range(steps+1))
    test_volt = test_volt*(maximum-minimum)/steps+minimum
    actualV = np.zeros_like(test_volt)
    
    curr_av = np.array([])
    average_points = 2
    aper_time = 0.05
    # keys.set_aper(aper_time)
    
    for i, volt in enumerate(test_volt):
        dac.set_voltage(volt+0.1)
        time.sleep(sleeptime/2)
        V = dac.set_voltage(volt)
        time.sleep(sleeptime/2)
        
        actualV[i] = V
        """ Get current """
#        curr = 0
#        dynamic_max = max_amps
#        while curr < dynamic_max*0.8: # dynamic range adjustment, make sure it isn't overflowing but also getting best resolution
#            keys.set_range(dynamic_max)
#            curr = keys.get_current()
#            dynamic_max *= 0.1
        curr = keys.get_current()
        curr_av = np.append(curr_av, curr)
        print(V)
    
    plt.figure(figsize = (9, 7))
    plt.plot(actualV, curr_av)
    plt.ylabel('current')
    plt.xlabel('voltage (V)')
    
    plt.show()
    
    slope, intercept = np.polyfit(actualV, curr_av ,1)
    
    print(slope, " slope, ", intercept, " intercept")
    
    if save_file:
        file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
        file_path = file_base+"/ULS_intensity_"+file_suffix+"%s.txt"
        number = 1
        while os.path.exists(file_path % number):
            number += 1
            
        f = open(file_path % number, "wb")
        
        head = "voltage, current"
        np.savetxt(f, (test_volt, curr_av), header = head, delimiter = "\t") 
        
        f.close()
        
except Exception as e:
    keys.close()
    dac.close()
    raise e
    
keys.close()
dac.close()
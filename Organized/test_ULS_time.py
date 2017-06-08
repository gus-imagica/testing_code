# -*- coding: utf-8 -*-
"""
Created on Wed May 24 15:46:39 2017

This function samples the photodiode over a set period of time with the ULS
set to a particular level by the Labjack DAC. Useful for seeing changes in
the light level over time.

@author: Gus
"""

import matplotlib.pyplot as plt
from keysight import Keysight
import numpy as np
from labjackU3LV import Labjack
import os
import time


"""
Settings
"""

# voltages
time_s = 30 # how long to stream for

voltage = 3

max_amps = 2e-7

save_file = False

file_suffix = "ULS"

"""
Code
"""

t = time.time()

keys = Keysight()

dac = Labjack()

try:
    """ Initialize """
    keys.set_range(max_amps) # experiment with different ranges for best performance.
    keys.set_output_voltage(5) # Bit of an arbitrary choice. Shouldn't matter much.
    keys.auto_aper(True)
    
    array = np.array([])

    dac.set_voltage(voltage)
    print("Voltage: ", voltage)
        
    while time.time()-t < time_s:
        """ Read sensor """
        #print("Reading Sony Sensor...")
        curr = keys.get_current()
        array = np.append(array,curr)
    
    dac.set_voltage(3)
        
    fig = plt.figure(figsize = (12, 9))
    plt.plot(array)

    if save_file:
        file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
        file_path = file_base+"/SonyPTC_"+file_suffix+"%s.txt"
        number = 1
        while os.path.exists(file_path % number):
            number += 1
            
        f = open(file_path % number, "wb")
        
        head = "exposure_time_ms,"+str(names)
        savedata = np.concatenate((test_exp[:,None],np.transpose(noise_array)),axis=1)
        np.savetxt(f, savedata, header = head, delimiter = "\t") 
        
        f.close()
        
        data = np.loadtxt(file_path % number, unpack=True)
        lambda_nm = data[:,0] 
        curr_A = data[:,1]
        power_W = data[:,0]
        
except Exception as e:
    dac.close()
    keys.close()
    raise e
    
dac.close()
keys.close()
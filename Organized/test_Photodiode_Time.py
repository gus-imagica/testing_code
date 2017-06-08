# -*- coding: utf-8 -*-
"""
Created on Wed May 24 15:46:39 2017

Takes current readings over a certain amount of time and averages them.
Useful for taking dark current measurements with temperature.

@author: Gus
"""

from _Photodiode_Cal import diodeCal
from _Keysight_SMU import Keysight

import matplotlib.pyplot as plt
import numpy as np
import os
import time

"""
Settings
"""

# voltages

bias_voltage = 5

time_s = 10 # how long to stream for

max_amps = 2e-10

save_file = False

file_suffix = "PD"

"""
Code
"""

t = time.time()

keys = Keysight()

diode = diodeCal()

try:
    """ Initialize """
    keys.set_range(max_amps) # experiment with different ranges for best performance.
    keys.set_output_voltage(bias_voltage) # Bit of an arbitrary choice. Shouldn't matter much.
    keys.auto_aper(True)
    
    time.sleep(1)
    
    curr_array = np.array([])
    temp_array = np.array([])
        
    while time.time()-t < time_s:
        """ Read sensor """
        #print("Reading Sony Sensor...")
        curr = keys.get_current()
        temp = keys.get_temperature()
        curr_array = np.append(curr_array,curr)
        temp_array = np.append(temp_array, temp)
        
    fig = plt.figure(figsize = (12, 9))
    plt.plot(curr_array)
    fig = plt.figure(figsize = (12, 9))
    plt.plot(temp_array)
    
    print("Avg current: ", np.mean(curr_array), " Amps")
    print("Temperature: ", np.mean(temp_array), " Celcius")
    
    print("Predicted dark current: ", diode.dark(np.mean(temp_array)), " Amps")

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
    keys.close()
    raise e

keys.close()
# -*- coding: utf-8 -*-
"""
Created on Wed May 10 13:41:51 2017

@author: Gus
"""

import keysight
import pyvisa
import numpy as np
import matplotlib.pyplot as plot
import os

"""
Settings
"""

# voltage steps
steps = 100
minimum = 0
maximum = 20

save_file = False

file_suffix = ""

"""
Code
"""

try:
#    inst = newportTLS.TLS()
    
    keys = keysight.Keysight()
    
    # Build an array of the test voltages
    voltages = np.array(range(steps+1))
    voltages = voltages*(maximum-minimum)/steps+minimum
    
    data1 = np.array(keys.current_test(voltages, curr_range = 2e-9, aper_time_s = None))
    voltages2 = list(reversed(voltages))
    data2 = np.array(keys.current_test(voltages2, curr_range = 2e-9, aper_time_s = None))
        
    plot.figure()
    plot.plot(voltages,data1[:,0],voltages2,data2[:,0])
    plot.show()
    
    temp = keys.get_temperature()
    print("Temperature: "+str(temp))
    
    keys.close()
    
    if save_file:
        file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
        file_path = file_base+"/Dark_current_"+file_suffix+"%s.txt"
        number = 1
        while os.path.exists(file_path % number):
            number += 1
            
        f = open(file_path % number, "wb")
        
        head = "Voltage1_V, curr1_A, Voltage2_V, curr2_A, Temperature = %s" % temp
        np.savetxt(f, (voltages, data1[:,0], voltages2, data2[:,0]), header = head, delimiter = "\t") 
        
        f.close()
    
except pyvisa.errors.VisaIOError as e:
    print("Timed out waiting for a response. Make sure all sensors are connected.")
    print(e)
    
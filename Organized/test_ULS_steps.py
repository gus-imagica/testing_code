# -*- coding: utf-8 -*-
"""
Created on Wed May 24 09:00:32 2017

This function samples the photodiode at different ULS light levels selected
using the Labjack DAC. Good for finding the settling time of the ULS.

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
reps = 5000 # number of samples at each voltage

steps = 1
minimum = 0.0
maximum = 4.5

interval_ms = 5

max_amps = 2e-9

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
    # Build an array of the test voltages
    test_volt = np.array(range(steps+1))
    test_volt = test_volt*(maximum-minimum)/steps+minimum

    keys.set_range(max_amps) # experiment with different ranges for best performance.
    keys.set_output_voltage(5) # Bit of an arbitrary choice. Shouldn't matter much.
    keys.auto_aper(True)
    
#    fig = plt.figure(figsize = (12, 9))
#    graph1 = fig.add_subplot(1,1,1)
#    graph1.set_ylabel("level")
    array = []
    for volt in test_volt:
        dac.set_voltage(volt)
        print("Voltage: ", volt)
        """ rolling plot """   
#        frame = sens.get_spect()[700:1600]
#        array.append(frame)
#        graph1.clear()
#        graph1.plot(frame)            
#        plt.draw()
#        plt.pause(0.01)
        
        for i in range(reps):
            """ Read sensor """
            #print("Reading Sony Sensor...")
            curr = keys.get_current()
            time.sleep(interval_ms/1000)
            array.append(curr)
    
    dac.set_voltage(0)
        
    fig = plt.figure(figsize = (12, 9))
    plt.subplot(221)
    plt.plot(array)
    plt.subplot(222)
    plt.plot(array[0:2*reps])
    plt.subplot(223)
    plt.plot(array[int(steps/2)*reps:int(steps/2+2)*reps])
    plt.subplot(224)
    plt.plot(array[-reps*2+1:])

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
        
    elapsed = time.time()-t
    print("Total time: ",elapsed," seconds")
except Exception as e:
    dac.close()
    keys.close()
    raise e
    
dac.close()
keys.close()
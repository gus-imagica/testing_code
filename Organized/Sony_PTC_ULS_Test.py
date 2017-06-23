# -*- coding: utf-8 -*-
"""
Created on Fri May 19 15:37:17 2017

This function generates a photon transfer curve for the Sony ILX554 sensor. It
uses the method of varied intensity from the uniform light source, adjusted
using the Rigol power supply.

It is designed to be faster than the Sony_PTC_ULS.py function by taking a more
appropriate selection of voltages to drive the ULS.

@author: Gus
"""

from _FTDI_Sensor import sensor
from _Keysight_SMU import Keysight
from _Rigol_Power_Supply import Rigol

import matplotlib.pyplot as plt

import numpy as np

import os
import time


"""
Settings
"""

# voltages

repeats = 4 # number of times to take data and overlay

reps = 2 # number of samples to generate the standard deviation

minimum_V = 0.01
maximum_V = 4
steps_V = 50

integ_time_ms = 30

settle_s = 1

save_file = True

# use these if the Keysight is connected
realPower = True
bias_voltage = 5.0
max_amps = 2e-10


file_suffix = "ULS"

"""
Code
"""

t = time.time()

sens = sensor(port = "COM6", print_out = False)

rig = Rigol()

keys = Keysight()

try:
    """ Initialize """
    # Build an array of the test voltages
    
    test_volt = 0.01*(np.unique(np.geomspace(minimum_V*100,maximum_V*100,steps_V).astype(int)))

    sens.set_aper(integ_time_ms)
    sens.set_reps(1)
    
    overflows = []
    underflows = []

    keys.set_output_voltage(bias_voltage)
    keys.set_range(max_amps)
    
    fig = plt.figure(figsize = (12, 9))

    allnoise = [] # Records all the raw noise data
    
    noise_arrays = [] # Records the average noise
    curr_arrays = [] # Records the average current data
    dark_arrays = [] # Records the average temperature
    volt_arrays = [] # Records the commanded voltage
    light_arrays = [] # Records the light induced current
    reverse = False
    for repeat in range(repeats):
        reverse = not reverse
        test_volt = test_volt[::-1]
        noise_array = np.array([])
        actualV = np.array([])
        curr_in = np.array([])
        dark = np.array([])
        for volt in test_volt:
#            dac.set_voltage(volt+0.1)
#            time.sleep(settle_s/4)
            rig.set_output_voltage(volt)
#            V = dac.set_voltage(volt)
            V = volt
            actualV = np.append(actualV, V)
            print("\nVoltage: ", V)
#            time.sleep(settle_s*(3/4))
            time.sleep(settle_s)
            array = []

            curr1 = keys.get_current()
            
            for i in range(reps): # is this enough to assess noise?
                """ Read sensor """
                #print("Reading Sony Sensor...")
                image = np.delete(sens.get_spect(),1181)
                frame = image[200:1300]
                #print("Done")
                #print(max(frame))
                if max(frame) == 4095:
                    overflows.append(volt)
                    print("overflow")
                if min(frame) < 5:
                    underflows.append(volt)
                    print("underflow")
                array.append(frame)

            curr2 = keys.get_current()
            curr = 0.5*(curr1+curr2)
            print("PD Current: ", curr)
            if curr < 1:
                curr_in = np.append(curr_in, curr)
            
            """ Find the dark current for comparisson """
            rig.set_output_voltage(0)
            time.sleep(settle_s)
            dark_current = keys.get_current()-0.01e-11 # this seems to be the difference
            dark = np.append(dark, dark_current)
            print("Dark current: ",dark_current, " Amps")
                
            array = np.array(array)
            print("Average level: ", np.mean(array))
            noise = np.std(array, 0)
            allnoise.append(noise)
            av_noise = np.mean(noise)
            
            noise_array = np.append(noise_array, av_noise)
        
        light_in = curr_in-dark
        
        if reverse:
            noise_arrays.append(noise_array[::-1])
            curr_arrays.append(curr_in[::-1])
            dark_arrays.append(dark[::-1])
            light_arrays.append(light_in[::-1])
            volt_arrays.append(actualV[::-1])
        else: 
            noise_arrays.append(noise_array)
            curr_arrays.append(curr_in)
            dark_arrays.append(dark)
            light_arrays.append(light_in)
            volt_arrays.append(actualV)
        
        linax = plt.subplot(121)
        plt.plot(light_in, noise_array)
    
        logax = plt.subplot(122)
        plt.loglog(light_in, noise_array)  
        slope, intercept = np.polyfit(np.log(light_in), np.log(noise_array),1)
        plt.pause(0.01)
        print("Slope: ",slope)
        
        abline_values = [slope * i + intercept for i in np.log(light_in)]
        plt.loglog(light_in, np.exp(abline_values))
        
#    avnoise = np.mean(noise_arrays,0)
#    
#    y_y = (avnoise[-1]/avnoise[0])**2
#    b_a = (actualV[0]*y_y-actualV[-1])/(1-y_y)
#    print(b_a," power adjustment factor for 0.5 slope")
#    
#    linax = plt.subplot(121)
#    plt.plot(power_in, avnoise, linewidth = 5)
#
#    logax = plt.subplot(122)
#    plt.loglog(power_in, avnoise, linewidth = 5)
#    
#    avslope, avintercept = np.polyfit(np.log(power_in), np.log(avnoise),1)
#    print("Average slope: ", avslope)
    
    if save_file:
        file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
        file_path = file_base+"/SonyPTC_"+file_suffix+"%s.txt"
        number = 1
        while os.path.exists(file_path % number):
            number += 1
            
        f = open(file_path % number, "wb")
        
        head = "voltage, current, noise, dark current"
        savedata = (np.array(volt_arrays).flatten(), np.array(curr_arrays).flatten(), np.array(noise_arrays).flatten(), np.array(dark_arrays).flatten())
        np.savetxt(f, savedata, header = head, delimiter = "\t") 
        
        f.close()
        
#        data = np.loadtxt(file_path % number, unpack=True)
#        lambda_nm = data[:,0] 
#        curr_A = data[:,1]
#        power_W = data[:,0]
        
    elapsed = time.time()-t
    print("Total time: ",elapsed," seconds")
except Exception as e:
#    dac.close()
    rig.close()
    keys.close()
    sens.close()
    raise e
    
#dac.close()
rig.close()
keys.close()
sens.close()
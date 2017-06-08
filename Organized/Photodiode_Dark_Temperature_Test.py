# -*- coding: utf-8 -*-
"""
Created on Tue May 30 11:24:38 2017

This function is used to find the relationship between dark current and
temperature. The photodiode box with thermocouple should be allowed to go
through a wide temperature range (either cooling or warming) which allows a
best fit of the data to be more accurate. The data are fit to an exponential
function because dark current follows approximately doubles every 10 degrees.
The data produced and saved by this function are used in the photodiode
calibration to approximate the dark current in other tests.

Since the thermocouple has poor resolution, the fitting process is complicated.

@author: Gus
"""

import matplotlib.pyplot as plt
from keysight import Keysight
import numpy as np
from labjackU3LV import Labjack
import os
import time
from scipy.interpolate import interp1d as interp
from scipy.optimize import curve_fit
import scipy.ndimage

"""
Settings
"""

# voltages

bias_voltage = 5

time_s = 1200 # how long to stream for

max_amps = 2e-10

save_file = False

file_suffix = "5V"

"""
Code
"""

t = time.time()

keys = Keysight()

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

    """ MATH """
    
    def exp_fun(T, a, c, d):
        return a*np.exp(c*T)+d
    

    inds = np.array(range(len(temp_array)))
    smooth_temp = scipy.ndimage.gaussian_filter(temp_array,50)
    plt.plot(inds, smooth_temp, "r")
    
    popt, pcov = curve_fit(exp_fun, inds, smooth_temp, p0=(1, -1e-4, 50))
    fit_temp = exp_fun(inds, *popt)
    plt.plot(inds, fit_temp, "g")
    
    fig = plt.figure(figsize = (12, 9))
    plt.plot(fit_temp, curr_array)
    
    popt, pcov = curve_fit(exp_fun, fit_temp, curr_array, p0=(1e-11, 1e-2, 1e-11))

    plt.plot(fit_temp, exp_fun(fit_temp, *popt))
    
    if save_file:
        file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
        file_path = file_base+"/photodiode_temperature_darkcurrent_"+file_suffix+"%s.txt"
        number = 1
        while os.path.exists(file_path % number):
            number += 1
            
        f = open(file_path % number, "wb")
        
        head = "Temperature, Current"
        savedata = [temp_array, curr_array]
        np.savetxt(f, savedata, header = head, delimiter = "\t") 
        
        f.close()
        
#        data = np.loadtxt(file_path % number, unpack=True)
#        lambda_nm = data[:,0] 
#        curr_A = data[:,1]
#        power_W = data[:,0]
        
except Exception as e:
    keys.close()
    raise e

keys.close()
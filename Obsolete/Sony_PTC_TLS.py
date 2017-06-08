# -*- coding: utf-8 -*-
"""
Created on Fri May 19 15:37:17 2017

This script generates a photon trnsfer curve for the Sony sensor using the
method of varying exposure time. The benefit of this is that it is a wavelength
specific curve. The downside is that the dark voltage scales with exposure
time at the same rate as the light induced voltage.

It takes pairs of measurements.

@author: Gus
"""


from FTDI_cam import sensor
import matplotlib.pyplot as plt

import numpy as np
from newportTLS import TLS
#from keysight import Keysight
#from photodiode_calibration import diodeCal
import os
import time


"""
Settings
"""

#steps_lam = 0
#start_lam = 450
#end_lam = 650
lam = 400

steps_integ_ms = 20
start_integ_ms = 1500
end_integ_ms = 4000

integ_offset = 4.3 # this is how many milliseconds the integration takes if the time is set to 0.

filterW = 1 # Wheel 1 is no filter, wheel 3 is dark

max_amps = 2e-7

save_file = False

file_suffix = "dark"

reps = 2

pairs = 3

"""
Code
"""

t = time.time()

sens = sensor(port = "COM6", print_out = False)

newp = TLS()

try:
    """ Initialize """
    # Initilize SMU
    
    # Initialize TLS
    newp.filterW(filterW)
    
#    # Build an array of the test frequencies
#    test_lam = np.array(range(steps_lam+1))
#    test_lam = test_lam*(end_lam-start_lam)/steps_lam+start_lam
    
    # Build an array of the test exposures
    test_exp = np.array(range(steps_integ_ms+1))
    test_exp = test_exp*(end_integ_ms-start_integ_ms)/steps_integ_ms+start_integ_ms
    
#    noise_array = np.empty((len(test_lam),len(test_exp)))
#    average_array = np.empty((len(test_lam),len(test_exp)))
    noise_array = np.array([])
    average_array = np.array([])
    allnoise = []
    
#    for lam_ind, lam in enumerate(test_lam):  
#        print("Wavelength ",lam,"nm")
    _ = newp.set_lambda(lam)
    _ = newp.get_lambda()
    for exp_ind, exp in enumerate(test_exp):
        print("Integraton time ",exp," ms")
        # Initialize sensor
        sens.set_aper(exp)
        sens.set_reps(1)
        array = []
        """ Get one frame and normalize to it """
        frame = sens.get_spect()[7:]
        first_average = np.median(frame)
        
        for i in range(reps): # is this enough to assess noise?
            """ Read sensor """
            #print("Reading Sony Sensor...")
            frame = sens.get_spect()[7:]
            frame_average = np.median(frame)
            frame = frame+first_average-frame_average # normalize

            if max(frame) == 4095:
                print("overflow")
            if min(frame) < 5:
                print("underflow")
            array.append(frame)
        array = np.array(array)
        average = np.median(array)
        noise = np.std(array, 0)
        allnoise.append(noise)
        av_noise = np.mean(noise)
#        average_array[lam_ind, exp_ind] = average
#        noise_array[lam_ind, exp_ind] = av_noise
        average_array = np.append(average_array, average)
        noise_array = np.append(noise_array, av_noise)
    test_exp = test_exp+integ_offset
        
#    names = []
#    for lam in test_lam:
#        names.append(str(lam)+"nm")
     
    plt.figure(figsize = (15,9))
    linax = plt.subplot(121)
#    for i in range(lam_ind):
#        plt.plot(test_exp, noise_array[i,:])
#    plt.legend(names)
    plt.plot(test_exp, noise_array)    

    logax = plt.subplot(122)
    logslope = []
#    for i in range(lam_ind):
#        plt.loglog(test_exp, noise_array[i,:])  
#        slope, intercept = np.polyfit(np.log(test_exp), np.log(noise_array[i,:]),1)
#        logslope.append(slope)
#    plt.legend(names)
    plt.loglog(test_exp, noise_array)
    slope, intercept = np.polyfit(np.log(test_exp), np.log(noise_array),1)
    print(slope)
    
    plt.figure()
    plt.plot(test_exp, average_array)
            
    

    if save_file:
        file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
        file_path = file_base+"/SonyPTC_TLS_"+file_suffix+"%s.txt"
        number = 1
        while os.path.exists(file_path % number):
            number += 1
            
        f = open(file_path % number, "wb")
        
        head = "exposure_time_ms, median level, noise"
#        savedata = np.concatenate((test_exp[:,None],np.transpose(noise_array)),axis=1)
        savedata = [test_exp, average_array, noise_array]
        np.savetxt(f, savedata, header = head, delimiter = "\t") 
        
        f.close()
        
#        data = np.loadtxt(file_path % number, unpack=True)
#        lambda_nm = data[:,0] 
#        curr_A = data[:,1]
#        power_W = data[:,0]
        
    elapsed = time.time()-t
    print(elapsed)
except Exception as e:
    newp.close()
    sens.close()
    raise e
    
newp.close()
sens.close()
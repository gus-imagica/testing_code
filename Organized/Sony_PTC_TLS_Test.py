# -*- coding: utf-8 -*-
"""
Created on Fri May 19 15:37:17 2017

Creates a photon transfer curve using the varying exposure method with the
Tunable Light Source set to a specific wavelength. Only one pass is made through
the exposure times. Uses a geometric series of exposure times.

@author: Gus
"""


from _Newport_TLS import TLS
from _FTDI_Sensor import sensor

import matplotlib.pyplot as plt
import numpy as np
import os
import time


"""
Settings
"""

#steps_lam = 0
#start_lam = 450
#end_lam = 650
lam = 400

steps_integ_ms = 200
start_integ_ms = 1
end_integ_ms = 5000

integ_offset = 4.3 # this is how many milliseconds the integration takes if the time is set to 0.

filterW = 1 # Wheel 1 is no filter, wheel 3 is dark

max_amps = 2e-7

save_file = False

file_suffix = "dark"

reps = 2

"""
Code
"""

t = time.time()

sens = sensor(port = "COM7", print_out = False)

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
#    test_exp = np.array(range(steps_integ_ms+1))
#    test_exp = test_exp*(end_integ_ms-start_integ_ms)/steps_integ_ms+start_integ_ms
    test_exp = np.unique(np.geomspace(start_integ_ms,end_integ_ms,steps_integ_ms).astype(int))
    
#    noise_array = np.empty((len(test_lam),len(test_exp)))
#    average_array = np.empty((len(test_lam),len(test_exp)))
    noise_array = np.array([])
    average_array = np.array([])
    
#    for lam_ind, lam in enumerate(test_lam):  
#        print("Wavelength ",lam,"nm")
    _ = newp.set_lambda(lam)
    _ = newp.get_lambda()
    for exp_ind, exp in enumerate(test_exp):
        print("Integraton time ",exp," ms")
        # Initialize sensor
        sens.set_aper(exp)
        sens.set_reps(1)
        
        noises = []
        averages = []
        for i in range(reps): # is this enough to assess noise?
            """ Get one frame and normalize to it """
            frame1 = sens.get_spect()[7:]
            frame1_average = np.mean(frame1)
            """ Read sensor """
            #print("Reading Sony Sensor...")
            frame2 = sens.get_spect()[7:]
            frame2_average = np.mean(frame2)
            frame2 = frame2+frame1_average-frame2_average # normalize
            
            noise = np.std([frame1, frame2], 0, ddof = 1)
            average = frame1_average

            if max(frame1) == 4095:
                print("overflow")
            if min(frame1) < 5:
                print("underflow")
            noises.append(noise)
            averages.append(average)
        average = np.mean(averages)
        av_noise = np.mean(noises)
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
    
    # We only want to see the slope in the linear region.
    slopeind1 = (np.abs(test_exp-0.01*max(test_exp))).argmin()
    slopeind2 = (np.abs(test_exp-0.4*max(test_exp))).argmin()
    fit_exp = test_exp[slopeind1:slopeind2]
    slope, intercept = np.polyfit(np.log(fit_exp), np.log(noise_array[slopeind1:slopeind2]),1)
    print("Linear region slope: ", slope)
    fit_noise = np.exp(intercept)*np.power(fit_exp,slope)
    
#    for i in range(lam_ind):
#        plt.plot(test_exp, noise_array[i,:])
#    plt.legend(names)
    plt.plot(test_exp, noise_array, 'bo')
    plt.plot(fit_exp, fit_noise, 'r-')
    plt.xlabel("Exposure time (ms)")
    plt.ylabel("Digital standard deviation")
    plt.legend(["Data", "Fit"]) 
    
    logax = plt.subplot(122)
    logslope = []
#    for i in range(lam_ind):
#        plt.loglog(test_exp, noise_array[i,:])  
#        slope, intercept = np.polyfit(np.log(test_exp), np.log(noise_array[i,:]),1)
#        logslope.append(slope)
#    plt.legend(names)
    plt.loglog(test_exp, noise_array,'bo')
    plt.loglog(fit_exp, fit_noise, 'r-')
    
    plt.xlabel("Exposure time (ms)")
    plt.ylabel("Digital standard deviation")
    plt.legend(["Data", "Fit (Slope = %s)" % slope]) 
    
#    plt.figure()
#    plt.plot(test_exp, average_array)
            
    

    if save_file:
        file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
        file_path = file_base+"/SonyPTC_TLS_"+file_suffix+"%s.txt"
        # file_path = file_base+"/ILX554_PTC_TLS_3diffuser_400nm.txt"
        number = 1
        while os.path.exists(file_path % number):
            number += 1
            
        f = open(file_path % number, "wb")
        
        head = "exposure_time_ms, median_level, standard_deviation"
#        savedata = np.concatenate((test_exp[:,None],np.transpose(noise_array)),axis=1)
        savedata = [test_exp, average_array, noise_array]
        np.savetxt(f, savedata, header = head, delimiter = "\t") 
        
        f.close()
        
#        data = np.loadtxt(file_path % number, unpack=True)
#        exposure_ms = data[:,0] 
#        average_level = data[:,1]
#        average_noise = data[:,2]
        
    elapsed = time.time()-t
    print(elapsed)
except Exception as e:
    newp.close()
    sens.close()
    raise e
    
newp.close()
sens.close()
# -*- coding: utf-8 -*-
"""
Created on Fri May 12 14:31:50 2017

Determines properties of the Sony ILX554 sensor using the methods outlined in EMVA1288-3.0.pdf
Properties determined:
    Saturation level
    Responsivity R (digital steps per photon)
    System gain K (digital steps per electron)
    Quantum efficiency E (electrons per photon)

Outline
        ---
    Set lambda
    Saturation level:
        Granular data
        Find maximum variance point
    Dark values and noise:
        filter 3
        10-70% of saturation exposure
        2 images at each level
        variance, mean, stdev
    Light values and noise:
        filter 1
        10-70% of saturation exposure
        2 images at each level
        variance, mean, stdev
        photons:
            PD current - dark current
            current -> light power
            light power -> photons at lambda
    Responsivity (R):
        fit values and photons linear relationship
    System gain (K):
        fit variance and values linear relationship
    Quantum efficiency (n): R/K
    Signal to noise ratio (SNR):
        Plot with ideal SNR for comparission on loglog
    Dynamic range (DR):
        Ratio of saturation photons to minimum photons
        ---
        
@author: Gus
"""

from FTDI_cam import sensor
import matplotlib.pyplot as plt

import numpy as np
from newportTLS import TLS
from keysight import Keysight
from photodiode_calibration import diodeCal
import os
import time

"""
Settings
"""

#steps_lam = 0
#start_lam = 450
#end_lam = 650
lam = 550

find_sat_ms = True
sat_ms_default = 200
steps_ms = 50

pixel_area = 14*56e-12 # From spec sheet
integ_offset = 4.3 # This is how many milliseconds the integration takes if the time is set to 0.

filterW = 1 # Wheel 1 is no filter, wheel 3 is dark

bias_voltage = 5
max_amps = 2e-9

save_file = False

file_suffix = "trial"

reps = 2

"""
Code
"""

t = time.time()

sens = sensor(port = "COM6", print_out = False)
keys = Keysight()
newp = TLS()

try:
    """
    Initialize devices
    """
    keys.set_output_voltage(bias_voltage)
    keys.set_range(max_amps)
    keys.set_aper(0.1) # long exposure for better averageing
    
    sens.set_reps(1)    
    """
    Set lambda
    """
    newp.set_lambda(lam)
    
    """
    Saturation level:
        Granular data
        Find maximum variance point
    """
    if find_sat_ms:
        newp.filterW(1) # Light mode
        
        start_integ_ms = 4
        multiplier = 1.3
        max_integ_ms = 3000
        var_av_a = np.array([])
        integ_ms_a = np.array([])
        
        sat_ms = 0
        sat_var = 0
        integ_ms = start_integ_ms
        while integ_ms<0:
            sens.set_aper(integ_ms)
            frame1 = sens.get_spect()
            frame2 = sens.get_spect()
            var = np.var([frame1,frame2],0)
            var_av = np.mean(var)
            var_av_a = np.append(var_av_a, var_av)
            if var_av > sat_var:
                sat_ms = integ_ms
                sat_var = var_av
            if np.mean(frame1)>4050: # its obviously maxed out here. Right?
                break
            
            integ_ms *= multiplier
            
        plt.figure()
        plt.loglog(integ_ms_a, var_av_a)
        plt.plot([sat_ms, sat_ms],[sat_var,var_av_a[0]])
        plt.xlabel("Integration Time (ms)")
        plt.ylabel("Digital value variance (unitless)")
        plt.title("Finding the saturation exposure")
    else:
        sat_ms = sat_ms_default
    
    # Generate list of integration times to test over 
    start_ms = sat_ms*0.1
    end_ms = sat_ms*0.7
    steps = steps_ms
    test_ms = np.array(range(steps+1))
    test_ms = test_ms*(end_ms-start_ms)/steps+start_ms
    
    """
    Dark values and noise:
        filter 3
        10-70% of saturation exposure
        2 images at each level
        variance, mean, stdev
    """
    
    newp.filterW(3)
    
    dark_mean = np.zeros_like(test_ms)
    dark_var = np.zeros_like(test_ms)
    for ind, integ_ms in enumerate(test_ms):
        sens.set_aper(integ_ms)
        frame1 = sens.get_spect()
        frame2 = sens.get_spect()
        var = np.var([frame1,frame2],0)
        var_av = np.mean(var)
        dark_var[ind] = var_av
        mean = np.mean([frame1,frame2])
        dark_mean[ind] = mean
    
    dark_curr = keys.get_current()
    
    """
    Light values and noise:
        filter 1
        10-70% of saturation exposure
        2 images at each level
        variance, mean, stdev
        photons:
            PD current - dark current
            current -> light power
            light power -> photons at lambda
    """
    
    newp.filterW(1)
    
    light_mean = np.zeros_like(test_ms)
    light_var = np.zeros_like(test_ms)
    light_curr = np.zeros_like(test_ms)
    for ind, integ_ms in enumerate(test_ms):
        sens.set_aper(integ_ms)
        frame1 = sens.get_spect()
        frame2 = sens.get_spect()
        curr = keys.get_current
        var = np.var([frame1,frame2],0)
        var_av = np.mean(var)
        light_var[ind] = var_av
        mean = np.mean([frame1,frame2])
        light_mean[ind] = mean
        light_curr[ind] = curr-dark_curr # These should all be basically the same
    
    diode = diodeCal()
    power_W = light_curr/diode.func(lam) # power coming from the photodiode
    """ Convert power to photons """
    hc = 1.98644568e-16 # J nm
    photon_J = hc/lam
    photons_persec = power_W/photon_J # photon current on the photodiode
    photon_intensity = photons_persec/diode.area
    
    exposure_ms = test_ms + integ_offset # the way the sensor works
    irradiation = np.multiply(exposure_ms, photon_intensity)*pixel_area
    
    """
    Responsivity (R):
        fit values and photons linear relationship
    """
    plt.figure()
    plt.plot(irradiation, light_mean-dark_mean, 'bo')
    plt.xlabel("Irradiation (photons/pixel)")
    plt.ylabel("Digital value mean (dark offset removed)")
    plt.title("Responsivity")
    plt.pause(0.01)
    
    R, intercept = np.polyfit(irradiation, light_mean-dark_mean, 1)
    print("Responsivity: ", R)
    
    abline_values = [R * i + intercept for i in irradiation]
    plt.plot(irradiation, abline_values)
    
    plt.legend(["Data", "Fit"])
    
    """
    System gain (K):
        fit variance and values linear relationship
    """
    plt.figure()
    plt.plot(light_mean-dark_mean, light_var-dark_var, 'bo')
    plt.xlabel("Digital value mean (dark offset removed)")
    plt.ylabel("Digital value variance (dark offset removed)")
    plt.title("System gain")
    plt.pause(0.01)
    
    K, intercept = np.polyfit(light_mean-dark_mean, light_var-dark_var, 1)
    print("System gain (digital steps per electron): ", K)
    
    abline_values = [K * i + intercept for i in light_mean-dark_mean]
    plt.plot(light_mean-dark_mean, abline_values)
    
    plt.legend(["Data", "Fit"]) 
    
    """
    Quantum efficiency (n): R/K
    """
    QE = R/K
    print("Quantum efficiency: ", QE, " electrons per photon")
    
    """
    Temporal dark noise
    """
    plt.figure()
    plt.plot(exposure_ms, dark_var, 'bo')
    plt.xlabel("Digital value mean (dark offset removed)")
    plt.ylabel("Digital value variance (dark offset removed)")
    plt.title("System gain")
    plt.pause(0.01)
    
    slope, dark_var_min = np.polyfit(exposure_ms, dark_var, 1)
    print("Dark variance intercept: ", dark_var_min)
    
    abline_values = [slope * i + dark_var_min for i in exposure_ms]
    plt.plot(exposure_ms, abline_values)
    
    plt.legend(["Data", "Fit"])

    quantization_noise = 1/12 # is this right??
    temporal_dark_noise = np.sqrt(dark_var_min-quantization_noise)/K

    """
    Absolute Sesitivity Threshold
    """
    up_min = 1/QE*(np.sqrt(dark_var_min)+1/2)
    
    """
    Saturation capacity
    """
    sat_exposure_ms = sat_ms + integ_offset # the way the sensor works
    up_sat = sat_exposure_ms*np.mean(photon_intensity)*pixel_area
    ue_sat = QE*up_sat
    
    """
    Signal to noise ratio (SNR)
    """
    SNR = np.divide((light_mean-dark_mean),np.sqrt(light_var-dark_var))
    plt.figure()
    plt.loglog(irradiation, SNR)
    plt.xlabel("Irradiation (photons per pixel)")
    plt.ylabel("SNR")
    plt.title("SNR")
    plt.pause(0.01)
    
    print("SNR_max: ", np.sqrt(ue_sat))
    
    SNR_ideal = np.sqrt(irradiation)
#    plt.plot(irradiation, SNR_ideal)
    
    """
    Dynamic range (DR)
    """
    DR = up_sat/up_min
    print("Dynamic range: ", DR)
    """
    SAVE DATA
    """
    if save_file:
        file_base = "//READYSHARE/USB_Storage/GusFiles/test_data"
        file_path = file_base+"/SonyEvaluation_"+file_suffix+"%s.txt"
        number = 1
        while os.path.exists(file_path % number):
            number += 1
            
        f = open(file_path % number, "wb")
        
        head = "dark_mean, light_mean, dark_var, light_var, light_curr"
        head += ", Responsivity = %s" % R
        head += ", System gain = %s" % K
        head += ", QE = %s" % QE
        head += ", DR = %s" % DR
        savedata = [dark_mean, light_mean, dark_var, light_var, light_curr]
        np.savetxt(f, savedata, header = head, delimiter = "\t") 
        
        f.close()
        
    elapsed = time.time()-t
    print("Run time: ", elapsed)
    
except Exception as e:
    keys.close()
    newp.close()
    sens.close()
    raise e
    
keys.close()
newp.close()
sens.close()
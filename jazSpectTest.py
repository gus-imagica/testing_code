# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import seabreeze.spectrometers as sb
import numpy as np

class Spect(object):
    def __init__(self, port = "COM5", int_time = 1500):
        devices = sb.list_devices() # Find the spectrometer, there is only one
        # print(devices)
        self.spec = sb.Spectrometer(devices[0])
        self.min_int_time = spec.minimum_integration_time_micros
        self.int_time = int_time
        
        self.set_int_time_ms(int_time)
        
         # This is the minimum
        spec.minimum_integration_time_micros
        
    
    # Sends a command, returns 1 if successful 0 otherwise
    def set_int_time(self, ms):
        ms = max(self.min_int_time, ms)
        self.int_time = ms
        spec.integration_time_micros(self.int_time)
        return ms


    
    while True:
        lambda_in = input("Enter nominal wavelength")
        if not lambda_in:
            break
        else:
            lambda_vect.append(int(lambda_in))
        specData = spec.intensities()
        spectra = np.append(spectra,specData)
        
        # absolute maximum value
        index_max = np.argmax(specData)
        lam_max = spectrum_lambda[index_max]
        print("maximum wavelength: ", lam_max)
        
        # Remove the noise at all wavelengths using median.
        med = np.median(specData)
        specData = specData-med
        
        # Find the average data point by bisecting data.
        integ = sum(specData)
        halfint = integ/2
        csum = 0
        for x in range(len(specData)):
            csum = csum+specData[x]
            if csum > halfint:
                lam_bisect = spectrum_lambda[x]
                print("data average wavelength: ", lam_bisect)
                break
        
        maxes.append([lam_max, lam_bisect])
        
        plt.figure()
        plt.plot(spectrum_lambda, specData)
        plt.show()
        
        plt.figure()
        plt.plot(spectrum_lambda[index_max-50:index_max+50], specData[index_max-50:index_max+50])
        plt.show()
    
    spec.close()
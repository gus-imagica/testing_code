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
        self.min_int_time = self.spec.minimum_integration_time_micros
        self.wavelengths = self.spec.wavelengths()
        self.int_time = int_time
        
        self.set_int_time_ms(int_time)
    
    # Set the integration time. Limits to the minimum value.
    def set_int_time_ms(self, ms):
        ms = max(self.min_int_time, ms)
        self.int_time = ms
        self.spec.integration_time_micros(self.int_time)
        return ms
    
    def get_intensities(self):
        intensities = self.spec.intensities()
        return intensities
    
    # returns the maximum lambda and corresponding intensity
    def get_maximum(self):
        intens = self.get_intensities()
        index_max = np.argmax(intens)
        lam_max = self.wavelengths[index_max]
        intens_max = max(intens)
        return lam_max, intens_max
        
    # returns a plot of the intensities [in the range max plus/minus rang]
    def plot(self, intensities, rang = None): 
        index_max = np.argmax(intensities)
        wavelengths = self.wavelengths
        
        if rang is not None:
            upper = rang
            lower = rang
            
            if index_max+upper > len(wavelengths):
                upper = len(wavelengths)-index_max-1
            if index_max-lower < 0:
                lower = index_max
            
            intensities = intensities[index_max-lower:index_max+upper]
            wavelengths = wavelengths[index_max-lower:index_max+upper]
        
        plt.figure()
        plt.plot(wavelengths, intensities)
        plt.ylabel('intensity')
        plt.xlabel('wavelength (nm)')
        
        plt.show()
            
    
    def close(self):
        self.spec.close()
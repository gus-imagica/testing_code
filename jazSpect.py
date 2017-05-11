# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import matplotlib.pyplot as plt
import seabreeze.spectrometers as sb
import numpy as np

class Spect(object):
    
    def __init__(self, int_time = 1500):
        devices = sb.list_devices() # Find the spectrometer, there is only one
        if len(devices) > 1:
            print(devices)
        if len(devices) < 1:
            raise Exception("No spectrometer connected to computer")
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
    def get_maximum(self, intens):
        index_max = np.argmax(intens)
        lam_max = self.wavelengths[index_max]
        intens_max = max(intens)
        return lam_max
    
    def get_double_peak(self, intens):
        intens = intens
        maxval = max(intens)
        cut_point = maxval/2
        cut_inds = []
        for ind in range(len(intens)-1):
            if intens[ind] <= cut_point and intens[ind+1] >= cut_point:
                cut_inds.append(ind)
            elif intens[ind] >= cut_point and intens[ind+1] <= cut_point:
                cut_inds.append(ind)
                
        if len(cut_inds) is 4:
            ind_max1 = np.argmax(intens[cut_inds[0]:cut_inds[1]])+cut_inds[0]
            ind_min = np.argmin(intens[cut_inds[1]:cut_inds[2]])+cut_inds[1]
            ind_max2 = np.argmax(intens[cut_inds[2]:cut_inds[3]])+cut_inds[2]
            lam_max1 = self.wavelengths[ind_max1]
            lam_min = self.wavelengths[ind_min]
            lam_max2 = self.wavelengths[ind_max2]
            return lam_max1, lam_min, lam_max2
        else:
            return None
        
    # returns a plot of the intensities [in the range max plus/minus rang]
    def plot(self, intensities, rang = None, int_time = None, filterW = None, lam = None): 
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
        
        plt.figure(figsize = (12, 9))
        plt.plot(wavelengths, intensities)
        plt.ylabel('intensity')
        plt.xlabel('wavelength (nm)')
        
        title = "Intensity Spectrum\n"
        if lam is not None:
            title += "Nominal wavelength (nm): "+str(lam)+". "
        if int_time is not None:
            title += "Integration time (ms): "+str(int_time)+". "
        if filterW is not None:
            title += "Filter setting: "+str(filterW)+". "
            
        plt.suptitle(title)
        
        plt.show()
            
    
    def close(self):
        self.spec.close()
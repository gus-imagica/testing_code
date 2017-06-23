# -*- coding: utf-8 -*-
"""
Created on Wed May 10 17:08:00 2017

This class contains properties of the calibrated photodiode that are important
for understanding the current measurements.

@author: Gus
"""

from scipy.interpolate import interp1d as interp
import scipy.ndimage
from scipy.optimize import curve_fit
import numpy as np
import matplotlib.pyplot as plt

class diodeCal(object):
    def __init__(self, filepath = r"C:\Users\Gus\GoogleDrive\GeneralShare\Testing\Equipment/Photodiodes/PhotodiodeCal.txt"):
        cal_file = open(filepath, 'r')
        
        result = []
        lams = []
        effs = []
        for line in cal_file.readlines()[1:]:
            strlist = line.split('\t')
            lam = float(strlist[0])
            eff = float(strlist[1])
            result.append([lam, eff])
            lams.append(lam)
            effs.append(eff)
        
        cal_file.close()
        
        result = np.array(result)
        
        self.array = result
        self.lambdas = lams
        self.effic = effs
        
        self.area = (3.6e-3)**2 # 13 mm squared
        
        self.func = interp(lams, effs, kind = "cubic")
        
        self.dark = self.dark_function()
        
    def dark_function(self, file1 = "//READYSHARE/USB_Storage/GusFiles/test_data/photodiode_temperature_darkcurrent_5V1.txt", file2 = "//READYSHARE/USB_Storage/GusFiles/test_data/photodiode_temperature_darkcurrent_5V2.txt"):
        high_data = np.loadtxt(file1, unpack=True)
        temp_array1 = high_data[:,0]
        curr_array1 = high_data[:,1]
        temp_array1 = temp_array1[::-1]
        curr_array1 = curr_array1[::-1]
        
        # only use the half of the data closes to room temp
        temp_array1 = temp_array1[:len(temp_array1)//2]
        curr_array1 = curr_array1[:len(curr_array1)//2]
        
#        temp_array1 = temp_array1 # adjust this for difference between photodiode temperature and thermocouple temperature
        
        low_data = np.loadtxt(file2, unpack=True)
        temp_array2 = low_data[:,0]
        curr_array2 = low_data[:,1]
        temp_array2 = temp_array2[len(temp_array2)//2:]
        curr_array2 = curr_array2[len(curr_array2)//2:]
        
#        temp_array2 = temp_array2 # adjust this for difference between photodiode temperature and thermocouple temperature
        
        all_temp = np.append(temp_array2, temp_array1)
        all_curr = np.append(curr_array2, curr_array1)
        
                
#        fig = plt.figure(figsize = (12, 9)) # REMOVE
        
        
        def exp_fun(T, a, c, d):
            return a*np.exp(c*T)+d
        
        inds1 = np.array(range(len(temp_array1)))
        smooth_temp1 = scipy.ndimage.gaussian_filter(temp_array1,50)
        # plt.plot(inds, smooth_temp, "r")
        
        popt, pcov = curve_fit(exp_fun, inds1, smooth_temp1, p0=(1, 1e-6, 25))
        fit_temp1 = exp_fun(inds1, *popt)
        # plt.plot(inds, fit_temp, "g")
        
        inds2 = np.array(range(len(temp_array2)))
        smooth_temp2 = scipy.ndimage.gaussian_filter(temp_array2,50)
        # plt.plot(inds, smooth_temp, "r")
        
        popt, pcov = curve_fit(exp_fun, inds2, smooth_temp2, p0=(-1, -1e-6, 25))
        fit_temp2 = exp_fun(inds2, *popt)
        # plt.plot(inds, fit_temp, "g")
        
        all_fit_temp = np.append(fit_temp2, fit_temp1)
        # plt.plot(all_fit_temp, "g")        
        
        popt, pcov = curve_fit(exp_fun, all_fit_temp, all_curr, p0=(1e-11, 1e-2, 1e-11)) 
        
        print(popt)
        
        def dark_fun(T):
            return exp_fun(T,*popt)
        
#        plt.plot(all_fit_temp, all_curr)
#        plt.plot(all_temp,all_curr)
#        plt.plot(all_fit_temp,dark_fun(all_fit_temp))
        
        return dark_fun
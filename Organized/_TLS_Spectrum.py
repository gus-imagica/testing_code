# -*- coding: utf-8 -*-
"""
Created on Mon May  8 14:03:13 2017

This class allows easy access to the TLS spectrum (Xe Lamp spectrum).

@author: Gus
"""

from scipy.interpolate import interp1d as interp
import numpy as np

class TLS_Cal(object):
    def __init__(self, filepath = "//READYSHARE/USB_Storage/GusFiles/test_data/TLS_intensity_bare5.txt"):
        
        data = np.loadtxt(filepath, unpack=True)
        lambda_nm = data[:,0] 
        curr_A = data[:,1]
        power_W = data[:,2]
        
        self.array = np.array(data)
        self.lambdas = lambda_nm
        self.curr = curr_A
        self.power = power_W
        
        self.power_func = interp(self.lambdas, self.power, kind = "cubic")
        self.curr_func = interp(self.lambdas, self.curr, kind = "cubic")
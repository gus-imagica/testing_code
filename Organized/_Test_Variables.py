# -*- coding: utf-8 -*-
"""
Created on Mon Jun 12 09:10:21 2017

This set of classes defines the variables needed to run an arbitrary test.

@author: Gus
"""

import os

class keysightVars(object):
    enable = False
    curr_range = 0
    volt_val = 0
    start = 0
    end = 0
    steps = 0
    aperature_time = None
    
class TLSVars(object):
    enable = False
    lambda_val = 550
    start = 0
    end = 0
    steps = 0
    filterW = 1

class spectVars(object):
    enable = False
    pass

class DACVars(object): # this can be used for either Rigol or Labjack
    enable = False
    volt_val = 0
    start = 0
    end = 0
    steps = 0
    
class sensorVars(object):
    enable = False
    pixel_range = slice(0,0)
    integ_ms = 0
    

class testVars(object): # this contains all other test variables
    save_dir = os.pardir
    sensor = sensorVars()
    DAC = DACVars()
    spect = spectVars()
    keysight = keysightVars()
    TLS = TLSVars()
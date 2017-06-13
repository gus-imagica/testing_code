# -*- coding: utf-8 -*-
"""
Created on Fri May  5 12:05:30 2017

This script will eventally allow control over the various functions and
settings elsewhere in the project.

@author: Gus
"""

import os
import tkinter as tk
from tkinter import font
from serial import SerialException
from _Test_Variables import testVars
#from _Jaz_Spectrometer import Spect # Not in py3.6
from _Keysight_SMU import Keysight

class testGui(object):
    
    def __init__(self):
        self.root = tk.Tk()
        
        # font to use for titles
        uline = font.Font(underline = True)
        
        # test variables object contains all information needed to run a test.
        self.testVars = testVars()
        
        ## top frame
        self.masterFrame = tk.Frame(self.root, relief = tk.GROOVE, bd = 4, width = 666)
        # self.masterFrame.grid(sticky = tk.N)
        self.masterFrame.grid(sticky = tk.E+tk.W+tk.N+tk.S)
        self.root.title("Imagica Test Suite")
        self.label = tk.Label(self.masterFrame, text = "All Devices", justify = 'center', font = uline)
        self.label.grid(sticky=tk.N)
        
        """
        electrometer frame
        """
        
        subframe = tk.Frame(self.masterFrame, relief = tk.RIDGE, bd = 2)
        subframe.grid(sticky=tk.N+tk.E+tk.W)
        
        subsubframe = tk.Frame(subframe)
        subsubframe.grid(sticky = tk.W)
        label = tk.Label(subsubframe, text = "Keysight Electrometer", font = uline)
        label.grid(sticky = tk.W)

        self.enableKeysight = tk.IntVar()
        command = lambda: self.enableDevice("Keysight", self.enableKeysight.get())
        enable = tk.Checkbutton(subsubframe, text = "Enable", variable = self.enableKeysight, command = command)
        enable.grid(sticky = tk.W, row = 0, column = 1)
        
        # This little frame contains the entry and label field. It is easier to organize.
        subsubframe = tk.Frame(subframe)
        subsubframe.grid(sticky = tk.N)
        # the maximum current defines the range
        self.maxCurrBox = tk.Entry(subsubframe)
        self.maxCurrBox.insert(0, "0")
        label = tk.Label(subsubframe, text = "Maximum Current Readout (ex. 2E-10): ")
        label.grid(sticky = tk.W)
        self.maxCurrBox.grid(row = 0, column = 1, sticky = tk.W)
        
        subsubframe = tk.Frame(subframe)
        subsubframe.grid(sticky = tk.N)
        # the maximum current defines the range
        self.timeCurrBox = tk.Entry(subsubframe)
        label = tk.Label(subsubframe, text = "Averageing time (ms : 0 for automatic): ")
        label.grid(sticky = tk.W)
        self.timeCurrBox.grid(row = 0, column = 1, sticky = tk.W)

        subsubframe = tk.Frame(subframe)
        subsubframe.grid(sticky = tk.NW)
        # the maximum current defines the range
        self.startBiasBox = tk.Entry(subsubframe)
        label = tk.Label(subsubframe, text = "Start Output Voltage (V): ")
        label.grid(sticky = tk.W)
        self.startBiasBox.grid(row = 0, column = 1, sticky = tk.W)
        
        subsubframe = tk.Frame(subframe)
        subsubframe.grid(sticky = tk.NW)
        # the maximum current defines the range
        self.endBiasBox = tk.Entry(subsubframe)
        label = tk.Label(subsubframe, text = "End Output Voltage (V): ")
        label.grid(sticky = tk.W)
        self.endBiasBox.grid(row = 0, column = 1, sticky = tk.W)
        
        subsubframe = tk.Frame(subframe)
        subsubframe.grid(sticky = tk.NW)
        # the maximum current defines the range
        self.sweepStepsBox = tk.Entry(subsubframe)
        label = tk.Label(subsubframe, text = "Voltage Sweep Steps: ")
        label.grid(sticky = tk.W)
        self.sweepStepsBox.grid(row = 0, column = 1, sticky = tk.W)
        
        self.sweepBool = tk.IntVar()
        command = lambda: self.enableEntry([self.endVoltBox, self.sweepStepsBox], self.sweepBool.get())
        self.sweepSwitch = tk.Checkbutton(subframe, text = "Voltage sweep?", variable = self.sweepBool, command = command)
        self.sweepSwitch.select()
        self.sweepSwitch.grid(sticky = tk.W)
        
        self.goBut = tk.Button(subframe, text = "Save", command = self.saveElec)
        self.goBut.grid(sticky = tk.N)
        
        """
        spectrometer frame
        """
        subframe = tk.Frame(self.masterFrame, relief = tk.RIDGE, bd = 2, width = 666)
        subframe.grid(sticky=tk.E+tk.W)
        
        subsubframe = tk.Frame(subframe)
        subsubframe.grid(sticky = tk.N)
        label = tk.Label(subsubframe, text = "Jaz Spectrometer", justify = 'center', font = uline)
        label.grid(sticky = tk.W)
        
        self.enableSpect = tk.IntVar()
        command = lambda: self.enableDevice("Spect", self.enableSpect.get())
        enable = tk.Checkbutton(subsubframe, text = "Enable", variable = self.enableSpect, command = command)
        enable.grid(sticky = tk.E, row = 0, column = 1)
        
        command = lambda: self.spect.get_intentities()
        self.frame_But = tk.Button(subframe, text = "Get Spectrum", command = self.get_sensor_frame)
        self.frame_But.grid(sticky = tk.N)
        
        
        """
        TLS frame
        """        
        subframe = tk.Frame(self.masterFrame, relief = tk.RIDGE, bd = 2)
        subframe.grid(sticky=tk.N)
        label = tk.Label(subframe, text = "Newport TLS", font = uline)
        label.grid(sticky = tk.N)
        
        self.enableTLS = tk.IntVar()
        command = lambda: self.enableDevice("TLS", self.enableTLS.get())
        enable = tk.Checkbutton(subframe, text = "Enable", variable = self.enableTLS, command = command)
        enable.grid(sticky = tk.E, row = 0)
        
        """
        Sensor frame
        """
        title = "Sony Sensor"
        
        self.Frame = tk.Frame(self.masterFrame, relief = tk.RIDGE, bd = 2)
        self.Frame.grid(sticky=tk.N)
        Lab = tk.Label(self.Frame, text = title, font = uline)
        Lab.grid(sticky = tk.N)
        
        self.frame_But = tk.Button(self.Frame, text = "Grab Frame", command = self.get_sensor_frame)
        self.frame_But.grid(sticky = tk.N)
        
        
        """ Button to run the test """
        runBut = tk.Button(self.masterFrame, text = "Run Test", command = lambda: self.runTest())
#        runBut.grid(row=frame_row_ind, column = 0)
        runBut. grid(sticky = tk.N)
        
        
    def run(self):
        self.root.mainloop()
    
    """ Gui functions """
    # Right now it just prints the max current.
    def saveElec(self):
        self.testVars.keysight.curr_range = float(self.maxCurrBox.get())
        self.testVars.keysight.aperature_time = float(self.timeCurrBox.get())
        self.testVars.keysight.start = float(self.startBiasBox.get())
        self.testVars.keysight.end = float(self.endBiasBox.get())
        self.testVars.keysight.steps = float(self.stepBiasBox.get())
        print(self.testVars.keysight.curr_range)
        
    def enableEntry(self, entry_boxes, enable = True):
        if enable:
            state = "normal"
        else:
            state = "disabled"
            
        for box in entry_boxes:
            box.configure(state = state)
            
    def enableDevice(self, deviceTypeStr, enable):
        if deviceTypeStr is "Spect":
            if enable:
                self.Spect = Spect()
            else:
                self.Spect.close()
        if deviceTypeStr is "Keysight":
            if enable:
                self.Keys = Keysight()
                self.testVars.keysight.enable = True
            else:
                self.Keys.close()
                self.testVars.keysight.enable = False
    
    def get_sensor_frame(self):
        try:
            from _FTDI_Sensor import sensor
            sens = sensor()
            sens.print_frame()
        except SerialException as e:
            print("Unable to connect to the sensor.\n",e)
            
    def runTest(self):
        print("running!")
        print(self.testVars)
    
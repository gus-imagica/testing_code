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

class testGui(object):
    
    def __init__(self):
        self.root = tk.Tk()
        
        # font to use for titles
        uline = font.Font(underline = True)
        
        # test variables
        maxCurr = 0
        startVolt = 0
        endVolt = 0
        sweepSteps = 0
        saveLoc = os.pardir
        self.testVars = [maxCurr, startVolt, endVolt, sweepSteps, saveLoc]
        
        ## top frame
        self.masterFrame = tk.Frame(self.root, relief = tk.GROOVE, bd = 4)
        self.masterFrame.grid(row=0)
        self.root.title("Imagica Test Suite")
        self.titleLab = tk.Label(self.masterFrame, text = "All Devices", justify = 'center', font = uline)
        self.titleLab.grid(sticky=tk.N)
        
        """
        electrometer frame
        """
        rowind = 0
        self._elecFrame = tk.Frame(self.masterFrame, relief = tk.RIDGE, bd = 2)
        self._elecFrame.grid(row=1, column = 0, sticky=tk.N)
        self._elecLab = tk.Label(self._elecFrame, text = "Keysight Electrometer", font = uline)
        self._elecLab.grid(row = rowind, column = 0)
        rowind += 1
        
        # the maximum current defines the range
        self.maxCurrBox = tk.Entry(self._elecFrame)
        label = tk.Label(self._elecFrame, text = "Maximum Current Readout (ex. 1E-10): ")
        label.grid(row = rowind, sticky = tk.W)
        self.maxCurrBox.grid(row = rowind, column = 1, sticky = tk.W)
        rowind += 1
        
        # Will we be sweeping or outputting a constant voltage?
        self.sweepBool = tk.IntVar()
        self.sweepSwitch = tk.Checkbutton(self._elecFrame, text = "Voltage sweep?", variable = self.sweepBool, command = self.enableSweep())
        self.sweepSwitch.select()
        self.sweepSwitch.grid(row=rowind)
        rowind += 1
        
        self.startVoltBox = tk.Entry(self._elecFrame)
        label = tk.Label(self._elecFrame, text = "Start Output Voltage (V): ")
        label.grid(row = rowind, sticky = tk.W)
        self.startVoltBox.grid(row = rowind, column = 1, sticky = tk.W)
        rowind += 1
        
        self.endVoltBox = tk.Entry(self._elecFrame)
        label = tk.Label(self._elecFrame, text = "End Output Voltage (V): ")
        label.grid(row = rowind, sticky = tk.W)
        self.endVoltBox.grid(row = rowind, column = 1, sticky = tk.W)
        rowind += 1
        
        self.sweepStepsBox = tk.Entry(self._elecFrame)
        label = tk.Label(self._elecFrame, text = "Voltage Sweep Steps: ")
        label.grid(row = rowind, sticky = tk.W)
        self.sweepStepsBox.grid(row = rowind, column = 1, sticky = tk.W)
        rowind += 1
        
        
        self.goBut = tk.Button(self._elecFrame, text = "Save")
        self.goBut.bind("<Button-1>", self.saveElec())
        self.goBut.grid(row= rowind)
        
        """
        spectrometer frame
        """
        self._specFrame = tk.Frame(self.masterFrame, relief = tk.RIDGE, bd = 2)
        self._specFrame.grid(row=2, column = 0, sticky=tk.N)
        label = tk.Label(self._specFrame, text = "Jaz Spectrometer", font = uline)
        label.grid(sticky=tk.N)
        
        """
        TLS frame
        """
        self.tlsFrame = tk.Frame(self.masterFrame, relief = tk.RIDGE, bd = 2)
        self.tlsFrame.grid(row=3, column = 0, sticky=tk.N)
        tlsLab = tk.Label(self.tlsFrame, text = "Newport TLS", font = uline)
        tlsLab.grid(sticky = tk.N)
        
        """ Button to run the test """
        runBut = tk.Button(self.masterFrame, text = "Run Test", command = self.runTest())
        runBut.grid(row = 4, column = 0)
        
        
    def run(self):
        self.root.mainloop()
    
    """ Gui functions """
    def saveElec(self, event):
        print(event)
        print(self.maxCurrBox.get())
        
    def enableSweep(self):
        if self.sweepBool.get():
            self.endVoltBox.configure(state="normal")
            self.sweepStepsBox.configure(state="normal")
        else:
            self.endVoltBox.configure(state="disabled")
            self.sweepStepsBox.configure(state="disabled")
            
    def runTest(self):
        print("running!")
        print(self.testVars)
    
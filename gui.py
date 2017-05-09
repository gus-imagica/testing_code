# -*- coding: utf-8 -*-
"""
Created on Fri May  5 12:05:30 2017

@author: Gus
"""

import os
import tkinter as tk
from tkinter import font
root = tk.Tk()

""" Gui functions """
def saveElec(event):
    print(event)
    print(maxCurrBox.get())
    
def enableSweep():
    if sweepBool.get():
        endVoltBox.configure(state="normal")
        sweepStepsBox.configure(state="normal")
    else:
        endVoltBox.configure(state="disabled")
        sweepStepsBox.configure(state="disabled")
        
def runTest(testVars):
    print("running!")
    print(testVars)
    
# font to use for titles
uline = font.Font(underline = True)

# test variables
maxCurr = 0
startVolt = 0
endVolt = 0
sweepSteps = 0
saveLoc = os.pardir
testVars = [maxCurr, startVolt, endVolt, sweepSteps, saveLoc]

## top frame
masterFrame = tk.Frame(root, relief = tk.GROOVE, bd = 4)
masterFrame.grid(row=0)
root.title("Imagica Test Suite")
titleLab = tk.Label(masterFrame, text = "All Devices", justify = 'center', font = uline)
titleLab.grid(sticky=tk.N)

"""
electrometer frame
"""
rowind = 0
elecFrame = tk.Frame(masterFrame, relief = tk.RIDGE, bd = 2)
elecFrame.grid(row=1, column = 0, sticky=tk.N)
elecLab = tk.Label(elecFrame, text = "Keysight Electrometer", font = uline)
elecLab.grid(row = rowind, column = 0)
rowind += 1

# the maximum current defines the range
maxCurrBox = tk.Entry(elecFrame)
label = tk.Label(elecFrame, text = "Maximum Current Readout (ex. 1E-10): ")
label.grid(row = rowind, sticky = tk.W)
maxCurrBox.grid(row = rowind, column = 1, sticky = tk.W)
rowind += 1

# Will we be sweeping or outputting a constant voltage?
sweepBool = tk.IntVar()
sweepSwitch = tk.Checkbutton(elecFrame, text = "Voltage sweep?", variable = sweepBool, command = enableSweep)
sweepSwitch.select()
sweepSwitch.grid(row=rowind)
rowind += 1

startVoltBox = tk.Entry(elecFrame)
label = tk.Label(elecFrame, text = "Start Output Voltage (V): ")
label.grid(row = rowind, sticky = tk.W)
startVoltBox.grid(row = rowind, column = 1, sticky = tk.W)
rowind += 1

endVoltBox = tk.Entry(elecFrame)
label = tk.Label(elecFrame, text = "End Output Voltage (V): ")
label.grid(row = rowind, sticky = tk.W)
endVoltBox.grid(row = rowind, column = 1, sticky = tk.W)
rowind += 1

sweepStepsBox = tk.Entry(elecFrame)
label = tk.Label(elecFrame, text = "Voltage Sweep Steps: ")
label.grid(row = rowind, sticky = tk.W)
sweepStepsBox.grid(row = rowind, column = 1, sticky = tk.W)
rowind += 1


goBut = tk.Button(elecFrame, text = "Save")
goBut.bind("<Button-1>", saveElec)
goBut.grid(row= rowind)

"""
spectrometer frame
"""
specFrame = tk.Frame(masterFrame, relief = tk.RIDGE, bd = 2)
specFrame.grid(row=2, column = 0, sticky=tk.N)
specLab = tk.Label(specFrame, text = "Jaz Spectrometer", font = uline)
specLab.grid(sticky=tk.N)

"""
TLS frame
"""
tlsFrame = tk.Frame(masterFrame, relief = tk.RIDGE, bd = 2)
tlsFrame.grid(row=3, column = 0, sticky=tk.N)
tlsLab = tk.Label(tlsFrame, text = "Newport TLS", font = uline)
tlsLab.grid(sticky = tk.N)

""" Button to run the test """
runBut = tk.Button(masterFrame, text = "Run Test", command = runTest(testVars))
runBut.grid(row = 4, column = 0)

root.mainloop()
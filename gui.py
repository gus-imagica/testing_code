# -*- coding: utf-8 -*-
"""
Created on Fri May  5 12:05:30 2017

@author: Gus
"""

import tkinter as tk
from tkinter import font
root = tk.Tk()

def saveElec(event):
    print(event)
    print(maxCurr.get())
    
def enableSweep():
    if sweep.get():
        endVolt.configure(state="normal")
        voltSteps.configure(state="normal")
    else:
        endVolt.configure(state="disabled")
        voltSteps.configure(state="disabled")
    

uline = font.Font(underline = True)

## top frame
masterFrame = tk.Frame(root, relief = tk.GROOVE, bd = 4)
masterFrame.grid(row=0)
root.title("Imagica Test Suite")
titleLab = tk.Label(masterFrame, text = "All Devices", justify = 'center', font = uline)
titleLab.grid(sticky=tk.N)

## electrometer frame
rowind = 0
elecFrame = tk.Frame(masterFrame, relief = tk.RIDGE, bd = 2)
elecFrame.grid(row=1, column = 0, sticky=tk.N)
elecLab = tk.Label(elecFrame, text = "Keysight Electrometer", font = uline)
elecLab.grid(row = rowind, column = 0)
rowind += 1

maxCurr = tk.Entry(elecFrame)
label = tk.Label(elecFrame, text = "Maximum Current Readout (ex. 1E-10): ")
label.grid(row = rowind, sticky = tk.W)
maxCurr.grid(row = rowind, column = 1, sticky = tk.W)
rowind += 1

sweep = tk.IntVar()
sweepSwitch = tk.Checkbutton(elecFrame, text = "Voltage sweep?", variable = sweep, command = enableSweep)
sweepSwitch.select()
sweepSwitch.grid(row=rowind)
rowind += 1

startVolt = tk.Entry(elecFrame)
label = tk.Label(elecFrame, text = "Start Output Voltage (V): ")
label.grid(row = rowind, sticky = tk.W)
startVolt.grid(row = rowind, column = 1, sticky = tk.W)
rowind += 1

endVolt = tk.Entry(elecFrame)
label = tk.Label(elecFrame, text = "End Output Voltage (V): ")
label.grid(row = rowind, sticky = tk.W)
endVolt.grid(row = rowind, column = 1, sticky = tk.W)
rowind += 1

voltSteps = tk.Entry(elecFrame)
label = tk.Label(elecFrame, text = "Voltage Sweep Steps: ")
label.grid(row = rowind, sticky = tk.W)
voltSteps.grid(row = rowind, column = 1, sticky = tk.W)
rowind += 1


goBut = tk.Button(elecFrame, text = "Save")
goBut.bind("<Button-1>", saveElec)
goBut.grid(row= rowind)

## spectrometer frame
specFrame = tk.Frame(masterFrame, relief = tk.RIDGE, bd = 2)
specFrame.grid(row=2, column = 0, sticky=tk.N)
specLab = tk.Label(specFrame, text = "Jaz Spectrometer", font = uline)
specLab.grid(sticky=tk.N)

## TLS frame
tlsFrame = tk.Frame(masterFrame, relief = tk.RIDGE, bd = 2)
tlsFrame.grid(row=3, column = 0, sticky=tk.N)
tlsLab = tk.Label(tlsFrame, text = "Newport TLS", font = uline)
tlsLab.grid(sticky = tk.N)

root.mainloop()
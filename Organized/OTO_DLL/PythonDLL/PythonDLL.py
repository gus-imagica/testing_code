import sys
import struct
from array import *
from ctypes import *
from matplotlib import pyplot as plt
import numpy as np
#OTO USB2.0 spectrameter's VID & PID
VID = 1592
PID = 2732
OTOdll = CDLL("UserApplication.dll")

""" THIS CRASHES PYTHON """
#intNumber = c_int(0)
#OTOdll.UAI_SpectrometerGetDeviceList(byref(intNumber),None)
#print intNumber.value
## intList = create_string_buffer(sizeof(c_int*intNumber.value*2))
#intList = create_string_buffer("0000000000000000", sizeof(c_int*intNumber.value*2))
#OTOdll.UAI_SpectrometerGetDeviceList(byref(intNumber),byref(intList))
#i = 0
#print struct.unpack('f', intList[i]+ intList[i+1]+ intList[i+2]+ intList[i+3])
#i = 4
#print struct.unpack('f', intList[i]+ intList[i+1]+ intList[i+2]+ intList[i+3])
#i = 8
#print struct.unpack('f', intList[i]+ intList[i+1]+ intList[i+2]+ intList[i+3])
#i = 12
#print struct.unpack('f', intList[i]+ intList[i+1]+ intList[i+2]+ intList[i+3])
##print intList.value

#Check how many device is connected with PC.
intDeviceAmount = c_int(0)
OTOdll.UAI_SpectrometerGetDeviceAmount(VID,PID,byref(intDeviceAmount))
print "Device amount:"
print intDeviceAmount.value

if intDeviceAmount.value < 1:
    print "NO device connecting"
    exit()

#Open Device
DeviceHandle = c_int(0)
OTOdll.UAI_SpectrometerOpen(0,byref(DeviceHandle),VID,PID)
print "Device handle:"
print DeviceHandle.value

#Get Framesize
intFramesize = c_int(0)
OTOdll.UAI_SpectromoduleGetFrameSize(DeviceHandle,byref(intFramesize))
print "Device framesize:"
print intFramesize.value

if intFramesize.value ==0:
     print "Framesize is invalid"
     exit()

#Get Module name
charModulename = create_string_buffer("0000000000000000", 16)
OTOdll.UAI_SpectrometerGetModelName(DeviceHandle,byref(charModulename))
print "Module name:"
print repr(charModulename.value)

#Get Serial number
#emp = array(
charSerialnumber = create_string_buffer("0000000000000000", 16)
charSerialnumber = create_string_buffer(16)
OTOdll.UAI_SpectrometerGetSerialNumber(DeviceHandle,byref(charSerialnumber))
print "Serial number:"
print repr(charSerialnumber.value)


#Init array
TempLambda = create_string_buffer(sizeof(c_float*intFramesize.value))
TempIntensity = create_string_buffer(sizeof(c_float*intFramesize.value))

#Get wavelength
OTOdll.UAI_SpectrometerWavelengthAcquire(DeviceHandle,byref(TempLambda))

Lambda = []
for i in xrange(0,sizeof(c_float*intFramesize.value),+4):
    Lambda.append(struct.unpack('f', TempLambda[i]+ TempLambda[i+1]+ TempLambda[i+2]+ TempLambda[i+3]))

Intensity = []

for i in xrange(1,10,+1):
    #Get Intensity
    OTOdll.UAI_SpectrometerDataOneshot(DeviceHandle,i*1000,byref(TempIntensity),1)

    #Do Background
    OTOdll.UAI_BackgroundRemove(DeviceHandle,i*1000,byref(TempIntensity))

    #Do Linearity
    OTOdll.UAI_LinearityCorrection(DeviceHandle,intFramesize,byref(TempIntensity))

    Intensity = []
    for i in xrange(0,sizeof(c_float*intFramesize.value),+4):
        Intensity.append(struct.unpack('f', TempIntensity[i]+ TempIntensity[i+1]+ TempIntensity[i+2]+ TempIntensity[i+3]))
    print Lambda[0] + Intensity[0]
    
TempIntensity = create_string_buffer(sizeof(c_float*intFramesize.value))

Intensity = []
OTOdll.UAI_SpectrometerDataAcquire(DeviceHandle,10000,byref(TempIntensity),1)
for i in xrange(0,sizeof(c_float*intFramesize.value),+4):
    Intensity.append(struct.unpack('f', TempIntensity[i]+ TempIntensity[i+1]+ TempIntensity[i+2]+ TempIntensity[i+3]))
intens = np.array(Intensity)
plt.plot(intens)
plt.show()


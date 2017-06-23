import sys
import struct
from array import *
from ctypes import *
#OTO USB2.0 spectrameter's VID & PID
VID = 1592
PID = 2732
dll_path = r"UserApplication"
OTOdll = CDLL(dll_path)

#Check how many device is connected with PC.
intDeviceAmount = c_int(0)
OTOdll.UAI_SpectrometerGetDeviceAmount(VID,PID,byref(intDeviceAmount))
print("Device amount:")
print(intDeviceAmount.value)

if intDeviceAmount.value < 1:
    print("NO device connecting")
    exit()

#Open Device
DeviceHandle = c_int(0)
OTOdll.UAI_SpectrometerOpen(0,byref(DeviceHandle),VID,PID)
print("Device handle:")
print(DeviceHandle.value)

#Get Framesize
intFrameSize = c_short(0)
print(DeviceHandle)
print(intFrameSize)
OTOdll.UAI_SpectromoduleGetFrameSize(DeviceHandle,byref(intFrameSize))
print("Device framesize:")
print(intFrameSize.value)

if intFrameSize.value ==0:
     print("Framesize is invalid")
     exit()

#Get Module name
charModulename = create_string_buffer("0000000000000000".encode(ascii), 16)
OTOdll.UAI_SpectrometerGetModelName(DeviceHandle,byref(charModulename))
print("Module name:")
print(repr(charModulename.value))

#Get Serial number
#emp = array(
charSerialnumber = create_string_buffer("0000000000000000", 16)
OTOdll.UAI_SpectrometerGetSerialNumber(DeviceHandle,byref(charSerialnumber))
print("Serial number:")
print(repr(charSerialnumber.value))


#Init array
TempLambda = create_string_buffer(sizeof(c_float*intFrameSize.value))
TempIntensity = create_string_buffer(sizeof(c_float*intFrameSize.value))

#Get wavelength
OTOdll.UAI_SpectrometerWavelengthAcquire(DeviceHandle,byref(TempLambda))

Lambda = []
for i in range(0,sizeof(c_float*intFrameSize.value),+4):
    Lambda.append(struct.unpack('f', TempLambda[i]+ TempLambda[i+1]+ TempLambda[i+2]+ TempLambda[i+3]))

Intensity = []

for i in range(1,100,+1):
    #Get Intensity
    OTOdll.UAI_SpectrometerDataOneshot(DeviceHandle,i*1000,byref(TempIntensity),1)

    #Do Background
    OTOdll.UAI_BackgroundRemove(DeviceHandle,i*1000,byref(TempIntensity))

    #Do Linearity
    OTOdll.UAI_LinearityCorrection(DeviceHandle,intFrameSize,byref(TempIntensity))

    Intensity = []
    for i in range(0,sizeof(c_float*intFrameSize.value),+4):
        Intensity.append(struct.unpack('f', TempIntensity[i]+ TempIntensity[i+1]+ TempIntensity[i+2]+ TempIntensity[i+3]))
    print(Lambda[0] + Intensity[0])
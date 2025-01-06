

"""
Heavily inspired from https://gist.github.com/rwb27/c728016f0f95f977034c26760ff9b6b7
"""
"""
This is a Python 3 wrapper for the Thorlabs KPZ101 KCube Piezo controller.
It relies on the Thorlabs Kinesis API (so you should copy in, or add to your
Python path, the Kinesis DLLs).  The easiest way to copy the right DLLs is
to use the "DLL copying utility" which is probably located in 
c:/Program Files/Thorlabs/Kinesis
I also use the excellent ``pythonnet`` package to get access to the .NET API.
This is by far the least painful way to get Kinesis to work nicely as it 
avoids the low-level faffing about.
"""
import clr # provided by pythonnet, .NET interface layer
import sys
import time

# this is seriously nasty.  Points for a better way of fixing this!
sys.path.append(r"C:/Program Files/Thorlabs/Kinesis")

# NB the 
clr.AddReference("Thorlabs.MotionControl.KCube.PiezoCLI")
clr.AddReference("Thorlabs.MotionControl.DeviceManagerCLI")
clr.AddReference("System")

from Thorlabs.MotionControl.KCube.PiezoCLI import  KCubePiezo
from Thorlabs.MotionControl.DeviceManagerCLI import DeviceManagerCLI
from System import Decimal

def list_devices():
    """Return a list of Kinesis serial numbers"""
    DeviceManagerCLI.BuildDeviceList()
    return DeviceManagerCLI.GetDeviceList()

_ser = list_devices()[0]
#>> 29250314 correct serial number
piezo = KCubePiezo.CreateKCubePiezo(_ser)
piezo.Connect(_ser)
#>> KCube screen buzz
piezo.EnableDevice()
#>> Device is enabled, it shows on the screen
print(Decimal.ToDouble(piezo.GetMaxOutputVoltage()))
#>> prints 75.O
print(Decimal.ToDouble(piezo.GetOutputVoltage()))
#>> prints 0.0
voltage = 0.5
piezo.SetOutputVoltage(Decimal(voltage))
#>> no change on the screen
print(Decimal.ToDouble(piezo.GetOutputVoltage()))
#>> prints 0.0
piezo.DisableDevice()
#>> shows disabled on the screen

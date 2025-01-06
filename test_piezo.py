
"""
from KPZ101 import *
cube = KPZ101()
sn = 29250314
sn2 = c_char_p(bytes(str(sn), 'utf-8'))
#cube.open_stage(sn)
cube.piezo.PCC_Open(sn)

from pylabinstrument.thorlabs.motion.KCubeDCServo import *
import pylabinstrument.thorlabs.motion.tools._KCubeDCServo as K

import ctypes
from ctypes import (
    Structure,
    cdll,
    c_bool,
    c_short,
    c_int,
    c_uint,
    c_int16,
    c_int32,
    c_char,
    c_byte,
    c_long,
    c_float,
    c_double,
    POINTER,
    CFUNCTYPE,
    c_ushort,
    c_ulong,
    c_char_p,
    byref,
    pointer
)

c_word = c_ushort
c_dword = c_ulong


def discover(typename='kdc'):
    '''
    Return a list of serial number of KDC101 devices connected to the computer.
    Inputs:
    typename -- a name of the device type to discover. For supported device, call .supportedDevices(). The default is 'kdc' because of this class is for.
    '''

    err_code = K.BuildDeviceList()
    if err_code==0:
        n = K.GetDeviceListSize()
        size = 512
        sbuffer = ctypes.create_string_buffer(b"",size)
        err_code = K.GetDeviceListExt(sbuffer, c_dword(size))
        if err_code==0:
            pbuffer = sbuffer.value
            serialList = pbuffer.decode('UTF-8').strip(',').split(',')
            return serialList
        else:
            raise Exception('Failed to get device list by type. Error code: {}.'.format(err_code))
    else:
        raise Exception('Failed to build device list. Error code: {}.'.format(err_code))

sn = discover()[0]
print(sn)
m = Motor(sn)
m.open()
print(m.getPosition())

#print(m.moveToPosition(0.2))
#print(m.getPosition())


#m.close()


import time
import numpy as np
from cubini.KPZ101 import KPZ101

# serial numbers of KPZ101 cubes
cuboids =  [29250314]

# connect to all modules
cubinis = []
for sn in cuboids:
    try:
        cubini = KPZ101(serial_number=sn)
        time.sleep(0.1)
        cubini.set_input_mode()
        cubinis.append(cubini)
        print('KPZ101 {} found.'.format(sn))
    except Exception as e:
        print(e)
        print('KPZ101 {} not found.'.format(sn))

# sequentially run a test sequence for each cube
for kpz in cubinis:
    kpz.set_max_voltage(150)
    kpz.enable_output()
    kpz.set_output_voltage(0)
    time.sleep(0.5)
    for v in np.linspace(0, 50, 50):
        kpz.set_output_voltage(v)
        time.sleep(0.1)
    kpz.set_output_voltage(0)
    kpz.disable_output()

"""
"""
This is a Python 3 wrapper for the Thorlabs BPC203 Benchtop Piezo controller.
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



class PiezoWrapper():
    def __init__(self, serial_number):
        self._ser = str(serial_number)
        DeviceManagerCLI.BuildDeviceList()
        self.piezo = KCubePiezo.CreateKCubePiezo(self._ser)
        self.channels = []
        self.connected = False

    def connect(self):
        """Initialise communications, populate channel list, etc."""
        assert not self.connected
        self.piezo.Connect(self._ser)
        self.connected = True
    
        self.piezo.WaitForSettingsInitialized(5000)
        self.piezo.StartPolling(250) # getting the voltage only works if you poll!
        time.sleep(0.5) # ThorLabs have this in their example...
        self.piezo.EnableDevice()
        # I don't know if the lines below are necessary or not - but removing them
        # may or may not work...
        time.sleep(0.5)
        info = self.piezo.GetDeviceInfo()
        print(info)
        max_v = Decimal.ToDouble(self.piezo.GetMaxOutputVoltage())
        print(max_v)

    def close(self):
        """Shut down communications"""
        if not self.connected:
            print(f"Not closing piezo device {self._ser}, it's not open!")
            return
        self.piezo.StopPolling()
        self.channels = []
        self.piezo.Disconnect(True)

    def __del__(self):
        try:
            if self.connected:
                self.close()
        except:
            print(f"Error closing communications on deletion of device {self._ser}")

    def set_voltage_source(self, ind):
        """Set the voltage source"""
        self.piezo.SetVoltageSource(ind)

    def set_output_voltages(self, v):
        """Set the output voltage"""
        self.piezo.SetOutputVoltage(Decimal(v))
    
    def get_output_voltages(self):
        """Retrieve the output voltages as a list of floating-point numbers"""
        return Decimal.ToDouble(self.piezo.GetOutputVoltage())

    output_voltages = property(get_output_voltages, set_output_voltages)


_ser = list_devices()[0]
pzw = PiezoWrapper(_ser)
pzw.connect()
pzw.set_voltage_source(0)
print(pzw.get_output_voltages())
pzw.set_output_voltages(10)
print(pzw.get_output_voltages())

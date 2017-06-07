from DriverVIP_Parent import DriverVIP

import clr
clr.AddReference("C:\Program Files\New Focus\New Focus Wavemeter Application\Samples\DeviceIOLib.dll")
clr.AddReference("C:\Program Files\New Focus\New Focus Wavemeter Application\Samples\CmdLibWM1210.dll")
#clr.AddReference("C:\Windows\Microsoft.NET\System.dll")
from Newport.DeviceIOLib import DeviceIOLib
from NewFocus.WavemeterApp import CmdLibWM1210
#from System.IO.Ports import SerialPort

import time

################################################################################
MICRO = 10**-6                                                        

################################################################################
class DriverWM1210(DriverVIP):
    """Use the imported modules to create a WM1210 driver instance and open
    a channel to the instrument associated with device_key
    """

    def __init__(self, instr_name):
        super(DriverWM1210, self).__init__(instr_name)

        print "(DriverWM1210.__init__("+instr_name+"))"                        ### instr_name is not really used in this driver yet

        try:
            self.Resource = self._get_CmdLibWM1210()
        except Exception as e:                                                ### Write down the names of particular Exceptions once they arise
            print "!!! (DriverWM1210, "+instr_name+", ._get_CmdLibWM1210), Exception:"
            print e
        ### Use GetFirstDeviceKey instead, for when the device key is not fixed or known:
        #self._device_key = self.Resource.GetFirstDeviceKey()

        try:
            B_opened = self.Resource.Open(self._local['S_device_key'])
            if not B_opened:
                print "! (DriverWM1210, "+instr_name+", "+self._local['S_device_key']+") Opening unsuccessful."
        except Exception as e:                                                ### Write down the names of particular Exceptions once they arise
            print "!!! (DriverWM1210, "+instr_name+", "+self._local['S_device_key']+", .Open), Exception:"
            print e

    def get_data(self, steps=1):
        ### In case this is re-written as a get_trace method for the VIP, steps must go into _local.
        ### In case this is re-written as a get_trace method for the VIP, four values must be returned.

        R_sleep_time  = float(self._local['R_sleep_time'])
        R_dWavelength = float(self._local['R_dWavelength'])
        R_dPower      = float(self._local['R_dPower'])

        print "\nGoing into measurement loop..."
        ps, ws = [], []
        for _ in range(steps):
            p = self.Resource.MeasurePower(self._local['S_device_key'], R_dPower)
            w = self.Resource.MeasureWavelength(self._local['S_device_key'], R_dWavelength)
            ### Note: MeasurePower and MeasureWavelength return a pair of type (Bool, Float).
            p = p[1]
            w = w[1]
            ps.append(p / MICRO)
            ws.append(w)
            print "p[1]: {}".format(p)
            print "w[1]: {}".format(w)
            time.sleep(R_sleep_time)

        ts = [(stp * R_sleep_time) for stp in range(steps)]

        print "/(DriverWM1210.get_data)"

        return ts, ps, ws

    def _get_CmdLibWM1210(self):
        m_DeviceIOLib = DeviceIOLib(True)                 ### Instantiate the the library objects with logging
        m_DeviceIOLib.SetUSBProductID(0x100F)             ### Only discover WM-1210 Wavemeter Controllers on the USB port
        m_DeviceIOLib.SetSerialDiscoveryRate(2**31/1000)  ### Set the serial port discovery rate to the max
        m_DeviceIOLib.DiscoverDevices(0x3, 3000)          ### Discover USB and serial devices (USB = 1 + Serial = 2) and delay
        return CmdLibWM1210(m_DeviceIOLib)

    def _call_deeper_methods(self):
        print
        print ".GetFirstDeviceKey:"
        print self.Resource.GetFirstDeviceKey()
        print ".GetDeviceCount:"
        print self.Resource.GetDeviceCount()
        print ".GetPortType:"
        print self.Resource.GetPortType(self._local['S_device_key'])
        print ".GetDisplayName:"
        print self.Resource.GetDisplayName(self._local['S_device_key'])
        #print ".Close:"
        #print self.Resource.Close(self._local['S_device_key'])



####################################################################################### Methods not used in this file

#m_SerialPort = SerialPort()

#m_DeviceIOLib.SetSerialPortDefaultSettings(19200, m_SerialPort.Parity.None, 8, m_SerialPort.StopBits.One, m_SerialPort.Handshake.None, 500, 500, "\n")
#m_DeviceIOLib.Shutdown()

#self.Resource.SetNumAverages(strDeviceKey,self.Resource.NumAverages.Four)
#self.Resource.Close(strDeviceKey)

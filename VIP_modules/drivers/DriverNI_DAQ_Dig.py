import numpy as np
import time

##########

try:
    import instrumental
except ImportError as e:
    print "!!! (DriverNI_DAQ) package 'instrumental' couldn't be imported:\n"+str(e)

from xxx import TaskHandle as xxx_TaskHandle

from PyDAQmx import Task as PyDAQmx_Task
### https://pythonhosted.org/PyDAQmx/index.html
### BINDS TO
### http://digital.ni.com/public.nsf/ad0f282819902a1986256f79005462b1/b77ebfb849f162cd86256f150048dbb1/$FILE/NIDAQmx.h

##########

import dictionaries.constants as cs
import dictionaries.hardware as hardware

from DriverVIP_Parent import DriverVIP



################################################################################




################################################################################
class DriverNI_DAQ(DriverVIP):
    def __init__(self, instr_name):
        super(DriverNI_DAQ, self).__init__(instr_name)

        print "(DriverVISA.__init__('{0}'))".format(instr_name)
        ### Note: instr_name is not really used in this driver yet

        try:
            self.Resource = instrumental.instrument('NIDAQ')
        except:
            print "!!! (DriverNI_DAQ) 'instrumental.instrument('NIDAQ')' couldn't be called."

        self.physicalChannel = "Dev1/ai2"
        self.taskHandle = xxx_TaskHandle(0)

    def send_pulse(self, settings, B_zeros, B_finite):                          ### TODO: Reweite this using the _local_data
        """"Create a PyDAQmx packege task instance to create a channel to the
        device and then activate the pins as specified in the session.
        Use the boolans B_zeros or B_finite to refer to the turned-off default
        pin setting and/or to turn them off after the time specified in the
        session
        """
        task = PyDAQmx_Task()

        self.__open_channel(task, settings)

        task.StartTask()

        if B_zeros:
            pin_vals = ZEROS
        else:
            pin_vals = [int(settings['B_pin_'+k]) for k in hardware.range_NI_pins]
        self.__write_to_pins(task, pin_vals)

        if B_finite:
            duration = cs.MILLI * float(settings['R_pulse_time'])
            time.sleep(duration)
            self.__write_to_pins(task, ZEROS)

        task.StopTask()

        device  = settings['N_device']
        port    = settings['N_port']
        message_scheme = "* (DriverNI_pulse) send_pulse: \n | Pulse | Device | Port | \n | {0} | {1} | {2} | "
        message = message_scheme.format(str(pin_vals), device, port)
        print message

        return message

    def __open_channel(self, pyDAQmx_Task, settings):                           ### TODO: Reweite this using the _local_data
        """Create an address string in the form that the PyDAQmx package wants
        it, e.g. '/dev1/port0/line0:7'. Here the device- and port-number are
        to be varied and the line range is always fixed.
        Then connect to the device by using the PyDAQmx CreateDOChan method:
            METHOD ARGUMENTS IN THE C ORIGINAL:
                TaskHandle (self) taskHandle
                const char        lines[]
                const char        nameToAssignToLines[]
                int32             (PyDAQmx.DAQmx_Val_ChanPerLine is 0 and PyDAQmx.DAQmx_Val_ChanForAllLines is 1)
        """
        device  = settings['N_device']
        port    = settings['N_port']
        line    = "0"+":"+str(int(settings['N_pins']) - 1)
        SEP     = "/"
        address = SEP+"dev"+device+SEP+"port"+port+SEP+"line"+line

        pyDAQmx_Task.CreateDOChan(address, "", 1)

    def __write_to_pins(self, pyDAQmx_Task, pin_vals):
        """The specifciation of pins to be activated is a list of binaries. Pin values:
        0 ... OFF
        1 ... ON
        Note that the PyDAQmx method 'WriteDigitalLines' first expects you to
        translate the list into a particular numpy string.
        Then pass this list to the instrument using the PyDAQmx CreateDOChan method:
            METHOD ARGUMENTS IN THE C ORIGINAL:
                TaskHandle (self) taskHandle
                int32             numSampsPerChan
                bool32            autoStart
                float64           timeout
                bool32            dataLayout (PyDAQmx.DAQmx_Val_GroupByChannel is 0 and DAQmx_Val_GroupByScanNumber is 1)
                uInt8             writeArray[]
                int32             *sampsPerChanWritten
                bool32            *reserved          lineGrouping
        """
        np_pin_vals = np.array(pin_vals, dtype=np.uint8)

        pyDAQmx_Task.WriteDigitalLines(1, 1, 10.0, 0, np_pin_vals, None, None)

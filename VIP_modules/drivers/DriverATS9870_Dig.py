# -*- coding: utf-8 -*-
from __future__ import division

import ctypes as ctypes
import numpy as np
from time import clock as time_clock

import dictionaries.menus as menus

import external.atsapi as ats

from DriverVIP_Parent import DriverVIP

################################################################################
class DriverATS9870(DriverVIP):
    """TODO: Function of driver description
    """
    def __init__(self, instr_name):
        """Create a attribute handle for the Board using the Alzatech file (ats)
        """
        super(DriverATS9870, self).__init__(instr_name)

        print "(DriverATS9870.__init__("+instr_name+"))"
        ### Note: instr_name is not really used in this driver yet

        self.Resource = ats.Board() # DEFAULT ARGUMENTS: systemId=1, boardId=1

    ########## ########## ########## ########## ########## ########## ##########

    def adopt_settings(self, settings):
        """Configure the board for acquisition
        *** Clock:
        Select clock parameters as required to generate the sample rate.
        For example:
        - To use on-board oscillators as a timebase select clock source
            INTERNAL_CLOCK and specify the sample rate (e.g. SAMPLE_RATE_100MSPS)
        - or select clock source FAST_EXTERNAL_CLOCK, sample rate
            SAMPLE_RATE_USER_DEF, and connect a 100MHz signal to the
            EXT CLK BNC connector
        - or select clock source EXTERNAL_CLOCK_10MHz_REF, sample rate
            1e9, and connect a 10MHz signal to the EXT CLK BNC connector
        *** Trigger:
        Select trigger inputs and levels as required.
        Currently this is set up to use only one trigger engine. To add the
        option of a second engine, all arguments of the method below have to be
        made dependent on given input parameters.
        The trigger level is specified as an unsigned 8-bit code that represents a
        fraction of the trigger level set in the method 'setExternalTrigger':
        0 represents the negative limit, 128 the 0 level, and 255 the positive limit.
        For example, if the trigger level is set to 5V,
        then 0 represents a -5V trigger level, 128 represents a 0V trigger level,
        and 255 represents +5V trigger level.
        After choosing trigger inputs and levels,
        a possible trigger delay can be applied.
        Finally a trigger timout can be set.
        The board will wait for a for this amount of time for a
        trigger event.  If a trigger event does not arrive, then the
        board will automatically trigger. Set the trigger timeout value
        to 0 to force the board to wait forever for a trigger event.
        """
        ### Update the full settings dict (strings)
        self._local.update(settings)
        print 30*"x"+" (.adopt_settings) called"

        ### Translate the settings dict (strings) to the associated ats values
        ats_settings = {k : menus.ATS9870[k][self._local[k]] for k in menus.ATS9870.keys()}

        samplesPerSec = 1e9
        self.Resource.setCaptureClock(ats.EXTERNAL_CLOCK_10MHz_REF,
                            samplesPerSec,
                            ats.CLOCK_EDGE_RISING,
                            ats_settings['F_decimation']) ###KEY

        ### Select channel A input parameters as required.
        self.Resource.inputControl(ats.CHANNEL_A,
                        ats_settings['F_channelA_coupling'], ###KEY
                        ats_settings['F_channelA_range'], ###KEY
                        ats.IMPEDANCE_50_OHM)

        ### Select channel A bandwidth limit as required.
        self.Resource.setBWLimit(ats.CHANNEL_A, 0)


        ### Select channel B input parameters as required.
        self.Resource.inputControl(ats.CHANNEL_B,
                        ats_settings['F_channelB_coupling'],
                        ats_settings['F_channelB_range'],
                        ats.IMPEDANCE_50_OHM)

        ### Select channel B bandwidth limit as required.
        self.Resource.setBWLimit(ats.CHANNEL_B, 0)

        ### Select external trigger parameters as required.
        self.Resource.setExternalTrigger(ats.DC_COUPLING, ats.ETR_5V)
        self.Resource.setTriggerOperation(ats.TRIG_ENGINE_OP_J,
                                ats.TRIG_ENGINE_J,
                                ats_settings['F_trigger_source_1'],
                                ats_settings['F_trigger_edge_1'],
                                int(self._local['N_trigger_level_1']),
                                ats.TRIG_ENGINE_K,
                                ats.TRIG_DISABLE,
                                ats.TRIGGER_SLOPE_POSITIVE,
                                128)

        ### Set trigger delay as required. Needs to be multiple of 16.
        triggerDelay_samples = 16 * int(self._local['N_trigger_delay'])
        self.Resource.setTriggerDelay(triggerDelay_samples)

        triggerTimeout_sec =  1 #Now set to 1 s + triggerDelay
        triggerTimeout_clocks = int(triggerTimeout_sec / 10e-6 + 0.5)
        self.Resource.setTriggerTimeOut(triggerTimeout_clocks)

        ### Configure AUX I/O connector as required
        self.Resource.configureAuxIO(ats.AUX_OUT_TRIGGER, 0)

        message = "/(DriverATS9870, adopt_settings):\nConfiguration completed!"
        return message

    ########## ########## ########## ########## ########## ########## ##########
    def get_trace(self):
        """Conduct the data acquisation.
        *** BUFFER ALLOCATION:
        AlazarTech digitizers use direct memory access (DMA) to transfer
        data from digitizers to the computer's main memory. The class 'DMABuffer'
        abstracts a memory buffer on the host, and ensures that all the
        requirements for DMA transfers are met.
        *** ARGUMENTS:
        c_sample_type (ctypes type): The datatype of the buffer to create.
        size_bytes (int): The size of the buffer to allocate, in bytes.
        The current acquisation mode uses AutoDMA. This allows a board to capture
        sample data to on-board dual-port memory while – at the same time –
        transferring sample data from the on-board memory to a buffer in
        host memory. Data acquisition and data transfer are done in parallel, so
        trigger events that occur while the board is transferring data will
        not be missed.
        If an application is unable to supply buffers as fast a board fills them,
        the board will run out of buffers into which it can transfer sample data.
        The board can continue to acquire data until it fills is on-board memory,
        but then it will abort the acquisition and report a buffer overflow error.
        The minimum number of buffers to be allocated for dual-port acquisition is
        two. However, due to the reasons stated above, it is recommended that an
        application supply three or more buffers to a board.
        This allows some tolerance for operating system latencies.
        """
        ### No pre-trigger samples in NPT mode available
        preTriggerSamples = 0
        postTriggerSamples = int(self._local['N_sweep_points']) ### (Multpile of 64!)

        ### Select the number of records per acquisition
        #recordsPerAcquisition = 100000  ###TODO

        ### Select the number of records per DMA buffer.
        recordsPerBuffer = int(self._local['N_records_per_buffer'])

        ### Select the number of buffers per acquisition.
        buffersPerAcquisition = int(self._local['N_buffers_per_acquisition'])

        ### Select the active channels.
        k = 'F_use_channel'
        channels = menus.ATS9870[k][self._local[k]]

        channelCount = 0
        for c in ats.channels:
            channelCount += (c & channels == c)

        ### Compute the number of bytes per record and per buffer

        ### Returns on-board memory size in samples per channel and number of bits per sample
        memorySize_samples, bitsPerSample = self.Resource.getChannelInfo()
        ### Turns bits per sample into bytes per sample
        bytesPerSample = (bitsPerSample.value + 7) // 8
        ### Number of samples per record
        samplesPerRecord = preTriggerSamples + postTriggerSamples
        ### Number of bytes per record
        bytesPerRecord = bytesPerSample * samplesPerRecord
        ### Number of bytes per buffer
        bytesPerBuffer = bytesPerRecord * recordsPerBuffer * channelCount

        ### Select number of DMA buffers to allocate
        bufferCount = 4 ### (*)
        bufferList = [[] for _ in range(channelCount)]

        ### Allocate DMA buffers
        sample_type = ctypes.c_uint8
        if bytesPerSample > 8:
            sample_type = ctypes.c_uint16
        buffers = []
        for _ in range(bufferCount):
            buffers.append(ats.DMABuffer(sample_type, bytesPerBuffer))

        ### Set the record size
        self.Resource.setRecordSize(preTriggerSamples, postTriggerSamples)

        recordsPerAcquisition = recordsPerBuffer * buffersPerAcquisition
        ### Configure the board to make an NPT AutoDMA acquisition
        self.Resource.beforeAsyncRead(channels,
                            -preTriggerSamples,
                            samplesPerRecord,
                            recordsPerBuffer,
                            recordsPerAcquisition,
                            ats.ADMA_EXTERNAL_STARTCAPTURE | ats.ADMA_NPT)

        ### Post DMA buffers to board
        for buff in buffers:
            self.Resource.postAsyncBuffer(buff.addr, buff.size_bytes)

        ### Keep track of when acquisition started
        start = time_clock()
        try:
            self.Resource.startCapture() # Start the acquisition
            print("Capturing %d buffers. Press <enter> to abort" %
                buffersPerAcquisition)
            buffersCompleted = 0
            bytesTransferred = 0
            while (buffersCompleted < buffersPerAcquisition and not
                ats.enter_pressed()):
                ### Wait for the buffer at the head of the list of available
                ### buffers to be filled by the board.
                buff = buffers[buffersCompleted % len(buffers)]
                self.Resource.waitAsyncBufferComplete(buff.addr, timeout_ms=5000)
                buffersCompleted += 1
                bytesTransferred += buff.size_bytes
                """Process sample data in the buffer here. Data is available
                as a NumPy array at buff.buffer
                While you are processing this buffer, the board is already
                filling the next available buffer.
                You MUST finish processing this buffer and post it back to the
                board before the board fills all of its available DMA buffers
                and on-board memory.
                """
                ### Split Channel Readout
                channelSplit = np.split(buff.buffer, channelCount)

                ### Calculate each channel individually
                for chan in range(channelCount):
                    ### Calculate mean values
                    bufferSplit = np.split(channelSplit[chan], recordsPerBuffer)
                    bufferMean = np.mean(bufferSplit,0)

                    ### Append result to bufferList
                    bufferList[chan].append(bufferMean)

                ### Add the buffer to the end of the list of available buffers.
                self.Resource.postAsyncBuffer(buff.addr, buff.size_bytes)
        finally:
            self.Resource.abortAsyncRead()

        ### OPTIONAL: Display of total transfer time and performance information.
        transferTime_sec = time_clock() - start
        print("Capture completed in %f sec" % transferTime_sec)
        buffersPerSec = 0
        bytesPerSec   = 0
        recordsPerSec = 0
        if transferTime_sec > 0:
            buffersPerSec = buffersCompleted / transferTime_sec
            bytesPerSec = bytesTransferred / transferTime_sec
            recordsPerSec = recordsPerBuffer * buffersCompleted / transferTime_sec
        print("Captured %d buffers (%f buffers per sec)" %
            (buffersCompleted, buffersPerSec))
        print("Captured %d records (%f records per sec)" %
            (recordsPerBuffer * buffersCompleted, recordsPerSec))
        print("Transferred %d bytes (%f Gbytes per sec)" %
            (bytesTransferred, bytesPerSec/1e9))

        ### Calculate mean value of buffer data
        bufferListMean = np.mean(bufferList, 1)

        #### Conversion from 8-bit to volts & split into channels for the return
        codeZero        = (1 << (bitsPerSample.value - 1)) - 0.5
        codeRange       = (1 << (bitsPerSample.value - 1)) - 0.5
        channelRange    = [float(self._local[k]) for k in ['F_channelA_range', 'F_channelB_range']]
        #channelCoupling = [self._local[k] for k in ['F_channelA_coupling', 'F_channelB_coupling']]

        y_axis = [[], []]
        for chan in range(channelCount):
            y_axis[chan] = channelRange[chan] * (bufferListMean[chan] - codeZero) / codeRange

        ### make sure y_axis[0] and y_axis[1] have the same format when returned.
        if (channelCount != 2):
            y_axis[1] = y_axis[0]

        ### IQ transformation
        ## Definitions
        i = []
        q = []
        ## Constants
        omega = 2 * np.pi * int(self._local['R_intermediate_frequency']) * 1e6 * 1e-9
        
        ## Create x-Axis
        chx = np.array(range(0,postTriggerSamples*int(self._local['F_decimation']),int(self._local['F_decimation'])))
        
        for el in range(postTriggerSamples):
            t = chx[el]
            i = np.append(i,np.dot([ np.cos(omega*t), np.sin(omega*t)],[y_axis[0][el],y_axis[1][el]]))
            q = np.append(q,np.dot([-np.sin(omega*t), np.cos(omega*t)],[y_axis[0][el],y_axis[1][el]]))
            
        filter_freq = float(self._local['R_filter_frequency'])
        if filter_freq:
            import interface.auxiliary_functions as auxi
            mov_av_time = int(1/(filter_freq*10**-3))
            #ss_dict[index]['axis'] = auxi.custom_axis(start+mov_av_time/2, stop-mov_av_time/2, sweep_points-mov_av_time, axis_mode)
              
            i = auxi.running_mean(i,mov_av_time)
            q = auxi.running_mean(q,mov_av_time)
          
            print 'I and Q lengths'
            print len(i)
            print len(q)
        return i, q, None, None




################################################################################
if __name__ == "__main__":
    ### NOTE:
    ### If you get an import error when running this file as a script, you may
    ### have to run the VIP_main.py file once, so the Canopy session sees all
    ### module files.

    sk = 'ATS9870_1'

    ######################################## Play pretend:
    DRIVER_DICT = {sk : DriverATS9870
                  }

    INSTRUMENT_LIST = DRIVER_DICT.keys()

    class fake_VIP(object):
        def __init__(self):
            self.instruments = {k : None for k in INSTRUMENT_LIST}
        def bn_connect(self, instr_name):
            driver = DRIVER_DICT[instr_name]
            self.instruments[instr_name] = driver(instr_name)
        def bn_adopt_settings(self, settings_update):
            VIP.instruments[sk].adopt_settings(settings_update)

    ######################################## Script:
    VIP = fake_VIP()

    VIP.bn_connect(sk)
    VIP.bn_adopt_settings({})

    channelA_y, channelB_y, _, _ = VIP.instruments[sk].get_trace()
    #VIP.instruments[sk].plot(channelA_y, x_label="Time [ns]", y_label="Amplitude [V]")
    #VIP.instruments[sk].plot(channelB_y, x_label="Time [ns]", y_label="Amplitude [V]")

"""
ERASE AFTER IMPLEMENTATION
INPUT VALUES:
For full flexibility, all of the following values should be chosen before acquisation.
They are marked with a ###KEY comment within the file.

The list is structered in this way:
("VARIABLE", "TITLE", "DEFAULT VALUE", "SIGNIFICANCE", "POSSIBLE VALUES")
If "VARIABLE" is -- , then the values are direct arguments of methods.

Optional values to be included are marked with one star (*).
Values that are permanent in our experimental setup but could be made adjustable for future
use are marked with two stars (*)(*) (maybe ask Johannes if implementation is wanted)

Record Values:
   ("postTriggerSamples", "Samples", 1024, "Sets the number of samples per record.", "Any integer value. 1 sample equals to 1 ns recorded signal.)
   ("recordsPerBuffer", "Records per Buffer", 1000, "Sets the number of records in each buffer", "Any integer value between 1 and 1000.")
   ("buffersPerAcquisition", "Buffers per Acquisition", 100, "Sets the total number of buffers that will be transferred before the aquisition is ended.", "Any integer value above 1. The total acquisition time if no trigger signal is missed equals to about [Trigger period * recordsPerBuffer * Buffers per Acquisition"]. This value could be displayed on the bottom of the input panel to give an idea of how long the acquisition will take.)

First Trigger:
   ( -- , "Trigger Source 1", ats.TRIG_EXTERNAL, "Sets the trigger input channel", ats.TRIG_EXTERNAL/ats.TRIG_CHAN_A/ats.TRIG_DISABLE)
   ( -- , "Trigger Edge 1", "Choose between positive or negative slope of trigger signal to trigger the record" , ats.TRIGGER_SLOPE_POSITIVE/ats.TRIGGER_SLOPE_NEGATIVE)
   ( -- , "Trigger Level 1", 160, "Sets the trigger value. See comment in the text for explanation of the values.", "Integer between 0 and 255")
(*)("triggerTimeout_sec", "Timeout", 0, "Choose value for trigger timeout", "Any integer value. Unit is seconds.")

Channel Settings:
   ("channels", "ChA and ChB", ats.CHANNEL_B, "Enable/Disable channel A and B. Maybe as a tickbox.", ats.CHANNEL_B/ats.CHANNEL_A/ats.CHANNEL_B | ats.CHANNEL_A)
   ( -- , "ChA Coupling", ats.AC_COUPLING, "Choose between AC and DC coupling for channel 1", ats.AC_COUPLING/ats.DC_COUPLING )
   ( -- , "ChA Range", ats.INPUT_RANGE_PM_40_MV, "Choose range of channel A", "See atsapy.py for full list of possible commands")

   ( -- , "ChB Coupling", analogous to "ChA")
   ( -- , "ChB Range", analogous to "ChA")

Buffer Count:
(*)("bufferCount", "Number of Buffers", 4, "Number of allocated buffers" , "Integer from 2 to 10. Should be kept at 4.")

Second Trigger:
(*)( -- ,"Trigger Source 2", analogous to "trigger_source1")
(*)( -- , "Trigger Edge 2", analogous to "trigger_edge1")
(*)( -- , "Trigger Level 2", analogous to "trigger_level1"),
(*)( -- , "Trigger Operation", TRIG_ENGINE_OP_J, "Choose correct trigger engine operation. Engine 1, engine 2, enginge 1 and 2, engine 1 or 2...", "See atsapy.py for full list of possible commands")
(*)( -- , "Trigger Coupling",  ats.DC_COUPLING, "Choose between AC and DC coupling for the trigger signal", ats.AC_COUPLING/ats.DC_COUPLING )


Clock Source:
(*)(*)( -- , "Clock Source", ats.EXTERNAL_CLOCK_10MHz_REF, "Set clock source", ats.EXTERNAL_CLOCK_10MHz_REF/ats.INTERNAL_CLOCK)
(*)(*)( -- , "Clock Edge", ats.CLOCK_EDGE_RISING, "Choose between rising or falling clock edges", ats.CLOCK_EDGE_RISING/ats.CLOCK_EDGE_FALLING)
(*)(*)("samplesPerSec", "Sample Rate", 1e9, "Choose sample rate", "See atsapy.py for full list of possible commands")
Descriminator
Trigger Delay
"""

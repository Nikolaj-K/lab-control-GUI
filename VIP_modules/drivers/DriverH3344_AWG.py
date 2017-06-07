# -*- coding: utf-8 -*-
from DriverVIP_Parent import DriverVIP
import external.signadyne as sd

PART_NUMBER   = 'SD-PXE-AWG-H3344-2G'
SERIAL_NUMBER = '0VKHSVMF'

################################################################################
class DriverH3344(DriverVIP):
    def __init__(self, instr_name):
        super(DriverH3344, self).__init__(instr_name)
            
        try:
            self.Resource = sd.SD_AOU()
        except:
            print "!!! (DriverH3344.__init__("+instr_name+")):"
            print "Wasn't able to open resource."

        try:
            self.Resource.close() 
        except:
            print "! (DriverH3344.__init__("+instr_name+")):"
            print "Exceptions at (close)"
        
    def open_close(my_method):
        def wrapper(self, *args, **kwargs): 
            self.Resource.openWithSerialNumber(PART_NUMBER, SERIAL_NUMBER)
            my_method(self, *args, **kwargs)
            self.Resource.close()
        return wrapper

########## ########## ########## ########## 
    @open_close
    def query_ID(self):
        print self.Resource.getProductName()
        print self.Resource.getSerialNumber()
        print self.Resource.getChassis()
        print "/(query_ID)"

########## ########## ########## ########## 
    
#this function is useful but we need to re-write it so it doesn't ask for input   
    @open_close
    def set_dc_offset(self, ch, offset,bound = 0.2):

        self.Resource.channelWaveShape(ch, sd.SD_Waveshapes.AOU_DC)

        val = offset
        if val > bound: 
            val = bound 
        elif (val < -bound): 
            val = -bound
        self.Resource.channelOffset(ch, val) ### (has a return value, which I don't understand yet)
        
        
    @open_close
    def set_phase(self, ch, phase):

        self.Resource.channelWaveShape(ch, sd.SD_Waveshapes.AOU_SINUSOIDAL)
        self.Resource.channelPhase(ch,phase)
        
    @open_close
    def set_amplitude(self, ch, amp,bound = 0.5):

        self.Resource.channelWaveShape(ch, sd.SD_Waveshapes.AOU_SINUSOIDAL)

        val = amp
        if val > bound: 
            val = bound 
        elif (val < -bound): 
            val = -bound
        self.Resource.channelAmplitude(ch, val) ### (has a return value, which I don't understand yet)

#FUNCTION THAT NEEDS TO WORK, should also include offset
    @open_close
    def waveform_from_file(self, settings):
        self.adopt_settings(settings)
        use_channels       = [ch for ch in range(4) if (self._local['B_channel_'+str(ch)]=='ON')]
        print 'use_channels'
        print use_channels
        FILE_PATH_waveform = [self._local['FILE_PATH_waveform_'+str(ch)] for ch in range(4)]
        print 'FILE_PATH_waveform'
        print FILE_PATH_waveform        
        self._clear_channels()
        #self.Resource.waveformFlush()
        
	for ch in use_channels:
	    wave_number = ch
            Wave = sd.SD_Wave()
            if self._local['B_use_trigger'] == 'ON':
                self._set_trigger(ch)
            Wave.newFromFile(FILE_PATH_waveform[ch])                         
            self.Resource.waveformLoad(Wave, wave_number)
            ### An arbitrary integer refering to some wave. sd.SD_Waveshapes.AOU_AWG
            ### The reference defined in 'waveformLoad'.
            self.Resource.channelWaveShape(ch, sd.SD_Waveshapes.AOU_AWG)
            self.Resource.channelAmplitude(ch, float(self._local['R_amplitude_'+str(ch)]))
            self.Resource.channelOffset(ch, float(self._local['R_offset_'+str(ch)]))	### Andreas: we also only need to load one wave object to the AWG board. this is because there is only one copy in memory that the board uses whenever you reference waveform '0'
            startDelay, cycles, prescaler = 0, 0, 0
            tm = sd.SD_TriggerModes.EXTTRIG_CYCLE
            self.Resource.AWGqueueWaveform(ch, wave_number, tm, startDelay, cycles, prescaler)
            # print(self.Resource.AWGFromFile(ch, 'waveforms/square.csv', SD_TriggerModes.AUTOTRIG, 0, 10000, 0).__str__())
            #self.Resource.AWGstart(ch)
        self.Resource.AWGstartMultiple(0b1111)
        
    @open_close
    def sin(self,ch,frequency,amp,offset,phase):
        
        self.Resource.channelAmplitude(ch, amp)
        self.Resource.channelOffset(ch, offset)
        self.Resource.channelFrequency(ch, frequency)
        self.Resource.channelPhase(ch,phase)
        self.Resource.channelWaveShape(ch, sd.SD_Waveshapes.AOU_SINUSOIDAL)

        self.Resource.AWGstart(ch)
        
 #we can keep this function or include it in waveform_from_file, I took off the @open_close to avoid double-opening/closing
    def _set_trigger(self, channel):
        td = sd.SD_TriggerDirections.AOU_TRG_IN
        sm = sd.SD_SyncModes.SYNC_CLK10
        te = sd.SD_TriggerExternalSources.TRIGGER_EXTERN
        tb = sd.SD_TriggerBehaviors.TRIGGER_RISE
        self.Resource.triggerIOconfig(td, sm)	                                ### here we configure the AWG's TRG port, setting it to be an input and syncing its reading with the PXI chassis' 10MHz ref clock
        self.Resource.AWGtriggerExternalConfig(channel, te, tb)	                ### here we set both AWG 0 and 1 to use an external trigger, triggering on that signal's rising edge    
     		                                      
    def _clear_channels(self):
        self.Resource.AWGstopMultiple(0b1111)					### stop all the AWG's
        for ch in range(4):
            self.Resource.AWGflush(ch)						### flush all the AWG queues
        self.Resource.waveformFlush()	
        ws = sd.SD_Waveshapes.AOU_OFF
        for ch in range(4):							### clear the AWG memory 
            self.Resource.channelWaveShape(ch, ws)	                        ### set all the channels to output OFF

    @open_close
    def ___flush(self):
        self.Resource.waveformFlush()
        print "/(flush)"
	


################################################################################ ON THE AWG
"""
SD AWG-H3344 (Arbitrary Waveform Generator)

(for programmitcally connecting to our AWG card)
NAME: 		SD AWG-H3344-PXIe-2G
SERIAL NUMBER: 	0VKHSVMF

Specs:
	Basics:
		-- 4 channels for function generation and arbitrary wave generation
		-- TRG in/out channel (used to trigger waveforms via external hardware OR to provide a synchronized trigger for other coupled hardware)
			-- Trigger should be TTL, between 3.3 and 5V (input is high impedance so sending in a pulse with Vpp = 1.8 and sufficient offset should be good)
		-- CLK out channel (for sampling CLKsys of AWG)
		-- 10MHz clock in reference (on back)
		-- 10MHz clock out reference (on back)
	Sampling Rate:
		-- MAX: 1GS/s (ie: 1 sample per nanosecond) <--FIXED (CANNOT BE CHANGED)
	Max Amplitude:
		-- 1.5V
	DC Offset settings:
		-- resolution: 183.1 uV (14 bits)
			-- allows for ~5400 (5460) data points for a sweep between -0.5V and 0.5V
		-- Max(Amplitude + Offset): still 1.5V (AWG cannot output more than this)
	Onboard Memory:
		-- 2GB of RAM (from PXIe hardware, limits the amount of waveforms you can have loaded on the hardware)
			-- this combined with the sampling rate specs allows for a total onboard waveform time of ~0.1s 
			-- note that total waveform time means total time of all waveforms loaded on hardware, not just for a single AWG 
Operation:
	Basics:
		-- 4 channels that allow for signal generation, very controllable
			-- allow for use of a function generator (preset period function generation (eg: sine wave, square wave, sawtooth, etc.))
			-- also one AWG per channel that can be used for your arbitrary wave generation
		-- things you can set for a given channel:
			-- amplitude (for both FG and AWG modes)
			-- DC offset of channel (both FG and AWG modes)
			-- phase (FG mode)
			-- frequency (FG mode)
			-- waveform type (define either that the channel will be using its AWG or which function you want the FG to generate)
		-- FG flow
			-- connect to module
			-- select channel to connect to
			-- set channel amplitude/frequency
			-- select waveform type from preset list
		-- AWG flow
			-- connect to module
			-- make sure to flush the queue of the AWG(s) you want to use to ensure there aren't any waveforms preloaded you aren't aware of 
			-- define a(some) wave(s): either with a wave file (see example gaussian.csv) (stored in PC memory) or an array of points (stored in PC RAM)
				-- different wave types (check documentation for this): simplest and likely best to use -> WAVE_ANALOG_16 or WAVE_ANALOG_32
			-- load wave(s) to on-board RAM (this is where memory limit matters)
			-- from waves stored in on-board RAM, selectively queue wave forms into AWGs
				-- here you define some important parameters:
					-- which channel's AWG to use
					-- which wave to load into your AWG (via a wave identifier number YOU define for a wave when you load it to the card)
					-- number of cycles (copies) of this specific waveform to queue up
					-- how you want the start of this wave to be triggered (ie: software/hardware trigger or one trigger necessary per one cycle or one trigger to start all the cycles)
						-- best trigger option is external hardware triggering (most synced up for multichannel purposes, software triggering includes a delay)
						-- for more trigger details, see manual or signadyne.py 
					-- set the start delay for this wave (how long in tens of nanoseconds the wave will start after trigger)
			-- set selected channel's amplitude
			-- set selected channel's waveform type to AWG
			-- start your selected AWG(s)
				
	Software (details of functionality included in using_signadyne_py.txt and examples in signadyne_awg_test.py):
		-- Using signadyne.py library included with signadyne's software libraries to control AWG (free to downlaod from site)
			-- reading and understanding this (short) library pays off greatly if you're going to be using it as there are some things that differ from/are additional to those in the manual(at least the definitions at the top and the SD_AOU class)
		-- there is currently a script with a number of basic test functions (check this file for specifics/documentation)
		-- Additionally there is currently a script for generating arbitrary Gaussians (this should be cleaned up)
			-- if a different waveform is desired, one can generate a waveform file of their own
	GUIs: 
		-- SDM (signadyne device manager) - check on the status of the PXI chassis and any cards
		-- Virtualknob (control the AWG ) - control the AWG from a desktop application (a bit cumbersome imo)
"""
	
################################################################################ ON PROGRAMMING FOR THE AWG
"""	
SD_AWG_H3344 - programming in python for AWG-H3344
(for best viewing, open full screen)

I highly recommend that as you familiarize yourself with this code you regularly look into the signadyne.py library. It's easy to read and helps clarify functionality a lot.

I also suggest printing the outcome of any function calls you make when you are first writing your code in order to see associated error codes in the event that anything goes wrong. The definitions of these error codes are located at:
C:\Program Files (x86)\Signadyne\Libraries\include\common\SD_Error.h
after installing signadyne's libraries (if not using windows, then just find where the Signadyne folder has been installed and follow the path from there). For example, error code -8032 is a hardware error and is raised if your software is trying to communicate with a hardware feature our AWG does not include (like a variable clocking rate)

Basic flow (see the documented python file for example):
	-- you set up a SD_AOU object to connect to a module (the AWG card in this case) either via its chassis number and port number or its name and serial number (the system will find it)
	-- you will flush the AWG to make sure you've removed any currently stored waveforms / currently queued waveforms (unless you desire them to remain) in order to avoid unexpected behaviour
	-- you will then set the desired channel variables for the channels you wish to use (ie: Amplitude, DC offset) via the channel<Variable>() methods of the SD_AOU class
	-- you will define as many wave forms as you need as SD_Wave objects (ideally with the use of a waveform file, see gaussian.csv for an example), but it is also possible to just use an array of points
	-- you will load the waveform(s) to the AWG card via the loadWaveform() method of the SD_AOU class
	-- you will queue the waveform(s) as desired via the AWGqueueWaveform() method of the SD_AOU class 
	-- you will run the AWG's via the AWGstart() method of the SD_AOU class
	
Relevant functions and brief explanations

######  (SETTING UP THE MODULE) ###############################################
SD_AOU() 											##-- = instantiates an SD_AOU object that you will use to control the whole AWG card

SD_AOU::openWithSerialNumber(name, serial_number) 	##-- = opens a connection to the specified module (the AWG card in our case)
													##	 + name is a string defining the AWG card's name
													##	 + serial_number is a string defining the AWG card's serial number (find these values in signadyne_awg_info.txt)

######  (CLEARING CHANNELS/AWG)	###############################################
SD_AOU::waveformFlush()								##-- = deletes all waveforms stored in the AWG card's on-board RAM and flushes each AWG channel's queue (ie: clears EVERYTHING)

SD_AOU::AWGflush(nAWG)								##-- = flushes the queue of the specified AWG (nAWG is an integer on [0,3] specifying which AWG you're using. it will always be used as such)
															
######  (SETTING UP CHANNELS) ###############################################
SD_AOU::channelAmplitude(nAWG, amplitude)			##-- = set the amplitude of the specified AWG
														 + Amplitude is amplitude of your channel in volts (wave file points are defined in +/- %amplitude). The limit is 1.5.

SD_AOU::channelWaveshape(nAWG, waveshape)			##-- = sets the waveshape of the specified AWG 
													##	 + waveshape is an integer defined by the SD_Waveshapes class. Use SD_Waveshapes.AOU_AWG to use the channel as an AWG 
													
###### 	(CREATING A NEW WAVE ON PC) ###############################################
SD_Wave()                                           ##-- = instantiates an SD_Wave object that will define a single waveform

SD_Wave::newFromFile(wavefile_name)					##-- = assignes the SD_Wave object a specific waveform defined in a wave file
													##	 + wavefile_name is the relative path to the wavefile defining the waveform of interest

######  (LOADING/QUEUEING WAVE ON AWG) ###############################################
SD_AOU::waveformLoad(wave, wave_number)				##-- = loads the specified wave form to the AWG's onboard RAM with the identification number wave_number
													##   + wave is an SD_Wave object you have created previously
													##   + wave_number is an integer number you choose to identify the wave when it's in the AWG (start at 1, get bigger from there)
													
SD_AOU::AWGqueueWaveform(nAWG, wfNum, 				##-- = queues the waveform in the specified AWG's queue according to the parameters
	triggerMode, startDelay, cycles, prescaler)		##   + wfNum is the wave_number associated with the wave loaded to the AWG card that you now want to queue up (this is the number you set with waveformLoad())
													##   + triggerMode is an integer defining how you want the waveform's release from the queue to be triggered (these integers are defined in signadyne.py's SD_TriggerMode class)
													##   + startDelay is an integer telling the AWG how many tens of ns to wait until it releases the waveform after it has been triggered
													##	 + cycles is an integer telling the AWG how many cycles of the desired waveshape to load into the queue (one after the other). EG: cycles=5 implies the AWG's queue will have 
															5 copies of the waveform loaded into it. SETTING CYCLES TO 0 (zero) MEANS INFINITE CYCLES LOADED (DOCUMENTATION SAYS USE A NEGATIVE NUMBER, THIS IS WRONG)
													##	 + prescaler is irrelevant for our AWG model, just set it to 0 (it only matters for variable clock frequency AWG models)

######  (CONFIGURING TRIGGER) ###############################################
SD_AOU::triggerIOconfig(direction, syncMode)		##-- = configures the TRG I/O port of the AWG card
													##	 + direction sets whether TRG is an input or an output (integer defined by SD_TriggerDirections class, 0 for out, 1 for in)
													##	 + syncMode sets what clock TRG is sampled with (integer defined by SD_SyncMode class, 0 for internal 100MHz clock, 1 for 10MHz PXIe reference clock (we use this one))

SD_AOU::AWGtriggerExternalConfig(nAWG, src,			##-- = configures the trigger behaviour of the specified AWG channel
	triggerBehaviour)								##	 + src sets the source from which the AWG gets its trigger (integer definied by SD_TriggerExternalSources class (use 0 for the TRG I/O))
													##	 + triggerBehaviour sets what counts as a trigger for the AWG (high signal, low signal, rising edge, falling edge) (integer defined by SD_TriggerBehaviour class)

SD_AOU::AWGtrigger(nAWG)							##-- = if the specified AWG is set to respond to a software trigger, this will trigger it

SD_AOU::AWGtriggerMultiple(bitMask)					##-- = if the specified AWG's are set to respond to a software trigger, this will trigger them. Note that there is a delay between triggers, so the channels will not be synced
													##	 + bitMask is a bit mask defining which AWG's to trigger (eg: 0b0001 (integer 1) triggers AWG 0, 0b0101 (integer 5) triggers AWG 0 and AWG 2, 0b1111 triggers each AWG)

######	(STARTING/STOPPING THE AWG's) ###############################################
SD_AOU::AWGstart(nAWG)								##-- = starts the specified AWG

SD_AOU::AWGstartMultiple(bitMask)					##-- = starts the specified AWGs 
													##	 + bitMask is a bit mask defining which AWG's to start (eg: 0b0001 (integer 1) starts AWG 0, 0b0101 (integer 5) starts AWG 0 and AWG 2, 0b1111 starts each AWG)
													
SD_AOU::AWGstop(nAWG)								##-- = stops the specified AWG 

SD_AOU::AWGstopMultiple(bitMask)					##-- = stops the specified AWGs 
													##	 + bitMask is best written as a binary number (can use integers too I guess) defining which AWG's to stop (eg: 0b0001 (integer 1) stops AWG 0, 0b0101 (integer 5) starts AWG 0 and AWG 2, 0b1111 triggers each AWG)
"""



################################################################################ FROM THE SIGNADYNE FILE
"""
CSV-FILES:
C:\Users\Public\Documents\Signadyne\Examples\Waveforms

WAVEFORM KEYS:
	AOU_OFF             = -1
	AOU_SINUSOIDAL      = 1
	AOU_TRIANGULAR      = 2
	AOU_SQUARE          = 4
	AOU_DC              = 5
	AOU_AWG             = 6
	AOU_PARTNER         = 8

ERRORS:
	STATUS_DEMO = 1
	OPENING_MODULE = -8000
	CLOSING_MODULE = -8001
	OPENING_HVI = -8002
	CLOSING_HVI = -8003
	MODULE_NOT_OPENED = -8004
	MODULE_NOT_OPENED_BY_USER = -8005
	MODULE_ALREADY_OPENED = -8006
	HVI_NOT_OPENED = -8007
	INVALID_OBJECTID = -8008
	INVALID_MODULEID = -8009
	INVALID_MODULEUSERNAME = -8010
	INVALID_HVIID = -8011
	INVALID_OBJECT = -8012
	INVALID_NCHANNEL = -8013
	BUS_DOES_NOT_EXIST = -8014
	BITMAP_ASSIGNED_DOES_NOT_EXIST = -8015
	BUS_INVALID_SIZE = -8016
	BUS_INVALID_DATA = -8017
	INVALID_VALUE = -8018
	CREATING_WAVE = -8019
	NOT_VALID_PARAMETERS = -8020
	AWG_FAILED = -8021
	DAQ_INVALID_FUNCTIONALITY = -8022
	DAQ_POOL_ALREADY_RUNNING = -8023
	UNKNOWN = -8024
	INVALID_PARAMETERS = -8025
	MODULE_NOT_FOUND = -8026
	DRIVER_RESOURCE_BUSY = -8027
	DRIVER_RESOURCE_NOT_READY = -8028
	DRIVER_ALLOCATE_BUFFER = -8029
	ALLOCATE_BUFFER = -8030
	RESOURCE_NOT_READY = -8031
	HARDWARE = -8032
	INVALID_OPERATION = -8033
	NO_COMPILED_CODE = -8034
	FW_VERIFICATION = -8035
	COMPATIBILITY = -8036
	INVALID_TYPE = -8037
"""





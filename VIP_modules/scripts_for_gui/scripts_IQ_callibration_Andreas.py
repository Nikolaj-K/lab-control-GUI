import visa
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy
from math import log10, sqrt
import time
from time import time as time_now

from external.signadyne import *

################################################################################

def main(vip):
    sk = 'Mixer calib.'

    TIC = time_now()
    
    # center_freq = float(input('input your desired LO frequency in GHz: '))
    # int_freq = float(input('input your desired intermediate frequency in MHz: '))
    # res_band = float(input('input your desired resolution bandwidth in kHz: '))
    # LO_pow = float(input('input your desired LO power in dBm: '))
    # amp = float(input('input your desired sinusoidal amplitude in V: '))
    center_freq = float(vip.get(sk, 'center_freq'))
    int_freq    = float(vip.get(sk, 'int_freq'))
    res_band    = float(vip.get(sk, 'res_band'))
    LO_pow      = float(vip.get(sk, 'LO_pow'))
    amp         = float(vip.get(sk, 'R_amplitude'))

    sa = connect_to_spectrum_analyzer(center_freq, res_band, int_freq)
    awg = connect_to_AWG()
    sg = connect_to_signal_generator(center_freq, LO_pow)
	
    reset_awg(awg)
    offset_sinusoids(awg, int_freq, amp)

    total_callibration(center_freq, int_freq, suppressed_freq, res_band, amp, sa, awg, sg)
    
    #span = 1/10*int_freq*100
    #rbw = 10*span
    #suppressed_freq = (center_freq*(10**3)) - int_freq
    #wanted_freq = (center_freq*(10**3)) + int_freq
    #inp_pow = 10*log10(1000*((amp)**2)/100)
    #axes = get_freq_spectrum_trace(sa, 'Freq Spectrum Script-SB-Callibrated Vector Source')

    TOC = time_now()
    print str(TOC - TIC)+" sec (demo_main)" 
    print "/// Script completed.(demo_main)"

################################################################################

#CONNECT TO AWG
def connect_to_AWG():
    awg = SD_AOU()
    awg.openWithSerialNumber('SD-PXE-AWG-H3344-2G', '0VKHSVMF')
    
    return awg

################################################################################

# 3 SEPERATE METHODS FOR MANIPULATING THREE DIFFERENT POWER MARKERS #
def collect_peak_power(instr): #marker 1
    instr.write('INIT:IMM; *WAI')                      #Perform a measurement
    instr.write('CALC:MARK:SGR:XY:MAX')                #Move marker 1 to the current maximum in the domain
    peak_pwr = float(instr.query('CALC:MARK:Y?'))      #Collect the power value there

    return peak_pwr
	
def collect_peak_power2(instr): #marker 2
    instr.write('INIT:IMM; *WAI')
    instr.write('CALC:MARK2:SGR:XY:MAX')
    peak_pwr = float(instr.query('CALC:MARK2:Y?'))

    return peak_pwr
	
def collect_peak_power3(instr): #marker 3
    instr.write('INIT:IMM; *WAI')
    instr.write('CALC:MARK3:SGR:XY:MAX')
    peak_pwr = float(instr.query('CALC:MARK3:Y?'))

    return peak_pwr

#######################################################################
 

#### sweep functions for minimizing unwanted frequencies that vary a single paramter according to a center value and a granularity and report the minimum minimum and the parameter value that achieves it
def phase_sweep(instr, awg, channel, center_phase, granularity, min_power=1000): #relative phase between I and Q
    start_phase = center_phase - (18*granularity)                                #begin sweep half a sweep length below the center value of the sweep parameter
    minimizing_phase = center_phase                                              #establish center value as a temporary minimizer
    for i in range(0,36):                                                        #sweep the parameter, making steps the size of the set granularity
        p = start_phase + i*granularity
        awg.channelPhase(channel,p)
        temp_pow = collect_peak_power2(instr)
        if temp_pow < min_power:                                                 #collect the peak value at the desired frequency and if its a new minimum, update values
            min_power = temp_pow
            minimizing_phase = p 
    awg.channelPhase(channel, minimizing_phase)                                  #set parameter to the minimizing value found during this sweep
    return minimizing_phase, min_power
	
def amplitude_sweep(instr, awg, channel, center_amp, granularity, min_power=1000): #multiplicative amplitude adjustment
    start_amp = center_amp - (20*granularity)
    minimizing_amp = center_amp
    for i in range(0,40):
        a = start_amp + i*granularity
        if a > 1.5:
            a = 1.5
        if a < 0:
            a = 0
        awg.channelAmplitude(channel,a)
        temp_pow = collect_peak_power2(instr)
        if temp_pow < min_power:
            min_power = temp_pow
            minimizing_amp = a		
    awg.channelAmplitude(channel, minimizing_amp)
    amp_ratio = minimizing_amp/center_amp
    return minimizing_amp, min_power, amp_ratio
	
def offset_sweep(instr, awg, channel, center_offset, granularity, min_power=1000): #dc offset of a single AWG channel
    start_offset = center_offset - (20*granularity)
    minimizing_offset = center_offset
    for i in range(0,40):
        o = start_offset + i*granularity
        awg.channelOffset(channel,o)
        temp_pow = collect_peak_power(instr)
        if temp_pow < min_power:
            min_power = temp_pow
            minimizing_offset = o 
    awg.channelOffset(channel, minimizing_offset)
    print(minimizing_offset, min_power)
    return minimizing_offset, min_power
##############################################################################################################

#METHOD FOR GENERATING THE TEST WAVEFORM TO CALLIBRATE AGAINST
def offset_sinusoids(awg, int_freq, amp):
    awg = SD_AOU()
    awg.openWithSerialNumber('SD-PXE-AWG-H3344-2G', '0VKHSVMF')

    awg.channelAmplitude(0, amp)
    awg.channelFrequency(0, int_freq*(10**6))
    awg.channelAmplitude(1, amp)
    awg.channelFrequency(1, int_freq*(10**6))
    awg.channelWaveShape(0, SD_Waveshapes.AOU_SINUSOIDAL)
    awg.channelWaveShape(1, SD_Waveshapes.AOU_SINUSOIDAL)
    awg.channelPhase(0,0)
    awg.channelPhase(1,0)

def reset_awg(awg):
    awg.channelOffset(0,0)
    awg.channelOffset(1,0)
    awg.channelPhase(0,0)
    awg.channelPhase(1,0)
	
# returns the data associated with the current trace on the spectrum analyzer screen
def get_freq_spectrum_trace(instr, title):
        instr.write('SWE:TIME:AUTO ON') #reset sweep time to scale in case time-domain measurement was previously made
        start_freq = int(instr.query('FREQuency:STARt?'))
        stop_freq = int(instr.query('FREQuency:STOP?'))
        num_points = int(instr.query('SENSe:SWEep:POINts?'))
        
        freq_vect = numpy.linspace(start_freq, stop_freq, num_points) #construct the frequency axis vector from set instrument parameters
        
        instr.write('FORM REAL')
        pow_vect = instr.query_binary_values('TRACe:DATA? TRACE1')#,
#                                                 converter='f')  # Returns trace values from power axis only
       
        plt.plot(freq_vect, pow_vect)
        plt.xlabel('Frequency (10\'s of GHz)')
        plt.ylabel('Power (dBm)')
        plt.title(title)
        
        return freq_vect, pow_vect

#iteratively calls the minimizing dc offset sweep to find the overall minimum possible callibrated value for the LO peak
def total_dc_offset_callibration(sa, awg, center_freq, int_freq, res_band):

    if int_freq == 0:
        int_freq = 10
    	
    #CENTER ON LO LEAKAGE
    sa.write('FREQ:CENT ' + str(center_freq*(10**9)))
    sa.write('FREQ:SPAN ' + str(10*(10**6)))
    sa.write('FREQ:BAND ' + str(res_band*(10**3)))
	
    sa.write('CALC:MARK1:X ' + str(center_freq*(10**9)))
	
	#CALLIBRATE THE DC OFFSET FOR THE GIVEN LO FREQUENCY
    co_0 = offset_sweep(sa, awg, 0, 0, 0.01)
    co_1 = offset_sweep(sa, awg, 1, 0, 0.01)
    co_0 = offset_sweep(sa, awg, 0, co_0[0], 0.001)
    co_1 = offset_sweep(sa, awg, 1, co_1[0], 0.001)
    co_0 = offset_sweep(sa, awg, 0, co_0[0], 0.0001)
    co_1 = offset_sweep(sa, awg, 1, co_1[0], 0.0001)
    lo_pow = co_1[1]
    channel_0_offset = co_0[0]
    channel_1_offset = co_1[0]
    
    return lo_pow, channel_0_offset, channel_1_offset

#iteratively calls the minimizing phase/amp sweeps to find the overall minimum possible callibrated value for the unwanted sideband
def total_phase_amp_callib(sa, awg, suppressed_freq, int_freq, amp):
    
    if int_freq == 0:
        int_freq = 10
	
    #CENTER ON UNWANTED SIDE BAND
    sa.write('FREQ:CENT ' + str(suppressed_freq*(10**6)))
    sa.write('FREQ:SPAN ' + str(10*(10**6)))
	
    sa.write('CALC:MARK2:X ' + str(suppressed_freq*(10**6)))
    
    cp = phase_sweep(sa, awg, 0, 180, 10)
    ca = amplitude_sweep(sa, awg, 0, amp, .02)
    cp = phase_sweep(sa, awg, 0, cp[0], 1, ca[1])
    ca = amplitude_sweep(sa, awg, 0, ca[0], .01, cp[1])
    cp = phase_sweep(sa, awg, 0, cp[0], 1, ca[1])
    ca = amplitude_sweep(sa, awg, 0, ca[0], .001, cp[1])
    cp = phase_sweep(sa, awg, 0, cp[0], 0.1, ca[1])
    ca = amplitude_sweep(sa, awg, 0, ca[0], .0001, cp[1])
    usb_pow = cp[1]
    phase_diff = cp[0]
    amp_factor = ca[2]
    
    return usb_pow, phase_diff, amp_factor

#PERFORMS THE OVERALL CALLIBRATION OF THE MIXER AND REPORTS RESULTS
def total_callibration(center_freq, int_freq, suppressed_freq, res_band, amp, sa, awg, sg):
	
    # CALLIBRATE THE PHASE/AMPLITUDE SHIFTS FOR THE GIVEN LO FREQUENCY
    phase_amp_params = total_phase_amp_callib(sa, awg, suppressed_freq, int_freq, amp)
    usb_pow = phase_amp_params[0]
    phase_diff = phase_amp_params[1]
    amp_imbalance = phase_amp_params[2]

    # # DC OFFSET CALLIBRATION
    dc_offset_params = total_dc_offset_callibration(sa, awg, center_freq, int_freq, res_band)
    lo_pow = dc_offset_params[0]
    channel_0_offset = dc_offset_params[1]
    channel_1_offset = dc_offset_params[2]

	# provide view of callibrated spectrum
    sa.write('FREQ:SPAN ' + str(12*int_freq*(10**6)))
    sa.write('FREQ:CENT ' + str(center_freq) + 'GHz')
	
    wsb_pow = collect_peak_power3(sa)

    return lo_pow, usb_pow, wsb_pow, phase_diff, amp_imbalance, channel_0_offset, channel_1_offset

#DOES IT ALL
def run(center_freq, int_freq, res_band, LO_pow, amp):

    #query the user for all relevant parameters
    center_freq = float(input('input your desired LO frequency in GHz: '))
    int_freq = float(input('input your desired intermediate frequency in MHz: '))
    res_band = float(input('input your desired resolution bandwidth in kHz: '))
    LO_pow = float(input('input your desired LO power in dBm: '))
    amp = float(input('input your desired sinusoidal amplitude in V: '))

    #calculate derived values from input
    suppressed_freq = (center_freq*(10**3)) - int_freq
    wanted_freq = (center_freq*(10**3)) + int_freq
    inp_pow = 10*log10(1000*((amp)**2)/100)

    #connect to measurement devices
    sa = connect_to_spectrum_analyzer(center_freq, res_band, int_freq)
    awg = connect_to_AWG()
    sg = connect_to_signal_generator(center_freq, LO_pow)

    #output the test waveform to be callibrated against
    reset_awg(awg)
    offset_sinusoids(awg, int_freq, amp)

    #perform the callibration and retrieve the desired results
    results = total_callibration(center_freq, int_freq, suppressed_freq, res_band, amp, sa, awg, sg)

    phase_diff = results[3]
    amp_imbalance = results[4]
    channel_0_offset = results[5]
    channel_1_offset = results[6]

    #report the results
    print(
        "Phase difference: " + str(phase_diff) + '\n'
        "Amplitude imbalance factor: " + str(amp_imbalance) + '\n'
        "Channel 0 offset: " + str(channel_0_offset) + '\n'
        "Channel 1 offset: " + str(channel_1_offset) + '\n'
    )

#HELPER GRAPHING FUNCTION
def peak_power_sweep(awg, sa):
    fn = input('input your filename root: ')
    lo_pow = []
    wsb_pow = []
    usb_pow = []
    ip = []
    
    for i in range(-41,65):
        pow = float(i)/10
        voltage = sqrt(10**((pow)/10 - 1))
        awg.channelAmplitude(0,voltage)
        awg.channelAmplitude(1,voltage)
        time.sleep(2)
        sa.write('FREQ:CENT 10GHz')
        sa.write('FREQ:SPAN 10MHz')
        sa.write('CALC:MARK:X 10GHz')
        time.sleep(1)
        lo_pow.append(sa.query('CALC:MARK:Y?'))
        #lo_pow.append(collect_peak_power(sa))
        sa.write('FREQ:CENT 9.9GHz')
        sa.write('FREQ:SPAN 10MHz')
        sa.write('CALC:MARK2:X 9.9GHz')
        time.sleep(1)
        #wsb_pow.append(collect_peak_power2(sa))
        wsb_pow.append(sa.query('CALC:MARK2:Y?'))
        sa.write('FREQ:CENT 10.1GHz')
        sa.write('FREQ:SPAN 10.1MHz')
        sa.write('CALC:MARK3:X 10.1GHz')
        time.sleep(1)
        #usb_pow.append(collect_peak_power3(sa))
        usb_pow.append(sa.query('CALC:MARK3:Y?'))
        ip.append(pow)
	
    f_lo = open('data/vec_source/' + fn + '_lop', 'w')
    f_wsb = open('data/vec_source/' + fn + '_wsp', 'w')
    f_usb = open('data/vec_source/' + fn + '_usp', 'w')
    for item in lo_pow:
        f_lo.write("%s\n" % item)
    for item in wsb_pow:
        f_wsb.write("%s\n" % item)
    for item in usb_pow:
        f_usb.write("%s\n" % item)
    plt.plot(ip, lo_pow, label='lo power')
    plt.plot(ip, wsb_pow, label='wsb power')
    plt.plot(ip, usb_pow, label='usb power')
    #plt.legend(loc='best')
    plt.title('vec source pow vs. pow')
    plt.xlabel('input power (dBm)')
    plt.ylabel('output power (dBm)')
		








#METHOD FOR CONNECTING TO SPECTRUM ANALYZER WITH SPECIFIC PARAMETERS
def connect_to_spectrum_analyzer(center_freq, bandwidth, int_freq):
    str_IP_FSWSSA01  = '10.21.64.30' # FSQ - Rohde & Schwarz Signal and Spectrum Analyzer nr. 01
    fun_IP_2_address = lambda arg_str_IP: 'TCPIP0::' + arg_str_IP + '::hislip0::INSTR'
    
    instr = visa.ResourceManager().open_resource(fun_IP_2_address(str_IP_FSWSSA01))
    # instr.write('*RST')
    del instr.timeout
    
    instr.write('BAND:RES ' + str(bandwidth) + 'kHz')
    instr.write('FREQ:CENT ' + str(center_freq) + 'GHz')
    instr.write('FREQ:SPAN 10MHz')
    instr.write('INIT:CONT OFF')
    instr.write('DISP:WIND:TRAC:MODE AVER')
    instr.write('AVER:TYPE LIN')
    instr.write('DET RMS')
    instr.write('SENS1:SWE:COUNT 10')
    instr.write('SENS:SWE:POIN 10001')
    
    print('----- SYST:ERR? -----\n' 
    + str(instr.query('SYST:ERR?'))
    )
    
    return instr

#CONNECT TO SIGNAL GENERATOR WITH SPECIFIED PARAMETERS
def connect_to_signal_generator(output_freq, output_power):
    str_IP_SGA01  = '10.21.64.31' # Rohde & Schwarz Signal generator nr. 01
    fun_IP_2_address = lambda arg_str_IP: 'TCPIP0::' + arg_str_IP + '::hislip0::INSTR'
    
    instr = visa.ResourceManager().open_resource(fun_IP_2_address(str_IP_SGA01))
    instr.write('*RST')
    del instr.timeout
    
    instr.write('ROSC:SOUR EXT')
    instr.write('FREQ ' + str(output_freq) + 'GHz')
    instr.write('POW:POW ' + str(output_power))
    instr.write('OUTP ON')

    return instr



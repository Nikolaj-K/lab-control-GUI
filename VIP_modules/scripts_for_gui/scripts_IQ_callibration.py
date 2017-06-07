import os
import sys
### Get the path to the current base directory (the path of this __file__).
### Then add 'DIR_PATH_modules' to the paths we can load files from.
DIR_PATH_modules = os.path.dirname(__file__)+os.sep+"VIP_modules" 
sys.path.insert(0, DIR_PATH_modules)
import visa
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from numpy import linspace
from math import log10, sqrt
import time
from time import time as time_now

import interface.auxiliary_functions as auxi

try:
    from external.signadyne import *
except ImportError as exception:
    print "!! (scrpts_IQ_calibration, ImportError) external.signadyne import ALL:"
    print exception

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
    SPEC_pow    = float(vip.get(sk, 'LO_pow'))
    amp         = float(vip.get(sk, 'R_amplitude'))
    
    dig = 'ATS9870_1'
    spec = 'SGS_31'
    lo = 'SGS_31'
    awg = 'H3344_1'
    ni = 'NI_pulse_1'
    
    
    cal_settings = {'LO':lo
                    ,'Spec':spec
                    ,'AWG': awg
                    ,'Dig': dig
                    ,'center_freq' : center_freq
                    ,'wanted_sideband' : center_freq-int_freq
                    ,'int_freq' : int_freq
                    ,'R_amplitude' : amp
                    }
    
    #CONNECT TO INSTRUMENTS
    
    vip.set(dig, {'B_connect' : 'TRY'})
    vip.set(spec, {'B_connect' : 'TRY'})
    vip.set(lo, {'B_connect' : 'TRY'})
    vip.set(awg, {'B_connect' : 'TRY'})
    vip.set(ni, {'B_connect' : 'TRY'})
    
    dig_settings = vip.get(dig)
    meas_type  = vip.get('Meas_main', 'meas_type')
    meas_instr = vip.get(meas_type, 'F_instr_name')
    old_settings = dict(vip._session[meas_type])

    print old_settings  
    print '^'*50
    print dig_settings
    ni_mode = vip.get(ni,'F_use_config')
    print ni_mode
    vip.set(ni,{'F_use_config':'6: Spec - UpC - DIG'})

    print vip.get(ni,'F_use_config')
    from interface.session_events import load_config_NI_pulse, safe_NI_pulse
    load_config_NI_pulse(vip,ni)
    safe_NI_pulse(vip, ni, False, False)
    
    from interface.session_events import bn_connect_to_lab
    bn_connect_to_lab(vip)

    #SET PARAMETERS
    #ideally it now reads off the session and saves it for later
    #then loads a pre-defined session for calibration
    
    vip.set(dig, {'F_channelA_coupling':'DC'})
    vip.set(dig, {'F_channelB_coupling':'DC'})
    vip.set(dig, {'R_intermediate_frequency':'0'})
    
#    vip.set(dig, {'N_records_per_buffer':'50'})
 #   vip.set(dig, {'N_buffers_per_acquisition':'50'})
    
    
    sweep_setting = {'sweep_title_1' : 'From trace'
                    }
    vip.set('Sweep', sweep_setting)
    vip.set('Meas_main', {'meas_type': 'Dig. sample'})

    lo_freq = vip.get(lo,'R_freq_source')
    center_freq = vip.get(spec,'R_freq_source')
    vip.set(lo, {'R_freq_source':str(center_freq)}) 
 
    
    sweep_setting = {'sweep_title_1' : 'From trace'
                    ,'B_is_max_1'    : 'ON'
                    ,'B_is_max_2'    : 'OFF'
                    }
    vip.set('Sweep', sweep_setting)
    vip.set('Meas_main', {'meas_type': 'Dig. sample'})
    vip.set('Dig. sample', {'N_records_per_buffer': '20'
                           ,'N_buffers_per_acquisition':'20'})
    vip.set('Dig. sample', {'N_samples_factor':'1'})                           

    
    vip.set(spec, {'R_freq_source':str(center_freq)})  
    vip.set(spec, {'R_power_source':str(15)})  
    vip.set(spec, {'B_output':'ON'})  
    vip.set(lo, {'R_freq_source':str(center_freq)})  
    vip.set(lo, {'R_power_source':str(15)}) 
    vip.set(lo, {'B_output':'ON'})   
    
    
    settings = vip._session['Dig. sample']
    vip.set(dig, settings)
 
    from interface.session_events import bn_adopt_settings
    bn_adopt_settings(vip)
    

    
    reset_awg(vip,awg)
    if int_freq == 0:
        offset_sinusoids(vip, awg, int_freq, 0)
        
    else:
        offset_sinusoids(vip, awg, int_freq, amp)
        
    wanted_freq = float(center_freq)
    unwanted_freq = float(center_freq)+2.*float(int_freq)
    leak_freq = float(center_freq)+float(int_freq)
   
    
    
    
    lo_pow, channel_0_offset, channel_1_offset, phase_diff, amp_imbalance = total_callibration(vip,cal_settings)
    
    #span = 1/10*int_freq*100
    #rbw = 10*span
    #suppressed_freq = (center_freq*(10**3)) - int_freq
    #wanted_freq = (center_freq*(10**3)) + int_freq
    #inp_pow = 10*log10(1000*((amp)**2)/100)
    #axes = get_freq_spectrum_trace(sa, 'Freq Spectrum Script-SB-Callibrated Vector Source')
    
    #vip.set(awg,{'R_offset_0':str(channel_0_offset)})
    #vip.set(awg,{'R_offset_1':str(channel_1_offset)})
    
    vip.instruments[awg].sin(0, int_freq, amp*amp_imbalance, offset = channel_0_offset, phase = phase_diff)   
    vip.instruments[awg].sin(1, int_freq, amp, offset = channel_1_offset, phase = 0)     
    #awg_settings = vip.get(awg)
    #vip.instruments[awg].waveform_from_file(awg_settings)
    #vip.set(ni,{'F_use_config':ni_mode})
    
    try:
        load_config_NI_pulse(vip,ni)
        safe_NI_pulse(vip, ni, False, False)
    except KeyError:
        pass
    
    print '@'*50
    print phase_diff
    print amp_imbalance
    print channel_0_offset
    print channel_1_offset
    print 'SUPPRESSED FREQ'
    print suppressed_freq
    vip.set(lo, {'R_freq_source':str(lo_freq)})  
    vip.set(dig,dig_settings)
    vip.set('Meas_main', {'meas_type': meas_type})
    vip.set(meas_type,{'F_instr_name':meas_instr})
    print old_settings
    vip.set(meas_type,old_settings)
    bn_adopt_settings(vip)
    print '@'*50
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
def collect_peak_power(vip,cal_settings): #marker 1
    
    dig = cal_settings['Dig']
    
    L_Q_data, L_I_data, _, _ = vip.instruments[dig].get_trace()
    powdBm = auxi.IQ_to_P_in_dB(L_I_data, L_Q_data)
    peak_pwr = numpy.mean(powdBm)

    return peak_pwr
	
def collect_peak_power_with_fit(vip, cal_settings):
    dig = cal_settings['Dig']
    time_start = float(vip.get(dig, 'N_samples_start'))
    time_stop = float(vip.get(dig, 'N_samples_stop'))
    time_sweep_points = int(vip.get(dig,'N_sweep_points'))
    
    tV = list(linspace(time_start, time_stop, time_sweep_points))

    L_Q_data, L_I_data, _, _ = vip.instruments[dig].get_trace()
    
    int_freq = float(cal_settings['int_freq'])
    
    powDC = auxi.FitSignal(tV,L_I_data,L_Q_data,int_freq)
    
    powdBm = auxi.to_dB(powDC)
    
    return powdBm

#######################################################################
 

#### sweep functions for minimizing unwanted frequencies that vary a single paramter according to a center value and a granularity and report the minimum minimum and the parameter value that achieves it
def phase_sweep(vip,cal_settings, channel, center_phase, granularity, min_power=1000): #relative phase between I and Q
    start_phase = center_phase - (18*granularity)                                #begin sweep half a sweep length below the center value of the sweep parameter
    minimizing_phase = center_phase         #establish center value as a temporary minimizer
    #get sideband freq and give it to collect_peak_power
    awg = cal_settings['AWG']
    dig = cal_settings['Dig']
    for i in range(0,36):                                                        #sweep the parameter, making steps the size of the set granularity
        p = start_phase + i*granularity
        vip.instruments[awg].set_phase(channel,p)
        #Collect DIG power
        temp_pow = collect_peak_power_with_fit(vip, cal_settings)
        print 'Power'
        print temp_pow
        if temp_pow < min_power:                                                 #collect the peak value at the desired frequency and if its a new minimum, update values
            min_power = temp_pow
            minimizing_phase = p 
    vip.instruments[awg].set_phase(channel,minimizing_phase)                            #set parameter to the minimizing value found during this sweep
    return minimizing_phase, min_power
	
def amplitude_sweep(vip,dig, cal_settings, center_amp, granularity, min_power=1000): #multiplicative amplitude adjustment
    awg = cal_settings['AWG']
    dig = cal_settings['Dig']
    start_amp = center_amp - (20*granularity)
    minimizing_amp = center_amp
    for i in range(0,40):
        a = start_amp + i*granularity
        if a > 0.5 or a < 0.5:
            break
        if a < 0:
            a = 0
        temp_pow = collect_peak_power_with_fit(vip, cal_settings)
        print 'Power'
        print temp_pow
        if temp_pow < min_power:
            min_power = temp_pow
            minimizing_amp = a		
    vip.instruments[awg].set_amplitude(channel,minimizing_amp)
    amp_ratio = minimizing_amp/center_amp
    return minimizing_amp, min_power, amp_ratio
	
def offset_sweep(vip,dig,cal_settings, center_offset, granularity, min_power=1000): #dc offset of a single AWG channel
    awg = cal_settings['AWG']
    dig = cal_settings['Dig']
    start_offset = center_offset - (20*granularity)
    minimizing_offset = center_offset
    for i in range(0,40):
        o = start_offset + i*granularity

        vip.instruments[awg].set_dc_offset(channel,o)
        
        #Collect DIG power
        temp_pow = collect_peak_power(vip, cal_settings)
        print 'Power'
        print temp_pow
        
        if temp_pow < min_power:
            min_power = temp_pow
            minimizing_offset = o 
            
        if o > 0.2 or o < -0.2:
            break
            
    vip.instruments[awg].set_dc_offset(channel,minimizing_offset)
    print(minimizing_offset, min_power)
    return minimizing_offset, min_power
##############################################################################################################

#METHOD FOR GENERATING THE TEST WAVEFORM TO CALLIBRATE AGAINST
def offset_sinusoids(vip,awg, int_freq, amp):
    
    vip.instruments[awg].sin(0, int_freq, amp, offset = 0, phase = 0)
    vip.instruments[awg].sin(1, int_freq, amp, offset = 0, phase = 0)

def reset_awg(vip,awg):
    vip.instruments[awg].set_dc_offset(0,0)
    vip.instruments[awg].set_dc_offset(1,0)

	

#iteratively calls the minimizing dc offset sweep to find the overall minimum possible callibrated value for the LO peak
def total_dc_offset_callibration(vip,cal_settings):
    spec = cal_settings['Spec']
    lo = cal_settings['LO']
    awg = cal_settings['AWG']
    dig = cal_settings['Dig']
    center_freq = cal_settings['center_freq']    
    
    vip.set(spec, {'R_freq_source':str(center_freq)}) 
    vip.set(lo, {'R_freq_source':str(center_freq)}) 	
	#CALLIBRATE THE DC OFFSET FOR THE GIVEN LO FREQUENCY
	
    #add to sweep center frequency value
    co_0 = offset_sweep(vip,cal_settings, 0, 0, 0.01)
    co_1 = offset_sweep(vip,cal_settings, 1, 0, 0.01)
    co_0 = offset_sweep(vip,cal_settings, 0, co_0[0], 0.001)
    co_1 = offset_sweep(vip,cal_settings, 1, co_1[0], 0.001)
    co_0 = offset_sweep(vip,cal_settings, 0, co_0[0], 0.0001)
    co_1 = offset_sweep(vip,cal_settings, 1, co_1[0], 0.0001)
    lo_pow = co_1[1]
    channel_0_offset = co_0[0]
    channel_1_offset = co_1[0]
    
    return lo_pow, channel_0_offset, channel_1_offset

##iteratively calls the minimizing phase/amp sweeps to find the overall minimum possible callibrated value for the unwanted sideband
def total_phase_amp_callib(vip,cal_settings):
    #dig, spec, lo, awg, suppressed_freq, amp
    spec = cal_settings['Spec']
    lo = cal_settings['LO']
    awg = cal_settings['AWG']
    dig = cal_settings['Dig']
    amp = cal_settings['R_amplitude']
    suppressed_freq = cal_settings['center_freq'] + cal_settings['int_freq']
    
    #CENTER ON UNWANTED SIDE BAND
    vip.set(spec, {'R_freq_source':str(suppressed_freq)}) 
    vip.set(lo, {'R_freq_source':str(suppressed_freq)}) 
        
    cp = phase_sweep(vip,cal_settings, 0, 180, 10)
    ca = amplitude_sweep(vip,cal_settings, 0, amp, .02)
    cp = phase_sweep(vip,cal_settings, 0, cp[0], 1, ca[1])
    ca = amplitude_sweep(vip,cal_settings, 0, ca[0], .01, cp[1])
    cp = phase_sweep(vip,cal_settings, 0, cp[0], 1, ca[1])
    ca = amplitude_sweep(vip,cal_settings, 0, ca[0], .001, cp[1])
    cp = phase_sweep(vip,cal_settings, 0, cp[0], 0.1, ca[1])
    ca = amplitude_sweep(vip,cal_settings, 0, ca[0], .0001, cp[1])
    usb_pow = cp[1]
    phase_diff = cp[0]
    amp_factor = ca[2]
    
    return usb_pow, phase_diff, amp_factor

#PERFORMS THE OVERALL CALLIBRATION OF THE MIXER AND REPORTS RESULTS
def total_callibration(vip,cal_settings):
    
    # CALLIBRATE THE PHASE/AMPLITUDE SHIFTS FOR THE GIVEN LO FREQUENCY
    phase_amp_params = total_phase_amp_callib(vip,cal_settings)
    usb_pow = phase_amp_params[0]
    phase_diff = phase_amp_params[1]
    amp_imbalance = phase_amp_params[2]

    # # DC OFFSET CALLIBRATION
    dc_offset_params = total_dc_offset_callibration(vip,cal_settings)
    lo_pow = dc_offset_params[0]
    channel_0_offset = dc_offset_params[1]
    channel_1_offset = dc_offset_params[2]

	## provide view of callibrated spectrum
 #   sa.write('FREQ:SPAN ' + str(12*int_freq*(10**6)))
 #   sa.write('FREQ:CENT ' + str(center_freq) + 'GHz')
	
    wsb_pow = collect_peak_power(vip,cal_settings)

    #return lo_pow, usb_pow, wsb_pow, phase_diff, amp_imbalance, channel_0_offset, channel_1_offset
    return lo_pow, channel_0_offset, channel_1_offset, phase_diff, amp_imbalance

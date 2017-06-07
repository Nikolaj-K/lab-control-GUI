# -*- coding: utf-8 -*-
import numpy as np
from PyQt4 import QtCore
import matplotlib.pyplot as plt

import subprocess

try:
    import external.ATS9870_CS_VNA as external_ATS9870_CS_VNA
except ImportError as exception:
    print "!! (scrpts_DAC_VNA, ImportError) external_ATS9870_CS_VNA:"
    print exception
    external_ATS9870_CS_VNA = None


### Setup:
"""
hook up digitizer to I or Q port of mixer NOT connected to P1.5.
have the SGS rf_sg going into cavity (fridge input 1)
have the SGS lo_sg going to the LO port of the previous mixer
have the signal from the fridge (out and through amp) going into the rf port of the prvevious mixer
"""

### E-mails, August 2016:
"""
#################################################################
From: Rouzbeh Khatibi [rouzbeh@alazartech.com]
Sent: Thursday, August 11, 2016 4:47 PM
To: Andreas BUTLER
Cc: support
Subject: RE: Support Request Form

 
Hi Andreas,
 
I uploaded a new version of the ATS-SDK v7.1.5 on out FTP server ftp://ist:nL7HKwXv@ftp.alazartech.com/
Please run the installation setup program “ATS-SDK-Setup-7.1.5.exe” and use the password UgfRGd3j
This new version of the ATS-SDK fixes the issue you were seeing in the compilation of NPT_Average and CS_Average projects.
 
Regards,
Rouzbeh
 
#################################################################
From: Rouzbeh Khatibi
Sent: August-08-16 12:19 PM
To: Andreas BUTLER
Cc: support
Subject: RE: Support Request Form
 
Hi Andreas,
 
Unfortunately we don’t have sample code for Averaging in Python.
But it won’t be a big change to start from NPT or CS sample codes and modify them into NPT_Average or CS_Average respectively.
What you need is to add some extra processing on each buffer.
To average samples inside a buffer you need to know the organization of data in the buffer, which is explained in sections 2.4.2.2 (for NPT) and 2.4.2.3 (for CS) of the SDK Guide.
Then you can reshape the data and average the samples in the way you need it.
 
Once I send you an updated C sample code for NPT_Average and CS_Average, you can do a diff with NPT or CS respectively, and identify the sections of code taking care of the averaging.
 
Please let me know if the above information helped.
 
Regards,
Rouzbeh
 
#################################################################
From: Andreas BUTLER [mailto:andreas.butler@ist.ac.at]
Sent: August-08-16 10:05 AM
To: Rouzbeh Khatibi
Subject: RE: Support Request Form
 
Thanks for the response,

Out of curiosity, is there any existing python code that has the same averaging behaviour as this C code? It would be easier for us to use.

Regards,
Andreas
"""

################################################################################

def main(vip):
    sk = 'Mixer-Dig VNA'

    IF_freq    = int(vip.get(sk, 'IF_freq'))
    start_freq = int(vip.get(sk, 'start_freq'))                                 ### denotes the starting frequency of the spectroscopy frequency sweep
    stop_freq  = int(vip.get(sk, 'stop_freq'))                                  ### denotes the stopping frequency of the spectroscopy sweep
    points     = int(vip.get(sk, 'points'))                                     ### denotes the number of points in the sweep
    SG_LO_name = vip.get(sk, 'source_LO')                                       ### freq: i_rf
    SG_rf_name = vip.get(sk, 'source_rf')                                       ### freq: i_rf + IF_freq

    sweep_param_list = np.linspace(start_freq, stop_freq, points)               ### sweep parameters and, finally, x-axis to the plot
    r_list = []

    #~~~~~~~~~
    try:
        DAC_instr = connect_to_DAC('a', 'b', 'c', 'd')                          ### TODO: Is AttributeError the right error when this fails? 

        for i_rf in sweep_param_list:
            vip.instruments[SG_LO_name].set_frequency(i_rf, 'Hz')           ### set the spectroscopy frequency
            vip.instruments[SG_rf_name].set_frequency(i_rf + IF_freq, 'Hz') ### set the down-conversion frequency

            curr_amp = collect_DAC_pow(DAC_instr, IF_freq)                      ### measure a power point
            
            r_list.append(curr_amp) 
            
            QtCore.QCoreApplication.processEvents() 
    except AttributeError:
        print "!!! Instruments possibly not connected."
        
    ########## PLOT
    plt.plot(sweep_param_list, r_list)
    plt.show()


def connect_to_DAC(input_range, trig_interval, acquisition_length, num_avg):
    """TODO: Desciption what I, the function, do"""
    return external_ATS9870_CS_VNA.connect_to_dig(input_range
                                                  ,trig_interval
                                                  ,acquisition_length
                                                  ,num_avg)

def collect_DAC_pow(dig, IF_freq):
    """TODO: Desciption what I, the function, do"""
    return external_ATS9870_CS_VNA.collect_amp(dig, IF_freq)

def run_script(script_name):                                                    ### Is this used at all?
    subprocess.call([script_name])
    

################################################################################# TODO
#
##TODO: implement some way of collecting a fast trace with the dig
#def collect_DAC_trace(dig):
#    
#    trace = []
#    
#    return trace
#
##TODO: implement some way of taking an FFT with the dig
#def collect_fft(dig):
#    
#    fft_pow = None
#    
#    return fft_pow
# -*- coding: utf-8 -*-

import os
import time
import interface.session_events as events


################################################################################
def H3344_script(vip):
    print 40*"#"
    
    sk = 'H3344_1'
    vip.set(sk, {'B_connect' : 'TRY'})
    
    events.bn_connect_to_lab(vip)
    
    ########## ########## ########## ########## 
    
    vip.instruments[sk].query_ID()

    #vip.instruments[sk].test_fg1_square(0, 1, 100000)
    #time.sleep(1.5)
    
    #settings = {'F_use_channel'      : 0                                        ###n <-- it's saver to pass a string, sis
    #           ,'R_amplitude'        : '1.0'
    #           ,'FILE_PATH_waveform' : "E:\Measurement_Software\VIP_all\VIP_170107\Data\Waveforms\Generated_waveforms/nikolaj_gaussian.csv" # Square.csv
    #           }  

    vip.set(sk, {'B_channel_0' : 'ON', 'B_channel_1' : 'ON'})
           
    #settings = {}   
    #vip.instruments[sk].waveform_from_file(settings)
    vip.instruments[sk].sin(0, 0.01*10**9, 0.5, offset = 0, phase = 0)
#    
#    
#    time.sleep(3)
#
#print "trigger"
    #vip.instruments[sk]._set_trigger(0)
    #vip.instruments[sk].test_output_on_two_AWG_extTrig_2(settings)
   
    #vip.instruments[sk].test_fg1_square(0, 1, 200000)
    #time.sleep(1.5)
    
    #for _ in range(2):
    #    a = 1
    #    f = 10000
    #    vip.instruments[sk].test_fg1_square(0, a, f)
    #    time.sleep(0.5)
    #    a = 0.5
    #    f = 20000
    #    vip.instruments[sk].test_fg1_square(0, a, f)
    #    time.sleep(1)
    #    vip.instruments[sk].offset_sinusoids()
    #    time.sleep(1.5)
    #    a = 0.75
    #    f = 5000
    #    vip.instruments[sk].test_fg1_square(0, a, f)
    #    time.sleep(0.5)
    
    #vip.instruments[sk].set_dc_offset(0)
    #time.sleep(2)

    #vip.instruments[sk]._clear_channels()
    #time.sleep(2)
    
    ########## ########## ########## ##########
    
    print "\n/(H3344_script)\n"
    
    
    
    
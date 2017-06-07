# -*- coding: utf-8 -*-

import os
import time
import interface.session_events as se
import interface.measurement as im

################################################################################
def fitting_test(vip):
    se.bn_load_session_to_vip(vip)
    
    sk = 'ZNB_1'
    vip.set(sk, {'B_connect' : 'TRY'})
    se.bn_connect_to_lab(vip)
    
    vip.Bpy_redo_sweep = True
    im.bn_do_sweep(vip)

    print "/(fitting_test)"

################################################################################
def phase_test(vip):
    sk = 'SGS_32'
    vip.set(sk, {'B_connect' : 'TRY'})
    
    se.bn_connect_to_lab(vip)
    vip.instruments[sk].set_phase(77)
    vip.instruments[sk].get_info()
    vip.instruments[sk].set_power(-50)
    vip.instruments[sk].set_phase(33)
    vip.instruments[sk].get_info()

    print "/(phase_test)"
    
################################################################################
def H3344_script(vip):
    print 40*"#"
    
    sk = 'H3344_1'
    vip.set(sk, {'B_connect' : 'TRY'})    
    se.bn_connect_to_lab(vip)
    
    ########## ########## ########## ########## 
    
    vip.instruments[sk].query_ID()
    print "trigger"
    vip.instruments[sk].set_trigger(0)

    #vip.instruments[sk].test_fg1_square(0, 1, 100000)
    #time.sleep(1.5)

    settings = {'F_use_channel'      : '0'
               ,'R_amplitude'        : '1.0'
               ,'FILE_PATH_waveform' : "C:/Users/Public/Documents/Signadyne/Examples/Waveforms/Gaussian.csv" # Square.csv
               }
    vip.instruments[sk].waveform_from_file(settings)
    #time.sleep(1.5)
    
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
    
    
    
    
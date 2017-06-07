# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import numpy as np

from PyQt4 import QtCore

import interface.auxiliary_functions as auxi
import interface.session_events as session_events
import dictionaries.script_dict as script_dict
import dictionaries.constants as cs
import dictionaries.menus as menus
import dictionaries.session as session

################################################################################
INDICES_123 = [str(i) for i in [1,2,3]]
SWEEP_KEYS  = ['R__start', 'R__stop', 'N__sweep_points', 'F__unit_sweep', 'F_axis_mode']
TRACE_KEYS  = {'Freq. trace' : ['R_freq_start'   , 'R_freq_stop'   , 'N_sweep_points', 'F_unit_freq', 'F_axis_mode']
              ,'Time trace'  : ['R_time_start'   , 'R_time_stop'   , 'N_sweep_points', 'F_unit_time', 'F_axis_mode']
              ,'Dig. sample' : ['N_samples_start', 'N_samples_stop', 'N_sweep_points', 'F_unit_time', 'F_axis_mode']
              }
              
################################################################################
def _set_sweep_parameters_and_run_script(vip, dI, iI):
    ### This functions is called at each value of the triple sweep.
    """If a sweep with the sweep spectification dictionary (ssI) should be
    performed (Bpy_do_sweep is True), perform the sweep_instr method that sets a
    parameter. E.g. set_power, set_frequency, set_voltage etc.
    Then, if specificed, run a script.
    Finally, call the Qt function 'processEvents' make sure all Qt processes
    are executed before the function call ends. This unfreezes the GUI.
    """
    if dI['Bpy_do_sweep']:
        vip.set(dI['sweep_instr'], {dI['k_sweep'] : str(iI)})

        if (dI['k_sweep'] == 'R_power_source'):
            vip.instruments[dI['sweep_instr']].set_power(iI, dI['unit'])
        elif (dI['k_sweep'] == 'R_freq_source'):
            vip.instruments[dI['sweep_instr']].set_frequency(iI, dI['unit'])
        elif (dI['k_sweep'] == 'R_phas_source'):
            vip.instruments[dI['sweep_instr']].set_phase(iI, dI['unit'])
        elif (dI['k_sweep'] == '~'+'voltage_source'):
            vip.instruments[dI['sweep_instr']].set_voltage(vip.get(dI['sweep_instr']), iI, dI['unit'])
        elif (dI['k_sweep'] == '~'+'AWG_channels'):
            index = dI['index']
            wave_file_lists = vip._file_list_dict[index]    
            channels = [vip.CHANNEL__SWEEP_0, vip.CHANNEL__SWEEP_1]
            for ch in range(len(channels)):            
                vip.set(dI['sweep_instr'], {'FILE_PATH_waveform_'+str(channels[ch]): wave_file_lists[ch][int(iI)]})
            settings = vip.get(dI['sweep_instr'])
            vip.instruments[dI['sweep_instr']].waveform_from_file(settings)
        elif (dI['k_sweep'] == '~'+'AWG_channels_param'):
            #print [(vip.get(dI['sweep_title'],['USE_channel_'+str(ch)])) for ch in range(4)]
            Bpy_channels = [vip.get(dI['sweep_title'],'USE_channel_'+str(int(ch))) == 'USE' for ch in range(4)]
            use_channels = [ch for ch in range(4) if Bpy_channels[ch]]
            sweep_type = vip.get(dI['sweep_title'],'F__sweep_type')
            for ch in use_channels:
                if sweep_type == 'Amplitude':
                    print 'changing Amplitude'
                    vip.set(dI['sweep_instr'],{'R_amplitude_'+str(ch): iI})
                elif sweep_type == 'Offset':
                    print 'changing offset'
                    vip.set(dI['sweep_instr'],{'R_offset_'+str(ch): iI})   
            settings = vip.get(dI['sweep_instr'])
            vip.instruments[dI['sweep_instr']].waveform_from_file(settings)

    B_during_sweep = vip.get('Script', 'B_during_sweep_'+dI['index'])
    if (B_during_sweep == 'ON'):
        TITLE_script = vip.get('Script', 'script_title_'+dI['index'])
        script_dict.script_dictionary[TITLE_script](vip)

    QtCore.QCoreApplication.processEvents()

    return None


################################################################################
def bn_do_sweep(vip):
    """
    This functions is structured into five parts:
    1. Adopt the measurement insturment settings set in the VIP GUI.
    2. Create the sweep specifications dictionary. The main complication here is
    that we have to distinguish between measurements where the first sweeping is
    done be the instrument itself ("From trace") of by Python code below.
    3. Check if all settings work out and check if the instruments are
    connected. Use Python Booleans as flags (those are tagged with 'Bpy').
    4. Print all specifications to the terminal/editor.
    5. Go into the triple for loop which does measurements and runs scripts at
    the specified parameters.
    """

    ########## ########## ########## ########## ########## ########## ##########
    """
    1. Adopt the measurement insturment settings set in the VIP GUI.
    """
    meas_type  = vip.get('Meas_main', 'meas_type')
    meas_instr = vip.get(meas_type, 'F_instr_name')

    
    ### clean up meas_type session
    if meas_type in ['Freq. trace']:
        B_averaging = vip.get(meas_instr, 'B_averaging')
        if B_averaging == 'OFF':
            vip.set(meas_type, {'N_averaging' : "1"})
        else:
            print meas_type
            Nav = vip.get(meas_instr,'N_averaging')
            print Nav
            vip.set(meas_type, {'N_averaging' : str(Nav)})
    elif meas_type in ['I Q point']:
        vip.set(meas_instr, {'N_sweep_points' : "1"})

    ### update measurement instrument session with meas_type session and then
    ### adopt those instrument settings
    settings = vip._session[meas_type]
    vip.set(meas_instr, settings)
    session_events.bn_adopt_settings(vip)

    ### clean up meas_instr settings
    if meas_instr in ['FSW_1']:
        if meas_type in ['Time trace', 'Power point']:
            if vip.is_connected(meas_instr):
                vip.instruments[meas_instr].go_to_time_domain_mode()

    ########## ########## ########## ########## ########## ########## ##########
    """
    2. Create the sweep specifications dictionary (ss_dict). The main 
    complication here is
    that we have to distinguish between measurements where the first sweeping is
    done be the instrument itself ("From trace") of by Python code below.
    """
    ss_dict = {}
    vip._file_list_dict = {}
    for index in INDICES_123:
        sweep_title = vip.get('Sweep', 'sweep_title_'+index)
        Bpy_from_trace = (sweep_title == 'From trace')  
           
        [start_key, stop_key, sweep_points_key, unit_key, axis_mode_key] = TRACE_KEYS[meas_type] if Bpy_from_trace else SWEEP_KEYS            
            
        Bpy_from_file = (sweep_title == 'File sweep ' + index)    
        if Bpy_from_file:
            DIR__PATH            = vip.get(sweep_title, 'DIR__PATH')
            FILE__NAME_0         = vip.get(sweep_title, 'FILE__NAME_0')
            FILE__NAME_1         = vip.get(sweep_title, 'FILE__NAME_1')
            vip.CHANNEL__SWEEP_0 = vip.get(sweep_title, 'CHANNEL__SWEEP_0')
            vip.CHANNEL__SWEEP_1 = vip.get(sweep_title, 'CHANNEL__SWEEP_1')
            print 'CHANNEL__SWEEP'
            print vip.CHANNEL__SWEEP_0
            print vip.CHANNEL__SWEEP_1
            
            FILE_EXTENSION             = ".csv"
            vip._file_list_dict[index] = [auxi.get_file_list(DIR__PATH, FILE__NAME_0, FILE_EXTENSION)
                                         ,auxi.get_file_list(DIR__PATH, FILE__NAME_1, FILE_EXTENSION)
                                         ]
        
        _k_sweep_dict = {'From trace'                   : '~'+meas_type
                        ,'Voltage sweep'+cs.BLANK+index : '~'+'voltage_source'
                        ,'Power sweep'  +cs.BLANK+index : 'R_power_source'
                        ,'Freq. sweep'  +cs.BLANK+index : 'R_freq_source'
                        ,'Phase sweep'  +cs.BLANK+index : 'R_phas_source'
                        ,'File sweep'   +cs.BLANK+index : '~'+'AWG_channels'
                        ,'AWG sweep'    +cs.BLANK+index : '~'+'AWG_channels_param'}
        k_sweep      = _k_sweep_dict[sweep_title]
        if Bpy_from_trace:
            sweep_title = meas_type
        sweep_instr  = vip.get(sweep_title, 'F_instr_name')
        start        = float(vip.get(sweep_title, start_key))
        stop         = float(vip.get(sweep_title, stop_key))         if (not Bpy_from_file) else len(vip._file_list_dict[index][1])-1
        sweep_points = float(vip.get(sweep_title, sweep_points_key)) if (not Bpy_from_file) else len(vip._file_list_dict[index][1])
        unit         = vip.get(sweep_title, unit_key)
        axis_mode    = vip.get(sweep_title, axis_mode_key)

        ss_dict[index] = {'index'         : index
                            ,'sweep_title'   : sweep_title
                            ,'sweep_instr'   : sweep_instr
                            ,'Bpy_do_sweep'  : True
                            ,'Bpy_is_max'    : (vip.get('Sweep', 'B_is_max_'+index) == 'ON')
                            ,'Bpy_connected' : vip.is_connected(sweep_instr)
                            ,'axis'          : auxi.custom_axis(start, stop, sweep_points, axis_mode)
                            ,'unit'          : unit
                            ,'k_sweep'       : k_sweep
                            ,'label'         : k_sweep+" ["+unit+"]"
                            }
        Bpy_from_dig = (vip.get('Meas_main','meas_type') == 'Dig. sample')
        
        if Bpy_from_dig:
            filter_freq = float(vip.get(meas_instr,'R_filter_frequency'))
            if filter_freq:
                mov_av_time = int(1/(filter_freq*10**-3))
                #ss_dict[index]['axis'] = auxi.custom_axis(start+mov_av_time/2, stop-mov_av_time/2, sweep_points-mov_av_time, axis_mode)
                print 'HERE'
                ss_dict[index]['axis'] = auxi.running_mean(ss_dict[index]['axis'],mov_av_time)
    print 'Axis length'
    print len(ss_dict[index]['axis'])
    ########## ########## ########## ########## ########## ########## ##########
    """
    3. Check if all settings work out and check if the instruments are connected.
    Use Python Booleans as flags (those are tagged with 'Bpy').
    """

    Bpy_abort                       = True
    Bpy_sweep1_instr_PERFORMS_trace = (ss_dict['1']['sweep_title'] in session.Traces.keys())

    if ss_dict['3']['Bpy_is_max']:
        if ss_dict['1']['Bpy_connected'] and ss_dict['2']['Bpy_connected'] and ss_dict['3']['Bpy_connected']:
            Bpy_abort = False
            message = "(sweep_specifications) Triple sweep !!!"
        else:
            message = "!!! (sweep 3) A sweep instrument was not connected"
    else:
        ss_dict['3']['Bpy_do_sweep'] = False
        ss_dict['3']['axis'] = [404] # should be a number for the plot
        if ss_dict['2']['Bpy_is_max']:
            if ss_dict['1']['Bpy_connected'] and ss_dict['2']['Bpy_connected']:
                Bpy_abort = False
                message = "(sweep_specifications) Double sweep !!"
            else:
                message = "!!! (sweep 2) A sweep instrument was not connected"
        else:
            ss_dict['2']['Bpy_do_sweep'] = False
            ss_dict['2']['axis'] = [404] # should be a number for the plot
            if ss_dict['1']['Bpy_is_max']:
                if ss_dict['1']['Bpy_connected']:
                    Bpy_abort = False
                    message = "(sweep_specifications) Single sweep !"
                else:
                    message = "!!! (sweep 1) A sweep instrument was not connected."
            else:
                ss_dict['1']['Bpy_do_sweep'] = False
                if not Bpy_sweep1_instr_PERFORMS_trace:
                    Bpy_abort = False
                    message = "!!! You didn't even attempt to do a sweep, mate. Check the checkboxes."
                else:
                    message = "!!! Can't do single point measurement with trace instrument."
        vip.GUI_feedback([message])

    Bpy_sweep1_From_trace_SELECTED = (vip.get('Sweep', 'sweep_title_'+'1') == 'From trace')
    Bpy_Meas_main_during_sweep1    = (vip.get('Meas_main', 'B_during_sweep_1') == 'ON')

    if (Bpy_sweep1_From_trace_SELECTED or Bpy_Meas_main_during_sweep1) and not vip.is_connected(meas_instr):
        Bpy_abort = True
        print "!!! ABORT ISSUE:\n" + "Measurement insturment was not connected."
    if (Bpy_sweep1_From_trace_SELECTED and not Bpy_sweep1_instr_PERFORMS_trace) or (Bpy_sweep1_instr_PERFORMS_trace and not Bpy_sweep1_From_trace_SELECTED):
        Bpy_abort = True
        print "!!! ABORT ISSUE:\n" + "Mismatch between sweep selection and instrument."

    ########## ########## ########## ########## ########## ########## ##########
    """
    4. Print all specifications to the terminal/editor.
    """

    print 4*"\n"
    print "=== SWEEP SPECIFICATIONS ==="
    print "* meas_type:\n",  meas_type
    print "* meas_instr:\n", meas_instr
    print ""
    print "* ss_dict['1']['sweep_title']:", ss_dict['1']['sweep_title']
    print "* ss_dict['2']['sweep_title']:", ss_dict['2']['sweep_title']
    print "* ss_dict['3']['sweep_title']:", ss_dict['3']['sweep_title']
    print "* ss_dict['1']['Bpy_do_sweep']:", ss_dict['1']['Bpy_do_sweep']
    print "* ss_dict['2']['Bpy_do_sweep']:", ss_dict['2']['Bpy_do_sweep']
    print "* ss_dict['3']['Bpy_do_sweep']:", ss_dict['3']['Bpy_do_sweep']
    print "* ss_dict['1']['Bpy_connected']:", ss_dict['1']['Bpy_connected']
    print "* ss_dict['2']['Bpy_connected']:", ss_dict['2']['Bpy_connected']
    print "* ss_dict['3']['Bpy_connected']:", ss_dict['3']['Bpy_connected']
    print "* Bpy_sweep1_instr_PERFORMS_trace:\n", Bpy_sweep1_instr_PERFORMS_trace
    print "* Bpy_sweep1_From_trace_SELECTED:\n", Bpy_sweep1_From_trace_SELECTED
    print "* Bpy_Meas_main_during_sweep1:\n",  Bpy_Meas_main_during_sweep1
    print "  (optional when doing a trace trace)"
    print 4*"\n"

    ########## ########## ########## ########## ########## ########## ##########
    """
    5. Go into the triple for loop which does measurements and runs scripts at
    the specified parameters.
    """

    if Bpy_abort:
        vip.GUI_feedback(message)
        session_events.bn_open_GUI_feedback(vip)
    else:
            ########## TRACKER
            vip.reset_sweep_tracker()

            ######### PLOT
            for k_data in menus.DATA_SET_KEYS:
                for dim_key in menus.PLOT_DIM_KEYS:
                    vip.plot_data[k_data][dim_key].update({'axis_1'  : ss_dict['1']['axis']
                                                          ,'label_1' : ss_dict['1']['label']
                                                          ,'label_2' : ss_dict['2']['label']
                                                          })
            ########## BREAK
            vip.Bpy_break_loop = False     # To interrupt the measurement via stop button

            vip.GUI_feedback("Going into the sweep loop...")

            ### This try concludes with a FINALLY statement.
            ### It is enabling data to be saved even if we manually BREAK from the loop

            for index in INDICES_123:
                axis_length = len(ss_dict[index]['axis'])
                print "Axislength, Index "+index+": "+str(axis_length)

            try:
                ### -------------------- -------------------- -------------------- --------------------
                for i3 in ss_dict['3']['axis']:

                    ########## BREAK
                    if vip.Bpy_break_loop:     # To interrupt the measurement via stop button
                        message = ["! The measurement has been interrupted manually"]
                        vip.GUI_feedback(message)
                        break

                    ########## TRACKER
                    for k_data in menus.DATA_SET_KEYS:
                        vip.sweep_tracker[k_data]['3'] += 1

                    message = ["\nSweep tracker level 3:", "\n", str(vip.sweep_tracker['I_data']['3'])]
                    vip.GUI_feedback(message)

                    ########## Result Index
                    i_old = vip.get('Results', 'N_result_index')
                    i_new = int(i_old) + 1
                    vip.set('Results', {'N_result_index' : str(i_new)})

                    ########## PROGRESS BAR
                    R_step_bar = 0.0 ### init

                    ######### PLOT
                    for k_data in menus.DATA_SET_KEYS:
                        vip.plot_data[k_data]['3d_data'].update({'axis_r' : []})

                    ### Set sweep parameters and run script
                    _set_sweep_parameters_and_run_script(vip, ss_dict['3'], i3)

                    ########## TRACKER
                    for k_data in menus.DATA_SET_KEYS:
                        vip.sweep_tracker[k_data]['2'] = 0

                    ### This try concludes with a FINALLY statement.
                    ### It is enabling data to be saved even if we manually BREAK from the loop
                    try:
                        ### -------------------- -------------------- -------------------- --------------------
                        for i2 in ss_dict['2']['axis']:

                            ########## BREAK
                            if vip.Bpy_break_loop:     # To interrupt the measurement via stop button
                                message = ["! The measurement has been interrupted manually"]
                                vip.GUI_feedback(message)
                                break                      
                            
                            
                            ########## PROGRESS BAR
                            vip._ProgressBar.setValue(100 * R_step_bar / len(ss_dict['2']['axis']))
                            R_step_bar += 1.0

                            ########## TRACKER
                            for k_data in menus.DATA_SET_KEYS:
                                vip.sweep_tracker[k_data]['2'] += 1

                            message = ["\nSweep tracker level 2:", "\n","", str(vip.sweep_tracker['I_data']['2'])]
                            vip.GUI_feedback(message)

                            ### Set sweep parameters and run script
                            _set_sweep_parameters_and_run_script(vip, ss_dict['2'], i2)

                            for k_data in menus.DATA_SET_KEYS:
                                vip.sweep_tracker[k_data]['1'] = 0

                            L_I_data = []
                            L_Q_data = []
                            L_P__dBm = []
                            L_phi___ = []
                            
                            L_P_dB__ = []
                            L_phidiv = []

                            if Bpy_sweep1_From_trace_SELECTED:

                                ########## TRACKER
                                for k_data in menus.DATA_SET_KEYS:
                                    vip.sweep_tracker[k_data]['1'] = len(ss_dict['1']['axis'])

                                ### Measure!
                                L_I_data, L_Q_data, L_P__dBm, L_phi___ = vip.instruments[meas_instr].get_trace()

                                print "Postprocessing trace for\n"+meas_type+", "+meas_instr
                                
                                if meas_type == 'Freq. trace':
                                    if meas_instr in session.VNA:
                                        L_P__dBm = auxi.IQ_to_P_in_dB(L_I_data, L_Q_data) # IQ_to_P_in_dB ####### TODO THIS DOESNT WORK FOR SA YET, BECAUSE what do we want as get_trace return values?
                                        L_phi___ = auxi.phi(L_I_data, L_Q_data) # phi
                                        _P_ref = None
                                        L_P_dB__ = auxi.IQ_to_P_in_dB(L_I_data, L_Q_data, P_ref=_P_ref)
                                        L_phidiv = auxi.pairwise_difference(L_phi___)
                                        ########## PLOT
                                        for dim_key in menus.PLOT_DIM_KEYS:
                                            vip.plot_data['I_data'][dim_key].update({'label_r' : "I"})
                                            vip.plot_data['Q_data'][dim_key].update({'label_r' : "Q"})
                                            vip.plot_data['P__dBm'][dim_key].update({'label_r' : "P dBm"})
                                            vip.plot_data['phi___'][dim_key].update({'label_r' : "phi"})
                                            vip.plot_data['P__dB_'][dim_key].update({'label_r' : "P dBm"})
                                            vip.plot_data['phidiv'][dim_key].update({'label_r' : "phi prime"})
                                            
                                    if meas_instr in session.SA:
                                        L_Q_data, L_P__dBm, L_phi___, L_P_dB__, L_phidiv = L_I_data, L_I_data, L_I_data, L_I_data, L_I_data
                                        ########## PLOT
                                        for dim_key in menus.PLOT_DIM_KEYS:
                                            vip.plot_data['I_data'][dim_key].update({'label_r' : "I"})
                                            vip.plot_data['Q_data'][dim_key].update({'label_r' : "Q"})
                                            vip.plot_data['P__dBm'][dim_key].update({'label_r' : "P dBm"})
                                            vip.plot_data['phi___'][dim_key].update({'label_r' : "phi"})
                                            vip.plot_data['P__dB_'][dim_key].update({'label_r' : "P dBm"})
                                            vip.plot_data['phidiv'][dim_key].update({'label_r' : "phi prime"})
  
                                ###---------- END 'for k_data in menus.DATA_SET_KEYS:'
                                            
                                elif meas_type == 'Time trace':
                                    if meas_instr == 'FSW_1':
                                        L_Q_data, L_P__dBm, L_phi___, L_P_dB__, L_phidiv = L_I_data, L_I_data, L_I_data, L_I_data, L_I_data
                                        ########## PLOT
                                        for dim_key in menus.PLOT_DIM_KEYS:
                                            vip.plot_data['P__dBm'][dim_key].update({'label_r' : "~Time trace"})
                                            
                                ### !!! TODO: This is basically a copy of the code above. Fix it!   
                                elif meas_type == 'Dig. sample': ### TODO: Merge with freq. trace measurement?
                                    if meas_instr == 'ATS9870_1':
                                        L_P__dBm = auxi.IQ_to_P_in_dB(L_I_data, L_Q_data) 
                                        L_phi___ = auxi.phi(L_I_data, L_Q_data)
                                        _P_ref = None
                                        L_P_dB__ = auxi.IQ_to_P_in_dB(L_I_data, L_Q_data, P_ref=_P_ref)
                                        L_phidiv = auxi.pairwise_difference(L_phi___)
                                        ########## PLOT
                                        for dim_key in menus.PLOT_DIM_KEYS:
                                            vip.plot_data['I_data'][dim_key].update({'label_r' : "I"})
                                            vip.plot_data['Q_data'][dim_key].update({'label_r' : "Q"})
                                            vip.plot_data['P__dBm'][dim_key].update({'label_r' : "P dBm"})
                                            vip.plot_data['phi___'][dim_key].update({'label_r' : "phi"})
                                            vip.plot_data['P__dB_'][dim_key].update({'label_r' : "P dBm"})
                                            vip.plot_data['phidiv'][dim_key].update({'label_r' : "phi prime"})
                                           
                                else:
                                    message = "!!! Unexpected measurement type for trace!"
                                    vip.GUI_feedback(message)
                            else:
                                ### -------------------- -------------------- -------------------- --------------------
                                for i1 in ss_dict['1']['axis']:

                                    ########## BREAK
                                    if vip.Bpy_break_loop:     # To interrupt the measurement via stop button
                                        message = ["! The measurement has been interrupted manually"]
                                        vip.GUI_feedback(message)
                                        break

                                    ### Set sweep parameters and run script
                                    _set_sweep_parameters_and_run_script(vip, ss_dict['1'], i1)

                                    ########## TRACKER
                                    for k_data in menus.DATA_SET_KEYS:
                                        vip.sweep_tracker[k_data]['1'] += 1

                                    if Bpy_Meas_main_during_sweep1:
                                        _meas_types_with_locking = ['Power point', 'I Q point']
                                        if meas_type in _meas_types_with_locking:
                                            if (vip.get(meas_type, 'B_lock_to_freq') == 'ON'):
                                                for n in [1, 2, 3]:
                                                    if vip.get(meas_type, 'F_lock_to_sweep') == ss_dict[str(n)]['sweep_title']:
                                                        if n==1:   freq_val = i1
                                                        elif n==2: freq_val = i2
                                                        elif n==3: freq_val = i3
                                                        F_frequency_shift = float(vip.get(meas_type, 'F_frequency_shift'))
                                                        freq_val  = freq_val + F_frequency_shift
                                                        freq_unit = ss_dict[str(n)]['unit']    
                                                        print "! .set_center_frequency argument shifted by d={0}{1}".format(str(F_frequency_shift), freq_unit)
                                                        vip.instruments[meas_instr].set_center_frequency(freq_val, freq_unit)

                                        if meas_type in ['Power point']:
                                            ### Measure!
                                            r1 = r2 = r3 = r4 = r5 = r6 = vip.instruments[meas_instr].measure_power()
                                        elif meas_type in ['I Q point']:
                                            ### Measure!
                                            r1, r2, _, _ = vip.instruments[meas_instr].get_trace()
                                            ### This returns a list, even if for just one value, i.e. r = [value].
                                            r3 = auxi.IQ_to_P_in_dB(r1, r2) ###  P dBm
                                            r4 = auxi.phi(r1, r2)      ### phi
                                            _P_ref = None #auxi.IQ_to_P_in_dB(L_I_data, L_Q_data, P_ref=_P_ref) ### P dB
                                            r5 = auxi.IQ_to_P_in_dB(r1, r2)
                                            r6 = auxi.pairwise_difference(r4) ### phi'
                                            r1, r2, r3, r4, r5, r6 = r1[0], r2[0], r3[0], r4[0], r5[0], r6[0]
                                            ### unpack: r = [value] --> r = value

                                        L_I_data.append(r1)
                                        L_Q_data.append(r2)
                                        L_P__dBm.append(r3)
                                        L_phi___.append(r4)
                                        L_P_dB__.append(r5)
                                        L_phidiv.append(r6)

                                    ###---------- END 'if Bpy_Meas_main_during_sweep1:' 

                                ###---------- END innermost loop

                                ########## PLOT
                                if meas_type in ['Power point']:
                                    for dim_key in menus.PLOT_DIM_KEYS:
                                        for k_data in menus.DATA_SET_KEYS:
                                            vip.plot_data[k_data][dim_key].update({'label_r' : "Power"})
                                elif meas_type in ['I Q point']:
                                    pass

                            ###---------- END 'if Bpy_sweep1_From_trace_SELECTED:' else inner loop

                            vip.plot_data['I_data']['2d_data'].update({'axis_r' : L_I_data})
                            vip.plot_data['Q_data']['2d_data'].update({'axis_r' : L_Q_data})
                            vip.plot_data['P__dBm']['2d_data'].update({'axis_r' : L_P__dBm})
                            vip.plot_data['phi___']['2d_data'].update({'axis_r' : L_phi___})
                            vip.plot_data['P__dB_']['2d_data'].update({'axis_r' : L_P_dB__})
                            vip.plot_data['phidiv']['2d_data'].update({'axis_r' : L_phidiv})

                            vip.plot_data['I_data']['3d_data']['axis_r'].append(L_I_data)
                            vip.plot_data['Q_data']['3d_data']['axis_r'].append(L_Q_data)
                            vip.plot_data['P__dBm']['3d_data']['axis_r'].append(L_P__dBm)
                            vip.plot_data['phi___']['3d_data']['axis_r'].append(L_phi___)
                            vip.plot_data['P__dB_']['3d_data']['axis_r'].append(L_P_dB__)
                            vip.plot_data['phidiv']['3d_data']['axis_r'].append(L_phidiv)

                            for k_data in menus.DATA_SET_KEYS:
                                axis_2 = ss_dict['2']['axis'][:vip.sweep_tracker[k_data]['2']]
                                vip.plot_data[k_data]['3d_data'].update({'axis_2' : axis_2})

                            if not ss_dict['2']['Bpy_do_sweep']:
                                vip.update_figures(dim='2d_data')
                            else:
                                vip.update_figures()

                        ########## PROGRESS BAR
                        vip._ProgressBar.setValue(100)

                    finally:
                        ### Processing all Qt events unfreezes the user interface
                        QtCore.QCoreApplication.processEvents()

                        HLINE = 10*"%"+cs.BLANK
                        vip.result = [[HLINE+vip.plot_data['I_data']['3d_data']['label_2']], list(vip.plot_data['I_data']['3d_data']['axis_2'])
                                     ,[HLINE+vip.plot_data['I_data']['3d_data']['label_1']], list(vip.plot_data['I_data']['3d_data']['axis_1'])
                                     #,[HLINE+vip.plot_data['P__dBm']['3d_data']['label_2']], list(vip.plot_data['I_data']['3d_data']['axis_2'])
                                     #,[HLINE+vip.plot_data['P__dBm']['3d_data']['label_1']], list(vip.plot_data['I_data']['3d_data']['axis_1'])
                                     ,[HLINE+vip.plot_data['I_data']['3d_data']['label_r']], map(list, vip.plot_data['I_data']['3d_data']['axis_r'])
                                     ,[HLINE+vip.plot_data['Q_data']['3d_data']['label_r']], map(list, vip.plot_data['Q_data']['3d_data']['axis_r'])
                                     #,[HLINE+vip.plot_data['P__dBm']['3d_data']['label_r']], map(list, vip.plot_data['P__dBm']['3d_data']['axis_r'])
                                     #,[HLINE+vip.plot_data['phi___']['3d_data']['label_r']], map(list, vip.plot_data['phi___']['3d_data']['axis_r'])
                                     ]

                        session_events.bn_save_switch(vip, auxi.textfile_formatting)
                            
                        vip.GUI_feedback(["Sweep completed!"])

                        session_events.bn_open_GUI_feedback(vip)

                    ###---------- END middle loop
                    
            finally:

                ########## TRACKER
                vip.reset_sweep_tracker()                                       ### Maybe remove this? Seems unnecessary?
      
                B_find_min_ON = (vip.get('Sweep', 'B_find_min') == 'ON')
                if B_find_min_ON and vip.Bpy_redo_sweep:
                    vip.Bpy_redo_sweep = False
                    k_start = 'R_freq_start'
                    k_stop  = 'R_freq_stop'
                    settings = vip.get(meas_type)
                    if set([k_start, k_stop]).issubset(settings.keys()):
                        R_freq_start = float(settings[k_start])
                        R_freq_stop  = float(settings[k_stop])
                        span         = R_freq_stop - R_freq_start
                        vip.set(meas_type, {k_start : str(vip.minimal_x - span / 2)})
                        vip.set(meas_type, {k_stop  : str(vip.minimal_x + span / 2)})
                        bn_do_sweep(vip)
                else:
                    vip.Bpy_redo_sweep = True

                ########## CLEANUP
                for index in INDICES_123:
                    sweep_instr = ss_dict[index]['sweep_instr']
                    try:
                        settings = vip.get(sweep_instr)
                        vip.instruments[sweep_instr].set_voltage_to_zero(settings)
                    except AttributeError:
                        pass

            ###---------- END outermost loop
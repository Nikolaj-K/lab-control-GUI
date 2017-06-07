from PySide import QtGui

import dictionaries.session as session
import dictionaries.constants as cs
import interface.session_events as se
import dictionaries.menus as menus

import interface.session_widgets as sw

################################################################################

def _build_Meas_main(vip):
    tb = 'Meas_main'

    vip.content['captions'][tb]['lb'] = {}
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {'B_during_sweep_1' : "Measure during sweep 1:"}
    vip.content['events'][tb]['le'] = {}
    vip.content['events'][tb]['cb'] = {'B_during_sweep_1'   : lambda state: se.cb_toggled(vip, tb,'B_during_sweep_1')}
    vip.content['events'][tb]['dm'] = {'meas_type'    : lambda text: se.le_or_dm_change(vip, tb,'meas_type', text)}
    vip.content['events'][tb]['bn'] = {}
    vip.content['cb_vals'][tb] = {'B_during_sweep_1'  : ('ON', 'OFF')}
    vip.content['dm_vals'][tb] = {'meas_type' : session.Tree['_Routines']['Traces'].keys()+session.Tree['_Routines']['Points'].keys()}
    sw.__fill_widgets(vip, tb)

    #### ----------
    vip._qWidgets['cb'][tb]['B_during_sweep_1'].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+1))
    vip._qWidgets['dm'][tb]['meas_type'].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+1))

########## ########## hBoxs

    hBox2 = QtGui.QHBoxLayout()

    hBox2.addStretch(1)

    hBox2.addWidget(vip._qWidgets['dm'][tb]['meas_type'])
    hBox2.addStretch(1)

########## ########## vBo
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBox2)

################################################################################

def _build_Sweep(vip):
    tb = 'Sweep'

    import interface.measurement as measurement
    vip.content['captions'][tb]['lb'] = {}
    vip.content['captions'][tb]['bn'] = {'_bn_do_sweep' : cs.BLANK+"Do sweep"+cs.BLANK
                                        ,'_bn_stop'     : cs.BLANK+"Stop"+cs.BLANK
                                        }
    vip.content['captions'][tb]['cb'] = {'B_is_max_1'   : "Single sweep"
                                        ,'B_is_max_2'   : "Double sweep"
                                        ,'B_is_max_3'   : "Triple trouble"
                                        ,'B_find_min'   : "Get minimum"
                                        }
    vip.content['events'][tb]['le'] = {}
    vip.content['events'][tb]['cb'] = {'B_is_max_1'     : lambda state: se.cb_toggled(vip, tb,'B_is_max_1')
                                      ,'B_is_max_2'     : lambda state: se.cb_toggled(vip, tb,'B_is_max_2')
                                      ,'B_is_max_3'     : lambda state: se.cb_toggled(vip, tb,'B_is_max_3')
                                      ,'B_find_min'     : lambda state: se.cb_toggled(vip, tb,'B_find_min')
                                      }
    vip.content['events'][tb]['dm'] = {'sweep_title_1' : lambda text: se.le_or_dm_change(vip, tb, 'sweep_title_1', text)
                                      ,'sweep_title_2' : lambda text: se.le_or_dm_change(vip, tb, 'sweep_title_2', text)
                                      ,'sweep_title_3' : lambda text: se.le_or_dm_change(vip, tb, 'sweep_title_3', text)
                                      }
    vip.content['events'][tb]['bn'] = {'_bn_do_sweep'   : lambda: measurement.bn_do_sweep(vip)
                                      ,'_bn_stop'       : lambda: se.bn_block_measurement(vip)
                                      }
    vip.content['cb_vals'][tb] = {'B_is_max_1'          : ('ON', 'OFF')
                                 ,'B_is_max_2'          : ('ON', 'OFF')
                                 ,'B_is_max_3'          : ('ON', 'OFF')
                                 ,'B_find_min'          : ('ON', 'OFF')
                                 }
    vip.content['dm_vals'][tb] = {'sweep_title_1'      : session.Tree['_Sweeps']['Sweep_1'].keys()
                                 ,'sweep_title_2'      : session.Tree['_Sweeps']['Sweep_2'].keys()
                                 ,'sweep_title_3'      : session.Tree['_Sweeps']['Sweep_3'].keys()
                                 }
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE+1)

    #### ----------
    for k in ['_bn_do_sweep']:
        vip._qWidgets['bn'][tb][k].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+4))
        vip._qWidgets['bn'][tb][k].adjustSize()
    for k in ['_bn_stop']:
        vip._qWidgets['bn'][tb][k].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+2))
        vip._qWidgets['bn'][tb][k].adjustSize()
    for k in vip.content['captions'][tb]['cb'].keys():
        vip._qWidgets['cb'][tb][k].setFixedWidth(200)
        vip._qWidgets['cb'][tb][k].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+1))

########## ########## hBoxs
    _RANGE3 = ['1', '2', '3']
    hBoxs = {k : QtGui.QHBoxLayout() for k in ['S', 'P']+_RANGE3}
    hBoxs['_B_find_min'] = QtGui.QHBoxLayout()

    hBoxs['S'].addStretch(1)
    hBoxs['S'].addWidget(vip._qWidgets['bn'][tb]['_bn_do_sweep'])
    hBoxs['S'].addWidget(vip._qWidgets['bn'][tb]['_bn_stop'])
    hBoxs['S'].addStretch(1)

    hBoxs['_B_find_min'].addWidget(vip._qWidgets['cb'][tb]['B_find_min'])
    hBoxs['_B_find_min'].addStretch(1)

    hBoxs['P'].addStretch(1)
    hBoxs['P'].addWidget(vip._qWidgets['qw']['Meas_main']) ###
    hBoxs['P'].addStretch(1)

    for i in _RANGE3:
        hBoxs[i].addStretch(1)
        hBoxs[i].addWidget(vip._qWidgets['cb'][tb]['B_is_max_'+i])
        hBoxs[i].addWidget(vip._qWidgets['dm'][tb]['sweep_title_'+i])
        hBoxs[i].addStretch(1)

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['S'])
    vBox.addLayout(hBoxs['_B_find_min'])
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(hBoxs['P'])
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(hBoxs['1'])
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(hBoxs['2'])
    vBox.addLayout(hBoxs['3'])


################################################################################

def _build_Script(vip):
    tb = 'Script'

    import dictionaries.script_dict as script_dict
    vip.content['captions'][tb]['lb'] = {}
    vip.content['captions'][tb]['bn'] = {'_bn_run_script'  : " Run script 3 now "}
    vip.content['captions'][tb]['cb'] = {'B_during_sweep_1'  : "Add to sweep 1"
                                        ,'B_during_sweep_2'  : "Add to sweep 2"
                                        ,'B_during_sweep_3'  : "Add to sweep 3"
                                        }

    vip.content['events'][tb]['le'] = {}
    vip.content['events'][tb]['cb'] = {'B_during_sweep_1' : lambda state: se.cb_toggled(vip, tb, 'B_during_sweep_1')
                                      ,'B_during_sweep_2' : lambda state: se.cb_toggled(vip, tb, 'B_during_sweep_2')
                                      ,'B_during_sweep_3' : lambda state: se.cb_toggled(vip, tb, 'B_during_sweep_3')
                                      }
    vip.content['events'][tb]['dm'] = {'script_title_1'   : lambda text: se.le_or_dm_change(vip, tb,'script_title_1', text)
                                      ,'script_title_2'   : lambda text: se.le_or_dm_change(vip, tb,'script_title_2', text)
                                      ,'script_title_3'   : lambda text: se.le_or_dm_change(vip, tb,'script_title_3', text)
                                      }
    vip.content['events'][tb]['bn'] = {'_bn_run_script' : lambda: se.bn_run_script(vip, '3')}

    vip.content['cb_vals'][tb] = {'B_during_sweep_1' : ('ON', 'OFF')
                                 ,'B_during_sweep_2' : ('ON', 'OFF')
                                 ,'B_during_sweep_3' : ('ON', 'OFF')
                                 }
    vip.content['dm_vals'][tb] = {'script_title_1' : script_dict.script_dictionary.keys()
                                 ,'script_title_2' : script_dict.script_dictionary.keys()
                                 ,'script_title_3' : script_dict.script_dictionary.keys()
                                 }

    sw.__fill_widgets(vip, tb)

    #### ----------
    for k in ['_bn_run_script']:
        vip._qWidgets['bn'][tb][k].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+2))
        vip._qWidgets['bn'][tb][k].adjustSize()
    for k in vip.content['captions'][tb]['cb'].keys():
        vip._qWidgets['cb'][tb][k].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+1))

########## ########## hBoxs

    _string_range_3 = [str(i) for i in range(1,4)]

    hBox = {i : QtGui.QHBoxLayout() for i in _string_range_3+["__run"]}

    for i in _string_range_3:
        hBox[i].addWidget(vip._qWidgets['dm'][tb]['script_title_'+i])
        hBox[i].addWidget(vip._qWidgets['cb'][tb]['B_during_sweep_'+i])

    hBox["__run"].addStretch(1)
    hBox["__run"].addWidget(vip._qWidgets['bn'][tb]['_bn_run_script'])
    hBox["__run"].addStretch(1)

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    for i in _string_range_3:
        vBox.addLayout(hBox[i])
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(hBox['__run'])
    vBox.addLayout(vip._blanks.next())

################################################################################

def _build_From_trace(vip):
    """This small tab is basically a dummy and as it contains only one label,
    I refrain from setting up all the content dictionaries and do it directly
    """
    sk = 'From trace'

    text = "Find the settings for different\ntrace measurements below."
    __label_widget = QtGui.QLabel(text)
    __label_widget.setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE-2))
    __label_widget.adjustSize()

########## ########## hBoxs
    hBox = QtGui.QHBoxLayout()

    hBox.addStretch(.1)

    hBox.addWidget(__label_widget)
    hBox.addStretch(.1)

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][sk])

    vBox.addLayout(hBox)

################################################################################

def _build_Freq_trace(vip):
    tb = 'Freq. trace'

    vip.content['captions'][tb]['lb'] = {'F_instr_name'     : "Instrument:"+10*cs.BLANK
                                        ,'N_sweep_points'   : "Sweep points:"+6*cs.BLANK
                                        ,'R_freq_start'     : "Start frequency:"+3*cs.BLANK
                                        ,'R_freq_stop'      : "Stop frequency:"+3*cs.BLANK
                                        ,'_R_freq_center'   : "Center frequency:"
                                        ,'_R_freq_span'     : "Frequency span:"+2*cs.BLANK
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}

    vip.content['events'][tb]['le'] = {'R_freq_start'    : lambda text: se.le_pow_vs_freq_start(vip, tb, text)
                                      ,'R_freq_stop'     : lambda text: se.le_pow_vs_freq_stop(vip, tb, text)
                                      ,'_R_freq_center'  : lambda text: se.le_pow_vs_freq_center(vip, tb, text)
                                      ,'_R_freq_span'    : lambda text: se.le_pow_vs_freq_span(vip, tb, text)
                                      ,'N_sweep_points'  : lambda text: se.le_or_dm_change(vip, tb, 'N_sweep_points', text)
                                      }
    vip.content['events'][tb]['dm'] = {'F_instr_name' : lambda text: se.le_or_dm_change(vip, tb, 'F_instr_name' , text)
                                      ,'F_unit_freq'  : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_freq' , text)
                                     }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}

    vip.content['dm_vals'][tb] = {'F_instr_name'   : session.instr_classification['VNA']+session.instr_classification['SA']
                                 ,'F_unit_freq'    : menus.FREQUENCY_UNITS
                                 }

    ### ----------
    ### set up two extra line edits (with event functions that affect other line edits)
    R_freq_start = float(session.default[tb]['R_freq_start'])
    R_freq_stop  = float(session.default[tb]['R_freq_stop'])
    vip.auxiliary_le[tb]['_R_freq_span']   = str((R_freq_start-R_freq_stop))
    vip.auxiliary_le[tb]['_R_freq_center'] = str((R_freq_start+R_freq_stop)/2)

    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-2)

    ### to guarantee preference, manually re-write the following
    ### line edit values with the default session
    settings = {'R_freq_start' : session.default[tb]['R_freq_start']
               ,'R_freq_stop'  : session.default[tb]['R_freq_stop']
               }
    vip.set(tb, settings)

########## ########## hBoxs

    le_ks = ['N_sweep_points'
            ,'R_freq_start'
            ,'R_freq_stop'
            ,'_R_freq_center'
            ,'_R_freq_span'
            ]
    dm_ks = ['F_instr_name']
    hBoxs_ks = dm_ks+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBoxs_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    hBoxs['F_instr_name'].addWidget(vip._qWidgets['lb'][tb]['F_instr_name'])
    hBoxs['F_instr_name'].addStretch(1)
    hBoxs['F_instr_name'].addWidget(vip._qWidgets['dm'][tb]['F_instr_name'])

    hBoxs['R_freq_start'].addWidget(vip._qWidgets['dm'][tb]['F_unit_freq'])

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['F_instr_name'])

    keysB = ['N_sweep_points'
            ,'R_freq_start'
            ,'R_freq_stop'
            ,'_R_freq_center'
            ,'_R_freq_span'
            ]
    for key in keysB:
        vBox.addLayout(hBoxs[key])

################################################################################

def _build_Time_trace(vip):
    tb = 'Time trace'

    vip.content['captions'][tb]['lb'] = {'F_instr_name'   : "Instrument:"+10*cs.BLANK
                                        ,'R_time_stop'      : "Sweep time:"+8*cs.BLANK
                                        ,'N_sweep_points' : "Sweep points:"+6*cs.BLANK
                                        ,'_R_freq_center' : "Center frequency:"
                                        ,'R_freq_start'   : "Start frequency:"+3*cs.BLANK
                                        ,'R_freq_stop'    : "Stop frequency:"+3*cs.BLANK
                                        ,'_R_freq_span'   : "Frequency span:"+2*cs.BLANK
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}

    vip.content['events'][tb]['le'] = {'R_freq_start'    : lambda text: se.le_pow_vs_freq_start(vip, tb, text)
                                      ,'R_freq_stop'     : lambda text: se.le_pow_vs_freq_stop(vip, tb, text)
                                      ,'_R_freq_center'  : lambda text: se.le_pow_vs_freq_center(vip, tb, text)
                                      ,'_R_freq_span'    : lambda text: se.le_pow_vs_freq_span(vip, tb, text)
                                      ,'N_sweep_points'  : lambda text: se.le_or_dm_change(vip, tb, 'N_sweep_points', text)
                                      ,'R_time_stop'     : lambda text: se.le_or_dm_change(vip, tb, 'R_time_stop', text)
                                      }
    vip.content['events'][tb]['dm'] = {'F_instr_name' : lambda text: se.le_or_dm_change(vip, tb, 'F_instr_name' , text)
                                      ,'F_unit_time'  : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_time' , text)
                                      ,'F_unit_freq'  : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_freq' , text)
                                      }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}

    vip.content['dm_vals'][tb] = {'F_instr_name' : session.instr_classification['SA']
                                 ,'F_unit_time'  : menus.TIME_UNITS
                                 ,'F_unit_freq'  : menus.FREQUENCY_UNITS
                                 }

    ### ----------
    ### set up two extra line edits (with event functions that affect other line edits)
    R_freq_start = float(session.default[tb]['R_freq_start'])
    R_freq_stop  = float(session.default[tb]['R_freq_stop'])
    vip.auxiliary_le[tb]['_R_freq_span']   = str((R_freq_start-R_freq_stop))
    vip.auxiliary_le[tb]['_R_freq_center'] = str((R_freq_start+R_freq_stop)/2)

    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

    ### to guarantee preference, manually re-write the following
    ### line edit values with the default session
    tmp = session.default[tb]['R_freq_start']
    settings = {'R_freq_start' : tmp
               ,'R_freq_stop'  : tmp
               }
    vip.set(tb, settings)

########## ########## hBoxs

    le_ks =   ['N_sweep_points'
              ,'R_time_stop'
              ,'_R_freq_center'
              ]
    dm_ks = ['F_instr_name']
    hBoxs_ks = dm_ks+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBoxs_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])

    hBoxs['R_time_stop'].addWidget(vip._qWidgets['dm'][tb]['F_unit_time'])

    hBoxs['_R_freq_center'].addWidget(vip._qWidgets['dm'][tb]['F_unit_freq'])

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['F_instr_name'])

    keysB = ['N_sweep_points'
            ,'R_time_stop'
            ,'_R_freq_center'
            ]
    for k in keysB:
        vBox.addLayout(hBoxs[k])



################################################################################

def _build_Dig_sample(vip):
    tb = 'Dig. sample'

    vip.content['captions'][tb]['lb'] = {'F_instr_name'              : "Instrument:"+10*cs.BLANK
                                        ,'N_samples_factor'          : "Post trigger samples 64*:"+1*cs.BLANK
                                        ,'N_records_per_buffer'      : "Records per buffer:"+8*cs.BLANK
                                        ,'N_buffers_per_acquisition' : "Buffers per acquisition:"+8*cs.BLANK
                                        ,'F_decimation'              : "Decimation:"+1*cs.BLANK
                                        ,'_N_sweep_points'           : "size = init"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}

    vip.content['events'][tb]['le'] = {'N_samples_factor'          : lambda text: se.le_or_dm_change__N_sweep_points(vip, tb, 'N_samples_factor', text)
                                      ,'N_records_per_buffer'      : lambda text: se.le_or_dm_change(vip, tb, 'N_records_per_buffer', text)
                                      ,'N_buffers_per_acquisition' : lambda text: se.le_or_dm_change(vip, tb, 'N_buffers_per_acquisition', text)
                                      }
    vip.content['events'][tb]['dm'] = {'F_instr_name' : lambda text: se.le_or_dm_change(vip, tb, 'F_instr_name' , text)
                                      ,'F_decimation' : lambda text: se.le_or_dm_change__N_sweep_points(vip, tb, 'F_decimation', text)
                                      }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}

    vip.content['dm_vals'][tb] = {'F_instr_name' : session.instr_classification['Dig']
                                 ,'F_decimation' : menus.ATS9870['F_decimation'].keys()
                                 }

    ### ----------
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

########## ########## hBoxs

    le_ks =   ['N_samples_factor'
              ,'N_records_per_buffer'
              ,'N_buffers_per_acquisition'
              ]
    dm_ks = ['F_instr_name'
            ,'F_decimation'
            ]
    hBoxs_ks = dm_ks+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBoxs_ks}

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(1)
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    hBoxs['N_samples_factor'].addWidget(vip._qWidgets['lb'][tb]['_N_sweep_points'])


########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['F_instr_name'])

    keysB = hBoxs_ks
    for k in keysB:
        vBox.addLayout(hBoxs[k])


################################################################################

def _build_Power_point(vip):
    from interface.session_widgets import sweep_ks
    
    tb = 'Power point'

    vip.content['captions'][tb]['lb'] = {'F_instr_name' : "Measurement instrument:"
                                        ,'F_frequency_shift' : "Frequency shift:"
                                        ,'_lb_unit_freq' : "[see sweep]"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {'B_lock_to_freq'  : "Lock center frequency to:"}

    vip.content['events'][tb]['le'] = {'F_frequency_shift' : lambda text: se.le_or_dm_change(vip, tb, 'F_frequency_shift', text)}
    vip.content['events'][tb]['dm'] = {'F_instr_name' : lambda text: se.le_or_dm_change(vip, tb, 'F_instr_name', text)
                                      ,'F_lock_to_sweep' : lambda text: se.le_or_dm_change(vip, tb, 'F_lock_to_sweep', text)
                                      }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {'B_lock_to_freq' : lambda state: se.cb_toggled(vip, tb, 'B_lock_to_freq')}

    vip.content['cb_vals'][tb] = {'B_lock_to_freq'  : ('ON' , 'OFF')}
    vip.content['dm_vals'][tb] = {'F_instr_name' : session.instr_classification['SA'] # session.instr_classification['SG']+session.instr_classification['VNA']+
                                 ,'F_lock_to_sweep' : sweep_ks('Freq.') # session.instr_classification['SG']+session.instr_classification['VNA']+
                                 }

    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

########## ########## hBoxs
    
    dm_ks = ['F_instr_name']
    le_ks = ['F_frequency_shift']
    cb_ks = ['_F_lock_to_sweep']

    ks = dm_ks + cb_ks + le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in ks}
    
    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    hBoxs['F_frequency_shift'].addWidget(vip._qWidgets['lb'][tb]['_lb_unit_freq'])

    for k in ['F_instr_name']:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])

    hBoxs['_F_lock_to_sweep'].addWidget(vip._qWidgets['cb'][tb]['B_lock_to_freq'])
    hBoxs['_F_lock_to_sweep'].addStretch(.1)
    hBoxs['_F_lock_to_sweep'].addWidget(vip._qWidgets['dm'][tb]['F_lock_to_sweep'])

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])
    
    for k in ks:
        vBox.addLayout(hBoxs[k])
        vBox.addLayout(hBoxs[k])
        vBox.addLayout(hBoxs[k])

################################################################################

def _build_I_Q_point(vip):
    from interface.session_widgets import sweep_ks

    tb = 'I Q point'

    vip.content['captions'][tb]['lb'] = {'F_instr_name' : "Measurement instrument:"
                                        ,'F_frequency_shift' : "Frequency shift:"
                                        ,'_lb_unit_freq' : "[see sweep]"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {'B_lock_to_freq'  : "Lock center frequency to:"}

    vip.content['events'][tb]['le'] = {'F_frequency_shift' : lambda text: se.le_or_dm_change(vip, tb, 'F_frequency_shift', text)}
    vip.content['events'][tb]['dm'] = {'F_instr_name' : lambda text: se.le_or_dm_change(vip, tb, 'F_instr_name', text)
                                      ,'F_lock_to_sweep' : lambda text: se.le_or_dm_change(vip, tb, 'F_lock_to_sweep', text)
                                      }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {'B_lock_to_freq' : lambda state: se.cb_toggled(vip, tb, 'B_lock_to_freq')}

    vip.content['cb_vals'][tb] = {'B_lock_to_freq'  : ('ON' , 'OFF')}
    vip.content['dm_vals'][tb] = {'F_instr_name' : session.instr_classification['VNA'] # session.instr_classification['SG']+session.instr_classification['VNA']+
                                 ,'F_lock_to_sweep' : sweep_ks('Freq.') # session.instr_classification['SG']+session.instr_classification['VNA']+
                                 }

    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

########## ########## hBoxs

    
    dm_ks = ['F_instr_name']
    le_ks = ['F_frequency_shift']
    cb_ks = ['_F_lock_to_sweep']

    ks = dm_ks + cb_ks + le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in ks}
    
    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    hBoxs['F_frequency_shift'].addWidget(vip._qWidgets['lb'][tb]['_lb_unit_freq'])

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])

    hBoxs['_F_lock_to_sweep'].addWidget(vip._qWidgets['cb'][tb]['B_lock_to_freq'])
    hBoxs['_F_lock_to_sweep'].addStretch(.1)
    hBoxs['_F_lock_to_sweep'].addWidget(vip._qWidgets['dm'][tb]['F_lock_to_sweep'])

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    for k in ks:
        vBox.addLayout(hBoxs[k])
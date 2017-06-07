from PySide import QtGui

import dictionaries.session as session
import dictionaries.constants as cs
import interface.session_events as se
import dictionaries.menus as menus

import interface.session_widgets as sw

################################################################################

def _build_Power_sweep(vip, tb):
    ### the values associated with the keywords with __ are not writen to the
    ### instrument tabs (only sweeped over in the measurement)
    sweep_quadruple = ['R__start'
                      ,'R__stop'
                      ,'N__sweep_points'
                      ,'R_AUXI_power_step_size'
                      ]

    vip.content['captions'][tb]['lb'] = {'F_instr_name'                : "Instrument:"+1*cs.BLANK
                                        ,'F_axis_mode'                 : "Axis mode:"+2*cs.BLANK
                                        ,'R__start'                    : "Start power:"+3*cs.BLANK
                                        ,'R__stop'                     : "Stop power:"+3*cs.BLANK
                                        ,'N__sweep_points'             : "Sweep points:"
                                        ,'_lb_power_step_size'         : "Step size:"+7*cs.BLANK
                                        ,'R_AUXI_power_step_size'      : ""
                                        ,'F_AUXI_power_star_unit'      : cs.BLANK+"dBm"+3*cs.BLANK
                                        ,'F_AUXI_power_stop_unit'      : cs.BLANK+"dBm"+3*cs.BLANK
                                        ,'F_AUXI_power_step_size_unit' : cs.BLANK+"dBm"+3*cs.BLANK
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}
    vip.content['events'][tb]['le'] = {'R__start'        : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'R__start'       , text)
                                      ,'R__stop'         : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'R__stop'        , text)
                                      ,'N__sweep_points' : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'N__sweep_points', text)
                                      }
    vip.content['events'][tb]['dm'] = {'F_instr_name'    : lambda text: se.le_or_dm_change(vip, tb, 'F_instr_name', text)
                                      ,'F_axis_mode'    : lambda text: se.le_or_dm_change(vip, tb, 'F_axis_mode', text)
                                      }
    vip.content['events'][tb]['cb'] = {}
    vip.content['events'][tb]['bn'] = {}
    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {'F_instr_name' : session.instr_classification['VNA']+session.instr_classification['SG']
                                 ,'F_axis_mode'  : menus.AXIS_MODES
                                 }
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

    ### ----------
    vip._qWidgets['lb'][tb][sweep_quadruple[3]].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE))
    se._fun_change_step_size_value_label(vip, tb, sweep_quadruple)

########## ########## hBoxs
    le_ks = ['R__start'
            ,'R__stop'
            ,'N__sweep_points'
            ]
    dm_ks = ['F_instr_name', 'F_axis_mode']
    hBoxs_ks = dm_ks+['__lb_power_step_size']+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBoxs_ks}

    for k in le_ks:
        for w in ['lb', 'le']:
            hBoxs[k].addWidget(vip._qWidgets[w][tb][k])

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])
    hBoxs['R__start'].addWidget(vip._qWidgets['lb'][tb]['F_AUXI_power_star_unit'])
    hBoxs['R__stop'].addWidget(vip._qWidgets['lb'][tb]['F_AUXI_power_stop_unit'])
    hBoxs['__lb_power_step_size'].addWidget(vip._qWidgets['lb'][tb]['_lb_power_step_size'])
    hBoxs['__lb_power_step_size'].addWidget(vip._qWidgets['lb'][tb]['R_AUXI_power_step_size'])
    hBoxs['__lb_power_step_size'].addStretch(1)
    hBoxs['__lb_power_step_size'].addWidget(vip._qWidgets['lb'][tb]['F_AUXI_power_step_size_unit'])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    for k in dm_ks:
        vBox.addLayout(hBoxs[k])
    for key in le_ks:
        vBox.addLayout(hBoxs[key])
    vBox.addLayout(hBoxs['__lb_power_step_size'])

################################################################################

def _build_Freq_sweep(vip, tb):
    ### the values associated with the keywords with __ are not writen to the
    ### instrument tabs (only sweeped over in the measurement)
    sweep_quadruple = ['R__start'
                      ,'R__stop'
                      ,'N__sweep_points'
                      ,'R_AUXI_freq_step_size'
                      ]

    vip.content['captions'][tb]['lb'] = {'F_instr_name'          : "Instrument:"+1*cs.BLANK
                                        ,'F_axis_mode'                 : "Axis mode:"+2*cs.BLANK
                                        ,'R__start'              : "Start frequency:"+3*cs.BLANK
                                        ,'R__stop'               : "Stop frequency:"+3*cs.BLANK
                                        ,'N__sweep_points'       : "Sweep points:"+5*cs.BLANK
                                        ,'_lb_freq_step_size'    : "Step size:"+12*cs.BLANK
                                        ,'R_AUXI_freq_step_size' : "init"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}
    vip.content['events'][tb]['le'] =   {'R__start'        : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'R__start'       , text)
                                        ,'R__stop'         : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'R__stop'        , text)
                                        ,'N__sweep_points' : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'N__sweep_points', text)
                                        }
    vip.content['events'][tb]['dm'] = {'F_instr_name'      : lambda text: se.le_or_dm_change(vip, tb, 'F_instr_name' , text)
                                      ,'F__unit_sweep'     : lambda text: se.le_or_dm_change(vip, tb, 'F__unit_sweep', text)
                                      ,'F_axis_mode'     : lambda text: se.le_or_dm_change(vip, tb, 'F_axis_mode', text)
                                      }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}

    vip.content['dm_vals'][tb] = {'F_axis_mode'  : menus.AXIS_MODES
                                 ,'F__unit_sweep' : menus.FREQUENCY_UNITS
                                 ,'F_instr_name'  : session.instr_classification['SG']
                                 }

    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

    ### ----------
    se._fun_change_step_size_value_label(vip, tb, sweep_quadruple)
    vip._qWidgets['lb'][tb][sweep_quadruple[3]].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE))

########## ########## hBoxs

    le_ks = ['R__start'
            ,'R__stop'
            ,'N__sweep_points'
            ]
    dm_ks = ['F_instr_name', 'F_axis_mode']
    hBoxs_ks = dm_ks+['__lb_freq_step_size']+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBoxs_ks}

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])
    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])
    hBoxs['__lb_freq_step_size'].addWidget(vip._qWidgets['lb'][tb]['_lb_freq_step_size'])
    hBoxs['__lb_freq_step_size'].addWidget(vip._qWidgets['lb'][tb]['R_AUXI_freq_step_size'])
    hBoxs['__lb_freq_step_size'].addStretch(.1)

    hBoxs['R__start'].addWidget(vip._qWidgets['dm'][tb]['F__unit_sweep'])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])
    
    for k in dm_ks:
        vBox.addLayout(hBoxs[k])
    for k in le_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(hBoxs['__lb_freq_step_size'])


################################################################################

def _build_Phase_sweep(vip, tb):
    ### the values associated with the keywords with __ are not writen to the
    ### instrument tabs (only sweeped over in the measurement)
    sweep_quadruple = ['R__start'
                      ,'R__stop'
                      ,'N__sweep_points'
                      ,'R_AUXI_freq_step_size'
                      ]

    vip.content['captions'][tb]['lb'] = {'F_instr_name'          : "Instrument:"+1*cs.BLANK
                                        ,'F_axis_mode'           : "Axis mode:"+2*cs.BLANK
                                        ,'R__start'              : "Start phase:"+3*cs.BLANK
                                        ,'R__stop'               : "Stop phase:"+3*cs.BLANK
                                        ,'N__sweep_points'       : "Sweep points:"+5*cs.BLANK
                                        ,'_lb_freq_step_size'    : "Step size:"+12*cs.BLANK
                                        ,'R_AUXI_freq_step_size' : "init"
                                        ,'_lb_unit_sweep' : '~Degree'
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}
    vip.content['events'][tb]['le'] =   {'R__start'        : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'R__start'       , text)
                                        ,'R__stop'         : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'R__stop'        , text)
                                        ,'N__sweep_points' : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'N__sweep_points', text)
                                        }
    vip.content['events'][tb]['dm'] = {'F_instr_name'      : lambda text: se.le_or_dm_change(vip, tb, 'F_instr_name' , text)
                                      ,'F_axis_mode'       : lambda text: se.le_or_dm_change(vip, tb, 'F_axis_mode', text)
                                     }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}

    vip.content['dm_vals'][tb] = {'F_instr_name'  : session.instr_classification['SG']
                                 ,'F_axis_mode'  : menus.AXIS_MODES
                                 }

    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

    ### ----------
    se._fun_change_step_size_value_label(vip, tb, sweep_quadruple)
    vip._qWidgets['lb'][tb][sweep_quadruple[3]].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE))

########## ########## hBoxs

    le_ks = ['R__start'
            ,'R__stop'
            ,'N__sweep_points'
            ]
    dm_ks = ['F_instr_name', 'F_axis_mode']
    hBoxs_ks = dm_ks+['__lb_freq_step_size']+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBoxs_ks}

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])
    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])
    hBoxs['__lb_freq_step_size'].addWidget(vip._qWidgets['lb'][tb]['_lb_freq_step_size'])
    hBoxs['__lb_freq_step_size'].addWidget(vip._qWidgets['lb'][tb]['R_AUXI_freq_step_size'])
    hBoxs['__lb_freq_step_size'].addStretch(.1)

    hBoxs['R__start'].addWidget(vip._qWidgets['lb'][tb]['_lb_unit_sweep'])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])
    
    for k in dm_ks:
        vBox.addLayout(hBoxs[k])
    for k in le_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(hBoxs['__lb_freq_step_size'])


################################################################################

def _build_Voltage_sweep(vip, tb):
    ### the values associated with the keywords with __ are not writen to the instrument tabs
    ### (only sweeped over in the measurement)
    sweep_quadruple = ['R__start'
                      ,'R__stop'
                      ,'N__sweep_points'
                      ,'R_AUXI_volt_step_size'
                      ]

    vip.content['captions'][tb]['lb'] = {'R__start'              : "Start voltage:"+3 *cs.BLANK
                                        ,'F_axis_mode'           : "Axis mode:"+2*cs.BLANK
                                        ,'R__stop'               : "Stop voltage:" +4 *cs.BLANK
                                        ,'N__sweep_points'       : "Sweep points:" +3 *cs.BLANK
                                        ,'_lb_volt_step_size'    : "Step size:"    +12*cs.BLANK
                                        ,'R_AUXI_volt_step_size' : "init"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}
    vip.content['events'][tb]['le'] =   {'R__start'        : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'R__start'       , text)
                                        ,'R__stop'         : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'R__stop'        , text)
                                        ,'N__sweep_points' : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'N__sweep_points', text)
                                        }
    vip.content['events'][tb]['dm'] = {'F_axis_mode'    : lambda text: se.le_or_dm_change(vip, tb, 'F_axis_mode', text)}
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}
    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {'F_axis_mode'  : menus.AXIS_MODES}
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

    ### ----------
    se._fun_change_step_size_value_label(vip, tb, sweep_quadruple)
    vip._qWidgets['lb'][tb][sweep_quadruple[3]].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE))

########## ########## hBoxs
    le_ks = ['R__start'
            ,'R__stop'
            ,'N__sweep_points']
    dm_ks = ['F_axis_mode']
    hBoxs_ks = dm_ks+['__lb_volt_step_size']+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBoxs_ks}

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])
    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])
    hBoxs['__lb_volt_step_size'].addWidget(vip._qWidgets['lb'][tb]['_lb_volt_step_size'])
    hBoxs['__lb_volt_step_size'].addWidget(vip._qWidgets['lb'][tb]['R_AUXI_volt_step_size'])
    hBoxs['__lb_volt_step_size'].addStretch(.1)

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    for k in dm_ks:
        vBox.addLayout(hBoxs[k])
    for k in le_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(hBoxs['__lb_volt_step_size'])

################################################################################
def _build_AWG_sweep(vip, tb):
    ### the values associated with the keywords with __ are not writen to the instrument tabs
    ### (only sweeped over in the measurement)

    ### Note: At the moment, H3344 is the only AWG and it has 4 channels (indexed by 0,1,2,3),
    ### and so is the range implemented here. In case there comes a AWG with more channels,
    ### a few things must be adjusted here. 
    ### Also, if there are different AWGs with different numbers of channels, that might make things unsafe.
    from dictionaries.hardware import range_H3344_channels as channels_list

    sweep_quadruple = ['R__start'
                      ,'R__stop'
                      ,'N__sweep_points'
                      ,'R_AUXI_volt_step_size'
                      ]

    vip.content['captions'][tb]['lb'] = {'R__start'              : "Start voltage:"+3 *cs.BLANK
                                        ,'R__stop'               : "Stop voltage:" +4 *cs.BLANK
                                        ,'N__sweep_points'       : "Sweep points:" +3 *cs.BLANK
                                        ,'_lb_volt_step_size'    : "Step size:"    +12*cs.BLANK
                                        ,'R_AUXI_volt_step_size' : "init"
                                        ,'USE_channel_'         : "Apply to"
                                        ,'F__sweep_type'         : "Sweep"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {'USE_channel_'+ch : ch for ch in channels_list}   
                                           
    vip.content['events'][tb]['le'] =   {'R__start'        : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'R__start'       , text)
                                        ,'R__stop'         : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'R__stop'        , text)
                                        ,'N__sweep_points' : lambda text: se.le_sweep_quadruple(vip, tb, sweep_quadruple, 'N__sweep_points', text)
                                        }
    vip.content['events'][tb]['dm'] = {'F__sweep_type'     : lambda text: se.le_or_dm_change(vip, tb, 'F__sweep_type' , text)
                                      }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {'USE_channel_0'        : lambda state: se.cb_toggled(vip, tb, 'USE_channel_0')
                                      ,'USE_channel_1'        : lambda state: se.cb_toggled(vip, tb, 'USE_channel_1')
                                      ,'USE_channel_2'        : lambda state: se.cb_toggled(vip, tb, 'USE_channel_2')
                                      ,'USE_channel_3'        : lambda state: se.cb_toggled(vip, tb, 'USE_channel_3')
                                      }
    ### I'm not sure if the following shorter function assignment might not make problems:
    #vip.content['events'][tb]['cb'] = {'USE_channel_'+ch : lambda state: se.cb_toggled(vip, tb, 'USE_channel_'+ch) for ch in channels_list}     
    vip.content['cb_vals'][tb] = {'USE_channel_'+ch : ('USE', 'DONT_USE') for ch in channels_list}      
    vip.content['dm_vals'][tb] = {'F__sweep_type'  : ['Amplitude', 'Offset']
                                 }
    
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

    ### ----------
    se._fun_change_step_size_value_label(vip, tb, sweep_quadruple)
    vip._qWidgets['lb'][tb][sweep_quadruple[3]].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE))

########## ########## hBoxs
    le_ks = ['R__start'
            ,'R__stop'
            ,'N__sweep_points']
    hBoxs_ks = ['USE_channel_']+['F__sweep_type']+['__lb_volt_step_size']+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBoxs_ks}


    hBoxs['USE_channel_'].addWidget(vip._qWidgets['lb'][tb]['USE_channel_'])
    for ch in range(4):
         hBoxs['USE_channel_'].addWidget(vip._qWidgets['cb'][tb]['USE_channel_'+str(ch)])

    hBoxs['F__sweep_type'].addWidget(vip._qWidgets['lb'][tb]['F__sweep_type'])
    hBoxs['F__sweep_type'].addWidget(vip._qWidgets['dm'][tb]['F__sweep_type'])
    
    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])
    hBoxs['__lb_volt_step_size'].addWidget(vip._qWidgets['lb'][tb]['_lb_volt_step_size'])
    hBoxs['__lb_volt_step_size'].addWidget(vip._qWidgets['lb'][tb]['R_AUXI_volt_step_size'])
    hBoxs['__lb_volt_step_size'].addStretch(.1)

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])
    vBox.addLayout(hBoxs['USE_channel_'])    
    vBox.addLayout(hBoxs['F__sweep_type'])
    for k in le_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(hBoxs['__lb_volt_step_size'])
    vBox.addLayout(hBoxs['F__sweep_type'])

################################################################################

def _build_File_sweep(vip, tb):
                    
    vip.content['captions'][tb]['lb'] = {'DIR__PATH'   : "Dir. path:"+3 *cs.BLANK
                                        ,'FILE__NAME_0' : 4 *cs.BLANK + "File name:" 
                                        ,'CHANNEL__SWEEP_0' : 'Channel'+4 *cs.BLANK
                                        ,'FILE__NAME_1' :  4 *cs.BLANK + "File name:" 
                                        ,'CHANNEL__SWEEP_1' : 'Channel'+4 *cs.BLANK
                                        }                    
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}
    vip.content['events'][tb]['le'] =   {'DIR__PATH'            : lambda text: se.le_or_dm_change(vip, tb, 'DIR__PATH'       , text)
                                        ,'FILE__NAME_0'         : lambda text: se.le_or_dm_change(vip, tb, 'FILE__NAME_0'    , text)
                                        ,'FILE__NAME_1'         : lambda text: se.le_or_dm_change(vip, tb, 'FILE__NAME_1'    , text)
                                        }
    vip.content['events'][tb]['dm'] = {'CHANNEL__SWEEP_0'      : lambda text: se.le_or_dm_change(vip, tb, 'CHANNEL__SWEEP_0', text)
                                      ,'CHANNEL__SWEEP_1'      : lambda text: se.le_or_dm_change(vip, tb, 'CHANNEL__SWEEP_1', text)
                                      }                                              
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}
    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {'CHANNEL__SWEEP_0'  : ['0','1','2','3']
                                 ,'CHANNEL__SWEEP_1'  : ['0','1','2','3']
                                 }
                                 
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

    ### ----------

########## ########## hBoxs
    le_ks = ['DIR__PATH'
            ,'CHANNEL__SWEEP_0'
            ,'FILE__NAME_0'
            ,'CHANNEL__SWEEP_1'
            ,'FILE__NAME_1']
            
    hBoxs_ks = le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBoxs_ks}
    
    hBoxs['DIR__PATH'].addWidget(vip._qWidgets['lb'][tb]['DIR__PATH'])
    hBoxs['DIR__PATH'].addWidget(vip._qWidgets['le'][tb]['DIR__PATH'])
    
    for k in range(2):
        hBoxs['CHANNEL__SWEEP_'+str(k)].addWidget(vip._qWidgets['lb'][tb]['CHANNEL__SWEEP_'+str(k)])
        hBoxs['FILE__NAME_'+str(k)].addWidget(vip._qWidgets['dm'][tb]['CHANNEL__SWEEP_'+str(k)])
        hBoxs['FILE__NAME_'+str(k)].addWidget(vip._qWidgets['lb'][tb]['FILE__NAME_'+str(k)])
        hBoxs['FILE__NAME_'+str(k)].addWidget(vip._qWidgets['le'][tb]['FILE__NAME_'+str(k)])


########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    for k in le_ks:
        vBox.addLayout(hBoxs[k])
        
        
        
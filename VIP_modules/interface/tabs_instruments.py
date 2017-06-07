from PySide import QtGui

import dictionaries.session as session
import dictionaries.constants as cs
import interface.session_events as se
import dictionaries.menus as menus
import dictionaries.addresses as addresses

import interface.session_widgets as sw

import dictionaries.hardware as hardware


################################################################################
def _build_RTE1054(vip, tb):
    vip.content['captions'][tb]['lb'] = {'N_sweep_points'   : "Sweep points:"
                                        ,'N_resolution'     : "Resolution [pico s]:"
                                        }
    vip.content['captions'][tb]['bn'] = {'S_get_info'       : cs.INSTRUMENT_INFO_LABEL
                                        }
    vip.content['captions'][tb]['cb'] = {'B_connect'        : 'Connect "{0}"'.format(addresses.address_dict[tb])
                                        }

    vip.content['events'][tb]['le'] = {'N_sweep_points'     : lambda text: se.le_or_dm_change__N_time_range(vip, tb, 'N_sweep_points', text)
                                      ,'N_resolution'       : lambda text: se.le_or_dm_change__N_time_range(vip, tb, 'N_resolution'  , text)}
    vip.content['events'][tb]['dm'] = {}
    vip.content['events'][tb]['bn'] = {'S_get_info'         : lambda: se.bn_get_info(vip, tb)}
    vip.content['events'][tb]['cb'] = {'B_connect'          : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                      }
    vip.content['cb_vals'][tb] = {'B_connect'               : ('TRY', 'DONT')
                                 }
    vip.content['dm_vals'][tb] = {}
    sw.__fill_widgets(vip, tb)

########## ########## hBoxs
    le_ks = ['N_sweep_points', 'N_resolution']
    cb_ks = ['B_connect']
    bn_ks = ['S_get_info']
    hBox_ks = bn_ks+le_ks+cb_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch()
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in cb_ks:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])

    for k in bn_ks:
        hBoxs[k].addWidget(vip._qWidgets['bn'][tb][k])
        hBoxs[k].addStretch(1)

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['B_connect'])

    vBox.addLayout(hBoxs['S_get_info'])
    vBox.addLayout(vip._blanks.next())

    for k in le_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())

    vBox.addStretch(1)

################################################################################
def _build_Santec_TSL_550(vip, tb):
    vip.content['captions'][tb]['lb'] = {'R_Wave_value' : "Laser wavelength (nm):"
                                        ,'R_Freq_value' : "Laser frequency (THz):"
                                        ,'R_Pow_dBm_value' : "Laser power (dBm):"
                                        ,'R_Pow_mW_value' : "Laser power (mW):"
                                        ,'F_dBm_or_mW' : "Used unit for optical power:"
                                        ,'F_freq_or_wave' : "Use Freq. or Wavel.:"
                                        }
    vip.content['captions'][tb]['bn'] = {'S_get_info'       : cs.INSTRUMENT_INFO_LABEL
                                        }
    vip.content['captions'][tb]['cb'] = {'B_connect'        : 'Connect "{0}"'.format(addresses.address_dict[tb])
                                        ,'B_Shutter'        : "Shutter open"
                                        }

    vip.content['events'][tb]['le'] = {'R_Wave_value'  : lambda text: se.le_or_dm_change(vip, tb, 'R_Wave_value', text)
                                      ,'R_Freq_value'  : lambda text: se.le_or_dm_change(vip, tb, 'R_Freq_value', text)
                                      ,'R_Pow_dBm_value'  : lambda text: se.le_or_dm_change(vip, tb, 'R_Pow_dBm_value', text)
                                      ,'R_Pow_mW_value'  : lambda text: se.le_or_dm_change(vip, tb, 'R_Pow_mW_value', text)
                                      }
    vip.content['events'][tb]['dm'] = {'F_freq_or_wave' : lambda text: se.le_or_dm_change(vip, tb, 'F_freq_or_wave', text)
                                      ,'F_dBm_or_mW' : lambda text: se.le_or_dm_change(vip, tb, 'F_dBm_or_mW', text)}
    vip.content['events'][tb]['bn'] = {'S_get_info'         : lambda: se.bn_get_info(vip, tb)}
    vip.content['events'][tb]['cb'] = {'B_connect'          : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                      ,'B_Shutter'          : lambda state: se.cb_toggled(vip, tb, 'B_Shutter')
                                      }
    vip.content['cb_vals'][tb] = {'B_connect'               : ('TRY', 'DONT')
                                 ,'B_Shutter'               : ('SO', 'SC')
                                 }
    vip.content['dm_vals'][tb] = {'F_freq_or_wave' : ['FREQ', 'WAVE']
                                 ,'F_dBm_or_mW' : ['DBM', 'MW']}
    sw.__fill_widgets(vip, tb)

########## ########## hBoxs
    lb_ks = []
    le_ks = ['R_Wave_value', 'R_Freq_value', 'R_Pow_dBm_value','R_Pow_mW_value']
    cb_ks = ['B_connect','B_Shutter']
    bn_ks = ['S_get_info']
    dm_ks = ['F_freq_or_wave','F_dBm_or_mW']
    hBox_ks = lb_ks+bn_ks+le_ks+cb_ks+dm_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(1)
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])

    for k in cb_ks:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])

    for k in bn_ks:
        hBoxs[k].addWidget(vip._qWidgets['bn'][tb][k])
        hBoxs[k].addStretch(1)

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['B_connect'])

    vBox.addLayout(hBoxs['S_get_info'])
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(hBoxs['B_Shutter'])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(hBoxs['F_freq_or_wave'])

#    for k in le_ks:
#        if k == 'R_Pow_dBm_value':
#            vBox.addLayout(vip._blanks.next())
#        vBox.addLayout(hBoxs[k])

    for k in ['R_Wave_value', 'R_Freq_value']:
        vBox.addLayout(hBoxs[k])


    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(hBoxs['F_dBm_or_mW'])

    for k in ['R_Pow_dBm_value','R_Pow_mW_value']:
        vBox.addLayout(hBoxs[k])

    vBox.addStretch(1)

################################################################################
def _build_Thorlabs_PM100D(vip, tb):
    vip.content['captions'][tb]['lb'] = {'N_averaging' : "Averaging bins:"
                                        }
    vip.content['captions'][tb]['bn'] = {'S_get_info'       : cs.INSTRUMENT_INFO_LABEL
                                        }
    vip.content['captions'][tb]['cb'] = {'B_connect'        : 'Connect "{0}"'.format(addresses.address_dict[tb])
                                        }

    vip.content['events'][tb]['le'] = {'N_averaging'  : lambda text: se.le_or_dm_change(vip, tb, 'N_averaging', text)
                                      }
    vip.content['events'][tb]['dm'] = {}
    vip.content['events'][tb]['bn'] = {'S_get_info'         : lambda: se.bn_get_info(vip, tb)}
    vip.content['events'][tb]['cb'] = {'B_connect'          : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                      }
    vip.content['cb_vals'][tb] = {'B_connect'               : ('TRY', 'DONT')
                                 }
    vip.content['dm_vals'][tb] = {}
    sw.__fill_widgets(vip, tb)

########## ########## hBoxs
    le_ks = ['N_averaging']
    cb_ks = ['B_connect']
    bn_ks = ['S_get_info']
    hBox_ks = bn_ks+le_ks+cb_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch()
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in cb_ks:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])

    for k in bn_ks:
        hBoxs[k].addWidget(vip._qWidgets['bn'][tb][k])
        hBoxs[k].addStretch(1)

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['B_connect'])

    vBox.addLayout(hBoxs['S_get_info'])
    vBox.addLayout(vip._blanks.next())

    for k in le_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())

    vBox.addStretch(1)

################################################################################
def _build_WM1210(vip, tb):
    vip.content['captions'][tb]['lb'] = {'R_sleep_time'  : "Sleep time:"
                                        ,'R_dWavelength' : "dWavelength:"
                                        ,'R_dPower'      : "dPower:"
                                        ,'S_device_key'  : 'Device key ... ' + vip.get(tb, 'S_device_key') ### At the moment, this is static
                                        }
    vip.content['captions'][tb]['bn'] = {'S_get_info'       : cs.INSTRUMENT_INFO_LABEL
                                        }
    vip.content['captions'][tb]['cb'] = {'B_connect'        : 'Connect !!! not implemented yet'
                                        }

    vip.content['events'][tb]['le'] = {'R_sleep_time'  : lambda text: se.le_or_dm_change(vip, tb, 'R_sleep_time', text)
                                      ,'R_dWavelength' : lambda text: se.le_or_dm_change(vip, tb, 'R_dWavelength', text)
                                      ,'R_dPower'  : lambda text: se.le_or_dm_change(vip, tb, 'R_dPower', text)
                                      }
    vip.content['events'][tb]['dm'] = {}
    vip.content['events'][tb]['bn'] = {'S_get_info'         : lambda: se.bn_get_info(vip, tb)}
    vip.content['events'][tb]['cb'] = {'B_connect'          : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                      }
    vip.content['cb_vals'][tb] = {'B_connect'               : ('TRY', 'DONT')
                                 }
    vip.content['dm_vals'][tb] = {}
    sw.__fill_widgets(vip, tb)

########## ########## hBoxs
    lb_ks = ['S_device_key'
            ]
    le_ks = ['R_sleep_time'
            ,'R_dWavelength'
            ,'R_dPower'
            ]
    cb_ks = ['B_connect']
    bn_ks = ['S_get_info']
    hBox_ks = lb_ks+bn_ks+le_ks+cb_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in lb_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch()

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch()
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in cb_ks:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])

    for k in bn_ks:
        hBoxs[k].addWidget(vip._qWidgets['bn'][tb][k])
        hBoxs[k].addStretch(1)

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['B_connect'])
    vBox.addLayout(hBoxs['S_device_key'])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(hBoxs['S_get_info'])
    vBox.addLayout(vip._blanks.next())

    for k in le_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())

    vBox.addStretch(1)

################################################################################
def _build_NI_DAQ(vip, tb):
    vip.content['captions'][tb]['lb'] = {'N_buffers_per_acquisition'   : "N_buffers_per_acquisition"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {'B_connect' : "Connect"
                                        }

    vip.content['events'][tb]['le'] = {'N_buffers_per_acquisition'     : lambda text: se.le_or_dm_change(vip, tb, 'N_buffers_per_acquisition', text)
                                      }
    vip.content['events'][tb]['dm'] = {
                                      }
    vip.content['events'][tb]['bn'] = {
                                      }
    vip.content['events'][tb]['cb'] = {'B_connect' : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                      }
    vip.content['cb_vals'][tb] = {'B_connect' : ('TRY', 'DONT')
                                 }
    vip.content['dm_vals'][tb] = {
                                 }

    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE+1)

########## ########## hBoxs
    le_ks = ['N_buffers_per_acquisition'
            ]
    cb_ks = ['B_connect'
            ]
    bn_ks = []
    dm_ks = []
    hBox_ks = bn_ks + le_ks + cb_ks + dm_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in cb_ks:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['B_connect'])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(hBoxs['N_buffers_per_acquisition'])

################################################################################
def _build_NI_DAQ_source(vip, tb):
    vip.content['captions'][tb]['lb'] = {'N_records_per_buffer'   : "N_records_per_buffer"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}

    vip.content['events'][tb]['le'] = {'N_records_per_buffer'     : lambda text: se.le_or_dm_change(vip, tb, 'N_records_per_buffer', text)
                                      }
    vip.content['events'][tb]['dm'] = {}
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}
    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {}

    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE+1)

########## ########## hBoxs
    le_ks = ['N_records_per_buffer']
    cb_ks = []
    bn_ks = []
    dm_ks = []
    hBox_ks = bn_ks + le_ks + cb_ks + dm_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in cb_ks:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['N_records_per_buffer'])

################################################################################
def _build_SGS100A(vip, tb):
    vip.content['captions'][tb]['lb'] = {'R_power_source'   : "Source power:"+5*cs.BLANK
                                        ,'R_phas_source'    : "Source phase:"+5*cs.BLANK
                                        ,'R_freq_source'    : "Source frequency:"
                                        ,'_S_unit_power'    : cs.BLANK+"dBm"+4*cs.BLANK
                                        }
    vip.content['captions'][tb]['bn'] = {'S_get_info'       : cs.INSTRUMENT_INFO_LABEL
                                        }
    vip.content['captions'][tb]['cb'] = {'B_output'         : "Source turned on"
                                        ,'B_reference_osci' : "Set reference oscillator to internal"
                                        ,'B_connect'        : 'Connect "{0}"'.format(addresses.address_dict[tb])
                                        }

    vip.content['events'][tb]['le'] = {'R_power_source'     : lambda text: se.le_or_dm_change(vip, tb, 'R_power_source', text)
                                      ,'R_phas_source'     : lambda text: se.le_or_dm_change(vip, tb, 'R_phas_source', text)
                                      ,'R_freq_source'      : lambda text: se.le_or_dm_change(vip, tb, 'R_freq_source' , text)
                                      }
    vip.content['events'][tb]['dm'] = {'F_unit_freq_source' : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_freq_source', text)}
    vip.content['events'][tb]['bn'] = {'S_get_info'         : lambda: se.bn_get_info(vip, tb)}
    vip.content['events'][tb]['cb'] = {'B_output'           : lambda state: se.cb_toggled(vip, tb, 'B_output')
                                      ,'B_reference_osci'   : lambda state: se.cb_toggled(vip, tb, 'B_reference_osci')
                                      ,'B_connect'          : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                      }
    vip.content['cb_vals'][tb] = {'B_output'                : ('ON', 'OFF')
                                 ,'B_reference_osci'        : ('INT', 'EXT')
                                 ,'B_connect'               : ('TRY', 'DONT')
                                 }
    vip.content['dm_vals'][tb] = {'F_unit_freq_source' : menus.FREQUENCY_UNITS}

    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE+1)

########## ########## hBoxs
    le_ks = ['R_power_source'
            ,'R_freq_source'
            ,'R_phas_source'
            ]
    cb_ks = ['B_connect'
            ,'B_output'
            ,'B_reference_osci'
            ]
    bn_ks = ['S_get_info']
    dm_ks = []
    hBox_ks = bn_ks + le_ks + cb_ks + dm_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in cb_ks:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    hBoxs['R_power_source'].addWidget(vip._qWidgets['lb'][tb]['_S_unit_power'])
    hBoxs['R_freq_source'].addWidget(vip._qWidgets['dm'][tb]['F_unit_freq_source'])
    hBoxs['S_get_info'].addWidget(vip._qWidgets['bn'][tb]['S_get_info'])
    hBoxs['S_get_info'].addStretch(1)

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['B_connect'])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(hBoxs['S_get_info'])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(hBoxs['B_output'])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(hBoxs['R_power_source'])
    vBox.addLayout(hBoxs['R_freq_source'])
    vBox.addLayout(hBoxs['R_phas_source'])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(hBoxs['B_reference_osci'])

################################################################################
def _build_ZNB20(vip, tb):
    vip.content['captions'][tb]['lb'] = {'R_freq_start'     : "Start frequency:"+3*cs.BLANK
                                        ,'R_freq_stop'      : "Stop frequency:"+3*cs.BLANK
                                        ,'R_power_source'   : "Source power:"+5*cs.BLANK
                                        ,'N_sweep_points'   : "Sweep points:"+6*cs.BLANK
                                        ,'N_averaging'      : "Averaging bins:"+4*cs.BLANK
                                        ,'R_bandwidth'      : "Bandwidth:"+10*cs.BLANK
                                        ,'R_freq_source'    : "Source frequency:"
                                        ,'F_Sij'            : "Matrix element:"+4*cs.BLANK
                                        ,'_unit_sour_powe'  : cs.BLANK+"dBm"+3*cs.BLANK
                                        }
    vip.content['captions'][tb]['bn'] = {'S_get_info'       : cs.INSTRUMENT_INFO_LABEL}
    vip.content['captions'][tb]['cb'] = {'B_averaging'      : "Averaging ON"
                                        ,'B_reference_osci' : "Set reference oscillator to internal"
                                        ,'B_connect'        : 'Connect "{0}"'.format(addresses.address_dict[tb])
                                        }
    vip.content['events'][tb]['le'] =   {'R_freq_start'     : lambda text: se.le_or_dm_change(vip, tb, 'R_freq_start'      , text)
                                        ,'R_freq_stop'      : lambda text: se.le_or_dm_change(vip, tb, 'R_freq_stop'       , text)
                                        ,'R_power_source'   : lambda text: se.le_or_dm_change(vip, tb, 'R_power_source'    , text)
                                        ,'N_sweep_points'   : lambda text: se.le_or_dm_change(vip, tb, 'N_sweep_points'    , text)
                                        ,'R_bandwidth'      : lambda text: se.le_or_dm_change(vip, tb, 'R_bandwidth'       , text)
                                        ,'N_averaging'      : lambda text: se.le_or_dm_change(vip, tb, 'N_averaging'       , text)
                                        ,'R_freq_source'    : lambda text: se.le_or_dm_change(vip, tb, 'R_freq_source'   , text)
                                        }
    vip.content['events'][tb]['cb'] =   {'B_averaging'      : lambda state: se.cb_toggled(vip, tb, 'B_averaging')
                                        ,'B_reference_osci' : lambda state: se.cb_toggled(vip, tb, 'B_reference_osci')
                                        ,'B_connect'        : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                        }
    vip.content['events'][tb]['dm'] = {'F_unit_freq_source' : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_freq_source', text)
                                      ,'F_unit_freq'        : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_freq' , text)
                                      ,'F_unit_bandwidth'   : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_bandwidth'  , text)
                                      ,'F_Sij'              : lambda text: se.le_or_dm_change(vip, tb, 'F_Sij'             , text)
                                      }
    vip.content['events'][tb]['bn'] =   {'S_get_info'       : lambda: se.bn_get_info(vip, tb)}
    vip.content['cb_vals'][tb] =        {'B_averaging'      : ('ON' , 'OFF')
                                        ,'B_reference_osci' : ('INT', 'EXT')
                                        ,'B_connect'        : ('TRY', 'DONT')
                                        }
    vip.content['dm_vals'][tb] =      {'F_unit_freq_source' : menus.FREQUENCY_UNITS
                                      ,'F_unit_freq'        : menus.FREQUENCY_UNITS
                                      ,'F_unit_bandwidth'   : menus.FREQUENCY_UNITS
                                      ,'F_Sij'              : menus.MATRIX_ELEMENTS_4x4
                                      }
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

########## ########## hBoxs
    le_ks = ['R_freq_start'
            ,'R_freq_stop'
            ,'R_power_source'
            ,'N_sweep_points'
            ,'R_bandwidth'
            ,'N_averaging'
            ,'R_freq_source'
            ]
    hBox_ks = ['B_connect'
              ,'S_get_info'
              ,'B_reference_osci'
              ,'F_Sij'
              ]+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    hBoxs['S_get_info'].addWidget(vip._qWidgets['bn'][tb]['S_get_info'])
    hBoxs['S_get_info'].addStretch(.1)

    hBoxs['R_power_source'].addWidget(vip._qWidgets['lb'][tb]['_unit_sour_powe'])
    hBoxs['B_connect'].addWidget(vip._qWidgets['cb'][tb]['B_connect'])
    hBoxs['B_reference_osci'].addWidget(vip._qWidgets['cb'][tb]['B_reference_osci'])
    hBoxs['N_averaging'].addWidget(vip._qWidgets['cb'][tb]['B_averaging'])
    hBoxs['R_freq_start'].addWidget(vip._qWidgets['dm'][tb]['F_unit_freq'])
    hBoxs['R_bandwidth'].addWidget(vip._qWidgets['dm'][tb]['F_unit_bandwidth'])
    hBoxs['R_freq_source'].addWidget(vip._qWidgets['dm'][tb]['F_unit_freq_source'])

    hBoxs['F_Sij'].addWidget(vip._qWidgets['lb'][tb]['F_Sij'])
    hBoxs['F_Sij'].addWidget(vip._qWidgets['dm'][tb]['F_Sij'])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox_ks1 = ['F_Sij'
               ,'R_power_source'
               ,'N_averaging'
               ,'R_bandwidth'
               ,'R_freq_source'
               ,'B_reference_osci'
               ,'N_sweep_points'
               ]
    vBox_ks2 = ['R_freq_start'
               ,'R_freq_stop']

    vBox.addLayout(hBoxs['B_connect'])
    vBox.addLayout(hBoxs['S_get_info'])
    for key in vBox_ks1:
        vBox.addLayout(hBoxs[key])
    vBox.addLayout(hBoxs['R_freq_start'])
    for key in vBox_ks2:
        vBox.addLayout(hBoxs[key])

################################################################################
def _build_ZVL13(vip, tb):
    vip.content['captions'][tb]['lb'] = {'R_freq_start'     : "Start frequency:"+3*cs.BLANK
                                        ,'R_freq_stop'      : "Stop frequency:"+3*cs.BLANK
                                        ,'R_power_source'   : "Source power:"+5*cs.BLANK
                                        ,'N_sweep_points'   : "Sweep points:"+6*cs.BLANK
                                        ,'N_averaging'      : "Averaging bins:"+4*cs.BLANK
                                        ,'R_bandwidth'      : "Bandwidth:"+10*cs.BLANK
                                        ,'R_freq_source'    : "Source frequency:"
                                        ,'F_Sij'            : "Matrix element:"+4*cs.BLANK
                                        ,'_unit_sour_powe'  : cs.BLANK+"dBm"+3*cs.BLANK
                                        }
    vip.content['captions'][tb]['bn'] = {'S_get_info'       : cs.INSTRUMENT_INFO_LABEL}
    vip.content['captions'][tb]['cb'] = {'B_averaging'      : "Averaging ON"
                                        ,'B_reference_osci' : "Set reference oscillator to internal"
                                        ,'B_connect'        : 'Connect "{0}"'.format(addresses.address_dict[tb])
                                        }
    vip.content['events'][tb]['le'] =   {'R_freq_start'     : lambda text: se.le_or_dm_change(vip, tb, 'R_freq_start'      , text)
                                        ,'R_freq_stop'      : lambda text: se.le_or_dm_change(vip, tb, 'R_freq_stop'       , text)
                                        ,'R_power_source'   : lambda text: se.le_or_dm_change(vip, tb, 'R_power_source'    , text)
                                        ,'N_sweep_points'   : lambda text: se.le_or_dm_change(vip, tb, 'N_sweep_points'    , text)
                                        ,'R_bandwidth'      : lambda text: se.le_or_dm_change(vip, tb, 'R_bandwidth'       , text)
                                        ,'N_averaging'      : lambda text: se.le_or_dm_change(vip, tb, 'N_averaging'       , text)
                                        ,'R_freq_source'    : lambda text: se.le_or_dm_change(vip, tb, 'R_freq_source'   , text)
                                        }
    vip.content['events'][tb]['cb'] =   {'B_averaging'      : lambda state: se.cb_toggled(vip, tb, 'B_averaging')
                                        ,'B_reference_osci' : lambda state: se.cb_toggled(vip, tb, 'B_reference_osci')
                                        ,'B_connect'        : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                        }
    vip.content['events'][tb]['dm'] = {'F_unit_freq_source' : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_freq_source', text)
                                      ,'F_unit_freq'        : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_freq' , text)
                                      ,'F_unit_bandwidth'   : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_bandwidth'  , text)
                                      ,'F_Sij'              : lambda text: se.le_or_dm_change(vip, tb, 'F_Sij'             , text)
                                      }
    vip.content['events'][tb]['bn'] =   {'S_get_info'       : lambda: se.bn_get_info(vip, tb)}
    vip.content['cb_vals'][tb] =        {'B_averaging'      : ('ON' , 'OFF')
                                        ,'B_reference_osci' : ('INT', 'EXT')
                                        ,'B_connect'        : ('TRY', 'DONT')
                                        }
    vip.content['dm_vals'][tb] =      {'F_unit_freq_source' : menus.FREQUENCY_UNITS
                                      ,'F_unit_freq'        : menus.FREQUENCY_UNITS
                                      ,'F_unit_bandwidth'   : menus.FREQUENCY_UNITS
                                      ,'F_Sij'              : menus.MATRIX_ELEMENTS_2x2
                                      }
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

########## ########## hBoxs
    le_ks = ['R_freq_start'
            ,'R_freq_stop'
            ,'R_power_source'
            ,'N_sweep_points'
            ,'R_bandwidth'
            ,'N_averaging'
            ,'R_freq_source'
            ]
    hBox_ks = ['B_connect'
              ,'S_get_info'
              ,'B_reference_osci'
              ,'F_Sij'
              ]+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    hBoxs['S_get_info'].addWidget(vip._qWidgets['bn'][tb]['S_get_info'])
    hBoxs['S_get_info'].addStretch(.1)

    hBoxs['R_power_source'].addWidget(vip._qWidgets['lb'][tb]['_unit_sour_powe'])
    hBoxs['B_connect'].addWidget(vip._qWidgets['cb'][tb]['B_connect'])
    hBoxs['B_reference_osci'].addWidget(vip._qWidgets['cb'][tb]['B_reference_osci'])
    hBoxs['N_averaging'].addWidget(vip._qWidgets['cb'][tb]['B_averaging'])
    hBoxs['R_freq_start'].addWidget(vip._qWidgets['dm'][tb]['F_unit_freq'])
    hBoxs['R_bandwidth'].addWidget(vip._qWidgets['dm'][tb]['F_unit_bandwidth'])
    hBoxs['R_freq_source'].addWidget(vip._qWidgets['dm'][tb]['F_unit_freq_source'])

    hBoxs['F_Sij'].addWidget(vip._qWidgets['lb'][tb]['F_Sij'])
    hBoxs['F_Sij'].addWidget(vip._qWidgets['dm'][tb]['F_Sij'])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox_ks1 = ['F_Sij'
               ,'R_power_source'
               ,'N_averaging'
               ,'R_bandwidth'
               ,'R_freq_source'
               ,'B_reference_osci'
               ,'N_sweep_points'
               ]
    vBox_ks2 = ['R_freq_start'
               ,'R_freq_stop']

    vBox.addLayout(hBoxs['B_connect'])
    vBox.addLayout(hBoxs['S_get_info'])
    for key in vBox_ks1:
        vBox.addLayout(hBoxs[key])
    vBox.addLayout(hBoxs['R_freq_start'])
    for key in vBox_ks2:
        vBox.addLayout(hBoxs[key])

################################################################################
def _build_FSW(vip, tb):
    vip.content['captions'][tb]['lb'] = {'R_freq_start'     : "Start frequency:"+3*cs.BLANK
                                        ,'R_time_stop'      : "Sweep time:"+8*cs.BLANK
                                        ,'R_freq_stop'      : "Stop frequency:"+3*cs.BLANK
                                        ,'N_sweep_points'   : "Sweep points:"+6*cs.BLANK
                                        ,'N_averaging'      : "Averaging bins:"+4*cs.BLANK
                                        ,'R_bandwidth'      : "Bandwidth:"+10*cs.BLANK
                                        ,'F_averaging_type' : "Averaging type:"+3*cs.BLANK
                                        ,'F_averaging_mode' : "Averaging mode:"+1*cs.BLANK
                                        #,'R_power_source'   : "Source power:"+5*cs.BLANK
                                        #,'R_freq_source'    : "Source frequency:"
                                        #,'F_Sij'            : "Matrix element:"+4*cs.BLANK
                                        #,'_unit_sour_powe'  : cs.BLANK+"dBm"+3*cs.BLANK
                                        }
    vip.content['captions'][tb]['bn'] = {'S_get_info'       : cs.INSTRUMENT_INFO_LABEL}
    vip.content['captions'][tb]['cb'] = {'B_reference_osci' : "Set reference oscillator to internal"
                                        ,'B_continous'      : "Continous"
                                        ,'B_power_meas'     : "Power meas"
                                        ,'B_connect'        : 'Connect "{0}"'.format(addresses.address_dict[tb])
                                        ,'B_averaging'      : "Averaging ON"
                                        }
    vip.content['events'][tb]['le'] =   {'R_freq_start'     : lambda text: se.le_or_dm_change(vip, tb, 'R_freq_start'      , text)
                                        ,'R_freq_stop'      : lambda text: se.le_or_dm_change(vip, tb, 'R_freq_stop'       , text)
                                        ,'N_sweep_points'   : lambda text: se.le_or_dm_change(vip, tb, 'N_sweep_points'    , text)
                                        ,'R_time_stop'      : lambda text: se.le_or_dm_change(vip, tb, 'R_time_stop'      , text)
                                        ,'R_bandwidth'      : lambda text: se.le_or_dm_change(vip, tb, 'R_bandwidth'       , text)
                                        ,'N_averaging'      : lambda text: se.le_or_dm_change(vip, tb, 'N_averaging'       , text)
                                        #,'R_power_source'   : lambda text: se.le_or_dm_change(vip, tb, 'R_power_source'    , text)
                                        #,'R_freq_source'    : lambda text: se.le_or_dm_change(vip, tb, 'R_freq_source'   , text)
                                        }
    vip.content['events'][tb]['cb'] =   {'B_reference_osci' : lambda state: se.cb_toggled(vip, tb, 'B_reference_osci')
                                        ,'B_connect'        : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                        ,'B_averaging'      : lambda state: se.cb_toggled(vip, tb, 'B_averaging')
                                        }
    vip.content['events'][tb]['dm'] = {'F_unit_freq'  : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_freq' , text)
                                      ,'F_unit_bandwidth'   : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_bandwidth'  , text)
                                      ,'F_unit_time'  : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_time'  , text)
                                      ,'F_averaging_type'   : lambda text: se.le_or_dm_change(vip, tb, 'F_averaging_type'  , text)
                                      ,'F_averaging_mode'   : lambda text: se.le_or_dm_change(vip, tb, 'F_averaging_mode'  , text)
                                      ,# 'F_unit_freq_source' : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_freq_source', text)
                                      # 'F_Sij'              : lambda text: se.le_or_dm_change(vip, tb, 'F_Sij'             , text)
                                      }
    vip.content['events'][tb]['bn'] =   {'S_get_info'       : lambda: se.bn_get_info(vip, tb)}
    vip.content['cb_vals'][tb] =        {'B_reference_osci' : ('INT', 'EXT')
                                        ,'B_continous'      : ('ON', 'OFF')
                                        ,'B_power_meas'     : ('ON', 'OFF')
                                        ,'B_connect'        : ('TRY', 'DONT')
                                        ,'B_averaging'      : ('ON' , 'OFF')
                                        }
    vip.content['dm_vals'][tb] =      {'F_unit_freq'        : menus.FREQUENCY_UNITS
                                      ,'F_unit_bandwidth'   : menus.FREQUENCY_UNITS
                                      ,'F_unit_time'        : menus.TIME_UNITS
                                      ,'F_averaging_type'   : ['LINear', 'VIDeo', 'POWer']
                                      ,'F_averaging_mode'   : ['RMS', 'AVER']
                                      #,'F_unit_freq_source' : menus.FREQUENCY_UNITS
                                      #,'F_Sij'              : menus.MATRIX_ELEMENTS_4x4
                                      }
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-1)

########## ########## hBoxs
    le_ks = ['R_freq_start'
            ,'R_freq_stop'
            #,'R_power_source'
            ,'R_time_stop'
            ,'R_bandwidth'
            ,'N_averaging'
            #,'R_freq_source'
            ,'N_sweep_points'
            ]
    dm_ks = ['F_averaging_type'
              ,'F_averaging_mode'
              ]
    ck_keys = ['B_connect'
              ,'B_averaging'
              ,'B_continous'
              ,'B_power_meas'
              ,'B_reference_osci'
              ] # 'F_Sij'
    hBox_ks = ['S_get_info']+ck_keys+le_ks+dm_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])
    #hBoxs['R_power_source'].addWidget(vip._qWidgets['lb'][tb]['_unit_sour_powe'])
    for k in ck_keys:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])
    hBoxs['N_averaging'].addWidget(vip._qWidgets['cb'][tb]['B_averaging'])
    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])
    hBoxs['R_freq_start'].addWidget(vip._qWidgets['dm'][tb]['F_unit_freq'])
    hBoxs['R_time_stop'].addWidget(vip._qWidgets['dm'][tb]['F_unit_time'])
    hBoxs['R_bandwidth'].addWidget(vip._qWidgets['dm'][tb]['F_unit_bandwidth'])
    #hBoxs['R_freq_source'].addWidget(vip._qWidgets['dm'][tb]['F_unit_freq_source'])
    #hBoxs['F_Sij'].addWidget(vip._qWidgets['lb'][tb]['F_Sij'])
    #hBoxs['F_Sij'].addStretch(1)
    #hBoxs['F_Sij'].addWidget(vip._qWidgets['dm'][tb]['F_Sij'])
    hBoxs['F_averaging_type'].addWidget(vip._qWidgets['cb'][tb]['B_continous'])
    hBoxs['F_averaging_mode'].addWidget(vip._qWidgets['cb'][tb]['B_power_meas'])
    hBoxs['S_get_info'].addWidget(vip._qWidgets['bn'][tb]['S_get_info'])
    hBoxs['S_get_info'].addStretch(1)

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox_ks1 = ['R_time_stop'
               ,'N_averaging'
               ,'R_bandwidth'
               ,'B_reference_osci'
               ,'N_sweep_points'
               #,'R_freq_source'
               #,'R_power_source'
               #,'F_Sij'
               ]
    vBox_ks2 = ['R_freq_start'
               ,'R_freq_stop'
               ]

    vBox.addLayout(hBoxs['B_connect'])
    vBox.addLayout(hBoxs['S_get_info'])
    vBox.addLayout(hBoxs['F_averaging_type'])
    vBox.addLayout(hBoxs['F_averaging_mode'])

    for k in vBox_ks1:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(hBoxs['R_freq_start'])
    for k in vBox_ks2:
        vBox.addLayout(hBoxs[k])

################################################################################

########## ########## ########## ########## ########## ##########

def _build_H3344(vip, tb):
    hardware.range_H3344_channels

    vip.content['captions'][tb]['lb'] = {'R_amplitude_0'        : "Amplitude:"
                                        ,'R_amplitude_1'        : "Amplitude:"
                                        ,'R_amplitude_2'        : "Amplitude:"
                                        ,'R_amplitude_3'        : "Amplitude:"
                                        ,'R_offset_0'           : "Offset:"
                                        ,'R_offset_1'           : "Offset:"
                                        ,'R_offset_2'           : "Offset:"
                                        ,'R_offset_3'           : "Offset:"
                                        ,'FILE_PATH_waveform_0' : "Waveform file:"
                                        ,'FILE_PATH_waveform_1' : "Waveform file:"
                                        ,'FILE_PATH_waveform_2' : "Waveform file:"
                                        ,'FILE_PATH_waveform_3' : "Waveform file:"
                                        }
    vip.content['captions'][tb]['bn'] = {'_S_load_waveform'   : "Load waveforms"
                                        ,'_bn_waveform_browse_0': "Browse"
                                        ,'_bn_waveform_browse_1': "Browse"
                                        ,'_bn_waveform_browse_2': "Browse"
                                        ,'_bn_waveform_browse_3': "Browse"
                                        }
    vip.content['captions'][tb]['cb'] = {'B_connect'          : "Connect"
                                        ,'B_use_trigger'      : "Use the trigger"
                                        ,'B_channel_0'        : "CH 0 ON"
                                        ,'B_channel_1'        : "CH 1 ON"
                                        ,'B_channel_2'        : "CH 2 ON"
                                        ,'B_channel_3'        : "CH 3 ON"
                                        }
    vip.content['events'][tb]['le'] =   {'R_amplitude_0'        : lambda text:  se.le_or_dm_change(vip, tb, 'R_amplitude_0', text)
                                        ,'R_amplitude_1'        : lambda text:  se.le_or_dm_change(vip, tb, 'R_amplitude_1', text)
                                        ,'R_amplitude_2'        : lambda text:  se.le_or_dm_change(vip, tb, 'R_amplitude_2', text)
                                        ,'R_amplitude_3'        : lambda text:  se.le_or_dm_change(vip, tb, 'R_amplitude_3', text)
                                        ,'R_offset_0'           : lambda text:  se.le_or_dm_change(vip, tb, 'R_offset_0', text)
                                        ,'R_offset_1'           : lambda text:  se.le_or_dm_change(vip, tb, 'R_offset_1', text)
                                        ,'R_offset_2'           : lambda text:  se.le_or_dm_change(vip, tb, 'R_offset_2', text)
                                        ,'R_offset_3'           : lambda text:  se.le_or_dm_change(vip, tb, 'R_offset_3', text)
                                        ,'FILE_PATH_waveform_0' : lambda text:  se.le_or_dm_change(vip, tb, 'FILE_PATH_waveform_0', text)
                                        ,'FILE_PATH_waveform_1' : lambda text:  se.le_or_dm_change(vip, tb, 'FILE_PATH_waveform_1', text)
                                        ,'FILE_PATH_waveform_2' : lambda text:  se.le_or_dm_change(vip, tb, 'FILE_PATH_waveform_2', text)
                                        ,'FILE_PATH_waveform_3' : lambda text:  se.le_or_dm_change(vip, tb, 'FILE_PATH_waveform_3', text)
                                        }
    vip.content['events'][tb]['cb'] =   {'B_connect'          : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                        ,'B_use_trigger'      : lambda state: se.cb_toggled(vip, tb, 'B_use_trigger')
                                        ,'B_channel_0'        : lambda state: se.cb_toggled(vip, tb, 'B_channel_0')
                                        ,'B_channel_1'        : lambda state: se.cb_toggled(vip, tb, 'B_channel_1')
                                        ,'B_channel_2'        : lambda state: se.cb_toggled(vip, tb, 'B_channel_2')
                                        ,'B_channel_3'        : lambda state: se.cb_toggled(vip, tb, 'B_channel_3')
                                        }
    vip.content['events'][tb]['dm'] =   {}
    vip.content['events'][tb]['bn'] =   {'_S_load_waveform'     : lambda:       se.bn_AWG_load_waveform(vip, tb)
                                        ,'_bn_waveform_browse_0': lambda:       se.bn_browse_for(vip, 'FILE_PATH_waveform_0')
                                        ,'_bn_waveform_browse_1': lambda:       se.bn_browse_for(vip, 'FILE_PATH_waveform_1')
                                        ,'_bn_waveform_browse_2': lambda:       se.bn_browse_for(vip, 'FILE_PATH_waveform_2')
                                        ,'_bn_waveform_browse_3': lambda:       se.bn_browse_for(vip, 'FILE_PATH_waveform_3')
                                        }
    vip.content['cb_vals'][tb] =        {'B_connect'          : ('TRY', 'DONT')
                                        ,'B_use_trigger'      : ('ON', 'OFF')
                                        ,'B_channel_0'        : ('ON', 'OFF')
                                        ,'B_channel_1'        : ('ON', 'OFF')
                                        ,'B_channel_2'        : ('ON', 'OFF')
                                        ,'B_channel_3'        : ('ON', 'OFF')
                                        }
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-2)

########## ########## hBoxs


    ck_ks_ = ['B_connect', 'B_use_trigger']
    ck_ks  = ['B_channel_0','FILE_PATH_waveform_0'
             ,'B_channel_1','FILE_PATH_waveform_1'
             ,'B_channel_2','FILE_PATH_waveform_2'
             ,'B_channel_3','FILE_PATH_waveform_3'
             ]
    bn_ks = ['_S_load_waveform']

    hBox_ks = ck_ks_ + ck_ks + bn_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in bn_ks:
        hBoxs[k].addWidget(vip._qWidgets['bn'][tb][k])

    for k in ck_ks_:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])

    for ch in hardware.range_H3344_channels:
        hBoxs['B_channel_'+ch].addWidget(vip._qWidgets['cb'][tb]['B_channel_'+ch])
        hBoxs['B_channel_'+ch].addWidget(vip._qWidgets['lb'][tb]['R_amplitude_'+ch])
        hBoxs['B_channel_'+ch].addWidget(vip._qWidgets['le'][tb]['R_amplitude_'+ch])
        hBoxs['B_channel_'+ch].addWidget(vip._qWidgets['lb'][tb]['R_offset_'+ch])
        hBoxs['B_channel_'+ch].addWidget(vip._qWidgets['le'][tb]['R_offset_'+ch])
        hBoxs['FILE_PATH_waveform_'+ch].addWidget(vip._qWidgets['lb'][tb]['FILE_PATH_waveform_'+ch])
        hBoxs['FILE_PATH_waveform_'+ch].addStretch(1)
        hBoxs['FILE_PATH_waveform_'+ch].addWidget(vip._qWidgets['le'][tb]['FILE_PATH_waveform_'+ch])
        hBoxs['FILE_PATH_waveform_'+ch].addStretch(1)
        hBoxs['FILE_PATH_waveform_'+ch].addWidget(vip._qWidgets['bn'][tb]['_bn_waveform_browse_'+ch])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox_ks = hBox_ks

    for key in vBox_ks:
        vBox.addLayout(hBoxs[key])
        vBox.addStretch(1)


################################################################################

def _build_ATS9870(vip, tb):
    vip.content['captions'][tb]['lb'] = {'F_use_channel'             : "Use channel:"+1*cs.BLANK
                                        ,'N_records_per_buffer'      : "Records per buffer:"+1*cs.BLANK
                                        ,'N_buffers_per_acquisition' : "Buffers per acquisition:"+1*cs.BLANK
                                        ,'N_trigger_level_1'         : "Trigger level 1:"+1*cs.BLANK
                                        ,'N_trigger_delay'           : "Trigger delay: 16*"
                                        ,'F_trigger_source_1'        : "Trigger source 1:"+1*cs.BLANK
                                        ,'F_channelA_range'          : "Channel A, range [V]:"+1*cs.BLANK
                                        ,'F_channelB_range'          : "Channel B, range [V]:"+1*cs.BLANK
                                        ,'F_channelA_coupling'       : "Channel A coupling:"+1*cs.BLANK
                                        ,'F_channelB_coupling'       : "Channel B coupling:"+1*cs.BLANK
                                        ,'F_trigger_edge_1'          : "Trigger edge 1:"+1*cs.BLANK
                                        ,'_N_delay_size'             : "size = init"
                                        ,'R_intermediate_frequency'  : "Downconversion frequency:"+1*cs.BLANK
                                        ,'R_filter_frequency'        : "Frequency for moving average:"+1*cs.BLANK
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {'B_connect' : "Connect"}
    vip.content['events'][tb]['le'] =   {'N_records_per_buffer'      : lambda text: se.le_or_dm_change(vip, tb, 'N_records_per_buffer', text)
                                        ,'N_buffers_per_acquisition' : lambda text: se.le_or_dm_change(vip, tb, 'N_buffers_per_acquisition', text)
                                        ,'N_trigger_level_1'         : lambda text: se.le_or_dm_change(vip, tb, 'N_trigger_level_1', text)
                                        ,'N_trigger_delay'           : lambda text: se.le_or_dm_change__N_delay_size(vip, tb, 'N_trigger_delay', text)
                                        ,'R_intermediate_frequency'  : lambda text: se.le_or_dm_change(vip, tb, 'R_intermediate_frequency', text)
                                        ,'R_filter_frequency'        : lambda text: se.le_or_dm_change(vip, tb, 'R_filter_frequency', text)
                                        }
    vip.content['events'][tb]['cb'] = {'B_connect' : lambda state: se.cb_toggled(vip, tb, 'B_connect')}
    vip.content['events'][tb]['dm'] = {'F_use_channel'       : lambda text: se.le_or_dm_change(vip, tb, 'F_use_channel', text)
                                      ,'F_trigger_source_1'  : lambda text: se.le_or_dm_change(vip, tb, 'F_trigger_source_1', text)
                                      ,'F_channelA_range'    : lambda text: se.le_or_dm_change(vip, tb, 'F_channelA_range', text)
                                      ,'F_channelB_range'    : lambda text: se.le_or_dm_change(vip, tb, 'F_channelB_range', text)
                                      ,'F_channelA_coupling' : lambda text: se.le_or_dm_change(vip, tb, 'F_channelA_coupling', text)
                                      ,'F_channelB_coupling' : lambda text: se.le_or_dm_change(vip, tb, 'F_channelB_coupling', text)
                                      ,'F_trigger_edge_1'    : lambda text: se.le_or_dm_change(vip, tb, 'F_trigger_edge_1', text)
                                      }
    vip.content['events'][tb]['bn'] = {}
    vip.content['cb_vals'][tb] =      {'B_connect' : ('TRY', 'DONT')}
    vip.content['dm_vals'][tb] =      {'F_use_channel'       : menus.ATS9870['F_use_channel'].keys()
                                      ,'F_trigger_source_1'  : menus.ATS9870['F_trigger_source_1'].keys()
                                      ,'F_channelA_range'    : menus.ATS9870['F_channelA_range'].keys()
                                      ,'F_channelB_range'    : menus.ATS9870['F_channelB_range'].keys()
                                      ,'F_channelA_coupling' : menus.ATS9870['F_channelA_coupling'].keys()
                                      ,'F_channelB_coupling' : menus.ATS9870['F_channelB_coupling'].keys()
                                      ,'F_trigger_edge_1'    : menus.ATS9870['F_trigger_edge_1'].keys()
                                      }
    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-2)

########## ########## hBoxs
    ck_ks = ['B_connect'
            ]
    le_ks = ['N_records_per_buffer'
            ,'N_buffers_per_acquisition'
            ,'N_trigger_level_1'
            ,'N_trigger_delay'
            ,'R_intermediate_frequency'
            ,'R_filter_frequency'
            ]
    dm_ks = ['F_use_channel'
            ,'F_trigger_source_1'
            ,'F_channelA_range'
            ,'F_channelB_range'
            ,'F_channelA_coupling'
            ,'F_channelB_coupling'
            ,'F_trigger_edge_1'
            ]
    hBox_ks = ck_ks+dm_ks+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in ck_ks:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(1)
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])

    hBoxs['N_trigger_delay'].addWidget(vip._qWidgets['lb'][tb]['_N_delay_size'])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox_ks = hBox_ks

    for key in vBox_ks:
        vBox.addLayout(hBoxs[key])
        vBox.addStretch(1)

################################################################################

def _build_Delft(vip, tb):
    n_DACs     = int(session.default[tb]['N_DACs'])
    range_DACs = [str(i) for i in range(1, 1+n_DACs)]
    R_volt_channel_labels = {'R_volt_channel_'+i : 4*cs.BLANK+"Channel "+i+":"+4*cs.BLANK for i in range_DACs}
    NUM_POSSIBLE_COM_PORTS = 9 ### Essentially arbitrary

    vip.content['captions'][tb]['lb'] = {'F_channel'        : "Write to channel:"+2*cs.BLANK
                                        ,'F_interface'      : "Port:"+11*cs.BLANK
                                        ,'F_polarity'       : "Polarity:"+3*cs.BLANK
                                        }
    vip.content['captions'][tb]['lb'].update(R_volt_channel_labels)
    vip.content['captions'][tb]['bn'] = {'S_get_info'       : "info (untested)"}#cs.INSTRUMENT_INFO_LABEL
    vip.content['captions'][tb]['cb'] = {'B_connect'        : "Connect"
                                        }
    vip.content['events'][tb]['le'] = {'R_volt_channel_1'  : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_1' , text)
                                      ,'R_volt_channel_2'  : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_2' , text)
                                      ,'R_volt_channel_3'  : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_3' , text)
                                      ,'R_volt_channel_4'  : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_4' , text)
                                      ,'R_volt_channel_5'  : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_5' , text)
                                      ,'R_volt_channel_6'  : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_6' , text)
                                      ,'R_volt_channel_7'  : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_7' , text)
                                      ,'R_volt_channel_8'  : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_8' , text)
                                      ,'R_volt_channel_9'  : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_9' , text)
                                      ,'R_volt_channel_10' : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_10', text)
                                      ,'R_volt_channel_11' : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_11', text)
                                      ,'R_volt_channel_12' : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_12', text)
                                      ,'R_volt_channel_13' : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_13', text)
                                      ,'R_volt_channel_14' : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_14', text)
                                      ,'R_volt_channel_15' : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_15', text)
                                      ,'R_volt_channel_16' : lambda text: se.le_or_dm_change(vip, tb, 'R_volt_channel_16', text)
                                      }
    vip.content['events'][tb]['dm'] = {'F_channel'          : lambda text: se.le_or_dm_change(vip, tb, 'F_channel' , text)
                                      ,'F_interface'        : lambda text: se.le_or_dm_change(vip, tb, 'F_interface' , text)
                                      ,'F_polarity'         : lambda text: se.le_or_dm_change(vip, tb, 'F_polarity', text)
                                      }
    vip.content['events'][tb]['bn'] = {'S_get_info'         : lambda: se.bn_get_info(vip, tb)}
    vip.content['events'][tb]['cb'] = {'B_connect'          : lambda state: se.cb_toggled(vip, tb, 'B_connect')}
    vip.content['cb_vals'][tb] = {'B_connect'               : ('TRY', 'DONT')}
    vip.content['dm_vals'][tb] = {'F_channel'               : range_DACs
                                 ,'F_interface'             : ['COM'+str(i) for i in range(1, 1+NUM_POSSIBLE_COM_PORTS)]
                                 ,'F_polarity'              : ['R_NEG', 'R_BIP', 'R_POS']
                                 }
    sw.__fill_widgets(vip, tb)

    #### ----------
    __resize = -2
    for i in range_DACs:
        for k in ['lb', 'le']:
            vip._qWidgets[k][tb]['R_volt_channel_'+i].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+__resize))

########## ########## hBoxs
    range_DACs_odd = range(1, 1+n_DACs, 2)
    le_ks = ['R_volt_channel_'+str(i) for i in range_DACs_odd]
    cb_ks = ['B_connect']
    bn_ks = ['S_get_info']
    dm_ks = ['F_channel']+['F_interface','F_polarity']
    hBox_ks = le_ks+bn_ks+cb_ks+dm_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in range_DACs_odd:
        hBoxs['R_volt_channel_'+str(k)].addWidget(vip._qWidgets['lb'][tb]['R_volt_channel_'+str(k)])
        hBoxs['R_volt_channel_'+str(k)].addWidget(vip._qWidgets['le'][tb]['R_volt_channel_'+str(k)])
        hBoxs['R_volt_channel_'+str(k)].addWidget(vip._qWidgets['lb'][tb]['R_volt_channel_'+str(k+1)])
        hBoxs['R_volt_channel_'+str(k)].addWidget(vip._qWidgets['le'][tb]['R_volt_channel_'+str(k+1)])
    for k in cb_ks:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])
    for k in bn_ks:
        hBoxs[k].addWidget(vip._qWidgets['bn'][tb][k])
        hBoxs[k].addStretch(1)
    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['B_connect'])
    vBox.addLayout(hBoxs['F_interface'])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(hBoxs['S_get_info'])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(vip._blanks.next())
    for k in ['F_channel', 'F_polarity']:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())

    ### Create a small label telling the user the unit of all the Voltage ports.
    ### Note that this widget '__label_widget' doesn't fit as nicely in the
    ### content dictionary scheme that I've used almost everywhere else.
    ### One could of course add it to the ['captions'][tb]['lb'] dict.
    text = "Voltages in [mV]:"
    __label_widget = QtGui.QLabel(text)
    __label_widget.setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE))  # QtGui.QFont(font, SIZE, QtGui.QFont.Bold)
    __label_widget.adjustSize()
    vBox.addWidget(__label_widget)

    for i in range_DACs_odd:
        vBox.addLayout(hBoxs['R_volt_channel_'+str(i)])



################################################################################
def _build_NI_pulse(vip, tb):
    vip.content['captions'][tb]['lb'] = {'N_device'     : "Device:"
                                        ,'N_port'       : "Port:"
                                        ,'R_pulse_time' : "Short pulse time:"
                                        }
    vip.content['captions'][tb]['bn'] = {'_Zero_pulse'     : "Zero pulse"
                                        ,'_Short_pulse'    : "Short pulse"
                                        ,'_Unending_pulse' : "Unending pulse"
                                        ,'_load_config'    : "Load configuration"
                                        }
    vip.content['captions'][tb]['cb'] = {'B_connect' : "Connect"
                                        }
    _pin_lbs = {'B_pin_'+k : "Pin"+cs.BLANK+k for k in hardware.range_NI_pins}
    vip.content['captions'][tb]['cb'].update(_pin_lbs)
    vip.content['events'][tb]['le'] = {'N_device'     : lambda text: se.le_or_dm_change(vip, tb, 'N_device', text)
                                      ,'N_port'       : lambda text: se.le_or_dm_change(vip, tb, 'N_port' , text)
                                      ,'R_pulse_time' : lambda text: se.le_or_dm_change(vip, tb, 'R_pulse_time' , text)
                                      }
    vip.content['events'][tb]['dm'] = {'F_unit_time'     : lambda text: se.le_or_dm_change(vip, tb, 'F_unit_time', text)
                                      ,'F_use_config'    : lambda text: se.le_or_dm_change(vip, tb, 'F_use_config', text)
                                      }
    vip.content['events'][tb]['bn'] = {'_Zero_pulse'     : lambda: se.safe_NI_pulse(vip, tb, True , False)
                                      ### The two booleans here are getting passed to B_zeros resp. B_finite
                                      ### For the zero pulse it doesn't really matter whether 'B_finite' is set True or False
                                      ,'_Short_pulse'    : lambda: se.safe_NI_pulse(vip, tb, False, True )
                                      ,'_Unending_pulse' : lambda: se.safe_NI_pulse(vip, tb, False, False)
                                      ,'_load_config' : lambda: se.load_config_NI_pulse(vip, tb)
                                      }
    vip.content['events'][tb]['cb'] = {'B_connect' : lambda state: se.cb_toggled(vip, tb, 'B_connect')
                                      ,'B_pin_'+str(0) : lambda state: se.cb_toggled(vip, tb, 'B_pin_'+str(0))
                                      ,'B_pin_'+str(1) : lambda state: se.cb_toggled(vip, tb, 'B_pin_'+str(1))
                                      ,'B_pin_'+str(2) : lambda state: se.cb_toggled(vip, tb, 'B_pin_'+str(2))
                                      ,'B_pin_'+str(3) : lambda state: se.cb_toggled(vip, tb, 'B_pin_'+str(3))
                                      ,'B_pin_'+str(4) : lambda state: se.cb_toggled(vip, tb, 'B_pin_'+str(4))
                                      ,'B_pin_'+str(5) : lambda state: se.cb_toggled(vip, tb, 'B_pin_'+str(5))
                                      ,'B_pin_'+str(6) : lambda state: se.cb_toggled(vip, tb, 'B_pin_'+str(6))
                                      ,'B_pin_'+str(7) : lambda state: se.cb_toggled(vip, tb, 'B_pin_'+str(7))
                                      }
    vip.content['cb_vals'][tb] = {'B_pin_'+k : ('1', '0') for k in hardware.range_NI_pins}
    vip.content['cb_vals'][tb]['B_connect'] = ('TRY', 'DONT')
    _config_script_dict = {} ### The dictoionary with the configuration functions was removed.
    vip.content['dm_vals'][tb] = {'F_unit_time'  : ['ms']
                                 ,'F_use_config' : _config_script_dict.keys()
                                 }

    sw.__fill_widgets(vip, tb)

########## ########## hBoxs
    le_ks = ['N_device', 'N_port'] + ['R_pulse_time']
    cb_ks = vip.content['events'][tb]['cb'].keys()
    bn_ks = ['_Zero_pulse', '_Short_pulse', '_Unending_pulse', '_load_config']
    hBox_ks = le_ks+cb_ks+bn_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch()
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in cb_ks:
        hBoxs[k].addWidget(vip._qWidgets['cb'][tb][k])
    hBoxs[k].addStretch()
    hBoxs['R_pulse_time'].addWidget(vip._qWidgets['dm'][tb]['F_unit_time'])

    for k in bn_ks:
        hBoxs[k].addWidget(vip._qWidgets['bn'][tb][k])
    hBoxs['_load_config'].addWidget(vip._qWidgets['dm'][tb]['F_use_config'])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addLayout(hBoxs['B_connect'])
    vBox.addLayout(vip._blanks.next())

    for k in ['N_device', 'N_port']:
        vBox.addLayout(hBoxs[k])

    for k in cb_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())

    for k in ['R_pulse_time']:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())

    for k in bn_ks:
        vBox.addLayout(hBoxs[k])

from PySide import QtGui

import dictionaries.session as session
import dictionaries.constants as cs
import interface.session_events as se
import dictionaries.menus as menus

import interface.session_widgets as sw

################################################################################

def _build_Freq_vs_drive_power(vip):
    tb = 'Freq. vs. drive power'

    vip.content['captions'][tb]['lb'] = {"Sweep_instr"           : "Sweep instrument:"
                                        ,"VNA_instr"             : "VNA instrument:"
                                        ,"R_freq_cavity_VNA"     : "Freq. (cavity) [GHz]:"
                                        ,"R_freq_span_cavity_VNA": "Freq. span (cavity) [Hz]:"
                                        ,"R_power_SG"            : "Source power:"
                                        ,"R_freq_start_SG"       : "Source freq. start [GHz]:"
                                        ,"R_freq_stop_SG"        : "Source freq. stop [GHz]:"
                                        ,"R_freq_step_size_SG"   : "Source freq. step size [GHz]:"
                                        ,"R_power_start_SG"      : "Source power start:"
                                        ,"R_power_stop_SG"       : "Source power stop:"
                                        ,"R_power_step_size_SG"  : "Source power step size:"
                                        }

    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}

    vip.content['events'][tb]['le'] = {"R_freq_cavity_VNA"     : lambda text: se.le_or_dm_change(vip, tb, "R_freq_cavity_VNA", text)
                                       ,"R_freq_span_cavity_VNA": lambda text: se.le_or_dm_change(vip, tb, "R_freq_span_cavity_VNA", text)
                                       ,"R_power_SG"            : lambda text: se.le_or_dm_change(vip, tb, "R_power_SG", text)
                                       ,"R_freq_start_SG"       : lambda text: se.le_or_dm_change(vip, tb, "R_freq_start_SG", text)
                                       ,"R_freq_stop_SG"        : lambda text: se.le_or_dm_change(vip, tb, "R_freq_stop_SG", text)
                                       ,"R_freq_step_size_SG"   : lambda text: se.le_or_dm_change(vip, tb, "R_freq_step_size_SG", text)
                                       ,"R_power_start_SG"      : lambda text: se.le_or_dm_change(vip, tb, "R_power_start_SG", text)
                                       ,"R_power_stop_SG"       : lambda text: se.le_or_dm_change(vip, tb, "R_power_stop_SG", text)
                                       ,"R_power_step_size_SG"  : lambda text: se.le_or_dm_change(vip, tb, "R_power_step_size_SG", text)
                                       }
    vip.content['events'][tb]['dm'] = {"Sweep_instr"  : lambda text: se.le_or_dm_change(vip, tb, "Sweep_instr", text)
                                      ,"VNA_instr"  : lambda text: se.le_or_dm_change(vip, tb, "VNA_instr", text)
                                      }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {'Sweep_instr' : session.instr_classification['SG']
                                 ,'VNA_instr' : session.instr_classification['VNA']
                                }

    sw.__fill_widgets(vip, tb)

########## ########## hBoxs

    dm_ks = ['Sweep_instr'
            ,'VNA_instr'
            ]

    le_ks = ["R_freq_cavity_VNA"
            ,"R_freq_span_cavity_VNA"
            ,"R_power_SG"
            ,"R_freq_start_SG"
            ,"R_freq_stop_SG"
            ,"R_freq_step_size_SG"
            ,"R_power_start_SG"
            ,"R_power_stop_SG"
            ,"R_power_step_size_SG"
            ]
    hBox_ks = dm_ks+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addStretch(1)

    for k in dm_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(vip._blanks.next())

    for k in le_ks:
        vBox.addLayout(hBoxs[k])

    vBox.addStretch(1)


################################################################################

def _build_Flux_sweep(vip):
    tb = 'Flux sweep'

    vip.content['captions'][tb]['lb'] = {"ssg_ip"      : "Source:"
                                        ,"vna_ip"      : "VNA:"

                                        ,"com_port"    : "COM port:"
                                        ,"dac_port"    : "DAC port:"
                                        ,"cav_freq"    : "Cavity freq.:"
                                        ,"span"        : "Span:"
                                        ,"pow"         : "Power:"
                                        ,"start_freq"  : "Start frequency:"
                                        ,"stop_freq"   : "Stop frequency:"
                                        ,"step_size_ssg" : "Step size (source):"
                                        ,"start_flux"  : "Flux start:"
                                        ,"stop_flux"   : "Flux stop:"
                                        ,"step_size_srs" : "Step size (srs):"
                                        ,"fn"          : "Results file name:"
                                        }

    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}

    vip.content['events'][tb]['le'] =  {"com_port"     : lambda text: se.le_or_dm_change(vip, tb, "com_port", text)
                                       ,"dac_port"     : lambda text: se.le_or_dm_change(vip, tb, "dac_port", text)
                                       ,"cav_freq"     : lambda text: se.le_or_dm_change(vip, tb, "cav_freq", text)
                                       ,"span"     : lambda text: se.le_or_dm_change(vip, tb, "span", text)
                                       ,"pow"     : lambda text: se.le_or_dm_change(vip, tb, "pow", text)
                                       ,"start_freq"     : lambda text: se.le_or_dm_change(vip, tb, "start_freq", text)
                                       ,"stop_freq"     : lambda text: se.le_or_dm_change(vip, tb, "stop_freq", text)
                                       ,"step_size_ssg"     : lambda text: se.le_or_dm_change(vip, tb, "step_size_ssg", text)
                                       ,"start_flux"     : lambda text: se.le_or_dm_change(vip, tb, "start_flux", text)
                                       ,"stop_flux"     : lambda text: se.le_or_dm_change(vip, tb, "stop_flux", text)
                                       ,"step_size_srs"     : lambda text: se.le_or_dm_change(vip, tb, "step_size_srs", text)
                                       ,"fn"     : lambda text: se.le_or_dm_change(vip, tb, "fn", text)
                                       }
    vip.content['events'][tb]['dm'] = {"ssg_ip"  : lambda text: se.le_or_dm_change(vip, tb, "ssg_ip", text)
                                      ,"vna_ip"  : lambda text: se.le_or_dm_change(vip, tb, "vna_ip", text)
                                      }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {'ssg_ip' : session.instr_classification['SG']
                                 ,'vna_ip' : session.instr_classification['VNA']
                                 }

    sw.__fill_widgets(vip, tb)

########## ########## hBoxs

    dm_ks = vip.content['events'][tb]['dm'].keys()

    le_ks = ["com_port"
            ,"dac_port"
            ,"cav_freq"
            ,"span"
            ,"pow"
            ,"start_freq"
            ,"stop_freq"
            ,"step_size_ssg"
            ,"start_flux"
            ,"stop_flux"
            ,"step_size_srs"
            ,"fn"
            ]

    hBox_ks = dm_ks+le_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])
    vBox.addLayout(vip._blanks.next())

    for k in dm_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(vip._blanks.next())

    for k in le_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())


################################################################################

def _build_Freq_query(vip):
    tb = 'Freq. query'

    vip.content['captions'][tb]['lb'] = {'TITLE_instr_name' : "Instrument to query:"}
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}
    vip.content['events'][tb]['le'] = {}
    vip.content['events'][tb]['dm'] = {"TITLE_instr_name"  : lambda text: se.le_or_dm_change(vip, tb, "TITLE_instr_name", text)}
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}
    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {'TITLE_instr_name' : session.instr_classification['SG']}

    sw.__fill_widgets(vip, tb)

########## ########## hBoxs

    dm_ks = ['TITLE_instr_name']

    hBox_ks = dm_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])
    vBox.addLayout(vip._blanks.next())

    for k in dm_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(vip._blanks.next())


################################################################################

def _build_Printer_demo(vip):
    tb = 'Printer demo'
    k = 'string_to_print'

    vip.content['captions'][tb]['lb'] = {k : "String to be printed:"}
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}
    vip.content['events'][tb]['le']   = {k : lambda text: se.le_or_dm_change(vip, tb, k, text)}
    vip.content['events'][tb]['dm']   = {}
    vip.content['events'][tb]['bn']   = {}
    vip.content['events'][tb]['cb']   = {}
    vip.content['cb_vals'][tb]        = {}
    vip.content['dm_vals'][tb]        = {}

    sw.__fill_widgets(vip, tb)

########## ########## hBoxs

    hBox_lb = QtGui.QHBoxLayout()
    hBox_le = QtGui.QHBoxLayout()

    hBox_lb.addWidget(vip._qWidgets['lb'][tb][k])
    hBox_le.addWidget(vip._qWidgets['le'][tb][k])

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addStretch(1)
    vBox.addLayout(hBox_lb)
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(hBox_le)
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(vip._blanks.next())
    vBox.addStretch(1)


################################################################################

def _build_DAC_VNA(vip):
    tb = 'Mixer-Dig VNA'

    vip.content['captions'][tb]['lb'] = {"start_freq" : "Start frequency [Hz]:"
                                        ,"stop_freq"  : "Stop frequency [Hz]:"
                                        ,"IF_freq"    : "IF frequency [Hz]:"
                                        ,"points"     : "Points:"
                                        ,'source_LO'  : "LO source:"
                                        ,'source_rf'  : "rf source:"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}

    vip.content['events'][tb]['le'] = {"start_freq"   : lambda text: se.le_or_dm_change(vip, tb, "start_freq", text)
                                      ,"stop_freq"    : lambda text: se.le_or_dm_change(vip, tb, "stop_freq", text)
                                      ,"points"       : lambda text: se.le_or_dm_change(vip, tb, "points", text)
                                      ,"IF_freq"      : lambda text: se.le_or_dm_change(vip, tb, "IF_freq", text)
                                      }
    vip.content['events'][tb]['dm'] = {'source_LO'    : lambda text: se.le_or_dm_change(vip, tb, 'source_LO', text)
                                      ,'source_rf'    : lambda text: se.le_or_dm_change(vip, tb, 'source_rf', text)
                                      }
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {'F_unit_freq_source' : menus.FREQUENCY_UNITS
                                 ,'source_LO'          : session.instr_classification['SG']
                                 ,'source_rf'          : session.instr_classification['SG']
                                }

    sw.__fill_widgets(vip, tb)

########## ########## hBoxs
    le_ks = ["start_freq"
            ,"stop_freq"
            ,"IF_freq"
            ,"points"
            ]
    dm_ks = ['source_LO'
            ,'source_rf'
            ]
    hBox_ks = le_ks+dm_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}
    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k])


########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addStretch(.1)

    for k in dm_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())

    vBox.addLayout(vip._blanks.next())

    for k in le_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(vip._blanks.next())
    vBox.addStretch(.1)


################################################################################

def _build_Mixer_calib(vip):
    tb = 'Mixer calib.'

    vip.content['captions'][tb]['lb'] = {"center_freq" : "Center frequency:"
                                        ,"int_freq"    : "Int. frequency:"
                                        ,'R_amplitude' : "Amplitude:"
                                        ,"LO_source"   : "LO source"
                                        ,"spec_source" : "spec source"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {}

    vip.content['events'][tb]['le'] = {"center_freq"   : lambda text: se.le_or_dm_change(vip, tb, "center_freq", text)
                                      ,"int_freq"      : lambda text: se.le_or_dm_change(vip, tb, "int_freq", text)
                                      ,"R_amplitude"   : lambda text: se.le_or_dm_change(vip, tb, "R_amplitude", text)
                                      }
    vip.content['events'][tb]['dm'] = {"LO_source"      : lambda text: se.le_or_dm_change(vip, tb, "LO_source", text)
                                      ,"spec_source"    : lambda text: se.le_or_dm_change(vip, tb, "spec_source", text)}
    vip.content['events'][tb]['bn'] = {}
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {"LO_source"     :session.instr_classification['SG']
                                 ,"spec_source"   :session.instr_classification['SG']}

    sw.__fill_widgets(vip, tb)

########## ########## hBoxs
    le_ks = ["center_freq"
            ,"int_freq"
            ,'R_amplitude'
            ]
    dm_ks = ['LO_source'
            ,'spec_source'
            ]
    hBox_ks = le_ks + dm_ks

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}
    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])
        
    for k in dm_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['dm'][tb][k]) 

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])
    vBox.addLayout(vip._blanks.next())

    for k in le_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())
    for k in dm_ks:
        vBox.addLayout(hBoxs[k])
    vBox.addLayout(vip._blanks.next())


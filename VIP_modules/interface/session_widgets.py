from PySide import QtGui

import dictionaries.session as session
import dictionaries.constants as cs
import interface.session_events as se

################################################################################

def sweep_ks(s):
    return [s+' sweep '+str(i) for i in [1, 2, 3]]

def _build_all(VIP):
        """
        This function calls a whole lot of functions defined in this file and is 
        itself only called once, namel from the VIP class init. 
        What is happening here is that for each session key 
        (called sk resp. tb, for example sk='ZNB_1') we initialize a widget for 
        each setting key (e.g. k='R_freq_start') and create a layout. 
        Most of the Qt-functions must be called for each session key, and this is
        thus done in a seperate function called '__fill_widgets', see below.
        """
        ########## Physical instruments  
        import interface.tabs_instruments as tin
        tin._build_ZVL13(VIP, 'ZVL_1')
        tin._build_FSW(VIP, 'FSW_1')
        tin._build_RTE1054(VIP, 'RTE1054_1')
        tin._build_Thorlabs_PM100D(VIP, 'Thorlabs_1')
        tin._build_Santec_TSL_550(VIP, 'Santec_1')
        for instr_name in ['ZNB_1', 'ZNB_2']: 
            tin._build_ZNB20(VIP, instr_name)
        ### We have six Signal generators of type SGS100A in the lab 
        for instr_name in session.instr_classification['SG']: 
            tin._build_SGS100A(VIP, instr_name)

        tin._build_ATS9870(VIP , 'ATS9870_1' )
        tin._build_Delft(VIP   , 'Delft_1'   )
        tin._build_NI_pulse(VIP, 'NI_pulse_1')
        tin._build_H3344(VIP   , 'H3344_1'   )
        tin._build_WM1210(VIP, 'WM1210_1')
        tin._build_NI_DAQ(VIP, 'NI_DAQ_1')
    
        ########## Sweeps
        import interface.tabs_sweeps as tsw
        for sk in sweep_ks('Freq.'):
            tsw._build_Freq_sweep(VIP, sk)
        for sk in sweep_ks('Phase'):
            tsw._build_Phase_sweep(VIP, sk)
        for sk in sweep_ks('Power'):
            tsw._build_Power_sweep(VIP, sk)
        for sk in sweep_ks('Voltage'):
            tsw._build_Voltage_sweep(VIP, sk)
        for sk in sweep_ks('File'):
            tsw._build_File_sweep(VIP, sk)
        for sk in sweep_ks('AWG'):
            tsw._build_AWG_sweep(VIP, sk)
    
        ########## Scripts 
        import interface.tabs_scripts as tsc
        tsc._build_Printer_demo(VIP)
        tsc._build_Freq_query(VIP)
        tsc._build_Freq_vs_drive_power(VIP)
        tsc._build_DAC_VNA(VIP)
        tsc._build_Mixer_calib(VIP)
        tsc._build_Flux_sweep(VIP)
    
        ########## Measurements 
        import interface.tabs_measurement as tmm
        tmm._build_From_trace(VIP)

        tmm._build_Meas_main(VIP)
        tmm._build_Sweep(VIP)
        tmm._build_Script(VIP)
    
        tmm._build_Freq_trace(VIP)
        tmm._build_Time_trace(VIP)
        tmm._build_Dig_sample(VIP)
        tmm._build_Power_point(VIP)
        tmm._build_I_Q_point(VIP)
    
        ########## Control
        import interface.tabs_control as tco
        for sk in sorted(session.Plot.keys()):
            tco._build_Canvas_columns(VIP, sk)
        tco._build_OptionsWindow(VIP)
        tco._build_Session(VIP)
        tco._build_Results(VIP)
        tco._build_Instrument_buttons(VIP)
        tco._build_Window_buttons(VIP)

def __fill_widgets(vip, tb, fontsize=cs.FONTSIZE, font=cs.FONT, stylesheet=None):
    #stylesheet=cs.STYLESHEET_PINK
    """
    For each tab (e.g. tb='ZNB_1') that is passed to this function,
    the vip.content dictionary entry is used to create a whole bunch of widgets,
    namely 1. QLabels, 2. QCheckBoxs, 3. QPushButtons and 4. QLineEditsw.
    """
    ### Use vip.content['captions']
    for k, v in vip.content['captions'][tb]['lb'].iteritems():
        vip._qWidgets['lb'][tb][k] = QtGui.QLabel(v, vip)
        vip._qWidgets['lb'][tb][k].setFont(QtGui.QFont(font, fontsize))  #
        #QtGui.QFont(font, SIZE, QtGui.QFont.Bold)
        vip._qWidgets['lb'][tb][k].setStyleSheet(stylesheet)
        vip._qWidgets['lb'][tb][k].adjustSize()
    for k, v in vip.content['captions'][tb]['cb'].iteritems():
        vip._qWidgets['cb'][tb][k] = QtGui.QCheckBox(v, vip)
        vip._qWidgets['cb'][tb][k].setFont(QtGui.QFont(font, fontsize))
        vip._qWidgets['cb'][tb][k].setStyleSheet(stylesheet)
    for k, v in vip.content['captions'][tb]['bn'].iteritems():
        vip._qWidgets['bn'][tb][k] = QtGui.QPushButton(v, vip)
        vip._qWidgets['bn'][tb][k].setFont(QtGui.QFont(font, fontsize))
        vip._qWidgets['bn'][tb][k].setStyleSheet(stylesheet)
        vip._qWidgets['bn'][tb][k].adjustSize()

    ### Use vip.content['events']
    for k, v in vip.content['events'][tb]['le'].iteritems():
        settings_1 = session.default[tb]
        settings_2 = vip.auxiliary_le[tb]
        text = settings_1[k] if (k in settings_1) else settings_2[k]
        vip._qWidgets['le'][tb][k] = QtGui.QLineEdit(text, vip)
        vip._qWidgets['le'][tb][k].setFont(QtGui.QFont(font, fontsize))
        vip._qWidgets['le'][tb][k].setTextMargins(5,0,5,0)
        vip._qWidgets['le'][tb][k].textChanged[str].connect(v)
        #vip._qWidgets['le'][tb][k].setMaxLength(10)
    for k, event in vip.content['events'][tb]['cb'].iteritems():
        vip._qWidgets['cb'][tb][k].stateChanged.connect(event)
        kv = {k : session.default[tb][k]}
        vip.set(tb, kv)
    for k, event in vip.content['events'][tb]['dm'].iteritems():
        vip._qWidgets['dm'][tb][k] = QtGui.QComboBox(vip)
        vip._qWidgets['dm'][tb][k].setFont(QtGui.QFont(font, fontsize))
        vip._qWidgets['dm'][tb][k].activated[str].connect(event)
        vip._qWidgets['dm'][tb][k].addItems(vip.content['dm_vals'][tb][k])
        kv = {k : session.default[tb][k]}
        vip.set(tb, kv)
    for k, event in vip.content['events'][tb]['bn'].iteritems():
        vip._qWidgets['bn'][tb][k].clicked.connect(event)



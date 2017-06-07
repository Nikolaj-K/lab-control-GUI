import session as session
import addresses as addresses

"""
Create a dictonary 'commands' of depth 3:
1. Kind of language the instrument understands
2. Kind of commands we have for the intrument
3. Name of the instrument
"""

################################################################################
"""Create the first two keyword levels"""

LANGS         = ['visa'
                ]
COMMAND_TYPES = ['query'
                ,'adopt'
                ,'write'
                ]

commands = {lang : {ct : {} for ct in COMMAND_TYPES} for lang in LANGS}

for lang in LANGS:
    commands[lang]['address'] = addresses.address_dict

################################################################################

"""
Provide the QUERY and ADOPT commands, and create a bigger WRITE dictionary.
The ADOPT commands are those writable commands that are to be send to the
instrument when the 'Adopt settings' button in clicked on the GUI.
The WRITE commands contain the ADOPT commands and possibly more.
"""

################################################################################ VISA

BASIC_VISA_QUERIES = {'a Instrument ID name'    : '*IDN?'
                     ,'a System Error?'         : 'SYST:ERR?'
                     ,'a System Version'        : 'SYSTem:VERSion?'
                     ,'a Individual status'     : '*IST?'             # returns e.g."0"
                     ,'a Option identification' : '*OPT?'             # returns e.g."ZNB20-B24"
                     ,'a Status byte'           : '*STB?'             # returns e.g."4"
                     }
BASIC_VISA_WRITING = {'command_Reset' : '*RST'
                     }

##########----------------------------------------------------------------------

for instr_name in session.ZNB20s:
    commands['visa']['query'][instr_name] = {'b Frquency start'       : 'FREQuency:STARt?'
                                            ,'b Frquency stop'        : 'FREQuency:STOP?'
                                            ,'b Source Freqeuncy'     : ':SOURce:FREQuency?'
                                            ,'b Source Power'         : ':SOURce:POWer?'
                                            ,'b Bandwith'             : 'SENS1:BAND:RES?'
                                            ,'b Sweep type'           : 'SENS:SWE:TYPE?'
                                            ,'b Sweep counts'         : 'SENS1:SWE:COUNT?'
                                            ,'b Center frequency'     : 'SOUR:FREQ:FIX?'

                                            ,'c Initiate immediatenly.Operation complete?'  : 'INIT1:IMM; *OPC?'
                                            ,'c Output State SON/OFF (0/1)'                  : ':OUTPut:STATe?'
                                            }
    commands['visa']['query'][instr_name].update(BASIC_VISA_QUERIES)

    commands['visa']['adopt'][instr_name] = {'z_command_Display_on'      : 'SYSTem:DISPlay:UPDate ON'                                                # Reset
                                            ,'command_Auto_sweep_time'     : 'SENS1:SWE:TIME:AUTO ON; TRIG1:SEQ:SOUR IMM'                     # Avoid a delay time between different partial measurements and before the  start of the sweeps and minimize sweep time (is default setting)
                                            ,'command_Display_param'     : 'DISPLAY:WINDOW1:TRACE1:FEED "Trc1"'                             # Show choosen parameter on display
                                            ,'command_Set_param_active'  : 'CALCULATE1:PARAMETER:SELECT "Trc1"'                             # Choosen parameter set to active
                                            #,'command_Adj_Averaging'         : 'CALC:SMO ON; :APER 0.5',                                   # There is also an option Smoothing - averaging between adjacent sweep points in percentage of overall num of points
                                            #,'command_F_data_form'       : 'CALC:FORM {F_data_form}'                                      # Setting up data format on y axes (MLIN - linear mag, MLOG - magnitude in dB, PHAS - Phase in deg, UPH - unwrapped phase in deg)
                                            #,'command_F_VNA_mode'        : 'SENS:SWE:TYPE {F_VNA_mode}'                                     # Choosing VNA mode (MLOG - Linear frequency sweep at constant source power, POIN - CW mode sweep ) # CW...Continuous wave

                                            ,'command_set_num_averaging' : 'SENS1:SWE:COUNT {N_averaging}'
                                            ,'command_reference_osci'    : 'ROSC {B_reference_osci}'
                                            ,'command_B_cont'     : 'INITiate1:CONTinuous {B_continous}'                           # Continuous mode ON/OFF
                                            ,'command_N_swee_point'       : 'SENS1:SWE:POIN {N_sweep_points}'                                   # Number of sweep points
                                            ,'command_R_sour_powe'       : 'SOUR:POW {R_power_source}'                                         # Setting source power in dBm (available from -30dBm to 10dBm)
                                            ,'command_F_Sij'             : 'CALCULATE1:PARAMETER:SDEFINE "Trc1", "{F_Sij}"'                 # Measured parameter choosing             #n previously just {F_Sij} instead of "{F_Sij}"

                                            ,'command_R_freq_start_stop'  : 'FREQ:STAR {R_freq_start} {F_unit_freq}; STOP {R_freq_stop} {F_unit_freq}'        # Setting stop and start frequency for frequency sweep measurement (Active only in MLOG mode)
                                            ,'command_R_freq_source'       : 'SOUR:FREQ:FIX {R_freq_source} {F_unit_freq_source}'           # Setting source frequency for time measurement (Active only in POIN mode)
                                            ,'command_R_bandwidth'       : 'SENS1:BAND:RES {R_bandwidth} {F_unit_bandwidth}'              # R_bandwidth selection in kHz - select the widest R_bandwidth compatible with your measurement

                                            ,'command_N_aver_B_aver' : 'SENS1:AVER:COUN {N_averaging}; :AVER {B_averaging}; CLE'        # Number of consecutive sweeps to be combined for the sweep average, average ON /OFF, clearing averag
                                            }
                                            #
                                            # 'DISPlay[:WINDow<Wnd>][:STATe] ON'
                                            # 'SYSTem:PRESet:USER:CAL <PresetUserCal>'
                                            # 'SOUR:POW:CORR:TCO:CAL OFF'
                                            # 'SYSTem:PRESet[:DUMMy]'...'*RST', equivalent to the PRESET key on the fron panel of the instrument

    commands['visa']['write'][instr_name] = {}
    commands['visa']['write'][instr_name].update(commands['visa']['adopt'][instr_name])
    commands['visa']['write'][instr_name].update(BASIC_VISA_WRITING)

##########----------------------------------------------------------------------

for instr_name in ['ZVL_1']:
    commands['visa']['query'][instr_name] = {'b Frquency start'       : 'FREQuency:STARt?'
                                            ,'b Frquency stop'        : 'FREQuency:STOP?'
                                            ,'b Source Freqeuncy'     : ':SOURce:FREQuency?'
                                            ,'b Source Power'         : ':SOURce:POWer?'
                                            ,'b Bandwith'             : 'SENS1:BAND:RES?'
                                            ,'b Sweep type'           : 'SENS:SWE:TYPE?'
                                            ,'b Sweep counts'         : 'SENS1:SWE:COUNT?'
                                            ,'b Center frequency'     : 'SOUR:FREQ:FIX?'

                                            ,'c Initiate immediatenly.Operation complete?'  : 'INIT1:IMM; *OPC?'
                                            ,'c Output State SON/OFF (0/1)'                  : ':OUTPut:STATe?'
                                            }
    commands['visa']['query'][instr_name].update(BASIC_VISA_QUERIES)

    commands['visa']['adopt'][instr_name] = {'z_command_Display_on'      : 'SYSTem:DISPlay:UPDate ON'                                                # Reset
                                            ,'command_Auto_sweep_time'     : 'SENS1:SWE:TIME:AUTO ON; TRIG1:SEQ:SOUR IMM'                     # Avoid a delay time between different partial measurements and before the  start of the sweeps and minimize sweep time (is default setting)
                                            ,'command_Display_param'     : 'DISPLAY:WINDOW1:TRACE1:FEED "Trc1"'                             # Show choosen parameter on display
                                            ,'command_Set_param_active'  : 'CALCULATE1:PARAMETER:SELECT "Trc1"'                             # Choosen parameter set to active
                                            #,'command_Adj_Averaging'         : 'CALC:SMO ON; :APER 0.5',                                   # There is also an option Smoothing - averaging between adjacent sweep points in percentage of overall num of points
                                            #,'command_F_data_form'       : 'CALC:FORM {F_data_form}'                                      # Setting up data format on y axes (MLIN - linear mag, MLOG - magnitude in dB, PHAS - Phase in deg, UPH - unwrapped phase in deg)
                                            #,'command_F_VNA_mode'        : 'SENS:SWE:TYPE {F_VNA_mode}'                                     # Choosing VNA mode (MLOG - Linear frequency sweep at constant source power, POIN - CW mode sweep ) # CW...Continuous wave

                                            ,'command_set_num_averaging' : 'SENS1:SWE:COUNT {N_averaging}'
                                            ,'command_reference_osci'    : 'ROSC {B_reference_osci}'
                                            ,'command_B_cont'             : 'INITiate1:CONTinuous {B_continous}'                           # Continuous mode ON/OFF
                                            ,'command_N_swee_point'       : 'SENS1:SWE:POIN {N_sweep_points}'                                   # Number of sweep points
                                            ,'command_R_sour_powe'       : 'SOUR:POW {R_power_source}'                                         # Setting source power in dBm (available from -30dBm to 10dBm)
                                            ,'command_F_Sij'             : 'CALCULATE1:PARAMETER:SDEFINE "Trc1", "{F_Sij}"'                 # Measured parameter choosing             #n previously just {F_Sij} instead of "{F_Sij}"

                                            ,'command_R_freq_start_stop'  : 'FREQ:STAR {R_freq_start} {F_unit_freq}; STOP {R_freq_stop} {F_unit_freq}'        # Setting stop and start frequency for frequency sweep measurement (Active only in MLOG mode)
                                            ,'command_R_freq_source'       : 'SOUR:FREQ:FIX {R_freq_source} {F_unit_freq_source}'           # Setting source frequency for time measurement (Active only in POIN mode)
                                            ,'command_R_bandwidth'       : 'SENS1:BAND:RES {R_bandwidth} {F_unit_bandwidth}'              # R_bandwidth selection in kHz - select the widest R_bandwidth compatible with your measurement

                                            ,'command_N_aver_B_aver' : 'SENS1:AVER:COUN {N_averaging}; :AVER {B_averaging}; CLE'        # Number of consecutive sweeps to be combined for the sweep average, average ON /OFF, clearing averag
                                            }
                                            #
                                            # 'DISPlay[:WINDow<Wnd>][:STATe] ON'
                                            # 'SYSTem:PRESet:USER:CAL <PresetUserCal>'
                                            # 'SOUR:POW:CORR:TCO:CAL OFF'
                                            # 'SYSTem:PRESet[:DUMMy]'...'*RST', equivalent to the PRESET key on the fron panel of the instrument

    commands['visa']['write'][instr_name] = {}
    commands['visa']['write'][instr_name].update(commands['visa']['adopt'][instr_name])
    commands['visa']['write'][instr_name].update(BASIC_VISA_WRITING)

##########----------------------------------------------------------------------

for instr_name in ['FSW_1']:  ### Rhode and Schwarz Specrum Analyzers
    commands['visa']['query'][instr_name] = {'b Frquency start'       : 'FREQuency:STARt?'
                                            ,'b Frquency stop'        : 'FREQuency:STOP?'
                                            ,'b Frquency center'       : 'FREQuency:CENT?'
                                            ,'b Frquency span'        : 'FREQuency:SPAN?'
                                            ### what is this doing there??,'b Source Freqeuncy'     : ':SOURce:FREQuency?'

                                            ### what is this doing there??, b  Source Power' : ':SOURce:POWer?'

                                            ,'b Bandwith'             : 'SENS1:BAND:RES?'
                                            ,'b Sweep type'           : 'SENS:SWE:TYPE?'
                                            ,'b Sweep counts'         : 'SENS1:SWE:COUNT?'
                                            ### what is this doing there??,'b Center frequency'     : 'SOUR:FREQ:FIX?'
                                            ,'b Number of Points'     : 'SENS:SWE:POIN?'
                                            ,'b Sweep time'           : 'SWE:TIME?'
                                            }
    commands['visa']['query'][instr_name].update(BASIC_VISA_QUERIES)

    commands['visa']['adopt'][instr_name] = {'command_Auto_sweep_time'       : 'SENS1:SWE:TIME:AUTO ON; TRIG1:SEQ:SOUR IMM'                                      # Avoid a delay time between different partial measurements and before the  start of the sweeps and minimize sweep time (is default setting)
                                            ,'command_Display_param'       : 'DISPLAY:WINDOW1:TRACE5:FEED "Trc1"'                                              # Show choosen parameter on display
                                            ,'command_Set_param_active'    : 'CALCULATE1:PARAMETER:SELECT "Trc1"'                                              # Choosen parameter set to active
                                            ,'command_Set_param_active'    : 'CALCULATE1:PARAMETER:SELECT "Trc1"'                                              # Choosen parameter set to active
                                            ,'command_averaging_activate'     : 'DISP:WIND:TRAC:MODE AVER'          # 'DISP:WIND:TRAC:MODE {F_averaging_activate}' #you should really only use AVER here as a parameter
                                            ,'command_return_format'     : 'FORM REAL'               # 'command_F_return_format'     : 'FORM {F_return_format}'      # REAL or ASCII.REAL returns binary numbers, ASCII returns ascii characters.REAL is faster
                                            #configures general measurement
                                            ,'command_B_reference_osci' : 'ROSC:SOUR {B_reference_osci}'
                                            #set frequency parameters for a frequency domain measurement
                                            #WE DON'T USE CENTER,'command_set_freq_cent'       : 'FREQ:CENT {frequency_center} {unit_freq_cent}'
                                            #WE DON'T USE SPAN,'command_set_span'            : 'FREQ:SPAN {frequency_span} {unit_span}'
                                            ,'command_R_bandwidth'         : 'BAND:RES {R_bandwidth} {F_unit_bandwidth}'
                                            #configure averaging/sampling parameters
                                            ,'command_N_aver'              : 'SENS1:SWE:COUNT {N_averaging}; :AVER {B_averaging}; CLE'
                                            ,'command_N_swee_point'         : 'SENS1:SWE:POIN {N_sweep_points}'        # Number of sweep points
                                            #configure averaging settings
                                            ,'command_F_averaging_type'         : 'AVER:TYPE {F_averaging_type}'               # LINear / VIDeo (logarithmic average) / POWer (converts to Watts, avgs, converts back.Don't ask me why)
                                            ,'command_F_averaging_mode'         : 'DET {F_averaging_mode}'                     # use RMS or AVER here, probably just use RMS
                                            ,'command_B_cont'               : 'INITiate1:CONTinuous {B_continous}'  # Countinuous mode ON/OFF
                                            #configures specifics for power time domain measurement
                                            ,'command_R_sweep_time'         : 'SWE:TIME {R_time_stop} {F_unit_time}'
                                            ,'command_R_freq_start_stop'  : 'FREQ:STAR {R_freq_start} {F_unit_freq}; STOP {R_freq_stop} {F_unit_freq}'        # Setting stop and start frequency for frequency sweep measurement (Active only in MLOG mode)
                                            ##    #configures specifics for power time domain averaging
                                            ##,'command_B_power_meas'  : 'CALC:MARK:FUNC:SUMM:STAT {B_power_meas}'

                                            ### ,'c Initiate immediatenly.Operation complete?' : 'INIT1:IMM; *OPC?'
                                            ### ,'c Output State ON/OFF (0/1)'                  : ':OUTPut:STATe?'
                                            }

    commands['visa']['write'][instr_name] = {}
    commands['visa']['write'][instr_name].update(commands['visa']['adopt'][instr_name])
    commands['visa']['write'][instr_name].update(BASIC_VISA_WRITING)

##########----------------------------------------------------------------------

for instr_name in session.SGS100As:

    commands['visa']['query'][instr_name] = {'b Frequency'               : 'FREQuency?'                              #query: frequency
                                            ,'b Phase'                   : 'PHASe?'                                  #query: frequency
                                            ,'b Power'                   : 'POWer:POWer?'                            #power
                                            ,'b Oscillator Reference'    : 'ROSCillator:SOURce?'                     #oscillator reference

                                            ,'c Output State ON/OFF (1/0)' : ':OUTPut?'                              #whether sg is on/off
                                            }
    commands['visa']['query'][instr_name].update(BASIC_VISA_QUERIES)

    commands['visa']['adopt'][instr_name] =  {'command_R_sour_powe'   : 'POW:POW {R_power_source}'                     #units in dBm    #set: power #??? SAME AS SOUR POW
                                            ,'command_R_phas_source'  : 'SOURce:PHASe {R_phas_source}' #frequency
                                            ,'command_R_freq_source'  : 'FREQ {R_freq_source} {F_unit_freq_source}' #frequency
                                            ,'command_reference_osci' : 'ROSC:SOUR {B_reference_osci}'           #reference oscillator source (EXT/INT)
                                            ,'command_B_output'       : 'OUTP {B_output}'                    #whether sg is on/off (ON/OFF)
                                            }

    commands['visa']['write'][instr_name] = {}
    commands['visa']['write'][instr_name].update(commands['visa']['adopt'][instr_name])
    commands['visa']['write'][instr_name].update(BASIC_VISA_WRITING)

##########----------------------------------------------------------------------

for instr_name in ['RTE1054_1']: ### Rhode and Schwarz Oscillators

    commands['visa']['query'][instr_name] = {'! ACQuire:RESolution?' : 'ACQuire:RESolution?'
                                            ,'! TIMebase:RANGe?' : 'TIMebase:RANGe?'
                                            ,'b TIMebase:SCALe?' : 'TIMebase:SCALe?'
                                            ,'b ACQuire:POINts?' : 'ACQuire:POINts?'

                                            ,'c ACQuire:MODE?' : 'ACQuire:MODE?'
                                            ,'c ACQuire:POINts:AUTO?' : 'ACQuire:POINts:AUTO?'
                                            }
    commands['visa']['query'][instr_name].update(BASIC_VISA_QUERIES)

    commands['visa']['adopt'][instr_name] = {'command_N_time_range' : 'TIMebase:RANGe {N_time_range}{S_time_unit}'
                                            ,'command_N_resolution' : 'ACQuire:RESolution {N_resolution}{S_time_unit}'
                                            }

    commands['visa']['write'][instr_name] = {'command_Acquire_mode' : 'ACQuire:POINts:AUTO {S_Acquire_mode}'}
    commands['visa']['write'][instr_name].update(commands['visa']['adopt'][instr_name])
    commands['visa']['write'][instr_name].update(BASIC_VISA_WRITING)

##########----------------------------------------------------------------------

for instr_name in ['Santec_1']: ### Rhode and Schwarz Lasers

    commands['visa']['query'][instr_name] = {}
    commands['visa']['query'][instr_name].update(BASIC_VISA_QUERIES)

    commands['visa']['adopt'][instr_name] = {'command_Pow_dBm' : 'OP{R_Pow_dBm_value}'
                                            ,'command_Shutter' : '{B_Shutter}'
                                            }

    commands['visa']['write'][instr_name] = {'command_Wavelength' : 'WA{R_Wave_value}'
                                            ,'command_Frequency' : 'FQ{R_Freq_value}'
                                            ,'command_Pow_dBm' : 'OP{R_Pow_dBm_value}'
                                            ,'command_Pow_mW' : 'LP{R_Pow_mW_value}'
                                            ,'command_LO' : 'LO'
                                            ,'command_Shutter' : '{B_Shutter}'
                                            }
    commands['visa']['write'][instr_name].update(commands['visa']['adopt'][instr_name])
    commands['visa']['write'][instr_name].update(BASIC_VISA_WRITING)

##########----------------------------------------------------------------------

for instr_name in ['Thorlabs_1']: ### Rhode and Schwarz Powermeters

    commands['visa']['query'][instr_name] = {'b Power'            : 'MEASure:SCALar:POWer?'
                                            ,'b Averaging count'  : 'SENSe:AVERage:COUNt?'
                                            }
    commands['visa']['query'][instr_name].update(BASIC_VISA_QUERIES)

    commands['visa']['adopt'][instr_name] = {}

    commands['visa']['write'][instr_name] = {'command_N_aver'     : 'SENS1:AVER:COUN {N_averaging}'
                                            }
    commands['visa']['write'][instr_name].update(commands['visa']['adopt'][instr_name])
    commands['visa']['write'][instr_name].update(BASIC_VISA_WRITING)

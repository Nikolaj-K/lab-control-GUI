"""
This file lists all initial values that are used in building the VIP GUI.
We do so by assembling a large dictionary of dictionaries of dictionaries,
called 'Tree'. From this we construct the smaller 'default' dictionary of
dictionaries. The default session dictionary assembled in the VIP_class
definition is a copy of 'default'.
"""

################################################################################
try:
    ### This except-clause is needed if you want to execute this file directly
    import dictionaries.hardware as hardware
except ImportError:
    import hardware as hardware
    print "(session.py, ImportError) It seems you executed the session file directly."

################################################################################ INSTRUMENT CLASSIFICATION

ZNB20s   = ['ZNB_1'
           ,'ZNB_2'
           ]

SGS100As = ['SGS_31'
           ,'SGS_32'
           ,'SGS_33'
           ,'SGS_34'
           ,'SGS_35'
           ,'SGS_37'
           ,'SGS_40'
           ,'SGS_41'
           ]

################################################################################ MEASUREMENT INSTURMENTS

VNA = {'ZVL_1' : {'B_continous' : 'OFF'  #,'Cont_off/on'      : 'OFF'
                  ,'F_data_form' : 'MLOG'
                  ,'F_VNA_mode'    : 'MLOG'

                  ,'R_freq_start'   : '10820'
                  ,'R_freq_stop'   : '10840'
                  ,'R_freq_source' : '15.5'
                  ,'R_power_source'   : '-10'
                  ,'R_bandwidth'   : '1'

                  ,'N_sweep_points'   : '2001'
                  ,'N_averaging'        : '1'

                  ,'F_Sij'              : 'S21'
                  ,'F_unit_bandwidth'   : 'MHz'
                  ,'F_unit_freq'   : 'MHz'
                  ,'F_unit_freq_source'    : 'MHz'

                  ,'B_averaging'       : 'OFF'
                  ,'B_reference_osci' : 'INT'
                  ,'B_connect' : 'DONT'
                  }
        }

for instr_name in ZNB20s:
    VNA[instr_name] =   {'B_continous' : 'OFF'  #,'Cont_off/on'      : 'OFF'
                        ,'F_data_form' : 'MLOG'
                        ,'F_VNA_mode'    : 'MLOG'
                        ,'R_freq_start'   : '10820'
                        ,'R_freq_stop'   : '10840'
                        ,'R_freq_source' : '15.5'
                        ,'R_power_source'   : '-10'
                        ,'R_bandwidth'   : '1'
                        ,'N_sweep_points'   : '2001'
                        ,'N_averaging'        : '1'
                        ,'F_Sij'              : 'S43'
                        ,'F_unit_bandwidth'   : 'MHz'
                        ,'F_unit_freq'   : 'MHz'
                        ,'F_unit_freq_source'    : 'MHz'
                        ,'B_averaging'       : 'OFF'
                        ,'B_reference_osci' : 'INT'
                        ,'B_connect' : 'DONT'
                        }

##########----------------------------------------------------------------------

SA = {'FSW_1' : {'R_freq_start'         : '10820'
                 ,'R_freq_stop'          : '10840'
                 ,'R_bandwidth'          : '1'
                 ,'R_time_stop'          : '10'
                 ,'N_sweep_points'       : '2001'
                 ,'N_averaging'          : '1'
                 ,'F_unit_freq'          : 'MHz'
                 ,'F_unit_time'          : 'ms'
                 ,'F_unit_bandwidth'     : 'MHz'
                 ,'F_averaging_type'     : 'LINear'
                 ,'F_averaging_mode'     : 'RMS'
                 ,'B_continous'          : 'OFF'
                 ,'B_power_meas'         : 'OFF'
                 ,'B_reference_osci'     : 'INT'
                 ,'B_connect'            : 'DONT'
                 ,'B_averaging'          : 'OFF'
                 }
     }

##########----------------------------------------------------------------------

Osci = {'RTE1054_1' : {'N_sweep_points' : '5000'
                      ,'N_resolution'   : '2'
                      ,'N_time_range'   : str(int('5000') * int('2'))
                      ,'S_time_unit'    : 'E-12' # pico second
                      ,'S_Acquire_mode' : 'RESolution'
                      ,'B_connect'      : 'DONT'
                      }
       }

##########----------------------------------------------------------------------

Laser = {'Santec_1' : {'R_Wave_value' : '1550.135'
                      ,'R_Freq_value' : '193.5300'
                      ,'R_Pow_dBm_value' : '-10'
                      ,'R_Pow_mW_value' : '0.1'
                      ,'B_connect'  : 'DONT'
                      ,'B_Shutter'  : 'SC'
                      ,'F_freq_or_wave' : 'FREQ'
                      ,'F_dBm_or_mW' : 'DBM'
                      }
        }

##########----------------------------------------------------------------------

WM = {'WM1210_1'   : {'S_device_key'  : 'WM-1210 SN0222' ### Wavelengthmeter
                     ,'R_sleep_time'  : '0.2'
                     ,'R_dWavelength' : '0.0'                                    
                     ,'R_dPower'      : '0.0'                                     
                     ,'B_connect'     : 'DONT'
                     }
     }

##########----------------------------------------------------------------------

PM = {'Thorlabs_1' : {'N_averaging' : '100' ### Powermeter
                     ,'B_connect'  : 'DONT'
                     }
     }

##########----------------------------------------------------------------------

Dig = {'ATS9870_1' : {'N_records_per_buffer'       : '250'
                     ,'N_buffers_per_acquisition'  : '400'
                     ,'N_trigger_level_1'          : '160'
                     ,'N_trigger_delay'            : '0'
                     ,'F_trigger_source_1'         : 'External'
                     ,'F_channelA_range'           : '0.04'
                     ,'F_channelB_range'           : '0.04'
                     ,'F_channelA_coupling'        : 'AC'
                     ,'F_channelB_coupling'        : 'AC'
                     ,'F_trigger_edge_1'           : 'POSITIVE'
                     ,'F_use_channel'              : 'A'
                     ,'N_sweep_points'             : '404'
                     ,'F_decimation'               : '405'
                     ,'R_intermediate_frequency'   : '0' ###MHZ
                     ,'R_filter_frequency'         : '0' ###MHZ

                     ,'B_connect'                  : 'DONT'
                     }
      ,'NI_DAQ_1'  : {'N_buffers_per_acquisition'  : '400'
                     ,'B_connect'                  : 'DONT'
                     }
      }

################################################################################ SOURCE INSTURMENTS

SG = {}
for instr_name in SGS100As:
    SG[instr_name] = {'R_power_source'     : '0'
                     ,'R_freq_source'      : '8'
                     ,'R_phas_source'      : '0'
                     ,'F_unit_freq_source' : 'GHz'
                     ,'B_output'           : 'OFF'
                     ,'B_reference_osci'   : 'EXT'
                     ,'B_connect'          : 'DONT'
                     }
                     
##########----------------------------------------------------------------------

AWG = {'H3344_1' : {'B_connect'            : 'DONT'
                   ,'R_amplitude_0'        : '0.1'
                   ,'R_amplitude_1'        : '0.1'
                   ,'R_amplitude_2'        : '0.1'
                   ,'R_amplitude_3'        : '0.1'
                   ,'R_offset_0'           : "0"
                   ,'R_offset_1'           : "0"
                   ,'R_offset_2'           : "0"
                   ,'R_offset_3'           : "0"
                   ,'B_use_trigger'        : "ON"
                   ,'FILE_PATH_waveform_0' : "E:\Measurement_Software\VIP\Data\Waveforms\dummy_name1.csv"
                   ,'FILE_PATH_waveform_1' : "E:\Measurement_Software\VIP\Data\Waveforms\Generated_waveforms\gaussian_matilda_short004.csv"
                   ,'FILE_PATH_waveform_2' : "E:\Measurement_Software\VIP\Data\Waveforms\dummy_name3.csv"
                   ,'FILE_PATH_waveform_3' : "E:\Measurement_Software\VIP\Data\Waveforms\dummy_name4.csv"
                   }
      }

for ch in hardware.range_H3344_channels:
    k = 'B_channel_'+ch
    AWG['H3344_1'][k] = 'OFF'

##########----------------------------------------------------------------------

NI_pulse = {'NI_pulse_1' : {'R_pulse_time' : '40'
                           ,'F_unit_time'  : 'ms'
                           ,'F_use_config' : '2: Spec - Fridge - SA'
                           ,'N_device'     : '1'
                           ,'N_port'       : '0'
                           ,'B_connect'    : 'DONT'
                           }
           }

for sk in NI_pulse:
    NI_pulse[sk].update(hardware.NI_pulse)
    for p in hardware.range_NI_pins:
        NI_pulse[sk]['B_pin_'+p] = '0'

##########----------------------------------------------------------------------

Delft = {'Delft_1' : {'F_interface' : 'COM1'
                     ,'F_polarity'  : 'R_BIP'
                     ,'F_channel'   : '3'
                     ,'B_connect'   : 'DONT'
                     }
        }

range_DACs       = [str(i) for i in range(1, 1+int(hardware.Delft['N_DACs']))]
zero_init_mvolts = {'R_volt_channel_'+i : '0' for i in range_DACs}

for sk in Delft:
    Delft[sk].update(hardware.Delft)
    Delft[sk].update(zero_init_mvolts)

################################################################################ SCRIPTS

Scripts = {'Freq. vs. drive power' : {"Sweep_instr"           : "SGS_33"
                                     ,"VNA_instr"             : "ZNB_1"
                                     ,"R_freq_cavity_VNA"     : "7.9524" # GHz
                                     ,"R_freq_span_cavity_VNA": "100" # Hz
                                     ,"R_power_SG"            : "-40" # Hz
                                     ,"R_freq_start_SG"       : "11.2" # GHz
                                     ,"R_freq_stop_SG"        : "11.4" # GHz
                                     ,"R_freq_step_size_SG"   : "0.1" # GHz
                                     ,"R_power_start_SG"      : "-40" # GHz
                                     ,"R_power_stop_SG"       : "-20" # GHz
                                     ,"R_power_step_size_SG"  : "10" # GHz
                                     }
          ,"Printer demo"          : {'string_to_print'  : '...this is the "Printer Demo" LineEdit string :)'}
          ,"Freq. query"           : {'TITLE_instr_name' : 'SGS_32'}
          ,"Mixer calib."          : {"center_freq"      : "10"
                                     ,"int_freq"         : "0"
                                     ,'R_amplitude'      : "0.5"
                                     ,'LO_source'        : 'SGS_31'
                                     ,'spec_source'        : 'SGS_31'
                                     }
          ,'Mixer-Dig VNA'         : {"start_freq"       : "6000000000"
                                     ,"stop_freq"        : "12000000000"
                                     ,"points"           : "301"
                                     ,"IF_freq"          : "100000000"
                                     ,"source_LO"        : 'SGS_32'
                                     ,"source_rf"        : 'SGS_31'
                                     }
          ,"Flux sweep"            : {"vna_ip"           : 'ZNB_1'
                                     ,"ssg_ip"           : 'SGS_33'
                                     ,"com_port"         : "1"
                                     ,"dac_port"         : "1"
                                     ,"cav_freq"         : "7.953"
                                     ,"span"             : "10"
                                     ,"pow"              : "-40"
                                     ,"start_freq"       : "10"
                                     ,"stop_freq"        : "12"
                                     ,"step_size_ssg"    : "0.1"
                                     ,"start_flux"       : "0"
                                     ,"stop_flux"        : "1"
                                     ,"step_size_srs"    : "0.1"
                                     ,"fn"               : "test_file_name"
                                     }
          }

################################################################################ SWEEPS

Sweep_1 = {'Power sweep 1'   :  {'R__start'      : '-20'
                                ,'R__stop'      : '0'
                                ,'N__sweep_points' : '5'
                                ,'F__unit_sweep'    : '~dBm'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'ZNB_1'
                                }
          ,'Freq. sweep 1'   :  {'R__start'      : '2'
                                ,'R__stop'      : '8'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'    : 'GHz'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'SGS_33'
                                }
          ,'Voltage sweep 1' :  {'R__start'        : '0'
                                ,'R__stop'         : '0'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'   : '~mV'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'Delft_1' 
                                }
          ,'Phase sweep 1' :    {'R__start'        : '0'
                                ,'R__stop'         : '0'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'   : '~Degree'
                                ,'F_axis_mode'     : 'Linear'
                                ,'F_instr_name'    : 'SGS_32'
                                }
            ,'File sweep 1'   : {'DIR__PATH' : 'E:\Measurement_Software\VIP\Data\Waveforms'
                                ,'FILE__NAME_0' : 'dummy_name'
                                ,'CHANNEL__SWEEP_0' : '0'
                                ,'FILE__NAME_1' : 'dummy_name'
                                ,'CHANNEL__SWEEP_1' : '1'
                                ,'R__start'      : '0'
                                ,'R__stop'      : '0'
                                ,'N__sweep_points' : '1'
                                ,'F__unit_sweep'    : '~'
                                ,'F_axis_mode'    : 'dBm' ### don't change
                                ,'F_instr_name'    : 'H3344_1'
                                }
            ,'AWG sweep 1' :  {'R__start'        : '0'
                                ,'R__stop'         : '0'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'   : '~V'
                                ,'F__sweep_type'   : 'Amplitude'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'H3344_1' 
                                }
          ,'From trace'       : {
                                }
          }

##########----------------------------------------------------------------------

Sweep_2 = {'Power sweep 2'   : {'R__start'      : '-99'
                                ,'R__stop'      : '0'
                                ,'N__sweep_points' : '5'
                                ,'F__unit_sweep'    : '~dBm'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'ZNB_1'
                                }
          ,'Freq. sweep 2'   : {'R__start'      : '2'
                                ,'R__stop'      : '8'
                                ,'N__sweep_points'    : '3'
                                ,'F__unit_sweep'    : 'GHz'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'SGS_34'
                                }
          ,'Voltage sweep 2' : {'R__start'      : '0'
                                ,'R__stop'      : '0'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'    : '~mV'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'Delft_1' 
                                }
          ,'Phase sweep 2' :    {'R__start'        : '0'
                                ,'R__stop'         : '0'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'   : '~Deg'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'SGS_32'
                                }
            ,'File sweep 2'   : {'DIR__PATH' : 'E:\Measurement_Software\VIP\Data\Waveforms'
                                ,'FILE__NAME_0' : 'dummy_name'
                                ,'CHANNEL__SWEEP_0' : '0'
                                ,'FILE__NAME_1' : 'dummy_name'
                                ,'CHANNEL__SWEEP_1' : '1'
                                ,'R__start'      : '0'
                                ,'R__stop'      : '0'
                                ,'N__sweep_points' : '1'
                                ,'F__unit_sweep'    : '~'
                                ,'F_axis_mode'    : 'dBm' ### don't change
                                ,'F_instr_name'    : 'H3344_1'
                                }
            ,'AWG sweep 2' :  {'R__start'        : '0'
                                ,'R__stop'         : '0'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'   : '~V'
                                ,'F__sweep_type'   : 'Amplitude'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'H3344_1' 
                                }
          }

##########----------------------------------------------------------------------

Sweep_3 = {'Power sweep 3'   : {'R__start'      : '-20'
                                ,'R__stop'      : '0'
                                ,'N__sweep_points' : '5'
                                ,'F__unit_sweep'    : '~dBm'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'ZNB_1'
                                }
          ,'Freq. sweep 3'   : {'R__start'      : '2'
                                ,'R__stop'      : '8'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'    : 'GHz'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'SGS_34'
                                }
          ,'Voltage sweep 3' : {'R__start'      : '0'
                                ,'R__stop'      : '0'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'    : '~mV'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'Delft_1' 
                                }
          ,'Phase sweep 3' :    {'R__start'        : '0'
                                ,'R__stop'         : '0'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'   : '~Deg'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'SGS_32'
                                }
            ,'File sweep 3'   : {'DIR__PATH' : 'E:\Measurement_Software\VIP\Data\Waveforms'
                                ,'FILE__NAME_0' : 'dummy_name'
                                ,'CHANNEL__SWEEP_0' : '0'
                                ,'FILE__NAME_1' : 'dummy_name'
                                ,'CHANNEL__SWEEP_1' : '1'
                                ,'R__start'      : '0'
                                ,'R__stop'      : '0'
                                ,'N__sweep_points' : '1'
                                ,'F__unit_sweep'    : '~'
                                ,'F_axis_mode'    : 'dBm' ### don't change
                                ,'F_instr_name'    : 'H3344_1'
                                }
            ,'AWG sweep 3' :  {'R__start'        : '0'
                                ,'R__stop'         : '0'
                                ,'N__sweep_points' : '3'
                                ,'F__unit_sweep'   : '~V'
                                ,'F__sweep_type'   : 'Amplitude'
                                ,'F_axis_mode'     : 'dBm'
                                ,'F_instr_name'    : 'H3344_1' 
                                }
          }

for ch in hardware.range_H3344_channels:
    k = 'USE_channel_'+ch
    Sweep_1['AWG sweep 1'][k] = 'DONT_USE'
    Sweep_2['AWG sweep 2'][k] = 'DONT_USE'
    Sweep_3['AWG sweep 3'][k] = 'DONT_USE'

################################################################################ CONTROL

Points = {'Power point' : {'F_instr_name'    : "FSW_1"
                          ,'B_lock_to_freq'  : 'ON'
                          ,'F_lock_to_sweep' : 'Freq. sweep 1'
                          ,'F_frequency_shift' : '0'
                          }
         ,'I Q point'   : {'F_instr_name'    : 'ZNB_1'
                          ,'B_lock_to_freq'  : 'OFF'
                          ,'F_lock_to_sweep' : 'Freq. sweep 1'
                          ,'F_frequency_shift' : '0'
                          }
         }

##########----------------------------------------------------------------------

Traces = {'Freq. trace' : {'F_instr_name'   : 'ZNB_1'
                          ,'R_freq_start'   : '10.81'
                          ,'R_freq_stop'    : '10.84'
                          ,'F_unit_freq'    : 'GHz'
                          ,'F_axis_mode'    : 'Linear' ### dummy, don't change
                          ,'N_sweep_points' : '2001'
                          }
         ,'Time trace'  : {'F_instr_name'   : 'FSW_1'
                          ,'F_unit_freq'    : 'GHz'
                          ,'R_freq_start'   : '9.31' ### R_freq_start = R_freq_stop
                          ,'R_freq_stop'    : '9.31' ### R_freq_start = R_freq_stop

                          ,'R_time_start'   : '0'    ### fixed value 0, only used to generate sweep axis
                          ,'R_time_stop'    : '10'
                          ,'N_sweep_points' : '1001'
                          ,'F_unit_time'    : 'ms'
                          ,'F_axis_mode'    : 'Linear'
                          }
         ,'Dig. sample' : {'F_instr_name'               : 'ATS9870_1'
                          ,'N_records_per_buffer'       : '250'
                          ,'N_buffers_per_acquisition'  : '400'

                          ,'N_samples_factor'           : '16'
                          ,'N_samples_start'            : '0'      ### fixed value 0, only used to generate sweep axis
                          ,'N_sweep_points'             : '1024'
                          ,'F_decimation'               : '1'
                          ,'N_samples_stop'             : '1024'
                          ,'F_unit_time'                : '~ns'
                          ,'F_axis_mode'                : 'Linear'
                          ,'F_intermediate_frequency'   : '25' ###MHZ
                          }
         }

##########----------------------------------------------------------------------

System = {'Session'  : {'FILE_PATH_session'    : "INIT"
                       ,'F_dict_index'         : '0'
                       }
         ,'Results'  : {'DIR_PATH_results'     : "INIT"
                       ,'TITLE_result'         : 'Measurement'
                       ,'N_result_index'       : '1'
                       ,'B_save_result'        : 'OFF'
                       ,'B_save_session'       : 'OFF'
                       ,'B_save_screenshot'    : 'OFF'
                       }
         ,'Options' : {"R_x_plot_label_rotation" : "0"
                      ,"R_axes_font_size"        : "12"
                      ,"R_x_plot_position"       : "0.25"
                      ,"R_y_plot_position"       : "0.13"
                      ,"R_x_plot_size"           : "0.7"
                      ,"R_y_plot_size"           : "0.8"
                      ,"FILE_PATH_notes"         : "INIT"
                      ,
                      }
         }

##########----------------------------------------------------------------------

Measurement = {'Meas_main'  : {'meas_type'       : 'Freq. trace'
                              ,'B_during_sweep_1': 'ON'
                              }
              ,'Sweep'  : {'sweep_title_1' : 'From trace'
                          ,'sweep_title_2' : 'Freq. sweep 2'
                          ,'sweep_title_3' : 'Power sweep 3'
                          ,'B_is_max_1'          : 'OFF'
                          ,'B_is_max_2'          : 'ON'
                          ,'B_is_max_3'          : 'OFF'
                          ,'B_find_min'          : 'OFF'
                          }
              ,'Script' : {'script_title_1'   : 'Power from freq.'
                          ,'script_title_2'   : 'Printer demo'
                          ,'script_title_3'   : 'Mixer calib.'
                          ,'B_during_sweep_1' : 'OFF'
                          ,'B_during_sweep_2' : 'OFF'
                          ,'B_during_sweep_3' : 'OFF'
                          }
              }

##########----------------------------------------------------------------------

### Note: This handle, 'Plot', is accessed from '.update_figures' in VIP_Qwidget
Plot  = {'Plot_column_1' : {'F_data_set'      : 'P__dBm'
                                 ,'F_plot_function' : 'density'
                                 ,'B_keep_updated'  : 'ON'
                                 }
        ,'Plot_column_2' : {'F_data_set'      : 'phi___'
                                 ,'F_plot_function' : 'density'
                                 ,'B_keep_updated'  : 'ON'
                                 }
        ,'Plot_column_3' : {'F_data_set'      : 'I_data'
                                 ,'F_plot_function' : 'density'
                                 ,'B_keep_updated'  : 'OFF'
                                 }
        ,'Plot_column_4' : {'F_data_set'      : 'Q_data'
                                 ,'F_plot_function' : 'surface'
                                 ,'B_keep_updated'  : 'OFF'
                                 }
        }

################################################################################ Create default session dictionary
"""
The 'Tree' dictionary contains all the information defined above and is then
torn apart and its data is saved into various smaller dictionaries and lists.
"""

Tree = {'_Experiment'   : {'System'      : System
                          ,'Measurement' : Measurement
                          ,'Plot'        : Plot
                          }
       ,'_Sweeps'       : {'Sweep_1' : Sweep_1
                          ,'Sweep_2' : Sweep_2
                          ,'Sweep_3' : Sweep_3
                          }
       ,'_Routines'     : {'Traces'  : Traces
                          ,'Points'  : Points
                          ,'Scripts' : Scripts
                          }
       ,'_Meas_Instr'   : {'VNA'   : VNA    ### Vector Network Analyzer
                          ,'SA'    : SA     ### Spectrum Analyzer
                          ,'Osci'  : Osci   ### Oscilloscope
                          ,'WM'    : WM     ### Wavelengthmeter
                          ,'PM'    : PM     ### Powermeter
                          ,'Dig'   : Dig    ### Digitizer
                          }
       ,'_Source_Instr' : {'SG'        : SG       ### Spource Generator
                          ,'Delft'     : Delft    ### (Delft) Voltage Generator
                          ,'NI_pulse'  : NI_pulse ### (National Instruments) Pin Pulse Generator
                          ,'AWG'       : AWG      ### Arbitrary Waveform Generator
                          ,'Laser'     : Laser    ### "Laser"
                          }
        }

##########----------------------------------------------------------------------

from interface.auxiliary_functions import cut_top
from interface.auxiliary_functions import cut_bottom

instr_fine_grained   = {k : cut_bottom(Tree[k]) for k in ['_Meas_Instr', '_Source_Instr']}
instr_classification = cut_top(instr_fine_grained)
instr_class_list     = instr_classification.keys()
instr_list           = cut_top(instr_classification)

class_classification = cut_bottom(Tree)
super_class_list     = class_classification.keys()

tab_classification   = cut_bottom(cut_top(Tree))
class_list           = tab_classification.keys()

default              = cut_top(cut_top(Tree)) ### The default session dictionary.
tab_list             = default.keys()

################################################################################
if __name__ == "__main__":
    print instr_classification

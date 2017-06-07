#import hardware

################################################################################
FREQUENCY_UNITS    = ['Hz', 'kHz', 'MHz', 'GHz']
TIME_UNITS         = ['ms']
AXIS_MODES         = ['Linear', 'dBm', 'Watts', 'Volts']

DATA_SET_KEYS      = ['I_data', 'Q_data', 'P__dBm', 'phi___', 'P__dB_', 'phidiv']
PLOT_DIM_KEYS      = ['2d_data', '3d_data']
PLOT_FUNCTION_KEYS = ['density', 'surface']

def _matrix_element_list(string, n):
    indices = [str(k) for k in range(1, 1+n)]
    return [string+i+j for j in indices for i in indices if j != i]

MATRIX_ELEMENTS_2x2 = _matrix_element_list('S', 2)
MATRIX_ELEMENTS_4x4 = _matrix_element_list('S', 4)

################################################################################
ATS9870 = {}
try:
    import external.atsapi as ats
    ATS9870['F_trigger_source_1']  = {'Channel A' : ats.TRIG_CHAN_A   ### = 0
                                     ,'Channel B' : ats.TRIG_CHAN_B   ### = 1
                                     ,'External'  : ats.TRIG_EXTERNAL ### = 2
                                     ,'Disable'   : ats.TRIG_DISABLE  ### = 3
                                     }
    ATS9870['F_channelA_coupling'] = {'AC'        : ats.AC_COUPLING
                                     ,'DC'        : ats.DC_COUPLING
                                     }
    ATS9870['F_channelB_coupling'] = {'AC'        : ats.AC_COUPLING
                                     ,'DC'        : ats.DC_COUPLING
                                     }
    ATS9870['F_use_channel']       = {'A'         : ats.CHANNEL_A
                                     ,'B'         : ats.CHANNEL_B
                                     ,'A and B'   : ats.CHANNEL_A | ats.CHANNEL_B
                                     }
    ATS9870['F_trigger_edge_1']    = {'POSITIVE'  : ats.TRIGGER_SLOPE_POSITIVE
                                     ,'NEGATIVE'  : ats.TRIGGER_SLOPE_NEGATIVE
                                     }
    ATS9870['F_channelA_range']    = {'0.04' : ats.INPUT_RANGE_PM_40_MV
                                     ,'0.1'  : ats.INPUT_RANGE_PM_100_MV
                                     ,'0.2'  : ats.INPUT_RANGE_PM_200_MV
                                     ,'0.4'  : ats.INPUT_RANGE_PM_400_MV
                                     ,'1.0'  : ats.INPUT_RANGE_PM_1_V
                                     ,'2.0'  : ats.INPUT_RANGE_PM_2_V
                                     ,'4.0'  : ats.INPUT_RANGE_PM_4_V
                                     }
    ATS9870['F_channelB_range']    = ATS9870['F_channelA_range']
    ATS9870['F_decimation']        = {str(k) : k for k in [1,2,4]+[10,20,30,40]}

except ImportError as exception: ### Except WindowsError...
    print "!! (menus, Exception) import external.atsapi as ats:"
    print exception
    substitute = {'F_trigger_source_1'  : {'External' : '404'}
                 ,'F_channelA_range'    : {'0.04'     : '405'}
                 ,'F_channelB_range'    : {'0.04'     : '406'}
                 ,'F_decimation'        : {'1'        : '407'}
                 ,'F_channelA_coupling' : {'AC'       : '408'}
                 ,'F_channelB_coupling' : {'AC'       : '409'}
                 ,'F_use_channel'       : {'A'        : '410'}
                 ,'F_trigger_edge_1'    : {'Positive' : '411'}
                 }
    ATS9870.update(substitute)

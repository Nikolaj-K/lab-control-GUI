from DriverVISA_Parent import DriverVISA as DriverVISA

import dictionaries.constants as cs

################################################################################

class DriverFSW(DriverVISA): # Rohde & Schwarz Vector Network Analyzer
    
    def __init__(self, instr_name):
        super(DriverFSW, self).__init__(instr_name)

##########

    def adopt_settings(self, settings): # overwrites the verion in META
        self.update_settings(settings)
        B_time_domain_mode = (self._local['R_freq_start'] == self._local['R_freq_stop'])

        for k in sorted(self.adopt_dict.keys()):
            if B_time_domain_mode and k == 'command_Auto_sweep_time':
                pass
            elif (not B_time_domain_mode) and k == 'command_R_sweep_time':
                pass
            else:
                self.write_key_value(k)
                    
##########
    def go_to_time_domain_mode(self):
        self.set_frequency_span("0", "GHz")
        
    def set_frequency_span(self, arg, unit):    
        freq = str(arg)+cs.BLANK+unit
        self.write('FREQ:SPAN '+freq)

    def set_center_frequency(self, arg, unit):
        freq = str(arg)+cs.BLANK+unit
        self.write('FREQ:CENT '+freq)
        
##########
    def get_trace(self):  # Stimulus values (x-axis) and trace
        self._INIT_IMM_OPC()
        if True:                                                                #self._local['F_trace_value'] == 'P':
            self.write('FORM REAL')    
            ### powers
            list_1 = self.Resource.query_binary_values('TRACe:DATA? TRACE1')             
            ###,converter='f')  ## Returns trace values from power axis only            
        else: ### IQ MODE
            print(self.query('TRAC:IQ:STAT?'))
            self.write('TRAC:IQ:STAT ON')
            print(self.query('TRAC:IQ:STAT?'))
            print(self.query('TRAC:IQ:DATA:FORM?'))
            self.write('TRAC:IQ:DATA:FORM IQP')
            self.write('TRAC:IQ:SET NORM,50MHZ,81.6MHZ,IMM,POS,0,1000')
            self.write('FORM REAL,32')    
            list_1 = self.Resource.query_ascii_values('TRAC:IQ:DATA?', converter='f')
        return list_1, None, None, None

    def measure_power(self, center_frequency = None):
        if center_frequency is not None:
            self.write('FREQ:CENT'+cs.BLANK+str(center_frequency))
        self.write('CALC:MARK:FUNC:SUMM:STAT ON')
        self.write('CALC:MARK:FUNC:SUMM:MEAN ON')
        self._INIT_IMM_OPC()
        return float(self.query('CALC:MARK:FUNC:SUMM:MEAN:RES?'))
         
    def _INIT_IMM_OPC(self):
        self.write('INIT1:IMM; *OPC?')  
        ### Immediatenly Initiating measurement and waiting till measurement is done. 
        ### The '1' after 'INIT' is probably unnecessary.


################################################################################ RS_FSW_SSA_SCPI instructions for SSA
################################################################################ (by Andreas Butler)
"""
General:
    ### usually you can specify which trace you are talking about by appending '1' or '2' to the end of the first word in a command
    ### note that the {} are not actually to be included when writing variable values, they are only included here for clarity
    writes:
        *RST # resets the instr to default settings
       
            ### one way to set frequency domain of measurement ###
        [SENS]:FREQ:STAR {start_frequency} # sets the starting frequency of the measurement sweep
        [SENS]:FREQ:STOP {stop_frequency}  # sets the stopping frequency of the measurement sweep
       
            ### another way to set frequency domain of measurement ###
        [SENS]:FREQ:CENT {center_frequency} # sets the center frequency of the measurement sweep
        [SENS]:FREQ:SPAN {frequency_span} # sets the span of the frequencies of the measurement sweep
       
        [SENS]:BAND:RES {bandwidth}    # sets the bandwidth of the measurement
        [SENS]:SWE:POIN {num_sweep_points} # sets the number of data points measured per sweep
       
        INIT:CONT {ON/OFF} # turns continuous measurement on/off (OFF will set instr in single sweep mode)
        DISP:WIND:TRAC:MODE AVER # turns on sweep averaging
        [SENS]:SWE:COUNT {sweep_count} # sets the number of sweeps the instrument makes (for averaging purposes)
       
        [SENS]:SWE:TIME {sweep_time} # sets the time for the sweep (should only be set for time domain measurements, otherwise SWE:TIME:AUTO automatically set OFF)
        [SENS]:SWE:TIME:AUTO {ON/OFF} # should be ON for freq domain measurements, OFF for time domain (when you want to set your own sweep time)
   
        FORM {REAL/ASCII} # sets the data return format to be either ascii (ASCII)(comma separated human readable values), or binary (REAL)(bin values returned faster)
   
    queries:
        ### All instr state variables can be queried by adding a question mark to their corresponding write commands ###
        ### If you must programatically use any syst state vars, only use values that you query from the instr to ensure correctness ###
   
        INIT:IMM; OPC? # conducts a measurement and does not continue executing commands until it is complete
        TRAC:DATA? TRACE1 # queries trace 1 data (the default trace for the ssa)
        SYST:ERR? # queries any error message the system currently has stored
   
   
###***NOTE THAT THE TRAC:DATA? TRACE1 QUERY DOES NOT RETURN x-axis VALUES, YOU MUST CONSTRUCT THESE YOURSELF***###   
Flow for spectrum power measurement ({v} is a standin for whatever value you want within the instr's specs):
    FREQ:CENT {v} # set the center frequency of the measurement (*RST default = fmax/2)
    FREQ:SPAN {v} # set the frequency span of the measurement  (*RST default = full span (fmax))
   
    SWE:POIN {v} # set the number of sweep points (*RST default = 1001)
   
    INIT:CONT OFF # turn on single sweep mode (*RST default = ON)
    DISP:WIND:TRAC:MODE AVER # turn on sweep averaging (*RST default = ?)
    SWE:COUNT {v} # set the number of sweeps to run for one measurement (*RST default = 0)

    FORM REAL,32 # set data to be returned as 32 bit binary numbers (the python method will translate these for you) (*RST default = ASCII)
   
    INIT:IMM; *OPC? # begin instruction immediately and wait for its completion
    TRAC:DATA? TRACE1 # collect the measurement data from TRACE1
   

Flow for time domain power measurement:
    FREQ:CENT {v}
    FREQ:SPAN 0 # setting the frequency span to 0 puts the instr into time-domain mode (ie: 0-span mode)
    SWE:TIME {v} # set the sweep time of the measurement (*RST default = depends on your settings, determined by AUTO unless you set this value yourself)
   
    INIT:CONT OFF
    DISP:WIND:TRAC:MODE AVER
    SWE:COUNT {v}
   
    FORM REAL,32
   
    INIT:IMM; *OPC?
    TRAC:DATA? TRACE1
   
Flow for average power measurement:   
    FREQ:CENT {v}
    FREQ:SPAN 0 # setting the frequency span to 0 puts the instr into time-domain mode (ie: 0-span mode)
    SWE:TIME {v} # set the sweep time of the measurement (*RST default = depends on your settings, determined by AUTO unless you set this value yourself)
   
    INIT:CONT OFF
    DISP:WIND:TRAC:MODE AVER
    SWE:COUNT {v}
   
    FORM REAL,32
   
    CALC:MARK:FUNC:SUMM:STAT ON # turn on time domain power calculations (default is OFF, and when off, attempting to call the following CALC:MARK:FUNC functions will yield an error)
    CALC:MARK:FUNC:SUMM:MEAN ON # turn on power averaging calculation
    CALC:MARK:FUNC:SUMM:RMS ON  # turn on RMS power averaging calculation
   
    CALC:MARK:X:SLIM ON # turn on time domain calculation limits (enables the next commands)
    CALC:MARK:X:SLIM:LEFT {v} # set the left calculation time limit
    CALC:MARK:X:SLIM:RIGHT {v} # set the right calculation time limit
   
    INIT:IMM; *OPC?
   
    CALC:MARK:FUNC:SUMM:MEAN:RES? # query the mean power of the measurment
    CALC:MARK:FUNC:SUMM:RMS:RES?  # query the RMS power of the measurement


Flow for IQ measurement (if needed):
    FREQ:CENT {v}
    FREQ:SPAN 0 # setting the frequency span to 0 puts the instr into time-domain mode (ie: 0-span mode)

    TRAC:IQ:STAT ON # enables IQ mode (other IQ instructions will give errors unless this has first been called)
    TRAC:IQ:DATA:FORM IQP # sets data to be returned as a list of interleaved I/Q pairs [I,Q,I,Q,...,I,Q]
    TRAC:IQ:SET NONE,{bandwidth_res},{sample_rate},{trigger_source},{trigger_slope},{pretrigger_samples},{num_samples}
        # configures the IQ measurement.trigger_source should probably be set to EXT (external), trigger_slope to POS (positive), pretrigger_samples to 0.the rest is up to your discretion
   
    INIT:IMM; *OPC?
   
    TRAC:IQ:DATA? # new command for querying IQ data

        



 10.21.17.202
 port 10.21.17.202_01
"""



from DriverVISA_Parent import DriverVISA as DriverVISA

import dictionaries.constants as cs

################################################################################

class DriverZNB20(DriverVISA): # Rohde & Schwarz Vector Network Analyzer
    
    def __init__(self, instr_name):    
        super(DriverZNB20, self).__init__(instr_name)
                      
##########

    def set_power(self, val_arg, unit_arg): ### unit_arg is ignored
        settings = {'R_power_source' : val_arg}
        self.update_settings(settings)
        self.write_key_value('command_R_sour_powe') # defined in the meta drive
        ### TODO implement: unit_arg
        
    def set_center_frequency(self, arg, unit):
        command = 'FREQ:CENT'+cs.BLANK+str(arg)+cs.BLANK+unit  
        self.write(command)
        
    def set_frequency_span(self, arg, unit): 
        command = 'FREQ:SPAN'+cs.BLANK+str(arg)+cs.BLANK+unit 
        self.write(command)

##########
      
    def get_stimu(self): # Stimulus values (x-axis) and trace   
        self.write('CALC:FORM: MLOG')
        self.write('FORM:DEXP:SOUR FDAT') 
        self.write('FORM REAL') 
        frequency_axis = self.Resource.query_binary_values('TRAC:STIM? CH1DATA')    # Trace stimulus readout (x-axes)   # 'TRAC:STIM? CH1DATA' 
        #frequency_axis = self.Resource.query_ascii_values('TRAC:STIM? CH1DATA', converter = 'f')    # Trace stimulus readout (x-axes)   # 'TRAC:STIM? CH1DATA'
        return frequency_axis
        
    def get_trace(self): # Stimulus values (x-axis) and trace 
        self._INIT_IMM_OPC()
        self.write('FORM REAL')
        trace = self.Resource.query_binary_values('CALC:DATA? SDAT')    # Trace values   readout (y-axes), real and imaginary
        #trace  = self.Resource.query_ascii_values('CALC:DATA? SDAT', converter = 'f')    # Trace values   readout (y-axes), real and imaginary
        # I'm pretty sure FDATa returns power.The results from SDAT and MDAT appear to be the same.
        # For get_trace and get_point, Josip had the command 'self.write('SENS1:AVER:CLE;')' commented out.
        return trace[0::2], trace[1::2], None, None
        """SDATa...Unformatted trace data: Real and imaginary part of each measurement point.
        2 values per trace point irrespective of the selected trace format.The trace mathematics is not taken into account.
        MDATa...Unformatted trace data (see SDATa) after evaluation of the trace mathematics.
        FDATa...Formatted trace data, according to the selected trace format (CALCulate<Chn>:FORMat).
        1 value per trace point for Cartesian diagrams, 2 values for polar diagrams.
                    
        converter = 'f' is also the default.If you e.g.use converter = 'x', you get hexidecimal data
        One can also specify a different seperator, e.g.with seperator = '$'"""
          
    def _INIT_IMM_OPC(self):
        self.write('INIT1:IMM; *OPC?')  
        # Immediatenly Initiating measurement and waiting till measurement is done. #n The '1' after 'INIT' is probably unnecessary
                           
"""
def get_point(self): # measurement average as single point                                                          
    
    self.write('INIT1:IMM; *OPC?')                                       # Initiating measurement and waiting till measurement is done.#n The '1' after 'INIT' is probably unnecessary.
    
    trace = self.Resource.query_ascii_values('CALC:DATA? FDAT', converter='f')    # Trace readout (this is tmp_FDAT above). Not using _query_trace because of speed
    
    return float(sum(trace)/len(trace))  

def get_unit(self): # Return value (y-axis) unit in string format 
    if self.settings['Data_format']   == 'MLIN':
        return  '%'
    elif self.settings['Data_format'] == 'MLOG':
        return 'dB' 
    elif self.settings['Data_format'] == 'PHAS' or 'UPH':                     #? where is phase delay??
        return 'deg'
    else:
        return 'arb.u.'                                                        # Arbitrary unit
"""                                                         



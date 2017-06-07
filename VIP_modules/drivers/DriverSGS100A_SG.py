from DriverVISA_Parent import DriverVISA

################################################################################

class DriverSGS100A(DriverVISA):   # Rohde & Schwarz Source, 100 Amperes

    def __init__(self, instr_name):
        super(DriverSGS100A, self).__init__(instr_name)
        
##########
    def set_frequency(self, val_arg, unit_arg):
        settings = {'R_freq_source'      : str(val_arg)
                   ,'F_unit_freq_source' : unit_arg
                   }
        self.update_settings(settings)
        self.write_key_value('command_R_freq_source')

    def set_power(self, val_arg, unit_arg=None):                             
        ### Note: 'unit_arg' is not actually used/implemented yet.
        settings = {'R_power_source' : str(val_arg)}
        self.update_settings(settings)
        self.write_key_value('command_R_sour_powe')

    def set_phase(self, val_arg, unit_arg=None):                             
        ### Note: 'unit_arg' is not actually used/implemented yet.
        settings = {'R_phas_source' : str(val_arg)}
        self.update_settings(settings)
        self.write_key_value('command_R_phas_source')

##########
    def get_frequency(self):
        message = self.get_info_value('b Frequency')
        print "(get_frequency) Result: "+message
        return message

    def get_power(self):
        message = self.get_info_value('b Power')
        print "(get_power) Result: "+message 
        return message



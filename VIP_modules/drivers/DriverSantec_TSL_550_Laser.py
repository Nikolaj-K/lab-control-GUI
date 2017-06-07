from DriverVISA_Parent import DriverVISA

import time

################################################################################
class DriverSantec_TSL_550(DriverVISA):

    def __init__(self, instr_name):
        super(DriverSantec_TSL_550, self).__init__(instr_name)

##########
    def get_stuff(self, R_wa_min=1550.123, N_wa_steps=30):

        command_scheme = self.write_dict['command_Wavelength'] # command_scheme ='WA{R_Wave_value}'

        for wa_step in range(N_wa_steps):
            wa = R_wa_min + float(wa_step) / 1000
            print wa
            command = command_scheme.format(R_Wave_value=wa)
            self.write(command)
            time.sleep(0.01)

        print "/(.get_stuff)"
        return None

    #def get_shit():
    #    return "bla"

    def adopt_settings(self, settings={}):
        self.update_settings(settings)
        for key in sorted(self.adopt_dict.keys()):
            self.write_key_value(key)

        if self._local['F_freq_or_wave'] == 'FREQ':
            self.write_key_value('command_Frequency')
        elif self._local['F_freq_or_wave'] == 'WAVE':
            self.write_key_value('command_Wavelength')
        else:
            pass

        if self._local['F_dBm_or_mW'] == 'DBM':
            self.write_key_value('command_Pow_dBm')
        elif self._local['F_dBm_or_mW'] == 'MW':
            self.write_key_value('command_Pow_mW')
        else:
            pass

##########
#    def get_XXX(self):
#        message = self.get_info_value('b XXXXXX')
#        print '(get_XXX) Result: '+message
#        return message

#    def set_sample_number(self, val_arg):
#        settings = {'N_sample_number' : str(val_arg)}
#        self.update_settings(settings)
#        self.write_key_value('command_N_sample_number')

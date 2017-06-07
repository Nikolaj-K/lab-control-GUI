from DriverVISA_Parent import DriverVISA

################################################################################
class DriverThorlabs_PM100D(DriverVISA):

    def __init__(self, instr_name):
        super(DriverThorlabs_PM100D, self).__init__(instr_name)
        
##########
#    def get_stuff(self):
#
#        #self.write('blablabla')            
#
#        print "/(.get_stuff)"
#        return None

##########
#    def get_XXX(self):
#        message = self.get_info_value('b XXXXXX')
#        print '(get_XXX) Result: '+message
#        return message

#    def set_sample_number(self, val_arg):
#        settings = {'N_sample_number' : str(val_arg)}
#        self.update_settings(settings)
#        self.write_key_value('command_N_sample_number')


from DriverVISA_Parent import DriverVISA

BLANK = ' '

################################################################################
class DriverRTE1054(DriverVISA):   # Rohde & Schwarz Source, 100 Amperes

    def __init__(self, instr_name):
        super(DriverRTE1054, self).__init__(instr_name)

        ### Set 'ACQuire:POINts:AUTO' to the default (namely 'RESolution')
        ### We need this because there are varioous ways to set the sampling rate.
        self.write_key_value('command_Acquire_mode')

##########
        ### In case this is re-written as a get_trace method for the VIP, four values must be returned.
    def get_data(self, channel): # Stimulus values (x-axis) and trace

        self.write('EXPort:WAVeform:INCXvalues ON')            ### Return not just Y values, but also X (time)

        data_query_string = 'CHAN{N_channel}:WAV1:DATA?'.format(N_channel=channel) # 'CHAN{N_channel}:WAV1:DATA:VALues?'
        data_string = self.query(data_query_string)
        data        = [float(v) for v in data_string.split(',')]

        print "/(.get_data)"
        return data[0::2], data[1::2]

#    def get_data_old__delete_this(RTE1054, channel=1):
#        SAMPLES=5000
#
#        ### self.write('INIT1:IMM; *OPC?')
#
#        RTE1054.write('STOP;') #*OPC?                                                  ### Stops running aquisition
#        RTE1054.write('EXPort:WAVeform:FASTexport'   + BLANK + 'ON')
#        RTE1054.write('CHANnel'+str(channel)+':WAVeform1:STATe'     + BLANK + '1')                 ### WHICH OF THOSE FOUR CAN BE DEFINED FAR IN ADVANCE
#        RTE1054.write('RUNSingle')   #;*OPC?                                           ### Starts (single) aquisition cycle
#        RTE1054.write('EXPort:WAVeform:DLOGging'     + BLANK + 'OFF')
#        RTE1054.write('EXPort:WAVeform:MULTichannel' + BLANK + 'ON')
#        RTE1054.write('FORMat:DATA'                  + BLANK + 'ASCii')             ### Alternative: 'REAL,32'
#
#        RTE1054.write("ACQuire:SRATe"+str(SAMPLES))
#
#        ## Read out the data to the PC and save it in variables
#        data_str = RTE1054.query("CHAN"+str(channel)+":WAV1:DATA?")
#
#        print
#        print "len(data_str):"
#        print len(data_str)

##########
#    def get_XXX(self):
#        message = self.get_info_value('b XXXXXX')
#        print '(get_XXX) Result: '+message
#        return message

#    def set_sample_number(self, val_arg):
#        settings = {'N_sample_number' : str(val_arg)}
#        self.update_settings(settings)
#        self.write_key_value('command_N_sample_number')

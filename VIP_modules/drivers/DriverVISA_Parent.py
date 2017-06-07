from visa import ResourceManager as visa_ResourceManager
import dictionaries.protocols as protocols
from DriverVIP_Parent import DriverVIP

################################################################################

class DriverVISA(DriverVIP):
    """General Driver class for insturments with static IP that understand VISA.
    (e.g. Rohde & Schwarz)
    It provides an interface to what in PyVisa terminology is called a 'resource'.
    """
    ### In Python 3, all classes are automatically made children of 'object'.
    ### For Python 2, we make DriverVISA explicitly a child of it. These
    ### 'new style' class then inherits some post Python 2.2 functionality.

    def __init__(self, instr_name):
        """For the class instance, make a local copy of the commands in
        protocols, including the (formatted) IP address for 'instr_name'.
        Then use the PyVisa page (visa) to create a ResourceManager instance,
        which is a channel to a lab device.
        """
        super(DriverVISA, self).__init__(instr_name)

        self.query_dict = protocols.commands['visa']['query'][instr_name]
        self.adopt_dict = protocols.commands['visa']['adopt'][instr_name]
        self.write_dict = protocols.commands['visa']['write'][instr_name]

        rm  = visa_ResourceManager()
        address = protocols.commands['visa']['address'][instr_name]
        try:
            self.Resource = rm.open_resource(address)
            message = "(DriverVISA.__init__("+instr_name+")), address:\n"+address
        except:
            message = "!!! (DriverVISA.__init__("+instr_name+"), \nVisaIOError):\n"
            message += "Wasn't able to open resource with address:\n"+address
        print message

        try:
            self.Resource.visalib.clear(self.get_session_index())
            ### The default timeout is 25000ms (25s) ("self.Resource.timeout = 25000").
            ### Here we set it to infinity.
            del self.Resource.timeout
        except AttributeError:
            print "!!! (DriverVISA, AttributeError)"

##########
    def write(self, string):
        r = self.Resource.write(string)
        return r

    def query(self, string='*IDN?'):
        r = self.Resource.query(string)
        return r

    def _query(self):
        u = self.query('*IDN?')
        x = self.query('*IST?')
        y = self.query('*OPT?')                                                 ### Option identification quiery
        z = self.query('*STB?')
        return u, x, y, z

##########
    def write_key_value(self, write_command_key):
        command_scheme = self.write_dict[write_command_key]
        try:
            write_command = command_scheme.format(**self._local)
        except KeyError:
            print "!!! KeyError at (write_key_value)"
        self.write(write_command)

    def adopt_settings(self, settings={}):
        self.update_settings(settings)
        for key in sorted(self.adopt_dict.keys()):
            self.write_key_value(key)

##########
    def reset(self):
        k = 'command_Reset'
        self.write_key_value(k) ### That's the same as # self.write('*RST')
        return True

##########
    def close_session(self):
        self.Resource.close()
        return True

    def get_session_index(self):
        return self.Resource._session

##########

    def get_info_value(self, query_command_key):
        query_command = self.query_dict[query_command_key]
        value         = self.query(query_command)
        return value

    def get_info(self):
        message = ""
        for query_command_key in sorted(self.query_dict.keys()):
            value = self.get_info_value(query_command_key)
            line = query_command_key + " (" + self.query_dict[query_command_key] + ") \n= " + value
            message += line
            message += "\n"
            print line
        message += "d Session ID\n= " + str(self.get_session_index())
        #message += 'System Error?' + " = " + self.query(query_dict['System Error?']) + "\n"
        print "\n/// (get_info)\n"
        return message

# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

################################################################################
class DriverVIP(object):
    """Meta driver that merely provides the local data handle, the
    get_session_index method and a basic plotting device.
    """
    def __init__(self, instr_name):
        """Create a handle for mutable settings data, locally carried by the driver
        instance. It's a layer between UI/API defined settings and the instrument.
        """
        try:                                                                    ### this sould be split into two different try-clauses
            from dictionaries.session import default
            self._local = default[instr_name]
            print "(DriverVIP), local data loaded for " + instr_name
        except (ImportError, KeyError) as exception:
            self._local = {}
            print "! (DriverVIP, __init__) Exception:"
            print exception
            print "Hint: Make sure that there is an entry with the session "+\
            "key '{0}' in session.py and also that this session file path "+\
            "can be accessed from where it's called (The latter might "+\
            "require youto execute VIP_main.py)\n".format(instr_name)

        self.Resource = "INIT Resource from DriverVIP('{0}')".format(instr_name)

    def update_settings(self, settings={}):
        self._local.update(settings)

    def adopt_settings(self, settings={}):
        self.update_settings(settings)
        ### And now, here, using self._local, do something with the
        ### physical instrument.

    def get_session_index(self):
        """Return True, signaling the VIP that the handle for which the
        'get_session_index' is called is refering to a driver.
        """
        return True

    def get_info(self):
        message = "\n- Local driver data after the most recent call of ADOPT SETTINGS:"
        for k, v in self._local.iteritems():
            message += "\n"+k+"\n"+v+"\n"
        return message

    def plot(self, y_axis, x_axis=None, x_label="x_label", y_label="y_label", style='k-'):
        ### Color keys here:
        ### http://stackoverflow.com/questions/22408237/named-colors-in-matplotlib
        """Create a plot figure (for the case when you don't use the VIP)"""
        if x_axis is None:
            x_axis = range(len(y_axis))
        plt.figure()
        plt.gcf().clear()
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.plot(x_axis, y_axis, style)
        plt.show()
        print "(DriverVIP) A figure has been drawn!"
        return None



################################################################################
if __name__ == "__main__":

    ######################################## A play pretend driver for an instrument called NAME
    class _DriverName(DriverVIP):

        def __init__(self, instr_name):
            super(_DriverName, self).__init__(instr_name)

    ######################################## A play pretend version of the VIP
    sk = 'Name 1'

    DRIVER_DICT = {sk : _DriverName
                  }

    class _VIP(object):
        def __init__(self):
            self.instruments = {k : None for k in DRIVER_DICT.keys()}
        def bn_connect(self, instr_name):
            driver = DRIVER_DICT[instr_name]
            self.instruments[instr_name] = driver(instr_name)
        def bn_adopt_settings(self, settings_update):
            VIP.instruments[sk].adopt_settings(settings_update)

    ######################################## Script:
    VIP = _VIP()

    VIP.bn_connect(sk)
    VIP.bn_adopt_settings({})

    #channelA_y, channelB_y, _, _ = VIP.instruments[sk].get_trace()
    #VIP.instruments[sk].plot(channelA_y, x_label="Time [ns]", y_label="Amplitude [V]", plot_index=1)
    #VIP.instruments[sk].plot(channelB_y, x_label="Time [ns]", y_label="Amplitude [V]", plot_index=2)

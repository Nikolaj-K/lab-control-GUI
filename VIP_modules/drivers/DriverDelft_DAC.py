import visa
import pyvisa.constants as pvc
import logging
import time

from DriverVIP_Parent import DriverVIP

################################################################################

BYTES = 2**8
MAX_MVOLTS = 4000
### Multiplicative constants:
MVOLTS_TO_BYTES = (BYTES+1)*(BYTES-1)/float(MAX_MVOLTS)
BYTES_TO_MVOLTS = 1/MVOLTS_TO_BYTES

################################################################################

class DriverDelft(DriverVIP):

    def __init__(self, instr_name):
        super(DriverDelft, self).__init__(instr_name)

        rm = visa.ResourceManager()
        try:
            interface = self._local['F_interface']
            self.Resource = rm.open_resource(interface)
        except:
            logging.warning('(DriverDelft) No visa instrument found.')
            raise Exception()

        try:
            self.Resource.set_visa_attribute(pvc.VI_ATTR_ASRL_BAUD, 115200)
            self.Resource.set_visa_attribute(pvc.VI_ATTR_ASRL_DATA_BITS, 8)
            self.Resource.set_visa_attribute(pvc.VI_ATTR_ASRL_PARITY, pvc.VI_ASRL_PAR_ODD)
            self.Resource.set_visa_attribute(pvc.VI_ATTR_ASRL_STOP_BITS, pvc.VI_ASRL_STOP_ONE)
            self.Resource.set_visa_attribute(pvc.VI_ATTR_ASRL_END_IN, pvc.VI_ASRL_END_NONE)
        except AttributeError:
            pass

##########

    def adopt_settings(self, settings_update):
        self._local.update(settings_update)

        F_channel  = self._local['F_channel']
        k = 'R_volt_channel_'+F_channel
        mvolts = float(self._local[k])

        self.set_voltage(self._local, mvolts, None)

##########

    def set_voltage(self, settings, mvolts, unit):
        channel  = int(settings['F_channel'])
        polarity = settings['F_polarity']
        shift = int(self._local[polarity])
        mvolts = mvolts + shift
        self.__write_bytes(channel, mvolts)

    def get_voltage(self, settings):
        channel  = int(settings['F_channel'])
        polarity = settings['F_polarity']
        shift = int(self._local[polarity])
        mvolts = self.__get_bytes(channel) - shift
        return mvolts

    def set_voltage_to_zero(self, settings):
        channel  = int(settings['F_channel'])
        polarity = settings['F_polarity']

        shift = int(self._local[polarity])
        start = self.__get_bytes(channel)
        print start
        stop  = 0 + shift
        step  = +1 if (start <= stop) else -1

        for mvolt in range(start, stop + step, step):
            self.__write_bytes(channel, mvolt)
            if int(mvolt) % 100 == 0: ### print every 100th voltage value
                print "Going down [mV]: "+str(mvolt-shift)
            time.sleep(0.002)

##########

    def close_session(self):
        self.Resource.close()

    def get_session_index(self):
        return self.Resource.session
        ### I don't know to what extent this makes a difference, but the
        ### other drivers haveinstead: str(self.Resource._session)

##########

    def get_info(self):
        message = ""
        message += "\n- Local driver data after the most recent call of ADOPT SETTINGS:\n"
        for k, v in self._local.iteritems():
            line = k+"\n"+v+"\n\n"
            message += line+"\n"
            print line
        message += "\n- Voltage [mvolt]:\n"
        message += str(self.get_voltage())
        return message

################################################################################

    def _write(self, message):
        session = self.get_session_index()
        self.Resource.visalib.write(session, message)

    def _read(self, slot):
        session = self.get_session_index()
        return self.Resource.visalib.read(session, slot)

    def __write_bytes(self, channel, mvolts):
        self.__clear_all()

        ### mvolts to bytes
        byte  = int(round(MVOLTS_TO_BYTES*mvolts))
        dataH = int(byte/BYTES)
        dataL = byte - dataH*BYTES

        message_tuple = (7, 0, 2, 1, channel, dataH, dataL)
        message_c_int = "%c%c%c%c%c%c%c" % message_tuple
        self._write(message_c_int)

    def __get_bytes(self, channel):
        self.__clear_all()
        print "all clear"

        n_DACs = int(self._local['N_DACs'])
        message_tuple = (4, 0, n_DACs*2 + 2, 2)
        message_c_int = "%c%c%c%c" % message_tuple
        print message_tuple
        print message_c_int
        self._write(message_c_int)

        data1  = [ord(dat) for dat in self._read(2)[0]]
        data2  = [ord(dat) for dat in self._read(data1[0]-2)[0]]
        nums   = data1+data2
        byte   = nums[2*channel]*BYTES + nums[2*channel+1]
        mvolts = int(round(BYTES_TO_MVOLTS*byte))

        print byte
        print mvolts

        return mvolts

    def __clear_all(self):
        session = self.get_session_index()
        navail  = self.Resource.visalib.get_attribute(session, pvc.VI_ATTR_ASRL_AVAIL_NUM)
        self._read(int(navail[0]))

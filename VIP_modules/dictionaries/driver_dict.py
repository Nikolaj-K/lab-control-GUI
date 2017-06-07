"""This file is similar to the script_dict, except there we load the whole
package and eventually try to call a (main) function, whereas here we directly
load a class.
We attempt to load all the file from the 'drivers' folder.
In some cases, one may try to open the VIP where it then tries to load a package
from a computer where this doesn't work, e.g. if some package isn't installed
yet. So In some cases we  have to skip loading particular packages and that's
why we put a try clause around the loading command that throws and exeption if
something doesn't work. And then the class is assigned a dummy value.
"""
import sys

try:
    ################################################################################
    from drivers.DriverZNB20_VNA import DriverZNB20
    from drivers.DriverZVL13_VNA import DriverZVL13
    from drivers.DriverFSW_SA import DriverFSW
    from drivers.DriverRTE1054_Osci import DriverRTE1054
    from drivers.DriverSGS100A_SG import DriverSGS100A
    from drivers.DriverDelft_DAC import DriverDelft
    from drivers.DriverSantec_TSL_550_Laser import DriverSantec_TSL_550
    from drivers.DriverThorlabs_PM100D_PM import DriverThorlabs_PM100D

    try:
        from drivers.DriverATS9870_Dig import DriverATS9870
    except (NotImplementedError, WindowsError) as exception:
        print "! (driver_dict) Exception for DriverATS9870:"
        print str(exception)
        DriverATS9870 = None
    try:
        from drivers.DriverNI_pulse_IO import DriverNI_pulse
    except (NotImplementedError, ImportError) as exception:
        print "! (driver_dict) Exception for DriverNI_pulse:"
        print str(exception)
        DriverNI_pulse = None
    try:
        from drivers.DriverNI_DAQ_Dig import DriverNI_DAQ
    except (NotImplementedError, ImportError) as exception:
        print "! (driver_dict) Exception for DriverNI_DAQ:"
        print str(exception)
        DriverNI_DAQ = None
    try:
        from drivers.DriverH3344_AWG import DriverH3344
    except (NotImplementedError, ImportError, WindowsError) as exception:
        print "! (driver_dict) Exception for DriverH3344_AWG:"
        print str(exception)
        DriverH3344 = None
    try:
        from drivers.DriverWM1210_WM import DriverWM1210
    except (ImportError, AttributeError) as exception:
        print "! (driver_dict) Exception for DriverWM1210:"
        print str(exception)
        DriverWM1210 = None

    ################################################################################
    driver_dict = {'ZNB_1'      : DriverZNB20
                ,'ZNB_2'      : DriverZNB20
                ,'ZVL_1'      : DriverZVL13
                ,'FSW_1'      : DriverFSW
                ,'RTE1054_1'  : DriverRTE1054
                ,'Delft_1'    : DriverDelft
                ,'NI_pulse_1' : DriverNI_pulse
                ,'NI_DAQ_1'   : DriverNI_DAQ
                ,'ATS9870_1'  : DriverATS9870
                ,'H3344_1'    : DriverH3344
                ,'WM1210_1'   : DriverWM1210
                ,'Santec_1'   : DriverSantec_TSL_550
                ,'Thorlabs_1' : DriverThorlabs_PM100D
                }

    ### Also add source drivers
    from dictionaries.session import SGS100As
    driver_dict.update({k : DriverSGS100A for k in SGS100As})

except:
    ### "catch" all exceptions
    scream = "\n" + 20*"!" + "\n"
    print "{0}!!! fatal error in (driver_dict.py):".format(scream)
    print sys.exc_info()[0]
    print "(Most likely you just don't have all the instruments drivers.)"
    print "!!! Went on without loading any drivers{0}".format(scream)

IP_DICT = {'ZNB_1' : '66.66.66.29' # VNA - Rohde & Schwarz Vector Network Analyzer of type ZNB #1
          ,'ZNB_2' : '66.66.66.46' # VNA - Rohde & Schwarz Vector Network Analyzer of type ZNB #2
          ,'ZVL_1' : '66.66.66.47' # VNA - Rohde & Schwarz Vector Network Analyzer of type ZVL #1
          ,'FSW_1' : '66.66.66.30' # FSW - Rohde & Schwarz Signal and Spectrum Analyzer of type FSW #1
          ,'SGS_31' : '66.66.66.31' # SGS - Rohde & Schwarz FR Source #1
          ,'SGS_32' : '66.66.66.32' # SGS - Rohde & Schwarz FR Source #2
          ,'SGS_33' : '66.66.66.33' # SGS - Rohde & Schwarz FR Source #3
          ,'SGS_34' : '66.66.66.34' # SGS - Rohde & Schwarz FR Source #4
          ,'SGS_35' : '66.66.66.35' # SGS - Rohde & Schwarz FR Source #5
          ,'SGS_37' : '66.66.66.37' # SGS - Rohde & Schwarz FR Source #7
          ,'SGS_40' : '66.66.66.40' # SGS - Rohde & Schwarz FR Source #7
          ,'SGS_41' : '66.66.66.41' # SGS - Rohde & Schwarz FR Source #8          
          ,'RTE1054_1' : '66.66.66.42' # SGS - Rohde & Schwarz Oscilloscope #1
          }

################################################################################

"""
For e.g. usingc Visa, to onnect you need a particular kind of address string. 
For example
TCPIP::10.21.64.29::hislip0::INSTR
So for each insturment that has an entry in the 'instr_list' use the IP and  
create an address according to that standard scheme.
"""

########## IP schemes

BUS         = "TCPIP"
BOARD_INDEX = ""          # optional
LAN_DEVICE  = "hislip0"   # optional
INSTR       = "INSTR"     # optional

IP_scheme    = "{0}{1}::{2}::{3}::{4}".format(BUS, BOARD_INDEX, "{0}", LAN_DEVICE, INSTR)

address_dict = {k : IP_scheme.format(IP_DICT[k]) for k in IP_DICT}

########## USB schemes

BUS         = "USB"
BOARD_INDEX = "0"         # I assume this is optional too

USB_scheme     = "{0}{1}::{2}::{3}::{4}::{5}".format(BUS, BOARD_INDEX, "{0}", "{1}", "{2}", "{3}")

address_dict['Santec_1']  = USB_scheme.format('0x2428', '0x0105', '16060011', 'RAW'  )
address_dict['Thorlabs_1'] = USB_scheme.format('0x1313', '0x8078', 'P0013401', 'INSTR')

################################################################################ CALL OF MAIN FUNCTION
if __name__ == "__main__":
    print
    print "IP_scheme ="
    print IP_scheme
    print 
    print "USB_scheme ="
    print USB_scheme
    


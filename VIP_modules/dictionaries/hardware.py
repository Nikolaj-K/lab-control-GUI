### Hardware specifications that can't possibly be modified (unlike the session)

################################################################################

NI_pulse = {'N_pins'    : '8'   ### number of pins per port
           ,'N_devices' : '3'   ### number of devices
           ,'N_ports'   : '3'   ### number of ports
           }
range_NI_pins = [str(pin) for pin in range(int(NI_pulse['N_pins']))]

##########

Delft = {'N_DACs' : '16'   ### int value fixed by hardware
        ,'R_POS'  : '0'    ### [mvolt] value fixed by hardware
        ,'R_NEG'  : '4000' ### [mvolt] value fixed by hardware
        ,'R_BIP'  : '2000' ### [mvolt] value fixed by hardware
        }

##########

H3344 = {'N_channels' : '4'   ### number of channels
        }
range_H3344_channels = [str(ch) for ch in range(int(H3344['N_channels']))]





################################################################################ CALL OF MAIN FUNCTION
if __name__ == "__main__": 

    print range_H3344_channels
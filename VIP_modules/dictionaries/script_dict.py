"""This file is similar to the script_dictionary, except here we directly load a 
class and there we load the whole package and eventually try to call a (main)
function.
We attempt to load all the file from the 'scripts' folder.
In some cases, one may try to open the VIP where it then tries to load a package
from a computer where this doesn't work, e.g. if some package isn't in stalled
yet. So In some cases we  have to skip loading particular packages and that's
why we put a try clause around the loading command that throws and exeption if
something doesn't work. And then the (main) function is assigned a dummy value.
"""

##############################################################################
import scripts_for_gui.scripts_EXAMPLES as scripts_EXAMPLES
import scripts_for_gui.scripts_power_from_freq as scripts_power_from_freq
import scripts_for_gui.scripts_Freq_vs_drive_power as scripts_Freq_vs_drive_power
import scripts_for_gui.scripts_flux_sweep as scripts_flux_sweep
import scripts_for_gui.scripts_RF_set_phase as scripts_RF_set_phase

try:
    import scripts_for_gui.scripts_IQ_callibration as scripts_IQ_callibration
    scripts_IQ_callibration__main = scripts_IQ_callibration.main
except OSError as exception:
    print "!!! (script_dict, import scripts_IQ_callibration) OSError:\n"
    print str(exception)
    scripts_IQ_callibration__main = None

try:
    ### This requires the Alazard libraries
    import scripts_for_gui.scripts_DAC_VNA as scripts_DAC_VNA
    scripts_DAC_VNA__main = scripts_DAC_VNA.main
except WindowsError as exception:
    print "!!! (script_dict, import scripts_DAC_VNA) WindowsError:\n"
    print str(exception)
    scripts_DAC_VNA__main = None

##############################################################################
### This is the combobox (dropdown menu) dictonary for the VIP script block.
####
### Format:
### 'my script key' : scripts_file.my_function
### Each script takes exactly one argument, namely a VIP class instance ('VIP').
###
### Important note:
### Each script here must also be added to the session dictonary.

script_dictionary = {'Printer demo'          : scripts_EXAMPLES.printer_main
                    ,'Freq. query'           : scripts_EXAMPLES.get_frequency_main
        
                    ########## Matilda
                    ,'Power from freq.'      : scripts_power_from_freq.main
        
                    ########## Andreas Butler
                    ,'Freq. vs. drive power' : scripts_Freq_vs_drive_power.main
                    ,"Mixer calib."          : scripts_IQ_callibration__main
                    ,'Flux sweep'            : scripts_flux_sweep.main
                    ,'Mixer-Dig VNA'         : scripts_DAC_VNA__main

                    ########## Shabir
                    ,'Set RF phase'          : scripts_RF_set_phase.set_phase_main
                    }

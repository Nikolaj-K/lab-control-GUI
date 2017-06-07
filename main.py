# -*- coding: utf-8 -*-

### Get the path to the current base directory (the path of this __file__).
import os
DIR_PATH_this    = os.path.dirname(__file__)
DIR_PATH_data    = DIR_PATH_this + os.sep + "Data"
DIR_PATH_modules = DIR_PATH_this + os.sep + "VIP_modules"

### Add 'DIR_PATH_modules' to the import paths so you can load files from.
from sys import path as sys_path
sys_path.insert(0, DIR_PATH_modules)

### Import the modules necessary to create a VIP instance
from VIP_modules.scripts_for_main.QtGui_decorator import QtGui_decorator
from VIP_modules.VIP_Qwidget import VirtualInstrumentPanel

### Import the modules with the scripts you want to run
import VIP_modules.scripts_for_main.initialize_VIP as initialize_VIP
import VIP_modules.scripts_for_main.nikolaj as nikolaj
import VIP_modules.scripts_for_main.matilda as matilda
import VIP_modules.scripts_for_main.matthias as matthias

################################################################################
@QtGui_decorator ### this decorator function takes care of the GUI environment
def main():
    """Create a vip instance and execute the scripts of your choice."""
    vip = VirtualInstrumentPanel()
    initialize_VIP.customize_paths(vip, DIR_PATH_data)
    
    ### If you want to use the GUI, customize and then load open it.
    initialize_VIP.use_GUI_windows(vip)
    vip.ScriptsWindow.show()
    
    ### If you want to run scripts, call them here. (opening of GUI is optional)
    #nikolaj.fitting_test(vip)
    #matilda.H3344_script(vip)
    #matthias.set_osci_test(vip)

################################################################################
if __name__ == "__main__":
    main() ### This is the function being executed when VIP_main.py is executed

# -*- coding: utf-8 -*-
import os

import interface.session_events as se

################################################################################
def use_GUI_windows(vip):
    """Let the windows pop up that contain all the vip widgets.
    """
    message_cwd     = "Current working directory:\n{0}\n".format(os.getcwd())
    message_welcome = "Welcome to the Virtual Instrument Panel!\n"
    vip.GUI_feedback([message_cwd, message_welcome])

    se.bn_open_GUI_feedback(vip)
    se.bn_open_plots_12(vip)

    vip.show()

    print "\n/(use_GUI_windows)\n"

def customize_paths(vip, DIR_PATH_data):
    """Use the vip's .set method to set the path relevant to the user interface.
    """
    ### this sets several line edits to initial sensible values
    FILE_PATH_session  = DIR_PATH_data+os.sep+"session_init.txt"
    FILE_PATH_notes    = "K:\\_Computing\\MeasurementSoftware\\VIP_notes.txt"
    FILE_PATH_waveform = "C:/Users/Public/Documents/Signadyne/Examples/Waveforms/Gaussian.csv"

    ### The format is: vip.set(SESSION_KEY, REPLACEMENT_DICTIONARY)
    ### Note that we could also save those settings to a .txt file and load it.
    vip.set('Results', {'DIR_PATH_results'   : DIR_PATH_data})
    vip.set('Session', {'FILE_PATH_session'  : FILE_PATH_session})
    vip.set('Options', {'FILE_PATH_notes'    : FILE_PATH_notes})
    vip.set('H3344_1', {'FILE_PATH_waveform' : FILE_PATH_waveform})

    for index in vip._sessions_local.keys():
        vip.set('Session', {'F_dict_index' : str(index)})     # why is this not setting the index??/
        se.bn_vip_to_list_session(vip)

    vip.set('Session', {'F_dict_index'       : 'default'})

    ### Unless it already exists, create a results data file directory.
    if not os.path.isdir(DIR_PATH_data):
        os.makedirs(DIR_PATH_data)
    ###Finally, make the Data folder the working directory for our session.
    os.chdir(DIR_PATH_data)

    print "\n/(customize_DIR_and_FILE_paths)\n"

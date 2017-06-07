import os
from time import strftime
import json as json
import copy

from PyQt4.QtGui import QWidget, QFileDialog, QPixmap

import dictionaries.constants as cs

from widgets.NotesWindow_Qwidget import NotesWindow
from widgets.InfoDialog_Qwidget import InfoDialog

import dictionaries.session as session
import dictionaries.driver_dict as driver_dict_file
import dictionaries.script_dict as script_dict

################################################################################
################################################################################ BUTTONS


############################################################ Load & Save

def _load_session_from_file(vip):
    dir_path_cwd      = os.getcwd()

    file_path_session = vip.get('Session', 'FILE_PATH_session')
    file_name_session = os.path.basename(file_path_session)
    dir_path_session  = os.path.dirname(file_path_session)

    if not os.path.isdir(dir_path_session):
        message = "{0} ... does not exist.".format(dir_path_session)
        vip.GUI_feedback(message)
    else:
        loaded_session = None

        ### Go to dir_path_session
        os.chdir(dir_path_session)
        try:
            with open(file_name_session, "r") as in_file:
                loaded_session = json.load(in_file)

            message = "Loaded: {0}".format(file_name_session)
        except IOError:
            message = "!!! {0} ... does not exist.".format(file_name_session)
        vip.GUI_feedback(message)
        ### Go back to dir_path_cwd
        os.chdir(dir_path_cwd)
        return loaded_session

def bn_save_session_to_file(vip):
    dir_path_cwd      = os.getcwd()
    file_path_session = vip.get('Session', 'FILE_PATH_session')
    file_name_session = os.path.basename(file_path_session)
    dir_path_session  = os.path.dirname(file_path_session)

    ### Go to dir_path_session
    if not os.path.isdir(dir_path_session):
        os.makedirs(dir_path_session)
    os.chdir(dir_path_session)

    with open(file_name_session, "w") as out_file:
        json.dump(vip._session, out_file, indent = 10, sort_keys = True)

    ### Go back to main dir
    os.chdir(dir_path_cwd)
def bn_load_session_to_vip(vip): ### load
    s = _load_session_from_file(vip)
    if s is not None:
        vip.adopt_session(s)

def bn_list_session_to_vip(vip): ### load
    k = vip.get('Session', 'F_dict_index')
    s = vip._sessions_local[k]
    vip.adopt_session(s)

def bn_vip_to_list_session(vip): ### save
    k = vip.get('Session', 'F_dict_index')
    vip._sessions_local[k] = copy.deepcopy(vip._session)
    print "- session was copied to list index #{0}".format(k)

def bn_back_to_default_options(vip):
    s = _load_session_from_file(vip)
    if s is not None:
        vip.set('Options', s['Options']) # these are le, dm and cb changes, triggered from this bn action

def bn_save_switch(vip, textfile_formatting = None):
    dir_path_cwd     = os.getcwd()

    dir_path_results = vip.get('Results', 'DIR_PATH_results')
    index            = vip.get('Results', 'N_result_index')
    title_result     = vip.get('Results', 'TITLE_result')+"_"+index
    this_second      = strftime("%y%m%d_%Hh%Mm%Ss")                             # use the function os get_time function here

    ### Go to dir_path_results
    if not os.path.isdir(dir_path_results):
        try:
            os.makedirs(dir_path_results)
            print "(bn_save_switch), Saving data to:"
            print dir_path_results
        except WindowsError as exception:
            print "!!! (bn_save_switch, WindowsError) Maybe you don't have directory access."
            print exception
    os.chdir(dir_path_results)

    ### Save session
    if vip.get('Results','B_save_session') == 'ON':
        file_name_session = title_result + "_sess_" + this_second
        with open(file_name_session+".txt", "w") as out_file:
            json.dump(vip._session, out_file, indent = 10)
        print "(bn_save_switch) Session file created."

    ### Save screenshot
    if vip.get('Results', 'B_save_screenshot') == 'ON':
        file_name_screenshot = title_result+"_snap_"+this_second
        widgets = {'VIP_tabs'  : vip
                  ,'plots_12'  : vip._PlotsWindow_12
                  ,'plots_34'  : vip._PlotsWindow_34
                  ,'__scripts' : vip.ScriptsWindow
                  }
        for name_k, widget_v in widgets.iteritems():
            if widget_v._B_can_make_screenshot:
                ### winId is the Qt method that returns the window widgets reference ID
                window = widget_v.winId()
                pixmap = QPixmap.grabWindow(window)
                B_success = pixmap.save(file_name_screenshot+"_"+name_k+".jpg", "jpg")
                if not B_success:
                    print "!!! (pixmap.save) There was an issue with the screenshot package."
        print "(bn_save_switch) Screenshot files created."

    ### Save result data
    if vip.get('Results', 'B_save_result') == 'ON':
        file_name_result = title_result + "_data_" + this_second
        with open(file_name_result+".txt", "w") as out_file:
            json.dump(vip.result, out_file, separators = (',', ':'), indent = None, sort_keys = True)
        if textfile_formatting is not None:
            textfile_formatting(file_name_result+".txt")
        print "(bn_save_switch) Data file created."
    ### Go back to dir_path_cwd
    os.chdir(dir_path_cwd)

def bn_meas_dir_today(vip):
    this_day = strftime("%y%m%d")
    old_path = vip.get('Results', 'DIR_PATH_results')
    new_path = old_path+os.sep+this_day

    vip.set('Results', {'DIR_PATH_results' : new_path}) # this is a le change, triggered from this bn action

def bn_browse_for(vip, k):
    Dialog = QWidget()
    Dialog.resize(50, 70) # *cs.RESIZE_BROWSE_DIALOG
    Dialog.move(100, 100)

    def _set_file_path(sk, file_extension):
        new_path = str(QFileDialog.getOpenFileName(Dialog, 'Open a file', os.sep, "*."+file_extension))
        if new_path: vip.set(sk, {k : new_path}) # this is a le change, triggered from this bn action
        return new_path

    def _set_dir_path(sk):
        new_path = str(QFileDialog.getExistingDirectory(Dialog, 'Open a folder', os.sep, QFileDialog.ShowDirsOnly))
        if new_path: vip.set(sk, {k : new_path}) # this is a le change, triggered from this bn action
        return new_path

    if k == 'FILE_PATH_session':
        new_path = _set_file_path('Session', "txt")
        if new_path:
            bn_load_session_to_vip(vip)
    elif k == 'DIR_PATH_results':
        _set_dir_path('Results')
    elif k in ['FILE_PATH_waveform_'+str(j) for j in range(4)]:
        _set_file_path('H3344_1', "csv")
    else:
        vip.GUI_feedback("!!! (bn_browse_for) A strange key was passed.")

    Dialog.close()

def bn_open_plots_12(vip):
    vip._PlotsWindow_12._B_can_make_screenshot = True

    vip._PlotsWindow_12.show()
    vip._PlotsWindow_12.raise_()

def bn_open_plots_34(vip):
    vip._PlotsWindow_34._B_can_make_screenshot = True

    vip._PlotsWindow_34.show()
    vip._PlotsWindow_34.raise_()

def bn_open_scripts(vip):
    vip.ScriptsWindow._B_can_make_screenshot = True

    vip.ScriptsWindow.show()
    vip.ScriptsWindow.raise_()

def bn_open_notes_in_editor(vip):
    vip._NotesWindow = NotesWindow(vip)
    vip._NotesWindow.show()
    vip._NotesWindow.raise_()

def bn_open_options(vip):
    vip._OptionsWindow.show()
    vip._OptionsWindow.raise_()


def bn_open_GUI_feedback(vip):
    vip._FeedbackWindow.show()
    vip._FeedbackWindow.raise_()

def ___not_implemented_yet(vip):
    message = "\nWell, this is awkward.\n\nThis feature still needs an implementation..."
    vip.GUI_feedback(message)

    bn_open_GUI_feedback(vip)

    vip.FeedbackWindow.show()
    vip.FeedbackWindow.raise_()

############################################################ Interact with instruments

def bn_connect_to_lab(vip):
    connected_instruments = "Added to connected instruments:\n"
    for instr_name in session.instr_list:
        if vip.get(instr_name, 'B_connect') == 'TRY':
            print "* "+instr_name+": Connect set to "+vip.get(instr_name, 'B_connect')
            try:
                #~~~~~~~~~
                vip.instruments[instr_name].close_session()
                closing_message = "* "+instr_name+": An old resource connection was closed."
            except AttributeError:
                closing_message = "* "+instr_name+": No previous session to be closed."
            print closing_message
            print "* "+instr_name+": Attempt to connect."
            try:
                #~~~~~~~~~
                _driver_class = driver_dict_file.driver_dict[instr_name]
                vip.instruments[instr_name] = _driver_class(instr_name)
                if vip.is_connected(instr_name):
                    message = "was connected!"
                    connected_instruments += instr_name+"\n"
                else:
                    vip.instruments[instr_name] = "INIT <"+instr_name+"> driver"
                    message = "!?? failure at 'is_connected'. "
                    message += "\n!!!! 'vip.instruments[instr_name]' handle  was reset to INIT value."
            except (AttributeError, TypeError) as e:
                message = "! Could not instantiate driver:\n"+str(e)

            vip.GUI_feedback(instr_name+": "+message)

        else:
            print "* "+instr_name+": Connection checkbox set to DONT."
    vip.GUI_feedback(connected_instruments)
    bn_open_GUI_feedback(vip)

def bn_adopt_settings(vip):
    for instr_name in session.instr_list:
        if vip.is_connected(instr_name):
            settings = vip._session[instr_name]
            vip.instruments[instr_name].adopt_settings(settings)

def bn_block_measurement(vip):
    vip.Bpy_break_loop = True

def bn_get_info(vip, instr_name):
    try:
        #~~~~~~~~~
        info_message = vip.instruments[instr_name].get_info()

        message = "~"
        vip.info_window = InfoDialog(info_message)
        vip.info_window.show()
    except AttributeError:
        message = "\n!!! Instrument was probably not connected."

    vip.GUI_feedback("Info request for " +"\n"+instr_name+":\n"+message)

def bn_run_script(vip, index_string):
    bn_adopt_settings(vip)
    k = vip.get('Script', 'script_title_'+index_string)
    #~~~~~~~~~
    vip.result = script_dict.script_dictionary[k](vip)
    bn_save_switch(vip)
    vip.GUI_feedback(['The script', k, 'was completed.'])

def safe_NI_pulse(vip, sk, B_zeros, B_finite):
    settings = vip.get(sk)
    try:
        message = vip.instruments[sk].send_pulse(settings, B_zeros, B_finite)
    except AttributeError:
        message = "(save_NI_pulse), AttributeError"
    vip.GUI_feedback(message)

def load_config_NI_pulse(VIP, sk):
    k = VIP.get(sk, 'F_use_config')
    _config_script_dict = {} ### The dictoionary with the configuration functions was removed.
    _config_script_dict[k](VIP, sk)

def bn_AWG_load_waveform(vip, sk):
    settings = vip._session[sk]
    try:
        vip.instruments[sk].waveform_from_file(settings)
    except AttributeError:
        print "!!! (bn_AWG_load_waveform) "+sk+" possibly not connected!"

################################################################################
################################################################################ CHECKBOXES

def cb_toggled(vip, sk, k):
    on, off = vip.content['cb_vals'][sk][k]

    if vip._qWidgets['cb'][sk][k].isChecked():
       text = on
    else:
       text = off

    vip._session[sk][k] = text

    print "- action for sk = '{0}':".format(sk)
    print "\tsetting = {{'{0}' : '{1}'}}".format(k, text)

    ### clean up sweep checkboxes:
    sk = 'Sweep'
    k1 = 'B_is_max_1'
    k2 = 'B_is_max_2'
    k3 = 'B_is_max_3'

    if (text == on):
        if (k == k1):
            vip.set(sk, {k2 : off})
            vip.set(sk, {k3 : off})
        elif (k == k2):
            vip.set(sk, {k1 : off})
            vip.set(sk, {k3 : off})
        elif (k == k3):
            vip.set(sk, {k1 : off})
            vip.set(sk, {k2 : off})
        else:
            pass

    ### Note that I could also make the cb change pass the state as in
    #vip.content['events'][tb]['cb'] = {'my_key' : lambda state: my_even_function(vip, tb, 'my_key', state)
    ### and then use state here.
    ### E.g.
    #state == QtCore.Qt.Checked
    ### is the same as
    #vip._qWidgets['cb'][tb]['my_key'].isChecked()


################################################################################
################################################################################ LINE EDITS / DROPDOWN MENU

def le_or_dm_change(vip, sk, k, text):
    vip._session[sk][k] = text
    print "- action for sk = '{0}':".format(sk)
    print "\tsetting = {{'{0}' : '{1}'}}".format(k, text)

def le_or_dm_change__N_time_range(vip, sk, k, text):
    le_or_dm_change(vip, sk, k, text)

    try:
        N_sweep_points = int(vip.get(sk, 'N_sweep_points'))
        N_resolution   = int(vip.get(sk, 'N_resolution'))
        N_time_range   = N_sweep_points * N_resolution
        vip._session[sk]['N_time_range'] = str(N_time_range)
        print "- extra action for session key '{0}'".format(sk)
    except ValueError:
        print "! (ValueError, le_or_dm_change__N_time_range) for", sk, k, text

    N_time_range = vip.get(sk, 'N_time_range')
    print "N_time_range = '{0}'".format(str(N_time_range))

def le_or_dm_change__N_sweep_points(vip, tb, k, text):
    le_or_dm_change(vip, tb, k, text)

    try: ### int conversion might fail
        N_samples_factor = int(vip.get(tb, 'N_samples_factor'))
        F_decimation     = int(vip.get(tb, 'F_decimation'))
        N_sweep_points = 2**6 * N_samples_factor
        N_samples_stop = F_decimation * N_sweep_points
        vip._session[tb]['N_sweep_points'] = str(N_sweep_points)
        vip._session[tb]['N_samples_stop'] = str(N_samples_stop)
        vip._qWidgets['lb'][tb]['_N_sweep_points'].setText("= "+str(N_sweep_points))
        print "- extra action for session key '{0}'".format(tb)
        print "N_sweep_points = '{0}'".format(str(N_sweep_points))
        print "- extra action for session key '{0}'".format(tb)
        print "N_samples_stop = '{0}'".format(str(N_samples_stop))
    except ValueError:
        print "! (ValueError, le_or_dm_change__N_sweep_points) for", tb, k, text

def le_or_dm_change__N_delay_size(vip, tb, k, text):
    le_or_dm_change(vip, tb, k, text)

    try: ### int conversion might fail
        delay_size = 2**4 * int(text)
        vip._qWidgets['lb'][tb]['_N_delay_size'].setText("= "+str(delay_size))
    except ValueError:
        print "! (ValueError, le_or_dm_change__N_delay_size) for", tb, k, text

def le_plot_options_update(vip, k, text):
    le_or_dm_change(vip, 'Options', k, text)

    vip.update_figures()

################################################################################ DROPDOWN MENU

def dm_plot_canvas_change(vip, tb, k, text):
    vip._session[tb][k] = text
    for canvas in vip.Canvas[tb].values():
        canvas.update_figure(tb, vip)

################################################################################ LINE EDITS

def le_sweep_quadruple(vip, tb, sweep_quadruple, k, text):
    vip._session[tb][k] = text
    print k + ", set to:", text
    _fun_change_step_size_value_label(vip, tb, sweep_quadruple)

########## ##########

def le_pow_vs_freq_start(vip, tb, text):
        vip._session[tb]['R_freq_start'] = text
        vip.B_auxiliary[tb]['R_freq_start'] = True

        if not vip.B_auxiliary[tb]['R_freq_stop']:
            try:
                tmp_span = float(vip.get(tb, 'R_freq_stop')) - float(text)
                tmp_center = float(text) + tmp_span / 2
                vip._qWidgets['le'][tb]['_R_freq_center'].setText(str(tmp_center))
                vip._qWidgets['le'][tb]['_R_freq_span'].setText(str(tmp_span))
            except ValueError:
                print "ValueError: "+text
        vip.B_auxiliary[tb]['R_freq_start'] = False

def le_pow_vs_freq_stop(vip, tb, text):
        vip._session[tb]['R_freq_stop'] = text
        vip.B_auxiliary[tb]['R_freq_start'] = True

        if not vip.B_auxiliary[tb]['R_freq_stop']:
            try:
                tmp_span   = float(text) - float(vip.get(tb, 'R_freq_start'))
                tmp_center = float(text) - tmp_span / 2
                vip._qWidgets['le'][tb]['_R_freq_center'].setText(str(tmp_center))
                vip._qWidgets['le'][tb]['_R_freq_span'].setText(str(tmp_span))
            except ValueError:
                print "ValueError: "+text
        vip.B_auxiliary[tb]['R_freq_start'] = False

def le_pow_vs_freq_center(vip, tb, text):
        vip.auxiliary_le[tb]['_R_freq_center'] = text
        vip.B_auxiliary[tb]['R_freq_stop'] = True

        if not vip.B_auxiliary[tb]['R_freq_start']:
            try:
                tmp_span = float(vip.auxiliary_le[tb]['_R_freq_span'])
                tmp_start = float(text) - tmp_span / 2
                tmp_stop  = float(text) + tmp_span / 2
                vip._qWidgets['le'][tb]['R_freq_start'].setText(str(tmp_start))
                vip._qWidgets['le'][tb]['R_freq_stop'].setText(str(tmp_stop))
            except ValueError:
                print "ValueError: "+text
        vip.B_auxiliary[tb]['R_freq_stop'] = False

def le_pow_vs_freq_span(vip, tb, text):
        vip.auxiliary_le[tb]['_R_freq_span'] = text
        vip.B_auxiliary[tb]['R_freq_stop'] = True

        if not vip.B_auxiliary[tb]['R_freq_start']:
            try:
                tmp_center = float(vip.auxiliary_le[tb]['_R_freq_center'])
                tmp_start  = tmp_center - float(text) / 2
                tmp_stop   = tmp_center + float(text) / 2
                vip._qWidgets['le'][tb]['R_freq_start'].setText(str(tmp_start))
                vip._qWidgets['le'][tb]['R_freq_stop'].setText(str(tmp_stop))
            except ValueError:
                print "ValueError: "+text
        vip.B_auxiliary[tb]['R_freq_stop'] = False

################################################################################

def _fun_change_step_size_value_label(vip, tb, local_dict):
    [key_star, key_stop, key_swee, key_step] = local_dict

    try:
        star = float(vip._session[tb][key_star])
        stop = float(vip._session[tb][key_stop])
        diff = abs(stop - star)
        poin = abs(int(vip._session[tb][key_swee])) - 1

        try:
            text = str(diff / poin)
        except ZeroDivisionError:
            text = "'ZeroDivisionError' at sweep points"
        vip._qWidgets['lb'][tb][key_step].setText(text)
    except ValueError:
        vip._qWidgets['lb'][tb][key_step].setText("Some values are invalid.")

from PySide import QtGui, QtCore

import dictionaries.session as session
import dictionaries.constants as cs
import interface.session_events as se
import dictionaries.menus as menus

import interface.session_widgets as sw

################################################################################

def _build_Canvas_columns(vip, tb):

    from widgets.ResultCanvas_QTAgg import Canvas2dData, Canvas3dData

    vip.Canvas[tb]['2d_data'] = Canvas2dData(tb, vip)
    vip.Canvas[tb]['3d_data'] = Canvas3dData(tb, vip)

########## ##########
    vip.content['captions'][tb]['lb'] = {'_lb_data_set'      : "Data set"
                                        ,'_lb_plot_function' : "with 3d data plotted as"
                                        }
    vip.content['captions'][tb]['bn'] = {}
    vip.content['captions'][tb]['cb'] = {'B_keep_updated'     : "Update "+tb}

    vip.content['events'][tb]['le'] = {}
    vip.content['events'][tb]['cb'] = {'B_keep_updated'  : lambda state: se.cb_toggled(vip, tb, 'B_keep_updated')}
    vip.content['events'][tb]['dm'] = {'F_data_set'      : lambda text: se.dm_plot_canvas_change(vip, tb, 'F_data_set'     , text)
                                      ,'F_plot_function' : lambda text: se.dm_plot_canvas_change(vip, tb, 'F_plot_function', text)
                                      }
    vip.content['events'][tb]['bn'] = {}

    vip.content['cb_vals'][tb] = {'B_keep_updated'     : ('ON', 'OFF')}

    vip.content['dm_vals'][tb] = {'F_data_set'      : menus.DATA_SET_KEYS
                                 ,'F_plot_function' : menus.PLOT_FUNCTION_KEYS
                                 }

    sw.__fill_widgets(vip, tb, fontsize=cs.FONTSIZE-2)

    #### ----------

    colours = {'Plot_column_1' : {'2d_data' : cs.COLOR_TRACE_1, '3d_data' : cs.COLOR_DENSITY_1}
              ,'Plot_column_2' : {'2d_data' : cs.COLOR_TRACE_2, '3d_data' : cs.COLOR_DENSITY_2}
              ,'Plot_column_3' : {'2d_data' : cs.COLOR_TRACE_3, '3d_data' : cs.COLOR_DENSITY_3}
              ,'Plot_column_4' : {'2d_data' : cs.COLOR_TRACE_4, '3d_data' : cs.COLOR_DENSITY_4}
              }
    for plot_type, color in colours[tb].iteritems():
        vip.Canvas[tb][plot_type]._Figure.set_facecolor(color)

########## ########## hBoxs
    hBox = QtGui.QHBoxLayout()

    hBox.addWidget(vip._qWidgets['cb'][tb]['B_keep_updated'])
    hBox.addLayout(vip._blanks.next())
    hBox.addStretch(.1)
    hBox.addWidget(vip._qWidgets['lb'][tb]['_lb_data_set'])
    hBox.addWidget(vip._qWidgets['dm'][tb]['F_data_set'])
    hBox.addWidget(vip._qWidgets['lb'][tb]['_lb_plot_function'])
    hBox.addWidget(vip._qWidgets['dm'][tb]['F_plot_function'])

########## ########## vBo
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    vBox.addWidget(vip.Canvas[tb]['2d_data'])
    vBox.addWidget(vip.Canvas[tb]['3d_data'])
    vBox.addLayout(vip._blanks.next())
    vBox.addLayout(hBox)

def _build_Session(vip):
    tb = 'Session'

    vip.content['captions'][tb]['lb'] = {'_lb_session_line' : "Session"
                                        ,'F_dict_index'     : "Session list index:"
                                        }
    vip.content['captions'][tb]['bn'] = {'_bn_session_save'      : "Save to file"
                                        ,'_bn_session_load'      : "Load from file"
                                        ,'_bn_session_browse'    : "Browse files"
                                        ,'_bn_session_save_local' : "Save to local"
                                        ,'_bn_session_load_local' : "Load from local"
                                        }
    vip.content['captions'][tb]['cb'] = {}

    vip.content['events'][tb]['le'] = {'FILE_PATH_session'    : lambda text: se.le_or_dm_change(vip, tb, 'FILE_PATH_session', text)
                                      }
    vip.content['events'][tb]['dm']   = {'F_dict_index' : lambda text: se.le_or_dm_change(vip, tb, 'F_dict_index', text)
                                        }
    vip.content['events'][tb]['bn'] = {'_bn_session_save'      : lambda: se.bn_save_session_to_file(vip)
                                      ,'_bn_session_load'      : lambda: se.bn_load_session_to_vip(vip)
                                      ,'_bn_session_save_local' : lambda: se.bn_vip_to_list_session(vip)
                                      ,'_bn_session_load_local' : lambda: se.bn_list_session_to_vip(vip)
                                      ,'_bn_session_browse'    : lambda: se.bn_browse_for(vip, 'FILE_PATH_session')
                                      }
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {'F_dict_index' : sorted(vip._sessions_local.keys())
                                 }

    sw.__fill_widgets(vip, tb)

    ### ----------
    vip._qWidgets['lb'][tb]['_lb_session_line'].setAlignment(QtCore.Qt.AlignCenter)

########## ########## hBoxs
    hBox_ks = ['_browse', '_path', '_file_bns', '_list_dm', '_list_bns']
    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    hBoxs['_browse'].addWidget(vip._qWidgets['lb'][tb]['_lb_session_line'])
    hBoxs['_browse'].addWidget(vip._qWidgets['bn'][tb]['_bn_session_browse'])

    hBoxs['_file_bns'].addWidget(vip._qWidgets['bn'][tb]['_bn_session_save'])
    hBoxs['_file_bns'].addWidget(vip._qWidgets['bn'][tb]['_bn_session_load'])

    hBoxs['_path'].addWidget(vip._qWidgets['le'][tb]['FILE_PATH_session'])

    hBoxs['_list_dm'].addWidget(vip._qWidgets['lb'][tb]['F_dict_index'])
    hBoxs['_list_dm'].addWidget(vip._qWidgets['dm'][tb]['F_dict_index'])
    hBoxs['_list_dm'].addStretch(.1)

    hBoxs['_list_bns'].addWidget(vip._qWidgets['bn'][tb]['_bn_session_save_local'])
    hBoxs['_list_bns'].addWidget(vip._qWidgets['bn'][tb]['_bn_session_load_local'])

########## ########## vBox
    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    for k in hBox_ks:
        vBox.addLayout(hBoxs[k])

################################################################################

def _build_Results(vip):
    tb = 'Results'

    vip.content['captions'][tb]['lb'] = {'_lb_session_line'   : "Results"
                                        ,'_lb_name_index'   : "File name:"
                                        ,'_lb_result_blank' : "_"
                                        ,'_lb_cb_selection' : "Save:"
                                        }
    vip.content['captions'][tb]['bn'] = {'_bn_result_dir_browse' : "Browse"
                                        ,'_bn_save_switch'       : "Save"
                                        ,'_bn_meas_dir_today'    : "Today"
                                        }
    vip.content['captions'][tb]['cb'] = {'B_save_result'     : "Data to file"
                                        ,'B_save_session'    : "Session"
                                        ,'B_save_screenshot' : "Screenshot"
                                        }

    vip.content['events'][tb]['le'] = {'DIR_PATH_results'      : lambda text: se.le_or_dm_change(vip, tb,'DIR_PATH_results', text)
                                      ,'TITLE_result'          : lambda text: se.le_or_dm_change(vip, tb,'TITLE_result' , text)
                                      ,'N_result_index'        : lambda text: se.le_or_dm_change(vip, tb,'N_result_index', text)
                                      }
    vip.content['events'][tb]['dm'] = {}
    import interface.auxiliary_functions as auxi
    vip.content['events'][tb]['bn'] = {'_bn_result_dir_browse' : lambda: se.bn_browse_for(vip, 'DIR_PATH_results')
                                      ,'_bn_save_switch'       : lambda: se.bn_save_switch(vip, auxi.textfile_formatting)
                                      ,'_bn_meas_dir_today'    : lambda: se.bn_meas_dir_today(vip)
                                      }
    vip.content['events'][tb]['cb'] = {'B_save_result'     : lambda state: se.cb_toggled(vip, tb,'B_save_result')
                                      ,'B_save_session'    : lambda state: se.cb_toggled(vip, tb,'B_save_session')
                                      ,'B_save_screenshot' : lambda state: se.cb_toggled(vip, tb,'B_save_screenshot')
                                      }

    vip.content['cb_vals'][tb] = {'B_save_result'     : ('ON', 'OFF')
                                 ,'B_save_session'    : ('ON', 'OFF')
                                 ,'B_save_screenshot' : ('ON', 'OFF')
                                 }

    sw.__fill_widgets(vip, tb)

    ### ----------
    vip._qWidgets['lb'][tb]['_lb_session_line'].setAlignment(QtCore.Qt.AlignCenter)
    vip._qWidgets['le'][tb]['N_result_index'].setFixedWidth(50)

########## ########## hBoxs

    hBox_ks = ['_cbs', '_browse', '_save', '_dir', '_file_name']
    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    hBoxs['_cbs'].addWidget(vip._qWidgets['lb'][tb]['_lb_cb_selection'])
    hBoxs['_cbs'].addLayout(vip._blanks.next())
    hBoxs['_cbs'].addWidget(vip._qWidgets['cb'][tb]['B_save_result'])
    hBoxs['_cbs'].addLayout(vip._blanks.next())
    hBoxs['_cbs'].addWidget(vip._qWidgets['cb'][tb]['B_save_session'])
    hBoxs['_cbs'].addLayout(vip._blanks.next())
    hBoxs['_cbs'].addWidget(vip._qWidgets['cb'][tb]['B_save_screenshot'])

    hBoxs['_browse'].addWidget(vip._qWidgets['lb'][tb]['_lb_session_line'])
    hBoxs['_browse'].addWidget(vip._qWidgets['bn'][tb]['_bn_result_dir_browse'])

    hBoxs['_save'].addWidget(vip._qWidgets['bn'][tb]['_bn_save_switch'])
    hBoxs['_save'].addWidget(vip._qWidgets['bn'][tb]['_bn_meas_dir_today'])

    hBoxs['_dir'].addWidget(vip._qWidgets['le'][tb]['DIR_PATH_results'])

    hBoxs['_file_name'].addWidget(vip._qWidgets['lb'][tb]['_lb_name_index'])
    hBoxs['_file_name'].addStretch(.1)
    hBoxs['_file_name'].addWidget(vip._qWidgets['le'][tb]['TITLE_result'])
    hBoxs['_file_name'].addWidget(vip._qWidgets['lb'][tb]['_lb_result_blank'])
    hBoxs['_file_name'].addWidget(vip._qWidgets['le'][tb]['N_result_index'])

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    for k in hBox_ks:
        vBox.addLayout(hBoxs[k])

################################################################################

def _build_OptionsWindow(vip):
    tb = 'Options'

    vip.content['captions'][tb]['lb'] = {"_lb_plot_section"        : "Axes relative to figure:"
                                        ,"R_x_plot_position"       : "x-position:"
                                        ,"R_y_plot_position"       : "y-position:"
                                        ,"R_x_plot_size"           : "x-size:"
                                        ,"R_y_plot_size"           : "y-size:"
                                        ,"R_x_plot_label_rotation" : "x-label rotation:"
                                        ,"R_axes_font_size"        : "Axes font size:"
                                        ,"_lb_FILE_PATH_notes"     : "Notes file path:"
                                        }
    vip.content['captions'][tb]['bn'] = {'_bn_default'      : " Reset from init file "
                                        }
    vip.content['captions'][tb]['cb'] = {}

    vip.content['events'][tb]['le'] =   {"R_x_plot_position"       : lambda text: se.le_plot_options_update(vip, "R_x_plot_position"    , text)
                                        ,"R_y_plot_position"       : lambda text: se.le_plot_options_update(vip, "R_y_plot_position"    , text)
                                        ,"R_x_plot_size"           : lambda text: se.le_plot_options_update(vip, "R_x_plot_size"    , text)
                                        ,"R_y_plot_size"           : lambda text: se.le_plot_options_update(vip, "R_y_plot_size"    , text)
                                        ,"R_x_plot_label_rotation" : lambda text: se.le_plot_options_update(vip, "R_x_plot_label_rotation"    , text)
                                        ,"R_axes_font_size"        : lambda text: se.le_plot_options_update(vip, "R_axes_font_size"    , text)
                                        ,"FILE_PATH_notes"         : lambda text: se.le_or_dm_change(vip, tb, "FILE_PATH_notes"    , text)
                                        }
    vip.content['events'][tb]['dm'] = {}
    vip.content['events'][tb]['bn'] = {'_bn_default'      : lambda: se.bn_back_to_default_options(vip)}
    vip.content['events'][tb]['cb'] = {}

    vip.content['cb_vals'][tb] = {}
    vip.content['dm_vals'][tb] = {}

    sw.__fill_widgets(vip, tb)

########## ########## hBoxs

    le_ks = ["R_x_plot_label_rotation"
            ,"R_axes_font_size"
            ,"R_x_plot_position"
            ,"R_y_plot_position"
            ,"R_x_plot_size"
            ,"R_y_plot_size"
            ]
    hBox_ks = ["_lb_plot_section"]+le_ks+['_bn_default']+['_lb_FILE_PATH_notes', 'FILE_PATH_notes']

    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    hBoxs['_lb_plot_section'].addWidget(vip._qWidgets['lb'][tb]['_lb_plot_section'])

    for k in le_ks:
        hBoxs[k].addWidget(vip._qWidgets['lb'][tb][k])
        hBoxs[k].addStretch(.1)
        hBoxs[k].addWidget(vip._qWidgets['le'][tb][k])

    hBoxs['_bn_default'].addStretch(.1)
    hBoxs['_bn_default'].addWidget(vip._qWidgets['bn'][tb]['_bn_default'])

    hBoxs["_lb_FILE_PATH_notes"].addWidget(vip._qWidgets['lb'][tb]["_lb_FILE_PATH_notes"])
    hBoxs['_lb_FILE_PATH_notes'].addStretch(.1)

    hBoxs["FILE_PATH_notes"].addWidget(vip._qWidgets['le'][tb]["FILE_PATH_notes"])

########## ########## vBox

    vBox = QtGui.QVBoxLayout(vip._qWidgets['qw'][tb])

    for k in hBox_ks:
        vBox.addLayout(hBoxs[k])
        if (k == '_lb_plot_section') or (k == "R_axes_font_size"):
            vBox.addLayout(vip._blanks.next())
        elif (k == "_bn_default"):
            vBox.addLayout(vip._blanks.next())
            vBox.addLayout(vip._blanks.next())
    vBox.addLayout(vip._blanks.next())

def _build_Instrument_buttons(vip):
    qw_ref = '_Instruments'

    tab_ws = ['le', 'dm', 'cb', 'bn', 'lb']
    for k in tab_ws:
        vip._qWidgets[k][qw_ref] = {}
    for k in ['captions', 'events']:
        vip.content[k][qw_ref] = {}

########## ########## content

    vip.content['captions'][qw_ref]['lb'] = {'_lb_instr'    : "Instruments"}
    vip.content['captions'][qw_ref]['bn'] = {'_bn_feedback' : "Feedback"
                                            ,'_bn_connect'  : "Connect"
                                            ,'_bn_adopt'    : "Adopt settings"
                                            }
    vip.content['captions'][qw_ref]['cb'] = {}
    vip.content['events'][qw_ref]['le'] = {}
    vip.content['events'][qw_ref]['cb'] = {}
    vip.content['events'][qw_ref]['dm'] = {}
    vip.content['events'][qw_ref]['bn'] = {'_bn_feedback' : lambda: se.bn_open_GUI_feedback(vip)
                                      ,'_bn_connect'  : lambda: se.bn_connect_to_lab(vip)
                                      ,'_bn_adopt'    : lambda: se.bn_adopt_settings(vip)
                                      }

    sw.__fill_widgets(vip, qw_ref)

    #### ----------
    vip._qWidgets['bn'][qw_ref]['_bn_connect'].setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+4))
    vip._qWidgets['bn'][qw_ref]['_bn_connect'].adjustSize()
    vip._qWidgets['lb'][qw_ref]['_lb_instr'].setAlignment(QtCore.Qt.AlignCenter)

########## ########## hBoxs

    hBox_ks = ['__instr', '__connect']
    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    hBoxs['__instr'].addWidget(vip._qWidgets['lb'][qw_ref]['_lb_instr'])
    hBoxs['__instr'].addWidget(vip._qWidgets['bn'][qw_ref]['_bn_feedback'])
    hBoxs['__connect'].addWidget(vip._qWidgets['bn'][qw_ref]['_bn_connect'])
    hBoxs['__connect'].addWidget(vip._qWidgets['bn'][qw_ref]['_bn_adopt'])

########## ########## vBox

    vip._instrument_qw_box = QtGui.QWidget()

    vBox = QtGui.QVBoxLayout(vip._instrument_qw_box)

    for k in hBox_ks:
        vBox.addLayout(hBoxs[k])


def _build_Window_buttons(vip):
    qw_ref = '_Popup_Windows'

    tab_ws = ['le', 'dm', 'cb', 'bn', 'lb']
    for k in tab_ws:
        vip._qWidgets[k][qw_ref] = {}
    for k in ['captions', 'events']:
        vip.content[k][qw_ref] = {}

########## ########## content

    vip.content['captions'][qw_ref]['lb'] = {'_lb_popup'    : " Popup windows "}
    vip.content['captions'][qw_ref]['bn'] = {'_bn_plots_12' : "Plot columns 1, 2"
                                            ,'_bn_plots_34' : "Plot columns 3, 4"
                                            ,'_bn_notes'    : "Notes"
                                            ,'_bn_options'  : "Options"         # "Check connection"
                                            ,'_bn_scripts'  : "Scripts"         # "Check connection"
                                            }
    vip.content['captions'][qw_ref]['cb'] = {}
    vip.content['events'][qw_ref]['le'] = {}
    vip.content['events'][qw_ref]['cb'] = {}
    vip.content['events'][qw_ref]['dm'] = {}
    vip.content['events'][qw_ref]['bn'] = {'_bn_plots_12' : lambda: se.bn_open_plots_12(vip)
                                          ,'_bn_plots_34' : lambda: se.bn_open_plots_34(vip)
                                          ,'_bn_scripts'  : lambda: se.bn_open_scripts(vip)
                                          ,'_bn_options'  : lambda: se.bn_open_options(vip)
                                          ,'_bn_notes'    : lambda: se.bn_open_notes_in_editor(vip)
                                          }

    sw.__fill_widgets(vip, qw_ref)

    vip._qWidgets['lb'][qw_ref]['_lb_popup'].setAlignment(QtCore.Qt.AlignCenter)

########## ########## hBoxs

    hBox_ks = ['_row_'+str(i) for i in [1,2,3]]
    hBoxs = {k : QtGui.QHBoxLayout() for k in hBox_ks}

    hBoxs['_row_1'].addWidget(vip._qWidgets['lb'][qw_ref]['_lb_popup'])
    hBoxs['_row_1'].addWidget(vip._qWidgets['bn'][qw_ref]['_bn_scripts'])
    hBoxs['_row_2'].addWidget(vip._qWidgets['bn'][qw_ref]['_bn_notes'])
    hBoxs['_row_2'].addWidget(vip._qWidgets['bn'][qw_ref]['_bn_options'])
    hBoxs['_row_3'].addWidget(vip._qWidgets['bn'][qw_ref]['_bn_plots_12'])
    hBoxs['_row_3'].addWidget(vip._qWidgets['bn'][qw_ref]['_bn_plots_34'])

########## ########## vBox

    vip._popup_window_qw_box = QtGui.QWidget()

    vBox = QtGui.QVBoxLayout(vip._popup_window_qw_box)

    for k in hBox_ks:
        vBox.addLayout(hBoxs[k])

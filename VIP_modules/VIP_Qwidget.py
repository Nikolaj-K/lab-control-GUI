from time import time as time_now
from PyQt4  import QtCore
from PySide import QtGui
import dictionaries.session as session
import dictionaries.constants as cs
import dictionaries.menus as menus
import interface.auxiliary_functions as auxi

HLINE1 = 5 * "|"
HLINE2 = "\n" + 9 * HLINE1 + "\n"

################################################################################

class VirtualInstrumentPanel(QtGui.QWidget):
    """
    When a VIP is instantiated, e.g. from the VIP_main.py, this class is called
    all it requires all other VIP modules. This file consists of:
    - Initialization of data and building of the GUI
    - The definition of the VIP Application Programming Interface (API)
    """
    def __init__(self):
        """
        Call 4 different subroutines that do the following:
        - Initialize several variables and dictionaries
        - Build all the GUI tabs with their layouts specifications
        - Build and specify the layout of the main VIP window itself
        - Initialize all the GUI class instances, such as e.g. the plot window
        Finally, create and set the layout of the VIP main window.
        """
        ### Print a bunch of "|"'s so that we see the VIP initialization in the
        ### editor/terminal.
        print HLINE2+HLINE1

        ### 'super(CLASSNAME, self)' returns the parent class. The VIP class is
        ### a child of QtGui.QWidget and we ought to call its __init__ method.
        super(VirtualInstrumentPanel, self).__init__()

        self.__initialize_session_handles()
        self.__initialize_content_handles()
        from interface.session_widgets import _build_all
        _build_all(self)
        self.__initialize_GUI_windows()

        ### Create and set the horizontal Box (containing the 3 columns of the main window)
        hBox = self._make_main_hBox()
        self.setLayout(hBox)

        ### Set the style as specified in the constants.py file
        self.__adopt_style()

        print "\n\nPlease ignore all the possible layout and stylesheet " + \
        "complainsts from the Python Qt package.\n\n"

    def __initialize_session_handles(self):
        """Initialize several variables and dictionaries"""
        ########## measurement
        ### This '_TIC' time value is merely used to compute the runtime.
        self._TIC = time_now()

        ### Many QWidget windows are given the following attribute to make it
        ### possible to exclude them form the screenshot routine.
        self._B_can_make_screenshot = True
        ### The follwing boolean enables breaking from the measurement loop:
        ### The event associated with the STOP button in the GUI sets it to 'True'.
        self.Bpy_break_loop = False
        ### If the follwing boolean is set to 'False', the first sweep will never be repeated.
        ### (See measurement file)
        self.Bpy_redo_sweep = True
        ### If the follwing boolean is set to 'True', the VIP can't be closed mannually.
        self.B_cannot_be_closed = False
        ### The result handle is used to store results before they are written
        ### to a text file.
        ### The following are a dictionary of booleans that can be associated
        ### with particular session keys.
        self.B_auxiliary = {'Freq. trace' : {'R_freq_start' : False
                                            ,'R_freq_stop'  : False
                                            }
                           ,'Time trace'  : {'R_freq_start' : False
                                            ,'R_freq_stop'  : False
                                            }
                           }
        self.result = "INIT"
        ### This is the internal handle for storing all of the VIP-GUI's current settings.
        import copy
        self._session = copy.deepcopy(session.default)
        ###
        self._sessions_local = {str(k) : copy.deepcopy(session.default) for k in range(cs.SESSION_DICT_INDICES)}
        for k in ['default', 'test_1', 'test_2']:
            self._sessions_local[k] = copy.deepcopy(session.default)
        ### This is the handle for all the insturment driver class instances.
        ### Given the connect checkboxes of the respective instruments are checked,
        ### the instruments drivers are looked up in the driver dict and assigned
        ### when the CONNECT button is pressed.
        self.instruments = {instr_name : "INIT <"+instr_name+"> driver" for instr_name in session.instr_list}
        ### The VIP has 8 plots, and they are rendered in a plot canvas class instance
        ### which is assigned to this handle in the 'build_all' call
        self.Canvas = {sk : {} for sk in sorted(session.Plot.keys())}
        ### The VIP sweep_tracker attribute is created here, which, e.g. in
        ### scripts can be used to keep track in which point of the measurment
        ### for-loop you are.
        self.reset_sweep_tracker()

        ### Create a handle with 1000 or so HBoxes with an empty text label
        def _text_box_generator(n, text):
            for _ in range(n):
                HBox = QtGui.QHBoxLayout()
                HBox.addWidget(QtGui.QLabel(text))
                yield HBox
        self._blanks = _text_box_generator(1000, "      ")

        import dictionaries.plot_data as plot_data
        ### This handle contains plot data and the default is taken from the
        ### plot_data folder.
        self.plot_data = plot_data.default_data

    def __initialize_content_handles(self):
        """"Initialize dictionaries that are filled with data when 'build_all' is called.
        Here are some shorts for Qwidgets class instances that are more or
        less standard. I use them as keys for dictionaries of widgets.

        * QW_KEYS, QW_KEYS_plus, Legend:
        lb ... label (Static text on the GUI surface that can not be edited by the user.)
        cb ... checkbox (A GUI checkbox, an object that can be in one of two states.)
        dm ... dropdown menu (An object that can be in one of finitely many states.)
        bn ... button (A GUI button that can be clicked)
        le ... line edit (A GUI text field that can be edited)
        tb ... tab QWidget
        qw ... QWidget parent class. (The above are children of that one.)

        My convention for setting keys that are edited by such widgets is
        that I start them with a capital letter that hint at the range of
        values (it's like a tpye). For example:
        'R_freq_start', 'N_sweep_points', 'F_unit_freq'
        We have
        S, B, F, N and R
        For singleton, boolean, finite set, natural number and real number.

        * CONTENT_KEYS, Legend:
        events ... functions that are called when some widget is triggered
        (e.g. when a button is pressed or some line edit field is changed)
        captions ... captions that are required for some widgets
        (e.g. the text that's written on a button or next to a checkbox)
        cb_vals ... the two values associated with a checked or un-checked
        checkbox (e.g. ON and OFF, EXT and INT, etc.)
        dm_vals ... List of values of a dropdown menu
        (e.g. FREQUENCY_UNITS = ['Hz', 'kHz', 'MHz', 'GHz'], as defined in
        the constants.py file)
        """

        QW_KEYS      = ['le', 'cb', 'dm', 'bn', 'lb']
        QW_KEYS_plus = ['tb', 'qw']
        CONTENT_KEYS = ['events', 'captions', 'cb_vals', 'dm_vals']
        TAB_KEYS     = session.default.keys()

        ### These dictionaries are filled with data later
        self.content      = {k : {sk : {} for sk in TAB_KEYS} for k in CONTENT_KEYS}
        self.auxiliary_le = {sk : {} for sk in TAB_KEYS}
        self._qWidgets    = {k : {} for k in QW_KEYS+QW_KEYS_plus}

        for sk in TAB_KEYS:
            for k in QW_KEYS:
                self._qWidgets[k][sk] = {}
                self._qWidgets['qw'][sk] = QtGui.QWidget()
                self._qWidgets['tb'][sk] = QtGui.QTabWidget()

        ### Create all the tab widgets from the session structure and group them
        ### accordingly. Here 'sup_cla' denotes the super classes, which is actually
        ### not part of the default dictionary, but rather the more detauled
        ### 'Tree', see the session.py file in the dictionaries folder.
        for sup_cla in session.Tree.keys():
            ### The '_Experiment' vbox widgets are not grouped in as a tab somwhere
            if sup_cla == '_Experiment':
                pass
            else:
                self._qWidgets['tb'][sup_cla] = QtGui.QTabWidget()
                for cla in session.Tree[sup_cla].keys():
                    self._qWidgets['tb'][cla] = QtGui.QTabWidget()
                    for sk in session.Tree[sup_cla][cla].keys():
                        self._qWidgets['tb'][cla].addTab(self._qWidgets['qw'][sk], sk)
                    ### Create the measurement insturment class widget here:
                    if sup_cla in session.instr_fine_grained.keys():
                        self._qWidgets['tb'][sup_cla].addTab(self._qWidgets['tb'][cla], cla)

    ################################################################################

    def __initialize_GUI_windows(self):
        """Build the 4 kinds of QWidget windows loaded from the 'widgets' folder.
        When the VIP is open, they are always there an cann be opened for the
        GUI with their respective buttons on the VIP main window.
        Assgin a reference keyword to all plot columns.
        """
        self._ProgressBar = QtGui.QProgressBar(self)

        from widgets.FeedbackWindow_Qwidget import FeedbackWindow
        from widgets.ScriptsWindow_Qwidget import ScriptsWindow
        from widgets.OptionsWindow_Qwidget import OptionsWindow
        from widgets.InvisibleWindow_Qwidget import InvisibleWindow
        from widgets.PlotsWindow_Qwidget import PlotsWindow
        self._FeedbackWindow  = FeedbackWindow(self)
        self.ScriptsWindow   = ScriptsWindow(self)
        self._OptionsWindow   = OptionsWindow(self)
        self._InvisibleWindow = InvisibleWindow(self)
        self._PlotsWindow_12  = PlotsWindow(self, ['Plot_column_1', 'Plot_column_2'])
        self._PlotsWindow_34  = PlotsWindow(self, ['Plot_column_3', 'Plot_column_4'])
        ### The self._NotesWindow widget is actually always freshly instantiated
        ### when the "Notes" button is clicked.

    def _make_main_hBox(self):
        """Build the layout of the main VIP widget window.
        A QHBoxLayout instance is a GUI surface to which one can other
        widgets, horizonally, one after the other.
        """
        ########## hBox_progress_bar
        hBox_progress_bar = QtGui.QHBoxLayout()
        ### Pop a blank line widget and add it to the hBox
        hBox_progress_bar.addLayout(self._blanks.next())
        ### Add the VIP's QProgressBar to the hBox
        ### It's going to be used to visualize progress in the measurement loop
        ### in the 'measurement' file, in the 'interface' folder.
        hBox_progress_bar.addWidget(self._ProgressBar)
        hBox_progress_bar.addLayout(self._blanks.next())

        ########## hBox_trace_lb
        text = "From trace:"
        trace_lb = QtGui.QLabel(text)
        trace_lb.setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+1))
        trace_lb.adjustSize() ### This line may be redundant.

        ### We add a second label in small font that has explanatory function.
        text = "(Sweep 1 done by measurement instrument itself)"
        trace_lb_info = QtGui.QLabel(text)
        trace_lb_info.setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE-4))
        trace_lb_info.adjustSize() ### This line may be redundant.

        hBox_trace_lb = QtGui.QHBoxLayout()
        hBox_trace_lb.addWidget(trace_lb)
        hBox_trace_lb.addWidget(trace_lb_info)
        ### addStretch pushes the first to widgets in the box to the very top
        ### and makes it so that the box rescales
        hBox_trace_lb.addStretch(1)

        ########## hBox_point_label
        text = "(Otherwise only script)"
        point_label_info = QtGui.QLabel(text)
        point_label_info.setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE-4))
        point_label_info.adjustSize() ### This line may be redundant.

        hBox_point_label = QtGui.QHBoxLayout()
        ### The boolean 'B_during_sweep' value determines if a measurement
        ### should be done during the sweep. Deactivating the measurement allows
        ### for merely sweeping over scripts.
        hBox_point_label.addWidget(self._qWidgets['cb']['Meas_main']['B_during_sweep_1'])
        hBox_point_label.addWidget(point_label_info)
        hBox_point_label.addStretch(1)

        ########## vBoxs
        ### Create and fill the three columns (as vBoxes) of the VIP main window.
        ### The VIP._qWidgets values were created in the '.build_all' call.
        ### The 'vBoxs' dictionary here is a local one (as opposed to an attribute
        ### of the VIP) and so the three keys are throwaway references that are
        ### not used later. This is why I use a prefix underline.
        vBox_KEYS = ['_control', '_measure', '_dosweep']
        vBoxs = {}
        for k in vBox_KEYS:
            vBoxs[k] = QtGui.QVBoxLayout()
            vBoxs[k].addStretch(.1)

        vBoxs['_control'].addWidget(self._qWidgets['qw']['Results'])
        vBoxs['_control'].addStretch(.1)
        vBoxs['_control'].addWidget(self._qWidgets['qw']['Session'])
        vBoxs['_control'].addStretch(.1)
        vBoxs['_control'].addWidget(self._instrument_qw_box)
        vBoxs['_control'].addLayout(self._blanks.next())
        vBoxs['_control'].addStretch(.1)
        vBoxs['_control'].addWidget(self._qWidgets['tb']['_Source_Instr'])

        vBoxs['_measure'].addLayout(self._blanks.next())
        vBoxs['_measure'].addWidget(self._qWidgets['tb']['Sweep_1'])
        vBoxs['_measure'].addLayout(hBox_point_label)
        vBoxs['_measure'].addWidget(self._qWidgets['tb']['Points'])
        vBoxs['_measure'].addStretch(.1)
        vBoxs['_measure'].addLayout(hBox_trace_lb)
        vBoxs['_measure'].addWidget(self._qWidgets['tb']['Traces'])
        vBoxs['_measure'].addStretch(.1)
        vBoxs['_measure'].addWidget(self._qWidgets['tb']['_Meas_Instr'])

        vBoxs['_dosweep'].addLayout(self._blanks.next())
        vBoxs['_dosweep'].addStretch(.1)
        vBoxs['_dosweep'].addLayout(hBox_progress_bar)
        vBoxs['_dosweep'].addStretch(.1)
        vBoxs['_dosweep'].addWidget(self._qWidgets['qw']['Sweep'])
        vBoxs['_dosweep'].addLayout(self._blanks.next())
        vBoxs['_dosweep'].addWidget(self._qWidgets['tb']['Sweep_2'])
        vBoxs['_dosweep'].addWidget(self._qWidgets['tb']['Sweep_3'])
        vBoxs['_dosweep'].addStretch(.1)
        vBoxs['_dosweep'].addWidget(self._popup_window_qw_box)

        ########## hBox
        ### Create a large hBox and put the three vBoxes into it.
        hBox = QtGui.QHBoxLayout()
        hBox.addLayout(self._blanks.next())
        hBox.addStretch(1)

        for k in vBox_KEYS:
            hBox.addLayout(vBoxs[k])
            hBox.addLayout(self._blanks.next())
            hBox.addStretch(1)

        return hBox

    def __adopt_style(self):
        ### At initialization, he might complain that he can't parse stylesheets
        ### of some widgets. I assume it has to do with the buttons or so, but
        ### it doesn't matter.

        self._popup_window_qw_box.setStyleSheet(cs.STYLE_control)
        for k in ['Results', 'Session']:
            self._qWidgets['qw'][k].setStyleSheet(cs.STYLE_control)

        self._instrument_qw_box.setStyleSheet(cs.STYLE_instruments)
        for k in ['_Source_Instr', '_Meas_Instr']:
            self._qWidgets['tb'][k].setStyleSheet(cs.STYLE_instruments)

        self._qWidgets['qw']['Sweep'].setStyleSheet(cs.STYLE_sweeps)
        for k in ['Sweep_1', 'Sweep_2', 'Sweep_3']:
            self._qWidgets['tb'][k].setStyleSheet(cs.STYLE_sweeps)

        self.setStyleSheet(cs.STYLE_VIP)

        ### Load some settings from the constants.py file and set them for the VIP
        self.move(*cs.MOVE_VIP)
        self.resize(*cs.RESIZE_VIP)
        self.setWindowTitle(cs.WINDOW_TITLE_VIP)

################################################################################ VIP-API

    def get(self, sk, k = None):
        """Return thesession dictonaries d for a session key 'sk' or a
        particular value of it, d[k].
        """
        try:
            r = self._session[sk]
            if k != None:
                r = r[k]
            return r
        except KeyError as exception:
            print "!!! (.get):\n{0}\n.get will liekly return 'None'.".format(exception)

    def set(self, sk, settings):
        """Using the dictionary 'settings', update the dictonary d with the
        session key 'sk'.
        """
        ### settings has format {'k1' : v1, 'k2' : v2, ...}
        ### where the values v must be convertible to strings for the command
        for k, v in settings.iteritems():
            v = str(v)
            self._session[sk][k] = v
            ### Note: There are some session values that are not loaded
            ### into any widget.
            try:
                if k in self._qWidgets['le'][sk].keys():
                    self._qWidgets['le'][sk][k].setText(v)
                elif k in self._qWidgets['dm'][sk].keys():
                    auxi.set_dm(self._qWidgets['dm'][sk][k], v)
                    self._session[sk][k] = v
                elif k in self._qWidgets['cb'][sk].keys():
                    on_off_pair = self.content['cb_vals'][sk][k]
                    auxi.set_cb(self._qWidgets['cb'][sk][k], on_off_pair, v)
            #auxi.sourced_print("("+sk+"), ignored "+k+", "+v)
            except KeyError:
                auxi.sourced_print("("+sk+"), KeyError exception for "+k)

    def adopt_session(self, session):
        for sk, settings in session.iteritems():
            self.set(sk, settings)
            print sk
            print len(settings)
        #vip.update_figures()
        auxi.sourced_print("called.")

    def is_connected(self, instr_name):
        """Return a boolean 'B_is_connected' that is true if the insturment with
        name 'instr_name' has its connect checkbox set positive, and if its
        corresponding VIP attribute '.instruments[instr_name]' has a driver
        associated with it. This is done by checking if the attribute has a
        method 'get_session_index()'.
        """
        ### Assume the instrument is connected and then check if your're wrong.
        B_is_connected = False

        if self.get(instr_name, 'B_connect') == 'TRY':
            try:
                session_index = self.instruments[instr_name].get_session_index()
                message = instr_name+": "+"is connected! Session index: "+str(session_index)
                self.GUI_feedback(message)
                ### If the routine got thus far, we can be confident that the
                ### instrument is connected.
                B_is_connected = True
            except AttributeError:
                ### This exception will be thrown if 'self.instruments[instr_name]'
                ### does not have a method 'get_session_index()'
                message = instr_name+": is not connected! (get_session_index fail)"
                print message
        else:
            pass # message = instr_name+": Connection checkbox not even set to TRY."

        return B_is_connected

    def GUI_feedback(self, message):
        """Write 'message' to the Widget window, 'self._FeedbackWindow'"""
        self._FeedbackWindow.update(self, message)
        ### Also print the 'message' to the editor/terminal. he function
        ### 'sourced_print' is just 'print' with a header that tells us the
        ### function it has been called from (in this case, 'GUI_feedback')
        auxi.sourced_print(message)

    def runtime(self):
        """Return the runtime of the VIP, i.e. the passed time since 'self._TIC'
        has been initialized via the VIP's __init__ method."""
        runtime_string_seconds = auxi.toc(self._TIC)
        return "\nVIP session runtime:\n{0}\n".format(runtime_string_seconds)

    def update_figures(self, dim = None):
        """The Canvas class instances have a 'update_figure' method.Depending
        on the session values and the argument 'dim', update the VIP plots.
        """
        for sk in session.Plot.keys():
            if self.get(sk, 'B_keep_updated') == 'ON':
                if (dim == None) or (dim == '2d_data'):
                    self.Canvas[sk]['2d_data'].update_figure(sk, self)
                if (dim == None) or (dim == '3d_data'):
                    self.Canvas[sk]['3d_data'].update_figure(sk, self)
        ### Finally, process all open Qt operations.
        QtCore.QCoreApplication.processEvents()
        #auxi.sourced_print("called.")

    def reset_sweep_tracker(self):
        """Set the VIP 'attribute self.sweep_tracker' to a dictionary that has
        the value '0' for all three measurement loop references, 1, 2 and 3.
        """
        self.sweep_tracker = {k_data : {str(i) : 0 for i in [1, 2, 3]} for k_data in menus.DATA_SET_KEYS}
        #auxi.sourced_print("called.")

################################################################################ closeEvent

    def closeEvent(self, evnt):
        """'closeEvent' is the name of a QWidget build in method that is called
        whenever the widget is closed. In the case that the VIP is closed, we
        want to close all other open widgets as well.
        """
        self._PlotsWindow_12.close()
        self._PlotsWindow_34.close()
        self._FeedbackWindow.close()
        self.ScriptsWindow.close()
        self._OptionsWindow.close()
        try:
            self._NotesWindow.close()
        except AttributeError:
            pass

        ### Actively remove from instrument to be connected:
        #for sk in ['H3344_1']:
        #    self.set(sk, {'B_connect' : 'DONT'})
        #import interface.session_events as events
        #events.bn_connect_to_lab(self)
        try:
            from drivers.DriverH3344_AWG import DriverH3344 as _DriverH3344
            _DriverH3344._clear_channels()
        except (NotImplementedError, ImportError, TypeError) as exception: ### except WindowsError
            print "! (VirtualInstrumentPanel, closeEvent) Exception for DriverH3344_AWG:"
            print str(exception)
        ### The boolean attribute VIP.B_cannot_be_closed defined above in this
        ### class makes it so that we can choose the VIP window to be indestrutable.
        if self.B_cannot_be_closed is True:
            evnt.ignore()
            self.setWindowState(QtCore.Qt.WindowMinimized)
            message = "The VIP is protected from being closed.\nRestart the Kernel to kill it."
        else:
            super(VirtualInstrumentPanel, self).closeEvent(evnt)
            message = "\nVIP was closed.\n"

        ### When the VIP closes, we report back with the total runtime.
        message += self.runtime()
        self.GUI_feedback(message)

        ### Print a bunch of "|"'s so that we see we are again allowed to use
        ### the editor/terminal.
        print HLINE1+HLINE2

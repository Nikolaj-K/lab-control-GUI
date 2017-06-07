from PyQt4  import QtGui, QtCore
from PySide import QtGui #, QtCore
import dictionaries.constants as cs

################################################################################
class InvisibleWindow(QtGui.QWidget):
    """This class is a window that collects widgets (from vip._qWidgets)
    which are not supposed to be adjustable from the VIP GUI, but which still
    have to be somewhere.
    (The issue is that PyQt will otherwise put those widgets into the upper 
    right corner of the VIP main window.)
    """

    def __init__(self, vip):
        super(InvisibleWindow, self).__init__()
        
        vBox = self._build_vBox(vip) ### ge the vBox containing unwanted stuff
        self.setLayout(vBox)
        
        self.setWindowTitle(cs.WINDOW_TITLE_INVISIBLE)
        
    def _build_vBox(self, vip):
        """Create a vBox and dump, for each session key, all the widgets that 
        are supposed to be invisible. 
        E.g. 'R_freq_start' for sk = 'Time trace'.
        """
        vBox = QtGui.QVBoxLayout()

        ########## BEGIN Time trace
        sk = 'Time trace'
        
        lb = QtGui.QLabel(sk)
        lb.setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE+2))
        lb.adjustSize()  
        vBox.addWidget(lb)
        
        le_ks = ['R_freq_start'
                ,'R_freq_stop'
                ,'_R_freq_span'
                ]
        for k in le_ks: 
            for qw in ['lb','le']:
                vBox.addWidget(vip._qWidgets[qw][sk][k])
    
        return vBox
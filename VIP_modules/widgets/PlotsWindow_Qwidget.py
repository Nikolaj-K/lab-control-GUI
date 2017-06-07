from PyQt4  import QtGui, QtCore
from PySide import QtGui

import dictionaries.constants as constants


################################################################################   

class PlotsWindow(QtGui.QWidget):

    def __init__(self, vip, columns_list):

        self._B_can_make_screenshot = False
        
        super(PlotsWindow, self).__init__()

        self.resize(*constants.RESIZE_PLOT)
        self.move(*constants.MOVE_PLOT)
        self.setWindowTitle(constants.WINDOW_TITLE_PLOT)

        ########## vBoxs

        vBoxs = {k : QtGui.QVBoxLayout() for k in columns_list}
            
        for sk in columns_list:
            vBoxs[sk].addWidget(vip._qWidgets['qw'][sk])
            
        ########## hBox
    
        hBox = QtGui.QHBoxLayout()
        hBox.addStretch(1)

        for k in columns_list:
            hBox.addLayout(vBoxs[k])
            hBox.addStretch(1)  
        
        self.setLayout(hBox)
        
    def closeEvent(self, evnt):
        
        self._B_can_make_screenshot = False
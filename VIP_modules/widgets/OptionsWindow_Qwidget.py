from PyQt4  import QtGui, QtCore
from PyQt4.QtGui import QPixmap #, QApplication
from PySide import QtGui #, QtCore

import dictionaries.constants as constants


################################################################################   

class OptionsWindow(QtGui.QWidget):

    def __init__(self, vip):
        
        super(OptionsWindow, self).__init__()

        self._build_layout(vip)
        
        self.resize(*constants.RESIZE_OPTIONS)
        self.move(*constants.MOVE_OPTIONS)
        self.setWindowTitle(constants.WINDOW_TITLE_OPTIONS)
         
        
    def _build_layout(self, vip):

        ########## vBoxs
    
        #vBox_ks = []

        #vBoxs = {k : QtGui.QVBoxLayout() for k in vBox_ks}
            
        #for tb in vBox_ks:
        #    vBoxs[tb].addWidget(vip._qWidgets['qw'][tb])
            
        ########## hBox
    
        hBox = QtGui.QHBoxLayout()

        hBox.addWidget(vip._qWidgets['qw']['Options'])
        hBox.addStretch(1)  
        
        self.setLayout(hBox)


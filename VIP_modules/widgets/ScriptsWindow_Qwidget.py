from PyQt4  import QtGui
from PySide import QtGui

################################################################################   

class ScriptsWindow(QtGui.QWidget):

    def __init__(self, vip):

        self._B_can_make_screenshot = False
        
        super(ScriptsWindow, self).__init__()

        self._build_layout(vip)
        
        import dictionaries.constants as cs
        self.resize(*cs.RESIZE_SCRIPTS)
        self.move(*cs.MOVE_SCRIPTS)
        self.setWindowTitle(cs.WINDOW_TITLE_TABS)

        self.setStyleSheet(cs.STYLE_VIP) 
        
    def _build_layout(self, vip):
    
        ########## vBoxs

        vBox = QtGui.QVBoxLayout()

        vBox.addWidget(vip._qWidgets['qw']['Script'])
        vBox.addStretch(1)
        vBox.addLayout(vip._blanks.next()) 
        vBox.addWidget(vip._qWidgets['tb']['Scripts'])
        vBox.addLayout(vip._blanks.next()) 
            
        self.setLayout(vBox)

        
    def closeEvent(self, evnt):
        
        self._B_can_make_screenshot = False
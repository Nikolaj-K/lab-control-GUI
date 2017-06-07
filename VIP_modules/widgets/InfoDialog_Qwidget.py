from PyQt4  import QtGui
from PySide import QtGui

import dictionaries.constants as cs

################################################################################

class InfoDialog(QtGui.QWidget):

    def __init__(self, info_message):
        super(InfoDialog, self).__init__()

        self.build_label(info_message) 
        self.build_button() 
        self.build_layout() 
        
    def build_layout(self):
        hbox = QtGui.QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self._bn_close_info_dialog)

        vbox = QtGui.QVBoxLayout()
        vbox.addWidget(self._lb_info_message)
        vbox.addStretch(1)
        vbox.addLayout(hbox)

        self.setLayout(vbox)
        self.resize(*cs.RESIZE_INFO)
        self.move(*cs.MOVE_INFO)
        self.setWindowTitle(cs.WINDOW_TITLE_INFO)
        
    def build_label(self, info_message):
        self._lb_info_message = QtGui.QLabel(info_message, self)
        self._lb_info_message.setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE-1))
        self._lb_info_message.adjustSize()
        self._lb_info_message.move(30*1.0/2, 30*1.0/2)

    def build_button(self):
        label = "Close"
        self._bn_close_info_dialog = QtGui.QPushButton(label)
        self._bn_close_info_dialog.setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE))
        self._bn_close_info_dialog.adjustSize()
        self._bn_close_info_dialog.clicked.connect(self.bn_close_info_dialog)

    def bn_close_info_dialog(self):
        self.close()

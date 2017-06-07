from PyQt4  import QtGui, QtCore
from PyQt4.QtGui import QPixmap #, QApplication
from PySide import QtGui #, QtCore

import dictionaries.constants as cs


################################################################################

sk = 'Feedback' # session key

class FeedbackWindow(QtGui.QWidget):

    def __init__(self, vip):
        
        super(FeedbackWindow, self).__init__()
        
        self.__build_content(vip) 
        self.__build_layout(vip) 
        
        self.resize(*cs.RESIZE_FEED)
        self.move(*cs.MOVE_FEED)
        self.setWindowTitle(cs.WINDOW_TITLE_FEED)


################################################################################

    def update(self, vip, value):
        
        message = "\n"
        
        if isinstance(value, basestring):
            message += value+"\n"
        else:
            try:
                for elem in value:
                    try:
                        message += elem+"\n"
                    except TypeError:
                        pass
            except TypeError:
                message = "!!! (FeedbackWindow, TypeError):\n"
                message += "A strange value was passed to the update method."
            
        self.lb_GUI_message.setText(message)
        self.lb_GUI_message.adjustSize()
        

################################################################################
        
    def __build_content(self, vip):
        
        button_label = " Close "
        self.bn_close = QtGui.QPushButton(button_label)
        self.bn_close.setFont(QtGui.QFont(cs.FANCYFONT, cs.FONTSIZE))
        self.bn_close.adjustSize()
        self.bn_close.clicked.connect(lambda: self.close())
        
        button_label = " Total VIP Runtime "
        self.bn_runtime = QtGui.QPushButton(button_label)
        self.bn_runtime.setFont(QtGui.QFont(cs.FANCYFONT, cs.FONTSIZE))
        self.bn_runtime.adjustSize()
        self.bn_runtime.clicked.connect(lambda: vip.GUI_feedback(vip.runtime()))
        
        self.lb_GUI_message = QtGui.QLabel()
        self.lb_GUI_message.setFont(QtGui.QFont(cs.FANCYFONT, cs.FONTSIZE+2))

    def __build_layout(self, vip):

        ########## hBoxs

        hBox_bn_close = QtGui.QHBoxLayout()
        hBox_bn_close.addStretch(1)
        hBox_bn_close.addWidget(self.bn_close)

        hBox_bn_runtime = QtGui.QHBoxLayout()
        hBox_bn_runtime.addWidget(self.bn_runtime)
        hBox_bn_runtime.addStretch(1)

        hBox_lb_feedback = QtGui.QHBoxLayout()
        hBox_lb_feedback.addStretch(1)
        hBox_lb_feedback.addWidget(self.lb_GUI_message)
        hBox_lb_feedback.addStretch(1)

        ########## vBox

        vBox = QtGui.QVBoxLayout()
        vBox.addLayout(hBox_bn_runtime)
        vBox.addStretch(1)
        vBox.addLayout(hBox_lb_feedback)
        vBox.addStretch(1)
        vBox.addLayout(hBox_bn_close)

        self.setLayout(vBox)
        
        

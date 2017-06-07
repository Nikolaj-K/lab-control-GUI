import os ### The os package is used a lot in this little file
from PyQt4 import QtGui

import dictionaries.constants as cs

################################################################################
class NotesWindow(QtGui.QWidget):
    """This is a window with a large text field. When opened, it tries to load 
    the content of a text file unsed some specified address. When closed, it 
    overwrites said text file with the (now probably altered) text from the text 
    field.
    """
    def __init__(self, vip):
        """Create handles for the name and path of the file as attribute and 
        call the functions to build the window.
        """
        super(NotesWindow, self).__init__()

        FILE_PATH_notes      = vip.get('Options', 'FILE_PATH_notes') 
        self.FILE_NAME_notes = os.path.basename(FILE_PATH_notes)
        self.DIR_PATH_notes  = os.path.dirname(FILE_PATH_notes)

        self._build()
        self._read_in_the_note_text()
        self._layout()

        self.resize(*cs.RESIZE_NOTES)
        self.move(*cs.MOVE_NOTES)
        self.setWindowTitle(cs.WINDOW_TITLE_NOTES)

    def bn_action__show_DIR_PATH_notes(self):   
        """When the button is clicked, the label text shall change to the string 
        that tells us the directory path of the notes that we're editing"""     
        self.lb_bottom.setText(self.DIR_PATH_notes)

    def _build(self):
        default_te_message  = "\n\n"+self.FILE_NAME_notes
        default_te_message += "\nin\n"+self.DIR_PATH_notes
        default_te_message += "\n\ncould not be loaded."
        default_te_message += "\n\nChange the path in the options dialog."
        self.te = QtGui.QTextEdit(default_te_message)
        self.te.setFont(QtGui.QFont(cs.FONT, cs.FONTSIZE)) 

        bn_text = cs.BLANK+"Get file location"+cs.BLANK
        self.button = QtGui.QPushButton(bn_text)
        self.button.clicked.connect(self.bn_action__show_DIR_PATH_notes)
        self.button.setFont(QtGui.QFont(cs.FANCYFONT, cs.FONTSIZE)) 

        lb_text_top = "Hello! Write down your notes here."
        self.lb_top = QtGui.QLabel(lb_text_top)
        self.lb_top.setFont(QtGui.QFont(cs.FANCYFONT, cs.FONTSIZE)) 

        lb_text_bottom = "Close this window to write the text to "+self.FILE_NAME_notes
        self.lb_bottom = QtGui.QLabel(lb_text_bottom)
        self.lb_bottom.setFont(QtGui.QFont(cs.FANCYFONT, cs.FONTSIZE)) 

    def _layout(self):
        ########## hBox
        hBox_top = QtGui.QHBoxLayout()
        hBox_top.addWidget(self.lb_top)
        hBox_top.addStretch(1)

        hBox_bottom = QtGui.QHBoxLayout()
        hBox_bottom.addWidget(self.lb_bottom)
        hBox_bottom.addStretch(1)
        hBox_bottom.addWidget(self.button)

        ########## vBox
        vBox = QtGui.QVBoxLayout(self)
        vBox.addLayout(hBox_top)
        vBox.addWidget(self.te)
        vBox.addLayout(hBox_bottom)
        
        self.setLayout(vBox)

    def _read_in_the_note_text(self):  
        """Try to open the file in the directory path. If that works, read in
        the text and use the setText method of the text edit widget (to) 
        to copy the file content to that widget."""   
        if not os.path.isdir(self.DIR_PATH_notes):   
            message = "(NotesWindow) Specified directory does not exist."     
        else:
            ### Store the current directory path in a local variable
            DIR_PATH_cwd = os.getcwd() 
            ### Go to DIR_PATH_session
            os.chdir(self.DIR_PATH_notes) 
            try:
                notes_file = open(self.FILE_NAME_notes, 'r')
                with notes_file:
                    text = notes_file.read()
                self.te.setText(text)
                message = "(NotesWindow) Notes text was loaded."
            except IOError:
                message = "!!! (NotesWindow, IOError) The specified file was not found in the directory." 
            ### GGo back to main dir  
            os.chdir(DIR_PATH_cwd) 

        message = "(NotesWindow) was opened.\n" + message
        print message
        
    def closeEvent(self, evnt):
        """When the notes window widget is closed (usually in the normal way, 
        through the red X closing button that each Window window has), do 
        essentially the reverse of what you did when you read in the file:
        Open the file and write the text edit content to the text file."""
        super(NotesWindow, self).closeEvent(evnt) 
        ### The above is the basic closing even for such Qwidgets and now comes
        ### the extra stuff that we want to happen.
        
        if not os.path.isdir(self.DIR_PATH_notes):   
            message = "(NotesWindow) Specified directory does not exist."     
        else:
            DIR_PATH_cwd    = os.getcwd()
            ### Go to DIR_PATH_session
            os.chdir(self.DIR_PATH_notes)
            try:
                text = self.te.toPlainText()
                with open(self.FILE_NAME_notes, 'w') as out_file:
                    out_file.write(text)
                message = "(NotesWindow) Text write to notes file."
            except IOError:
                message = "(NotesWindow, IOError) The specified file was not found in the directory."     
            ### GGo back to main dir
            os.chdir(DIR_PATH_cwd)

        message = "(NotesWindow) was closed." + message
        print message
        
        
        
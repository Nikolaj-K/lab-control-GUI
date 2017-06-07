# -*- coding: utf-8 -*-
import sys
import os
from PyQt4 import QtGui

################################################################################
def QtGui_decorator(my_function):
    """Provide a wrapper for the main function to create the enviorment to run 
    a PyQt GUI application.
    """
    def wrapper(*args, **kwargs):
        try: 
            GUIapp = QtGui.QApplication(sys.argv)
        except RuntimeError:
            ### Uses the app from a previous instantiation.
            GUIapp = QtGui.QCoreApplication.instance() 
            print "! (Qt_decorator) An older PyQt4 application was used."  
           
        print
        print "Working directory BEFORE the main function call:"
        print os.getcwd()
        
        my_function()
        
        print "Working directory AT THE END OF the main function call:"
        print os.getcwd() 
        print
        print "If you didn't call the GUI via VIP.show() from VIP_main, " + \
        "using PyQt4 will eventually require you to reset the kernel. "
        print "Otherwise, have fun with the user interface! <3"
        print
        print "/(Qt_decorator)" + 4*"\n"
        
        sys.exit(GUIapp.exec_())
    return wrapper
    
    
    
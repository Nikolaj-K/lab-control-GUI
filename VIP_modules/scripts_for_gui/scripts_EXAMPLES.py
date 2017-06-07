from time import time as time_now

#VIP.instr['instr_name']
#VIP.result
#VIP.trace_plot
#VIP.densi_plot

################################################################################

def printer_main(VIP):
    ### This short script takes the current VIP session value under
    box = 'Printer demo'
    k   = 'string_to_print'
    ### and writes it to the GUI Feedback window. (and then automatically also 
    ### to the Python terminal/editor) This key is also associated with a 
    ### LineEdit widget in the Printer demo tab. For this, obtain the value with 
    ### the VIP method '.get'
    message = VIP.get(box, k) 
    
    print 3*"\n"
    VIP.GUI_feedback(message)
    print 3*"\n"

    ### Finally, we use the '.set' method to overwrite the curreent LineEdit value. 
    ### In particular, we add a star at the end of the message.
    settings_new = {k : message+" *"}
    VIP.set(box, settings_new) 

def get_frequency_main(VIP):
    TIC = time_now()
    INSTR_NAME = 'SGS_32'
    try:
        ### The connect button associates a driver with the entry
        ### 'instr['SGS_32']' of the instrument dictonary and this driver tries
        ### to open a resource (the physical insturment)
        ### We then call the drivers method 'get_frequency()', which returns a 
        ### string
        #~~~~~~~~~
        SG_frequency = VIP.instruments[INSTR_NAME].get_frequency()
        message  = "(SG-Script, get_frequency_main):\n"
        message += SG_frequency
    except AttributeError:
        message  = "!!! Instrument object "
        message += INSTR_NAME
        message += " was not connected to resource."
    VIP.GUI_feedback(message)
    
    TOC = time_now()
    message = "(get_frequency_main) Runtime:\n" + str(TOC-TIC) + " sec"
    VIP.GUI_feedback(message)





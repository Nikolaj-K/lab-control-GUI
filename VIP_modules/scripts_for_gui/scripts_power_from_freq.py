"""This script does not have a tab associated with it. 
In such a tab, one could e.g. change the sweep index (1, 2 or 3) 
for which the script is supposed to be performed. 
One also may set the power for another insturment
than for the sweeping instrument itself.
"""

################################################################################
def main(VIP):
    """This main function essentially splits into three parts.:
    - Get the frequency of the sweep instrument. 
    - Compute an associated power value.
    - Set that power value.    
    We may presuppose the chosen instrument has the get_frequency method.
    To be saver, we can add a TRY clause and catch a possible AttributeError.
    A 4-line version of it is the following:
    
        sweep_instr = VIP.get('Freq. sweep 1', 'F_instr_name')
        freq = VIP.instruments[sweep_instr].get_frequency() 
        power = numerical_function(freq)
        VIP.instruments[sweep_instr].set_power(power) 
    """
    sweep_index = 1

    ########## GET-part of the script
    ### Automatically compute which instrument is doing sweep
    title_key   = 'sweep_title_'+str(sweep_index) 
    sweep_type  = VIP.get('Sweep', title_key) 
    sweep_instr = VIP.get(sweep_type, 'F_instr_name')

    try:
        freq = VIP.instruments[sweep_instr].get_frequency() 
    except AttributeError:
        print "!!! Methods of wrong insturments were called."
          
    ########## COMPUTING-part of the script                                                  
    power = numerical_function(freq)

#XXX REMOVE THIS
#XXX 
#XXX Since I don't know your 'numerical_function', I overwrite 'power' again
#XXX 
    instr_name = sweep_instr  
    try:
        power = VIP.instruments[instr_name].get_power()
        power = float(power) - 1.5
    except AttributeError:
        print "!!! Methods of wrong insturments were called."
#XXX / REMOVE THIS

    ########## SET-part of the script
    ### Reference name of the instrument for which we will set the power
    ### Instead, we could also go with something like: instr_name = 'ZNB_1'
    instr_name = sweep_instr  

    ### The follwoing line just updates the session value and is thus optional
    ### Instead, we could also go with something like: session_key = 'R_freq_source'
    source_key = 'R_power_source'                                              
    VIP.set(instr_name, {source_key : str(power)})

    try:
        VIP.instruments[instr_name].set_power(power, None) 
    except AttributeError:
        print "!!! Methods of wrong insturments were called."
    
################################################################################
    
def numerical_function(val_in):
    """Desciption of the function"""
    val_in = float(val_in)
    local_val = val_in + 1
    val_out = local_val - 1
    return val_out
    
    
    
    
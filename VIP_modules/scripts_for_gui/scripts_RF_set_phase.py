import time

def set_phase_main(VIP):
    
    INSTR_NAME = 'SGS_32'

    try:
        phase = VIP.sweep_tracker['I_data']['2'] * 7

        VIP.instruments[INSTR_NAME].set_phase(phase)
        message  = "done"
    except AttributeError:
        message  = "!!! Exception"
        
    time.sleep(3)
        
    VIP.GUI_feedback(message)





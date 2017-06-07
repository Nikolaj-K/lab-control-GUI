import time

try:
    import external.delft as external_delft ### from Josip
except ImportError as exception:
    print "!! (scrpts_flux_sweep, ImportError) external_delft:"
    print exception
    external_delft = None

################################################################################

### Setup
"""
srs output should go into fridge via the flux input (through all the srs stuff, loads and whatnot)
sgs should go to qubit in the fridge
VNA port one into cavity
VNA port two out from cavity (and through amp)
"""

    # com_port = int(input('Input your desired COM port: '))
    # dac_port = int(input('Input your desired dac port identifier: '))
    #print('------------------------------------------------------------------------')
    # cav_freq = float(input('Input the cavity frequency in GHz: '))
    # span = float(input('Input your desired span about the cavity frequency in Hz: '))
    # fn = input('input your desired filename: ')
    #print('------------------------------------------------------------------------')
    # pow = float(input('Input your desired power for the source frequency sweep: '))
    # start_freq = float(input('Input your desired start frequency (GHz) for the source frequency sweep: '))
    # stop_freq = float(input('Input your desired stop frequency (GHz) for the source frequency sweep: '))
    # step_size_ssg = float(input('Input your desired step size for the source frequency sweep: '))
    #print('------------------------------------------------------------------------')
    # start_flux = float(input('Input your desired start flux for the SRS power sweep: '))
    # stop_flux = float(input('Input your desired stop flux for the SRS power sweep: '))
    # step_size_srs = float(input('Input your desired step size for the SRS flux sweep: '))

    #power = float(my_session["Flux sweep"]["pow"]) ### NOT USED

def main(vip):

    com_port = float(vip.get("Flux sweep", "com_port"))
    dac_port = float(vip.get("Flux sweep", "dac_port"))
    DAC_instance = external_delft.DAC('COM' + str(com_port), dac_port, 'POS')
    DAC_instance.set(0)

    SGS_name = vip.get("Flux sweep", "ssg_ip")
    
    cav_freq = float(vip.get("Flux sweep", 'cav_freq'))
    span     = float(vip.get("Flux sweep", 'span'))
    
    VNA_name = vip.get("Flux sweep", "vna_ip")
    vna = vip.instruments[VNA_name]
    vna.write('SENS:FREQ:CENT ' + str(cav_freq) + 'GHz')
    vna.write('SENS:FREQ:SPAN ' + str(span))
    vna.write('SENS:SWE:COUNT 5')
    vna.write('SENS:AVER ON')
    vna.write("CALCulate1:PARameter:SDEFine 'Trc1', 'S21'")
    vna.write("CALCulate1:FORMat MLOG")
    vna.write("SYSTem:DISPlay:UPDate ON")

    ##########

    start_freq    = float(vip.get("Flux sweep", "start_freq"))
    stop_freq     = float(vip.get("Flux sweep", "stop_freq"))
    step_size_ssg = float(vip.get("Flux sweep", "step_size_ssg"))
    
    num_steps = int((stop_freq - start_freq) / step_size_ssg + 1)
    if num_steps <= 1 or start_freq < 0 or stop_freq < 0:
        print('Improper sweep values for source')
        quit()
    print(vna.write('SOUR:FREQ:SPAN ' + str(span)))

    ##########

    start_flux    = float(vip.get("Flux sweep", "start_flux"))
    stop_flux     = float(vip.get("Flux sweep", "stop_flux"))
    step_size_srs = float(vip.get("Flux sweep", "step_size_srs"))
    values = []

    for i in range(0, num_steps):
        f = start_freq + i * step_size_ssg
        
        vip.instruments[SGS_name].write('SOUR:FREQ ' + str(f) + 'GHz')
        
        triplets = _srs_flux_sweep(DAC_instance, vna, f, start_flux, stop_flux, step_size_srs, span)

        values.extend(triplets)
        
        print('FREQ STEP DONE: ' + str(i))
    
    ##########
        
    r = str(values)
    r = r.replace('[', '{')
    r = r.replace(']', '}')

    file_name = vip.get("Flux sweep", "fn")
    f = open(file_name+".txt", 'w')
    f.write(r)


################################################################################

def _srs_flux_sweep(dac, vna, ssg_freq, start_flux, stop_flux, step_size, span):

    num_steps = int((stop_flux - start_flux) / step_size + 1)

    if num_steps <= 1:
        print('Improper sweep values for VNA')
        quit()

    triplets = []

    for i in range(0, num_steps):
        time.sleep(.5)
        tmp_flux = start_flux + i * step_size
        dac.set(tmp_flux)
        vna.write("DISPlay:WINDow1:TRACe1:FEED 'Trc1'")
        vna.write("SYSTem:DISPlay:UPDate ON")
        avg_phase = _collect_phase_average(vna, span)
        triplets.append([tmp_flux, ssg_freq, avg_phase])
        
        print('    FLUX STEP DONE: ' + str(i))

    return triplets


def _collect_phase_average(vna, span):

    vna.write('CALC:FORM: MLOG')
    vna.write('INIT1:IMM; *OPC?')
    vna.write('CALC:FORM: MLOG')
    vna.write("FORM:DEXP:SOUR FDAT")
    
    phases = vna.query_ascii_values("TRAC:DATA:RESPONSE? CH1DATA")
    # average = sum(phases)/len(phases)
    # return average
    # integral = sum(phases)*step_size
    integral = sum(phases)
    
    return integral




################################################################################

sk = 'Freq. vs. drive power' # session key


################################################################################

def main(vip):
    
    try:
        vna = vip.instruments[vip.get(sk, "VNA_instr"  )]
        ssg = vip.instruments[vip.get(sk, "Sweep_instr")]
    except AttributeError:
        message = "!!! ("+sk+", main, AttributeError):\nCould not connect."
        vip.GUI_message(message)

    r = source_freq_vna_pow_sweep(vip, vna, ssg)

    return formating(r)

def formating(val):
    
    s = str(val)
    s = s.replace('[', '{')
    s = s.replace(']', '}')

    return s

	
def source_freq_vna_pow_sweep(vip, vna, ssg):

    cav_freq = float(vip.get(sk, "R_freq_cavity_VNA"))
    span     = float(vip.get(sk, "R_freq_span_cavity_VNA"))

    vna.write('SENS:FREQ:CENT ' + str(cav_freq) + 'GHz')
    vna.write('SENS:FREQ:SPAN ' + str(span))	
    vna.write("CALCulate1:PARameter:SDEFine 'Trc1', 'S21'")	
    vna.write("CALCulate1:FORMat MLOG")
    vna.write("SYSTem:DISPlay:UPDate ON")
    
    power_SG = vip.get(sk, "R_power_SG")

    ssg.write('POW:POW ' + str(power_SG))
    print(vna.write('SOUR:FREQ:SPAN ' + str(span)))

##########

    start_freq    = float(vip.get(sk, "R_freq_start_SG"))
    stop_freq     = float(vip.get(sk, "R_freq_stop_SG"))
    step_size_ssg = float(vip.get(sk, "R_freq_step_size_SG"))

    num_steps = int(float(stop_freq - start_freq)/step_size_ssg + 1)
    if (num_steps <= 1) or (start_freq < 0) or (stop_freq < 0):
        print('Improper sweep values for source')
        quit()

##########

    start_pow     = float(vip.get(sk, "R_power_start_SG"))
    stop_pow      = float(vip.get(sk, "R_power_stop_SG"))
    step_size_vna = float(vip.get(sk, "R_power_step_size_SG"))

    values = []
    for i in range(0, num_steps):    
        tmp_freq = start_freq + i*step_size_ssg
        ssg.write('SOUR:FREQ ' + str(tmp_freq) + 'GHz')
        #triplets = VNA_pow_sweep(vna, tmp_freq, start_pow, stop_pow, step_size_vna, span)
        triplets = SGS_pow_sweep(vna, ssg, tmp_freq, start_pow, stop_pow, step_size_vna, span)
        values.extend(triplets)
        print('FREQ STEP DONE: ' + str(i))
        
    return values
	
	
def SGS_pow_sweep(vna, sgs, ssg_freq, start_pow, stop_pow, step_size, span):
	
    num_steps = int((stop_pow - start_pow)/step_size + 1)
    tmp_pow = start_pow
	
    if num_steps <= 1:
        print('Improper sweep values')
        quit()
	
    triplets = []

    #trace = collect_trace(vna)
    #print(str(trace))
    #
    # for el in trace:
        # triplets.append([ssg_freq,el[0],el[1]])
    # # print(str(triplets))
	
    for i in range(0, num_steps):
        print('Power step: ' + str(i))
        
        tmp_pow = start_pow + i*step_size
        sgs.write('POW:POW ' + str(tmp_pow))
        vna.write("DISPlay:WINDow1:TRACe1:FEED 'Trc1'")
        vna.write("SYSTem:DISPlay:UPDate ON")
        avg_phase = collect_phase_average(vna, span)
        triplets.append( [tmp_pow, ssg_freq, avg_phase] )
	#triplets.append('{' + str(tmp_pow) + ',' + str(ssg_freq) + ',' + str(avg_phase) +'}')
        print('    POW STEP DONE: ' + str(i))
	
    return triplets

	
def collect_phase_average(vna, span):
    
    vna.write('CALC:FORM: MLOG')
    vna.write('INIT1:IMM; *OPC?')
    vna.write('CALC:FORM: MLOG')
    vna.write("FORM:DEXP:SOUR FDAT")
    
    vna.write('FORM REAL')
    magnitude = vna.query_binary_values('CALC:DATA? SDAT')

    ###magnitude = vna.query_ascii_values("TRAC:DATA:RESPONSE? CH1DATA")
    #magnitude = vna.query_ascii_values('CALC1:DATA? SDAT'   , converter = 'f')
    #print(str(magnitude))
    
    #step_size = int(span/len(magnitude))
    # integral = sum(magnitude)*step_size
    #integral = sum(magnitude)
    #return integral
    
    average = float(sum(magnitude))/len(magnitude)
    
    return average


#def VNA_pow_sweep(vna, ssg_freq, start_pow, stop_pow, step_size, span):
#	
#    num_steps = int((stop_pow - start_pow)/step_size + 1)
#    tmp_pow = start_pow
#	
#    if num_steps <= 1:
#        print('Improper sweep values')
#        quit()
#	
#    triplets = []
#
#    #trace = collect_trace(vna)
#    #print(str(trace))
#    #
#    # for el in trace:
#        # triplets.append([ssg_freq,el[0],el[1]])
#    # # print(str(triplets))
#	
#    for i in range(0, num_steps):
#        tmp_pow = start_pow + i*step_size
#        vna.write('SOUR:POW ' + str(tmp_pow))
#        vna.write("DISPlay:WINDow1:TRACe1:FEED 'Trc1'")
#        vna.write("SYSTem:DISPlay:UPDate ON")
#        avg_phase = collect_phase_average(vna, span)
#        triplets.append( [tmp_pow, ssg_freq, avg_phase])
#	#triplets.append('{' + str(tmp_pow) + ',' + str(ssg_freq) + ',' + str(avg_phase) +'}')
#        print('    POW STEP DONE: ' + str(i))
#	
#    return triplets
#    
#	
#def collect_trace(vna):
#    vna.write('INIT1:IMM; *OPC?')
#    vna.write('CALC:FORM: MLOG')
#    vna.write('FORM:DEXP:SOUR FDAT')
#    omegas = vna.query_ascii_values('TRAC:STIM? CH1DATA', converter = 'f')
#    vals = vna.query_ascii_values('TRAC:DATA:RESPONSE? CH1DATA', converter = 'f')
#    to_return = []
#    for i in range(0,len(omegas)):
#        temp_list = []
#        #print(str(omegas[i]) + ', ' + str(vals[i]) + '\n')
#        temp_list.append(omegas[i])
#        temp_list.append(vals[i])
#        to_return.append(temp_list)
#    return omegas, vals
#    return to_return
#    
#
#def source_freq_vna_pow_sweep___for_nikolaj(ssg, vna, center_cavity_freq, span):
#    
#    vna.write('SENS:FREQ:CENT ' + str(center_cavity_freq) + 'GHz')
#    print(vna.write('SENS:FREQ:SPAN ' + str(span)))
#	
#    print('hi')
#	
#    vna.write('SENS1:SWE:COUNT 1')
#    vna.write('SENS1:AVER ON')
#	
#    vna.write("CALCulate1:PARameter:SDEFine 'Trc1', 'S12'")
#    vna.write("CALCulate1:FORMat MLOG")
#    vna.write("SYSTem:DISPlay:UPDate ON")
#
#
#    pow = float(input('Input your desired power for the source frequency sweep: '))
#    start_freq = float(input('Input your desired start frequency (GHz) for the source frequency sweep: '))
#    stop_freq = float(input('Input your desired stop frequency (GHz) for the source frequency sweep: '))
#    step_size_ssg = float(input('Input your desired step size for the source frequency sweep: '))
#    print('------------------------------------------------------------------------')
#	
#    num_steps = int(float(stop_freq - start_freq)/step_size_ssg + 1)
#    tmp_freq = start_freq
#    if num_steps <= 1 or start_freq < 0 or stop_freq < 0:
#        print('Improper sweep values for source')
#        quit()
#	
#    start_pow = float(input('Input your desired start power for the VNA power sweep: '))
#    stop_pow = float(input('Input your desired stop power for the VNA power sweep: '))
#    step_size_vna = float(input('Input your desired step size for the VNA power sweep: '))
#    print('------------------------------------------------------------------------')
#	
#    ssg.write('POW:POW ' + str(pow))
#    print(vna.write('SOUR:FREQ:SPAN ' + str(span)))
#
#    values = []
#    omega = []
#    ssg_freqs = []
#    for i in range(0, num_steps):
#        tmp_freq = start_freq + i*step_size_ssg
#        ssg.write('SOUR:FREQ ' + str(tmp_freq) + 'GHz')
#        #triplets = VNA_pow_sweep(vna, tmp_freq, start_pow, stop_pow, step_size_vna, span)
#        trace = collect_trace(vna)
#        ssg_freqs.append(tmp_freq)
#        omega.extend(trace[0])
#        values.extend(trace[1])
#        print('FREQ STEP DONE: ' + str(i))
#        #freqs.append(tmp_freq)
#    omega = f(omega)
#    values = reshape(len(omega), len(ssg_freqs), values)
#    file = open('values_file.txt', 'w')
#    file.write(str(values))
#    contour_plot(omega, ssg_freqs, values)
#    return values
#	
#def test_vna(vna):
#    center_cavity_freq = float(input('INPUT CCF in GHz: '))
#    print(vna.write('SENS:FREQ:SPAN 5Hz'))
#    print(vna.write('SENS:FREQ:CENT ' + str(center_cavity_freq) + 'GHz'))
#    
#    vna.write("DISPlay:WINDow1:TRACe1:FEED 'Trc1'")
#    vna.write("SYSTem:DISPlay:UPDate CONT")
#	
#    vna.write('INIT1:IMM; *OPC?')
#    #vna.write("CALCulate1:PARameter:SDEFine 'Trc1', 'S12'") 
#    vna.write("CALCulate1:FORMat DELAy")
#    #vna.write("FORM:DEXP:SOUR FDAT")	
#    #idk = vna.query_ascii_values('CALC1:DATA? SDAT'   , converter = 'f')
#    idk2 = vna.query_ascii_values("TRAC:DATA:RESPONSE? CH1DATA", converter = 'f')
#    #print(str(idk2))
#	
#def contour_plot(x,y,z):
#    import matplotlib.pyplot as plt
#    cs = plt.contourf(x,y,z)
#    plt.colorbar(cs)
#    plt.show()
#    
#def f(seq): # Order preserving
#    ''' Modified version of Dave Kirby solution '''
#    seen = set()
#    return [x for x in seq if x not in seen and not seen.add(x)]	
#  
#def reshape(len1, len2, z_vals):
#    overall = []
#    sub = []
#    i = 0
#    for el in z_vals:
#        sub.append(el)
#        i+=1
#        if i%len1 == 0:
#            overall.append(sub)
#            sub = []
#    return overall    		



    
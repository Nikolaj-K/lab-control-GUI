import numpy as np
import operator
import math
import random
import inspect
import os
import time

################################################################################
""" Those are function that never need to get passed the VIP """                ### !!! TODO: Exception handling not complete. Will fail at zero division

def concat(f, g):
    return lambda x: f(g(x))
    
def to_dB(xs):
    return np.multiply(10, np.log10(xs))  

def custom_axis(start, stop, sweep_points, axis_mode):
    axis = np.linspace(start, stop, sweep_points)
    """Your favorite function using the arguments start, stop and sweep_points"""
    if axis_mode=='Linear':
        pass
    elif axis_mode=='dBm':                                  ###n Since axis mode is also a feature for e.g. phase sweep, I would name it according to the function, not the unit computed from the function
        pass
    elif axis_mode=='Watts':
        startW = 10**(start/10)/1000
        stopW  = 10**(stop/10)/1000
        axisW  = np.linspace(startW, stopW, sweep_points)
        axis   = 10*np.log10(axisW*1000)
    elif axis_mode=='Volts': 
        startW = 10**(start/10)/1000
        startV = np.sqrt(startW*50)
        stopW  = 10**(stop/10)/1000
        stopV  = np.sqrt(stopW*50)
        axisV  = np.linspace(startV, stopV, sweep_points)
        axisW  = axisV**2/50
        axis   = 10*np.log10(axisW*1000)
    return axis

def P(I, Q):
    ### pass a Real to make division work properly
    sqare = lambda x: x**2
    Q2    = map(sqare, Q)
    I2    = map(sqare, I)
    Q2pI2 = map(operator.add, Q2, I2)
    return Q2pI2
    
def IQ_to_P(I, Q, P_ref=None):
    ### pass a Real to make division work properly
    sqare = lambda x: x**2
    Q2    = map(sqare, Q)
    I2    = map(sqare, I)
    Q2pI2 = map(operator.add, Q2, I2)
    
    if P_ref is not None:
        try:
            Q2pI2 = map(operator.div, Q2pI2, P_ref)
        except ZeroDivisionError: ### !!! TODO: Ensure ZeroDivisionError can't happen
            print "!!! (IQ_to_P_in_dB)\nZeroDivisionError\nP_ref entry is zero\n"

    return Q2pI2 

def IQ_to_P_in_dB(I, Q, P_ref=None):
    Q2pI2 = IQ_to_P(I, Q, P_ref=None)
    return to_dB(Q2pI2) 

def phi(I, Q):
    ### pass a Real to make division work properly
    try:
        IdQ = map(operator.div, I, Q)
    except ZeroDivisionError: ### !!! TODO: Ensure ZeroDivisionError can't happen
        print "!!! (IQ_to_P_in_dB)\nZeroDivisionError\nQ entry is zero\n"
    return map(np.arctan, IdQ)

def pairwise_difference(xs_1):
    xs = xs = list(xs_1)
    if len(xs) > 1:
        for i in range(len(xs)-1):
            xs[i] = xs[i+1]-xs[i]
        xs[-1] = xs[-2] ### assign second to last value to last value
    return xs

def savitzky_golay_filter(y, window_size=51, order=3, deriv=0, rate=1):
    """Taken from
    http://scipy.github.io/old-wiki/pages/Cookbook/SavitzkyGolay
    """ 
    error = "! (savitzky_golay_filter) Error raised: "   
    try:
        window_size = np.abs(np.int(window_size))
        order       = np.abs(np.int(order))
    except ValueError, msg:
        raise ValueError(error + "Window_size and order have to be of type int")
    if (window_size % 2) != 1 or window_size < 1:
        raise  TypeError(error + "Window_size size must be a positive odd number")
    if window_size < (order + 2):
        raise  TypeError(error + "Window_size is too small for the polynomials order")
    order_range = range(order + 1)
    half_window = (window_size - 1) // 2
    # precompute coefficients
    b = np.mat([[k**i for i in order_range] for k in range(-half_window, half_window+1)])
    m = np.linalg.pinv(b).A[deriv] * rate**deriv * math.factorial(deriv)
    ### pad the signal at the extremes with, values taken from the signal itself
    first_vals = y[0]  - np.abs(y[1:half_window + 1][::-1] - y[0])
    last_vals  = y[-1] + np.abs(y[-half_window-1:-1][::-1] - y[-1])
    y = np.concatenate((first_vals, y, last_vals))
    return np.convolve(m[::-1], y, mode='valid')

################################################################################ MISC
def colour(color_range): ### color_range goes up to 265
    n      = lambda: random.randint(0, color_range)
    scheme = "#%02X%02X%02X"
    triple = (n(), n(), n())
    return scheme % triple

def toc(tic):
    runtime_seconds = time.time() - tic
    m, s = divmod(runtime_seconds, 60)
    h, m = divmod(m, 60)
    runtime_string_seconds = "%d:%02d:%02d" % (h, m, s)
    print "\n- Runtime in seconds:\n"+runtime_string_seconds
    return runtime_string_seconds

def cut_top(tree):
    """
    {B : {a : x, b : y}, B : {c : z}} --> {a : x, b : z, c : z}
    or
    {A : [a, b], B : [c]} --> [a, b, c]
    """
    r = {}
    try:
        for d in tree.values():
            for k,v in d.iteritems():
                r[k] = v
    except AttributeError:
        try:
            r = []
            for L in tree.values():
                for elem in L:
                    r.append(elem)
        except AttributeError:
            pass
    return r

def cut_bottom(tree):
    """
    {A : {a : x, b : y}, B : {c : z}} ---> {A : [a,b], B : [c]}
    """
    return {k : v.keys() for k, v in tree.iteritems()}
    
def textfile_formatting(file_name):
    my_formatting = [(']]' , ']\n\n')
                    ,('],' , ']\n\n')
                    #,('[[' , '\n' + 80*'%' + '\n')
                    ,('[' , '')
                    ,(']' , '')
                    ,('"' , '\n')
                    ,(',' , '\t')
                    ]
    try:            
        with open(file_name, 'r') as in_file:
            for one_line in in_file: # there is actionall only one line
                for pair in my_formatting:
                    one_line = one_line.replace(pair[0], pair[1])
                                    
        with open(file_name, "w") as out_file:
            out_file.write(one_line)
    except IOError:
        print "!!! (textfile_formatting, IOError)"

def sourced_print(message):
    caller_name = inspect.stack()[1][3]
    print "(@{0}) {1}".format(caller_name, str(message))

def get_file_list(dir_path, begin_phrase, file_extension):
    cwd = os.getcwd() 
    file_list = []
    for root, dirs, files in os.walk(dir_path): 
        os.chdir(root)
        for file_name in files:
            if file_name.startswith(begin_phrase) and file_name.endswith(file_extension):
                file_list.append(dir_path + os.sep +  file_name)     
    os.chdir(cwd)
    return sorted(file_list)
        
def set_cb(cb, on_off_pair, value):
    on, off = on_off_pair
    if value in on_off_pair:
        if cb.isChecked():
            if value == off: cb.toggle()
        else:
            if value == on:  cb.toggle()
    else:
        print "!!! (set_cb):\nA non-existing string, {0}, was assigned to checkbox.".format(value)
        
################################################################################
################################################################################ PURE Qt FUNCTIONS 
################################################################################

from PyQt4.QtCore import Qt as Qt_submodule       
                                                                                                                                                                                                                                                                                                           
def set_dm(dm, value):
    index = dm.findText(value, Qt_submodule.MatchFixedString)
    if index >= 0:
        dm.setCurrentIndex(index)
    else:
        print "!!! (set_dm):\nA non-existing string, {0}, was assigned to dropdown menu.".format(value)

#import gc as gc ### That's a "garbage collector" interface module    
#def get_object_by_id(python_id):
#    for obj in gc.get_objects():
#        if id(obj) == python_id:
#            return obj
#    print "!!! No object found with python id = {}".format(python_id)


#FUNCTIONS FOR DIGITIZER

def running_mean(x, N):
    cumsum = np.cumsum(np.insert(x, 0, 0)) 
    return (cumsum[N:] - cumsum[:-N]) / N 
    
def PeriodicSignal(timeVec, A0, A1, A2, phi1, phi2,freq):

    #freq = 0.01
    y = [A0 + A1*np.cos(freq*timeVec[i]*2*np.pi + phi1) + A2*np.cos(2*freq*timeVec[i]*2*np.pi + phi2) for i in range(len(timeVec))]
    
    return y
    
def FitSignal(t,I,Q,freq):
    
    initial_values = [0,0,0,0,0,freq]
    from scipy.optimize import curve_fit
    Qvals, covar = curve_fit(PeriodicSignal, t, Q, p0=initial_values)
    Ivals, covar = curve_fit(PeriodicSignal, t, Q, p0=initial_values)

    powerDC = Qvals[0]**2 + Ivals[0]**2
    
    return powerDC

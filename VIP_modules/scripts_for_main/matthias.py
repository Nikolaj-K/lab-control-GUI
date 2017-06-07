# -*- coding: utf-8 -*-

import os
import time
import interface.session_events as se
import interface.measurement as im

################################################################################
def set_instrument_test(vip):
    sk = 'ZNB_1'

    settings = {'B_connect'      : 'TRY'
               ,'N_sweep_points' : '4001'
               }
    vip.set(sk, settings)

    se.bn_connect_to_lab(vip)

    vip.instruments[sk].get_info()

    R_bandwidth = float(vip.get('ZNB_1', 'R_bandwidth'))
    print "\nBandwidth of {0}: {1}".format(sk, R_bandwidth)

    print "/(set_instrument_test)"


################################################################################
def set_osci_test(vip):
    sk = 'RTE1054_1'

    settings = {'B_connect'      : 'TRY'
               #,'N_sweep_points' : '4001'
               }
    vip.set(sk, settings)

    se.bn_connect_to_lab(vip)

    vip.instruments[sk].get_info()

    data_x, data_y = vip.instruments[sk].get_data(1)

    print data_x[3:9]
    print data_y[3:9]

    print "/(set_instrument_test)"

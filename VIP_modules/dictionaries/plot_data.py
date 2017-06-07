import numpy as np

import dictionaries.menus as menus

################################################################################

default_data = {}
for k_data in menus.DATA_SET_KEYS:
    default_data[k_data] = {}
    for dim_key in menus.PLOT_DIM_KEYS:
        default_data[k_data][dim_key] = {'label_1' : "label_1", 'label_r' : "label_r"}
    default_data[k_data]['3d_data'].update({'label_2' : "label_2"})

########## 2d_data

y_axis = [0, 1, 3, 6, 10]
default_data['I_data']['2d_data'].update({'axis_1' : range(len(y_axis)), 'axis_r' : y_axis})        
y_axis = [2, 4, 8, 7, 9, 10, 8, 5, 1, 0]
default_data['Q_data']['2d_data'].update({'axis_1' : range(len(y_axis)), 'axis_r' : y_axis})  
y_axis = [0, 1, 3, 6, 10, 14, 17, 18, 17]
default_data['P__dBm']['2d_data'].update({'axis_1' : range(len(y_axis)), 'axis_r' : y_axis})          
y_axis = [0, 3, 6, 9, 9, 10, 8, 5, 1, 0, -1, -3, -4, -5, -5, -4, -1, 1, 2, 4]
default_data['phi___']['2d_data'].update({'axis_1' : range(len(y_axis)), 'axis_r' : y_axis})          
y_axis = [3, 3, 6, 9, 8, 7, 6, 4, 2, 1, 0, -1, -2, -4, -5, -3, 0, 2, 2, 2]
default_data['P__dB_']['2d_data'].update({'axis_1' : range(len(y_axis)), 'axis_r' : y_axis})         
y_axis = [3, 1, 6, 1, 8, 1, 6, 1, 2, 1, 6, -1, -2, -1, 5, -3, 2, 2, 1, 1]
default_data['phidiv']['2d_data'].update({'axis_1' : range(len(y_axis)), 'axis_r' : y_axis})        

########## 3d_data

RANGE = range(-5, 5)
x_axis, z_axis = RANGE, RANGE 

for k_data in menus.DATA_SET_KEYS:
    default_data[k_data]['3d_data'].update({'axis_1' : x_axis, 'axis_2' : z_axis})
          
X, Z = np.meshgrid(x_axis, z_axis)

Y = np.exp(-0.2*((X-2.4)**2 + 0.3*(Z-2)**2)) + 0.7 * np.exp(-(0.4*(X + 4)**2+0.1*(Z-3)**2)) + 0.2 * np.exp(-(0.3*(X-8)**2+0.2*(Z+6)**2))
default_data['I_data']['3d_data'].update({'axis_r' : Y}) 
                         
Y = 0.4 * np.exp(-(0.4*(X-2)**2 + 0.1*(Z-3)**2)) + 0.2 * np.exp(-(0.4*(X+1)**2 + 0.1*(Z+3)**2))
default_data['Q_data']['3d_data'].update({'axis_r' : Y}) 
                    
Y = 0.3 * np.exp(-(0.2*(X-2.4)**2 + 1.3*(Z+2)**2))
default_data['P__dBm']['3d_data'].update({'axis_r' : Y}) 
                                                                                
Y = 0.1 * np.exp(-(0.1*(X+4)**2 + 0.15*(Z-3)**2))
default_data['phi___']['3d_data'].update({'axis_r' : Y}) 
                                                                                
Y = 0.2 * np.exp(-(0.3*(X+3)**2 + 0.1*(Z-2.5)**2))
default_data['P__dB_']['3d_data'].update({'axis_r' : Y}) 
                                                                                
Y = 0.2 * np.exp(-(0.5*(X+1)**2 + 0.2*(Z-1.5)**2))
default_data['phidiv']['3d_data'].update({'axis_r' : Y}) 

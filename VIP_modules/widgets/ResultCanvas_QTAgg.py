import random
import numpy as np
import operator
from scipy import optimize

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg
from matplotlib.figure import Figure as MatplotlibFigure
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm as color_map
from matplotlib.ticker import LinearLocator, FormatStrFormatter

import interface.auxiliary_functions as auxi
import dictionaries.constants as cs

#################################################################################

class ResultsCanvas(FigureCanvasQTAgg):

    def __init__(self, canvas_ref, vip):
        self._Figure  = MatplotlibFigure(figsize = cs.FIG_SIZE, dpi = cs.DPI)#, tight_layout=True, frameon=True)
        super(ResultsCanvas, self).__init__(self._Figure)
        self.update_figure(canvas_ref, vip)

    def _from_options(self, canvas_ref, vip): 
        self.Axes.set_position(self._get_axes_position(vip))
        labels_x = self.Axes.xaxis.get_ticklabels()
        labels_y = self.Axes.yaxis.get_ticklabels()
        fontsize = vip.get('Options', 'R_axes_font_size')
        angle    = vip.get('Options', 'R_x_plot_label_rotation')
        for label in labels_x+labels_y:   
            label.set_fontsize(fontsize)
        if vip.get(canvas_ref, 'F_plot_function') == 'density':  
            for label in labels_x:
                label.set_rotation(angle)  

    def _get_axes_position(self, vip):
        session_keys = ['R_x_plot_position', 'R_y_plot_position', 'R_x_plot_size', 'R_y_plot_size']
        f = lambda k: float(vip.get('Options', k))
        return map(f, session_keys)

#################################################################################

class Canvas2dData(ResultsCanvas):

    def __init__(self, canvas_ref, vip):
        super(Canvas2dData, self).__init__(canvas_ref, vip)

    def update_figure(self, canvas_ref, vip):
        self._Figure.clear() 
        
        #from numpy.random import rand
        #x, y, c, s = rand(4, 100)
        #def onpick3(event):
        #    ind = event.ind
        #    print 'onpick3 scatter:', ind, np.take(x_axis, ind), np.take(y_axis, ind)
        #self._Figure.canvas.mpl_connect('pick_event', onpick3)

        try:
            data_set  = vip.get(canvas_ref, 'F_data_set')
            plot_data2D = vip.plot_data[data_set]['2d_data']

            ########## Axes                                                                    
            self.Axes = self._Figure.add_axes(cs.AXES_POSITION_INIT)
            x_axis = plot_data2D['axis_1']
            y_axis = plot_data2D['axis_r']
            self.Axes.plot(x_axis, y_axis, auxi.colour(cs.PLOT_COLOR_RANGE)) 
            #self.Axes.set_xlim([x_axis[0], x_axis[-1]])  
            self.Axes.set_xlim(sorted([x_axis[0], x_axis[-1]]))                 
            self._from_options(canvas_ref, vip) 
            self.Axes.set_xlabel(plot_data2D['label_1'])
            self.Axes.set_ylabel(plot_data2D['label_r'])  
            #self.Axes.hold(False)

            ########## Extrema
            #max_index, max_y = max(enumerate(y_axis), key=operator.itemgetter(1))
            #vip.maximal_x = x_axis[max_index]
            min_index, min_y = min(enumerate(y_axis), key=operator.itemgetter(1))
            vip.minimal_x = x_axis[min_index]
            print "* GLOBAL MINIMUM:\n{0}".format(vip.minimal_x)

            if canvas_ref in ['Plot_column_1']:
                ########## Savitzky Golay Filter
                ws = len(y_axis)/cs.SAVITZKY_GOLAY_FILTER_RANGE_DENOMINATOR
                ws = ws if (ws % 2 == 1) else (ws + 1)
                try:
                    y_axis_sg = auxi.savitzky_golay_filter(y_axis, window_size=ws, order=cs.SAVITZKY_GOLAY_FILTER_ORDER)
                    self.Axes.plot(x_axis, y_axis_sg, cs.FILTER_CURVE_STYLE, linewidth=cs.FILTER_LINEWIDTH) 
                except TypeError as exception:
                    print "! (update_figure) couldn't compute 'savitzky_golay_filter':"
                    print exception 
    
                ########## Fit
                try:
                    def lorenzian_fit(x, A, k, ke):
                        """Take min_x of this session and define a fit function"""
                        def h(ke_):
                            return (k / 2 - ke_)**2 + (x - vip.minimal_x)**2
                        r = A * h(ke) / h(0)
                        return auxi.to_dB(r)
                    parameters, covariance = optimize.curve_fit(lorenzian_fit, x_axis, y_axis_sg)
                    
                    LINE = 40 * "." + "\n"
                    print LINE
                    print "LORENZIAN FIT AT FILTER CUVE MINIMUM:\n"
                    print "* PARAMETERS:\n\n  [A, kappa, kappa_e]\n= {0}\n".format(parameters)
                    print "* PARAMETERS:\n\n  kappa_e / kappa\n= {0}\n"    .format(parameters[1] / parameters[0])
                    print "* COVARIANCE:\n\n  Matrix\n= {0}\n"             .format(covariance)
                    print "* MINIMUM:   \n\n  (x,y)\n= ({0}, {1})\n"       .format(x_axis[min_index], y_axis[min_index])
                    print LINE
                    
                    fit_function = lambda x: lorenzian_fit(x, *parameters)
                    y_axis_fit   = map(fit_function, x_axis)
                    self.Axes.plot(x_axis, y_axis_fit, cs.FITTING_CURVE_STYLE, linewidth=cs.FITTING_LINEWIDTH, linestyle=cs.FITTING_LINESTYLE)  
                except:
                    print "! (update_figure) couldn't fit to lorenzian_fit."
            else:
                pass
                 
            try:
                self.draw()
            except ValueError:
                message = "! (update_figure, ValueError) at vip.draw."
                vip.GUI_feedback(message)        
        except KeyError: 
            message = "! (update_figure) The specified dataset might not exist."
            vip.GUI_feedback(message)
            
#################################################################################

class Canvas3dData(ResultsCanvas):

    def __init__(self, canvas_ref, vip):
        super(Canvas3dData, self).__init__(canvas_ref, vip)

    def update_figure(self, canvas_ref, vip):
        self._Figure.clear() 
        
        try:
            data_set  = vip.get(canvas_ref, 'F_data_set')
            plot_data3D = vip.plot_data[data_set]['3d_data']

            ########## Axes                                         
            X, Y = np.meshgrid(plot_data3D['axis_1'], plot_data3D['axis_2'])
            Z    = np.array(plot_data3D['axis_r'])
            
            if vip.get(canvas_ref, 'F_plot_function') == 'density':  
                self.Axes = self._Figure.add_axes(cs.AXES_POSITION_INIT)
                self.Axes.pcolormesh(X, Y, Z, cmap = color_map.coolwarm)
            elif vip.get(canvas_ref, 'F_plot_function') == 'surface':
                self.Axes = Axes3D(self._Figure)
                surf = self.Axes.plot_surface(X, Y, Z, cmap = color_map.coolwarm, rstride = 1, cstride = 1, linewidth = 0.15, antialiased = False)
                self.Axes.zaxis.set_major_locator(LinearLocator(10))
                self.Axes.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))
                #self.Axes.set_zlim(-1.01, 1.01)     
                position_color_bar = [0.015, 0.17, 0.015, 0.75]
                Axes_color_bar = self._Figure.add_axes(position_color_bar)
                self._Figure.colorbar(surf, cax = Axes_color_bar)

            self._from_options(canvas_ref, vip)
            
            #self.Axes.hold(False)
            self.Axes.set_xlabel(plot_data3D['label_1'])
            self.Axes.set_ylabel(plot_data3D['label_2'])
            ########## / Axes   

            try:
                self.draw()
            except ValueError:
                message = "(update_figure, vip.draw, ValueError)"
                vip.GUI_feedback(message)    
        except KeyError:
            message = "The specified dataset might not exist"
            vip.GUI_feedback(message)
            
            

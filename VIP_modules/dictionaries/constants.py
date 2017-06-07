
################################################################################ NUMERICS
SAVITZKY_GOLAY_FILTER_ORDER             = 3
SAVITZKY_GOLAY_FILTER_RANGE_DENOMINATOR = 10

################################################################################ NUMERICAL CONSTANTS
MILLI = 10**(-3)

################################################################################ GUI SPECS
SESSION_DICT_INDICES = 10

################################################################################ WINDOW SIZES AND LABELS
MOVE_VIP       = (100 ,  20) ### (x-direction, negative y-direction)
MOVE_PLOT      = (2100, 30)
RESIZE_FEED    = (550 , 300)
MOVE_SCRIPTS   = (1200, 150)
MOVE_FEED      = (3200,  20)
MOVE_OPTIONS   = ( 140, 140)
MOVE_INFO      = ( 300,  60)
MOVE_NOTES     = ( 300,  50)

RESIZE_VIP     = (1200, 1000)
RESIZE_PLOT    = (1100, 1000)
RESIZE_SCRIPTS = ( 400,  600)
RESIZE_OPTIONS = ( 350,  400)
RESIZE_INFO    = ( 600,  800)
RESIZE_NOTES   = ( 800,  950)
RESIZE_BROWSE_DIALOG = (50, 70)

WINDOW_TITLE_VIP       = "Virtural Instrument Panel"
WINDOW_TITLE_TABS      = "Measurement tabs"
WINDOW_TITLE_PLOT      = "Additional plot columns"
WINDOW_TITLE_FEED      = "Feedback dialog"
WINDOW_TITLE_NOTES     = "Notes editor"
WINDOW_TITLE_OPTIONS   = "Options"
WINDOW_TITLE_INFO      = "Instrument settings dialog"
WINDOW_TITLE_INVISIBLE = "Invisible Widgets"

BLANK = " "
INSTRUMENT_INFO_LABEL = BLANK + "Instrument info and status" + BLANK

################################################################################ COLORS AND SYLE
FONTSIZE  = 12
FONT      = 'Helvecia'
FANCYFONT = 'OldEnglish'

FIG_SIZE           = (6, 6) ### Given in inches.
DPI                = 90
AXES_POSITION_INIT = [0.2, 0.2, 1, 1] ### ... nrows, ncols, plot number
# projection = aitoff, hammer, lambert, mollweide, polar, rectilinear

PLOT_COLOR_RANGE    = 160      ### Goes up to 265

FILTER_CURVE_STYLE  = "c-"
FILTER_LINEWIDTH    = 1.5

FITTING_CURVE_STYLE = "m"
FITTING_LINEWIDTH   = 0.8
FITTING_LINESTYLE   = 'dotted'
        #b: blue
        #g: green
        #r: red
        #c: cyan
        #m: magenta
        #y: yellow
        #k: black
        #w: white

COLOR_TRACE_1   = 'SkyBlue'    ### 'SteelBlue'
COLOR_TRACE_2   = 'SkyBlue'
COLOR_TRACE_3   = 'Thistle'    ### 'Plum'
COLOR_TRACE_4   = 'Thistle'
COLOR_DENSITY_1 = 'PeachPuff'  ### 'Moccasin'
COLOR_DENSITY_2 = 'PeachPuff'
COLOR_DENSITY_3 = 'PeachPuff'  ### 'LightGreen'    ### 'DarkCyan'  
COLOR_DENSITY_4 = 'PeachPuff'

########## CSS STYLESHEETS
STYLESHEET_PINK = "color: rgb(244, 164, 096);"
### RGB colors:
### http://www.rapidtables.com/web/color/brown-color.htm

STYLE_sweeps      = """QWidget{color : #000000;}}"""
STYLE_instruments = """QWidget{color : #0000b3;}}"""
STYLE_control     = """QWidget{color : #005d00;}}"""
STYLE_VIP         = """QWidget{color : #c70553;}
                        QProgressBar{
                                border           : 2px solid grey;
                                border-radius    : 4px;
                                text-align       : center;
                                background-color : #FFFFFF;
                                width            : 2.15px;
                                margin           : 20px;
                        }
                        QPushButton : pressed{
                                border-width     : 1px;
                                border-color     : 1e1e1e;
                                border-style     : solid;
                                border-radius    : 5;
                                padding          : 3px;
                                padding-left     : 5px;
                                padding-right    : 5px;
                                background-color : QLinearGradient( 
                                    x1   : 0, 
                                    y1   : 0, 
                                    x2   : 0.5, 
                                    y2   : 1.7, 
                                    stop : 0   #F8F8F8, 
                                    stop : 0.1 #F8F8F8, 
                                    stop : 0.5 66CCFF, 
                                    stop : 0.9 282828, 
                                    stop : 0   #F8F8F8
                                ); 
                          }
                      """
### HTML Color Picker:
### http://www.w3schools.com/cssref/css_colors.asp
### Related StackOverflow thread:
### http://stackoverflow.com/questions/22332106/python-qtgui-qprogressbar-color

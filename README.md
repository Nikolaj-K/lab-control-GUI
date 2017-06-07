# Virtual Instrument Panel
Authored by Nikolaj Kuntner

7. June 2017

![VIP_screenshot_nikolaj_170401](http://i.imgur.com/EewrmiC.jpg)
![banner_fingroup_webpage](http://i.imgur.com/iyG61IK.jpg)

<br />

This is the **Graphical User Interface & instrument driver Application
Programming Interface for central laboratory device operation** I wrote for
the
[quantum computing group ](https://quantumids.com/)
under Prof. Fink at
[IST Austria](https://en.wikipedia.org/wiki/Institute_of_Science_and_Technology_Austria).
These 15000 lines of Python are intended to be ran from an [IDE](https://en.wikipedia.org/wiki/Integrated_development_environment).
It's a
[Qt](https://en.wikipedia.org/wiki/Qt_(software))
[GUI](https://en.wikipedia.org/wiki/GUI)
for any collection of lab devices and works most straightforwardly with machines
that can communicate via
[VISA](https://en.wikipedia.org/wiki/Virtual_Instrument_Software_Architecture),
making use of
[NI](https://en.wikipedia.org/wiki/National_Instruments)
software. It also comes with an
[API](https://en.wikipedia.org/wiki/API)
that provides nice state control and the possibility to track operation settings.
The measurement module is tailored for superconducting QuBit measurement
routines and thus fairly idiosyncratic.

## Overview
```
VIP
├── (main.py)               <─── execute that file to start the VIP
├── README.md                  <─── this file
└── VIP_modules
    ├── (VIP_Qwidget.py)       <─── VIP class definition
    ├── widgets                <─── smaller class definitions
    ├── dictionaries           <─── contains settings (session.py, constants.py,...)
    ├── configurations
    ├── documentation
    ├── drivers
    ├── interface
    ├── scripts_for_gui
    ├── scripts_for_main
    └── external               <─── contains files not written by me (Fink group)
```
The primary external Python software package imported and used in the code is
[PyQt4](https://wiki.python.org/moin/PyQt4),
the Python binding to the
[Qt GUI software](https://en.wikipedia.org/wiki/Qt_(software)).
It is used in the *main.py* file, as well as the *interface* folders and
many of the PyQt4 widgets.
Note that unless you want to play with fonts and the Qt widgets, a large screen
will help.
(As a side note, the VIP Panel GUI must be opened in a Qt-Application that only
lets the terminal/editor come back once the VIP-GUI is closed.
A decorator that does exactly that is implemented as a wrapper function for the
main function.
It is found in *QtGui_decorator.py* the *scripts_for_main folder*.)

Another important package is the
[PyVisa](https://pyvisa.readthedocs.io/en/stable/)
package, which provides a Python
programming interface for the
["Virtual Instrument Software Architecture" (VISA)](https://en.wikipedia.org/wiki/Virtual_Instrument_Software_Architecture)
[Application Programming Interface (API)](https://en.wikipedia.org/wiki/Application_programming_interface),
by which many instruments communicate.
It is mostly used in the 'drivers' folder, defining Python classes for each
instrument type.
Other folders and file concern settings, infrastructure and routines.
A lot of settings for the VIP itself, e.g. window size & positions, fonts,
etc., are defined as constants in the *constants.py* file in the dictionary folder.
The folder *external*  is reserved for third party instrument drivers that suite
your needs.

We run the script from the file *main.py*. This is the file
associated with the VIP-GUI which makes use of the whole VIP software package.
Note that you may need to add a few file paths to your python config or do that
explicitly in main. They way the VIP package is uploaded here, it runs
straightforwardly with IDEs such as Canopy.

## API
The VIP is a GUI to control this settings dictionary, the ```vip._session```,
as well as to send commands to the instruments and receive and
plot data. The default settings as above are hardcoded in session.py in
'dictionaries'. It is relevant to understand all the "tabs" or "session keys"
(often abbreviated "tb" or "sk") and the "setting keys" (usually called "k")
The settings are saved in a "session dictionary" and has the form
```
{session_key_1 : {settings_key_1 : value_1
                 ,settings_key_2 : value_2
                 ...
                 }
,session_key_2 : {settings_key_1 : value_1
                 ...
                 }
...
}
```
For example, two signal generator sources in the lab have default values as
```python
{
...
,'SGS_33' : {'R_power_source'     : '0'
            ,'R_freq_source'      : '8'   ### A real number
            ,'F_unit_freq_source' : 'GHz'
            ,'B_output'           : 'OFF' ### A boolean value, 'ON' or 'OFF'
            ,'B_reference_osci'   : 'EXT'
            ,'B_connect'          : 'DONT'
            }
,'SGS_35' : {'R_power_source'     : '0'
            ,'R_freq_source'      : '8'
            ...
            }
...
}
```
In the widgets folder, the VIP class is defined as subclass of the
QWidget class from the QtPy4 package that allows coding GUIs. As you can see in
the code below, this file calls a ```main()``` function,
which in the line
```python
vip = VirtualInstrumentPanel()
```
creates a class instance
and thus launches the VIP.
This app is finally made accessible as a GUI via the show
method ```vip.show()```.
That one above is inherited from the QWidget class, not for some custom tools.
VIPinstance attributes and methods that are intended to be accessed
include ```.set```, ```.get```, ```.GUI_feedback```, ```.instruments```, ```.result```, ```.plot_data```, ...

One could for example set the power and frequency settings for
the ```SGS_34``` via
```python
settings = {'R_freq_source'  : "7.4"
           ,'R_power_source' : "-5"
           }
vip.set('SGS_34', settings)
```
or query the power setting via
```python
p = float(vip.get('SGS_34', 'R_power_source'))
print p
```

or query all settings for this instrument via
```python
print vip.get('SGS_34')
```

We can use the API to trigger all events that can be accessed through
the GUI, for example
```python
### writes state variables to connected instruments
import session_events as se
se.bn_connect_to_lab(vip)
se.bn_adopt_settings(vip)
```
which amounts to clicking the "Connect"- followed by the
"Adopt settings"-button in the GUI.

Finally, in any script, one may also use methods from the drivers for connected
instruments directly, for example
```python
### Set a new current source generator frequency
f = 7402.5
SG = vip.instruments['SGS_34']
SG.set_frequency(f, 'MHz')
```
Almost all such operations will print an information or confirmation to the
standard output.

<br />

# GUI 

The default GUI is a dynamic "Jack of all trades, master of none". It consists of a driver object that uses PyQt5 render a login, and then a control window. The window draws widgets based on the number of supervisors and PLCs using custom classes in the directory, which are defined in the PLC config files. 

## GUIDriver

### GUI Panels

The GUIDriver also starts the supervisorDriver on the supervisor device, which starts the whole scenario. The driver loads in the config files for each PLC, and then uses each defined "function" to render a control panel. These panels are rendered using the class file in the GUI folder, which name must match as specified in the PLC config file. These classes should have three methods in addition to the __init__ class to be compatible with GUI driver:

1) createFuncBox(self, number): This should generate the PyQt widget that will be added to the window. The number is for labelling, and is simply the number of these widgets that have been drawn.
2) setValues(self,data): This is used to set the values drawn on the display. It is passes a dict in the format {name:value} where name is a string, and value is an integer. 
3) getValues(self): This method should return a dict, the same format as in setValues, and should contain the values that the user can input to the GUI

For examples of the implementation of these methods see Turbine.py

### Modbus Client

The GUI Driver also handles the modbus protocols. For each function defined, it starts a thread that contains a handler that sets and gets Values every 0.1 seconds using the methods defined above, and then reads/writes to modbus as appropriate. 

## Turbine.py

This is an example of a class that can be used to generate custom UIs to be loaded into the default GUI handler. Refer above for the required methods to make this work. This class uses PyQt to generate a widget, and then has helper methods to mamage input/output

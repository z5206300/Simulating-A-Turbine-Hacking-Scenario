#!/usr/bin/env python3

import PyQt5.QtWidgets as Q
import PyQt5.QtCore as Qt
import TurbineLogin
import Turbine
import sys
import paramiko
import time
import multiprocessing
import configparser
import importlib
import itertools
from pymodbus.client.sync import ModbusTcpClient as ModbusClient

IP='111.220.27.216'
USER='pi'
PWD='gr0upn@m3'


# ---------------------------------------------------------------- #
# Defines the parameters that can be used by PyQt signal processes
# to send signals outside the main GUI loop. Set and get are
# universal, as these cannot be dynamically created
# ---------------------------------------------------------------- #
class HandlerSignals(Qt.QObject):
    setValues = Qt.pyqtSignal(dict)
    getValues = Qt.pyqtSignal()
    stop = Qt.pyqtSignal()

# ---------------------------------------------------------------- #
# Handles the back end modbus integration for the GUI app
# ---------------------------------------------------------------- #
class ModbusHandler(Qt.QThread):

    def __init__(self,plc,func):
        super(ModbusHandler, self).__init__()
        self.run= True

        #Import config/object lists
        self.plc = plc
        self.func = func

        #Create signal handler object
        self.signals = HandlerSignals()

        #Start the modbus local client
        self.startModbusClient()

    #Main signal handler loop
    def run(self):
        # ------------------------------------------------------------ #
        # Loops over each function, and the assosiated plc config
        # Loads the data from the function class, writes the update
        # to modbus. It then reads from the modbus, and sends the updated
        # data to the function object. Note that each modbus parameter
        # must be read or write. They cannot be both. Refer to
        # documentation for further information
        # ------------------------------------------------------------ #
        while self.run == True:
            data = self.func.getValues()
            self.writeModbus(data,self.plc)
            data = self.readModbus(self.plc)
            self.signals.setValues.emit(data)
            time.sleep(0.1)
    def stop(self):
        self.run = False
        #Zeros data for each param

        data = {}
        for param in self.plc.items('parameter addresses'):
            data.update({param[0]:0})

        #Writes 0s to Modbus to stop turbine
        self.writeModbus(data,self.plc)
    # ---------------------------------------------------------------- #
    # Takes a data dict {parameter name:value} and a plc_config object
    # and then writes the data in the dict to the plc referenced in the
    # config. The parameter name in data must match the parameter addresses
    # in the plc_config file
    # ---------------------------------------------------------------- #
    def writeModbus(self,data,config):

        #Loads the address, and converts from base 16 from config
        address = int(config.get('address','address'),16)
        #Loops through each line in data and writes to the modbus
        for param in data.items():
            #Retrieves the parameter destination register from config
            register = int(config.get('parameter addresses',param[0]))
            #Write function
            self.client.write_register(register,param[1],unit=address)

    # ---------------------------------------------------------------- #
    # Returns the data dict for the given plc_config item from the
    # modbus
    # ---------------------------------------------------------------- #
    def readModbus(self,config):

        #Loads the address, and converts from base 16 from config
        address = int(config.get('address','address'),16)
        #Setup a data dict
        data = {}

        for param in config.items('parameter addresses'):
            register = int(param[1]) #Loads individual register address
            registers = self.client.read_holding_registers(register,unit=address) #Read register
            data.update({param[0]:registers.registers[0]}) #Adds results to data
        return(data)

    #Starts the client connection to the Modbus server
    def startModbusClient(self):
        self.client = ModbusClient(IP,5020)
        self.client.connect()

# ------------------------------------------------------------------------------------------ #
# Main GUI class
# Builds a base window that the GUI classes for the different types of devices can be loaded
# onto
# ------------------------------------------------------------------------------------------ #
class GUI:

    #Stores the configs as values in the dict for each PLC connected to the system
    plc_config = {}
    #Stores the objects that are created to handle each function
    func_list = {}

    def __init__(self):
        #starts supervisor and loads PLC configs
        self.startSupervisor()

        #Loads the base window
        self.buildGUI()

        #Loads the threadpool and handlers to process user inputs
        self.threadpool = Qt.QThreadPool()
        handlers = []

        # --------------------------------------------------------------------------------------- #
        # This section created a ModbusHandler object for each function object. The handler is
        # responsible for the modbus transactions for each device, and the slot/signal managment
        # to communicate information in and out of the GUI thread (see PyQt slot/signal docs)
        # --------------------------------------------------------------------------------------- #
        for func, plc in zip(self.func_list.values(), self.plc_config.values()):
            handler = ModbusHandler(plc,func)                       #Handler object
            handler.signals.setValues.connect(func.setValues)       #Assign signals
            handler.signals.getValues.connect(func.getValues)
            handler.signals.stop.connect(handler.stop)
            handler.start()                                         #Start the thread
            handlers.append(handler)                                #Store the handlers in a list so we can kill them later


        #Start the GUI loop
        self.window.show()
        self.app.exec_()

        # ------------------------------------------------------------ #
        # Sets the handler and modbus parameters to 0, then kills the
        # handler threads
        # ------------------------------------------------------------ #

        #data dict to pass to modbus
        data = {}

        #iterates each plc config file and handler object
        for handler in handlers:

            handler.signals.stop.emit()
            handler.quit()
            handler.wait()

    # ---------------------------------------------------------------- #
    # Starts the supervisor via SSH, and pulls the PLC config files
    # ---------------------------------------------------------------- #
    def startSupervisor(self):
        #Setup SSH connection
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.connect(IP,username=USER,password=PWD)

        #Starts the supervisor
        ssh.exec_command('python3 IT-Project-GROUPNAME/prototype1/supervisory_computer/supervisorDriver.py')
        time.sleep(5)

        #Setup the config parser
        supervisor_config = configparser.RawConfigParser()

        #Loads the supervisor core config
        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cat IT-Project-GROUPNAME/prototype1/supervisory_computer/config.txt')
        supervisor_config.read_string(ssh_stdout.read().decode('ascii').strip('\n'))

        for plc in supervisor_config.items('plc list'):
            #Opens the config for the PLC that stored on the Supervisory Computer
            filename = plc[1] + "_config.txt"
            config_temp = configparser.RawConfigParser()
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command('cat IT-Project-GROUPNAME/prototype1/supervisory_computer/' + filename)
            config_temp.read_string(ssh_stdout.read().decode('ascii').strip('\n'))

            #Stores the config in the local dict plc_configs
            self.plc_config.update({plc[0]:config_temp})

        #Close the SSH connection
        ssh.close()

    def buildGUI(self):

        #Setup PyQt window
        self.app = Q.QApplication([])
        self.window = Q.QWidget()

        # ----------------------------------------------------------------- #
        # Creates the windows for each supervisory computer. At this stage,
        # is only set up for a single supervisor and is hard coded.
        # ----------------------------------------------------------------- #
        self.createSupervisorBox("1")

        #Adds supervisor to layout
        layout = Q.QGridLayout()
        layout.addWidget(self.supervisorBox)

        #Adds layout to the window
        self.window.setLayout(layout)

    def createSupervisorBox(self,number):

        #Creates sub-box for supervisory computer
        self.supervisorBox = Q.QGroupBox("Supervisory Computer " + number)

        #Sets up layout
        layout = Q.QHBoxLayout()

        # ------------------------------------------------------------------ #
        # Creates two turbine objects dynamically using plc_config.
        # Importlib import modules based on an argument, meaning that we
        # can use dynamic parameters to import classes, such as those defined
        # in a config object.
        # Creates the turbine objects dynamically, using the plc_config
        # dictionary. In the current scenario only two turbines are used,
        # however, this method allows for n number of turbine objects to be
        # created. This is done by reading-in the plc_config.txt file and
        # interpreting the number of devices and what kind they are. Python
        # objects for these devices are imported as python classes. The classes
        # for the devices must have the same name as the device in the config
        # file.
        # ------------------------------------------------------------------ #
        for key, value in self.plc_config.items():
            for func in value.items('plc function'):
                #Loads the classname specified for each function in plc_config
                class_name = func[1]

                #Imports the classfile defined
                func_class = getattr(importlib.import_module(class_name), class_name)
                #Creates a new instance of the classfile
                func_obj = func_class()
                #Generates a string as a key
                func_key = key + func[0]
                #adds the object to the func_list
                self.func_list.update({func_key:func_obj})

        # Adds created device windows to layout, this is done dynamically, using
        # the func_list above and allocating it a space using the createFuncBox method.
        count = 1
        for value in self.func_list.values():
            layout.addWidget(value.createFuncBox(str(count)))
            count = count + 1

        #Adds layout to window
        self.supervisorBox.setLayout(layout)

if __name__=='__main__':

    #Starts the login window
    login = Q.QApplication(sys.argv)
    window = TurbineLogin.Ui()
    login.exec_()
    print("test")
    #Starts the main GUI program
    gui = GUI()


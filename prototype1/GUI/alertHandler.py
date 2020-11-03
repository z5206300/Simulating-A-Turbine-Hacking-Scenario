#!/usr/bin/env python3
import sqlite3
import datetime
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

class HandlerAlertSignals(Qt.QObject):
    setValues = Qt.pyqtSignal(dict)
    getValues = Qt.pyqtSignal()
    stop = Qt.pyqtSignal()

    
Class AlertHandler(Qt.QObject):

    def __init__(self,plc,func):
        super(AlertHandler, self).__init__()
        self.run= True
        #Import config/object lists
        self.plc = plc
        #Create signal handler object
        self.signals = HandlerSignals()

        #Start the modbus local client
        self.startModbusClient()


    #Override deafult PyQt run method
    #@Qt.pyqtSlot()
    def run(self):
        print("running: ", self)
        # ------------------------------------------------------------ #
        # Loops over each function, and the assosiated plc config
        # It then reads from the modbus, and sends the updated
        # data to the database. 
        # ------------------------------------------------------------ #

        #only print PMW alert if its looped through two times consecutively (10 seconds) and both times have had alertPMW = true
        count = 0
        while self.run == True:

            if(count > 2)
                count = 0
            

            ErrorMsg = ""

            #reads/gets current settings of the turbines from modbus
            data = self.readModbus(self.plc)

            currRpm = int(data.get('rpm'))
            currPwm = float(data.get('pwm'))

            self.recordNewValues(self, currRpm, currPwm)
            
            #checks the database
            alertRPM, alertPWM = self.checkAlert(self)

            if(alertRPM):
                ErrorMsg += "There Turbines speed are unstable"

            if(alertPWM):
                count +=1
                if(count > 1):
                    ErrorMsg += "There pressure is unstable"
            
            #reset counter to 0 if alertPMW is false at any point
            if(not alertPWM):
                count = 0

            
            print(ErrorMsg)
            self.signals.setValues.emit(data)
            time.sleep(5)

    def stop(self):
        self.run = False
    


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













    #currRpm = int, currPmw = double
    def recordNewValues(self, currRpm, currPwm):

        if(not(isinstance(currRpm, float))):
            if(not(isinstance(currRpm, int))):
                    return
            
        if(not(isinstance(currPwm, float))):
            if(not(isinstance(currPwm, int))):
                return

                
        # You can create a new database by changing the name within the quotes
        conn = sqlite3.connect('logs.db')

        # The database will be saved in the location where your 'py' file is saved
        c = conn.cursor()

        # Insert records into current database logs
        c.execute("INSERT INTO LOGS (date, rpm, pmw)  values('"+str(datetime.datetime.now())+"', '"+str(currRpm)+"', '"+str(currPwm)+"')")
    
        conn.commit()



    def checkAlert(self):


        alertRPM = False
        alertPWM = False
        errorMsg = ""

        # You can create a new database by changing the name within the quotes
        conn = sqlite3.connect('logs.db')

        # The database will be saved in the location where your 'py' file is saved
        c = conn.cursor()

        # get records from current database logs
        c.execute("SELECT * FROM LOGS ORDER BY date DESC LIMIT 1")
        
        result = c.fetchall()
        
        resultRemoveFromList = result[0]
        
        resultTuple1 = resultRemoveFromList[0]
        resultTuple2 = resultRemoveFromList[1]
        resultTuple3 = resultRemoveFromList[2]
        
        if(int(resultTuple2) > 100):
            print("alert")
            errorMsg += "\nError: The turbine speed (rpm) setting is unstable"
            alertRPM = True

        
        if(float(resultTuple3) > 800):
            print("alert")
            errorMsg += "\nError: The pressure (pwm) setting is unstable"
            alertPWM = True


        conn.commit()

        return alertRPM, alertPWM, errorMsg

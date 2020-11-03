import tkinter as tk
#import RPi.GPIO as GPIO
from tkinter.simpledialog import askstring, askinteger
#from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import sqlite3

def main():

    #modbus connection
    #client = ModbusClient("localhost", port=5020)
    #UNIT = 0x1
    #client.connect()

    while True:
        Turbine1 = 1
        Turbine2 = 2

        #GPIO.setmode(GPIO.BCM)
        #GPIO.setup(Turbine1, GPIO.OUT)
        #GPIO.setup(Turbine2, GPIO.OUT)

        m = tk.Tk()
        m.title("Power Plant Control System")
        m.geometry("300x200")

        Turbine1_state = True
        Turbine2_state = True

        def Turbine1button():
            global Turbine1_state
            if Turbine1_state == True:
                #GPIO.output(Turbine1, Turbine1_state)
                Turbine1_state = False
                ON = tk.Label(m, text="Running")
                ON.grid(row=0, column=1)
            else:
                #GPIO.output(Turbine1, Turbine1_state)
                Turbine1_state = True
                ON = tk.Label(m, text="Powered Off")
                ON.grid(row=0, column=1)

        def Turbine2button():
            global Turbine2_state
            if Turbine2_state == True:
                #GPIO.output(Turbine2, Turbine2_state)
                Turbine2_state = False
                ON1 = tk.Label(m, text="Running")
                ON1.grid(row=1, column=1)
            else:
                #GPIO.output(Turbine2, Turbine2_state)
                Turbine2_state = True
                ON1 = tk.Label(m, text="Powered Off")
                ON1.grid(row=1, column=1)

        def SetTurbine1():
            speed = int((speed1 * 10) + 10)
            #client.write_register(1, speed, unit=UNIT)

        def SetTurbine2():
            speed = int((speed2 * 10) + 10)
            #client.write_register(2, speed, unit=UNIT)

        def TurbineRPMStatus():
            con = sqlite3.connect("./db/log.db")
            cur = con.cursor()
            cur.execute()
            return cur.fetchall()


        ONbutton = tk.Button(m, text="Turbine 1", bg="green", command=Turbine1button)
        ONbutton.grid(row=0, column=0)

        ON2button = tk.Button(m, text="Turbine 2", bg="green", command=Turbine2button)
        ON2button.grid(row=1, column=0)

        tk.Label(m, text="Turbine 1 Speed").grid(row=3)
        tk.Label(m, text="Turbine 2 Speed").grid(row=4)
        speed1 = tk.Entry(m)
        speed2 = tk.Entry(m)
        speed1.grid(row=3, column=1)
        speed2.grid(row=4, column=1)

        DisplayRPMInfo = tk.Button(m, text="Turbine Status", bg="blue", command=TurbineRPMStatus)

        Exitbutton = tk.Button(m, text="Exit", bg="red", command=m.destroy)
        Exitbutton.grid(row=10, column=0)

        m.mainloop()


main()





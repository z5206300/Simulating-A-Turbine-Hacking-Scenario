#!/usr/bin/env python3
import sqlite3
import datetime



def checkAlert():


    alertRPM = False
    alertPMW = False
    

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
        #print("alert")
        alertRPM = True

    
    if(float(resultTuple3) > 800):
        #print("alert")
        alertPMW = True


    conn.commit()

    return alertRPM, alertPMW


checkAlert()

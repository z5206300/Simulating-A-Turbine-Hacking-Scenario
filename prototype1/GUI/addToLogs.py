#!/usr/bin/env python3
import sqlite3
import datetime


#currRpm = int, currPmw = double
def recordNewValues(currRpm, currPmw):

    if(not(isinstance(currRpm, float))):
        if(not(isinstance(currRpm, int))):
                return
        
    if(not(isinstance(currPmw, float))):
        if(not(isinstance(currPmw, int))):
            return

            
    # You can create a new database by changing the name within the quotes
    conn = sqlite3.connect('logs.db')

    # The database will be saved in the location where your 'py' file is saved
    c = conn.cursor()

    # Insert records into current database logs
    c.execute("INSERT INTO LOGS (date, rpm, pmw)  values('"+str(datetime.datetime.now())+"', '"+str(currRpm)+"', '"+str(currPmw)+"')")
  
    conn.commit()

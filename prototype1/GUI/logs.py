#!/usr/bin/env python3
import sqlite3

# You can create a new database by changing the name within the quotes
conn = sqlite3.connect('logs.db')

# The database will be saved in the location where your 'py' file is saved
c = conn.cursor()

# Create table - CLIENTS
c.execute('''DROP TABLE IF EXISTS LOGS ''')
c.execute('''CREATE TABLE IF NOT EXISTS LOGS
             ([date] DATETIME PRIMARY KEY NOT NULL, [rpm] INT NOT NULL, [pmw] DOUBLE NOT NULL)''')

conn.commit()

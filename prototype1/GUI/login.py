#!/usr/bin/env python3
import sqlite3
import hashlib
import uuid

# You can create a new database by changing the name within the quotes
conn = sqlite3.connect('login.db')

# The database will be saved in the location where your 'py' file is saved
c = conn.cursor()

# Create table - CLIENTS
c.execute('''DROP TABLE IF EXISTS LOGIN ''')
c.execute('''CREATE TABLE IF NOT EXISTS LOGIN
             ([username] VARCHAR(50) PRIMARY KEY NOT NULL,[password] VARCHAR(50) NOT NULL)''')

c.execute('''INSERT INTO LOGIN (username, password)  values('pi', 'gr0upn@m3')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('root', '5f4dcc3b5aa765d61d8327deb882cf99')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('guest', '0cef1fb10f60529028a71f58e54ed07b')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('BenChapmen', 'e99a18c428cb38d5f260853678922e03')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('JohnLyons', 'd8578edf8458ce06fbc5bb76a58c5ca4')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('LaurenBiggs2', '900150983cd24fb0d6963f7d28e17f72')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('DavidHeath', 'e10adc3949ba59abbe56e057f20f883e')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('TracyNewman', '96e79218965eb72c92a549dd5a330112')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('LaurenBiggs1', '7c6a180b36896a0a8c02787eeafb0e4c')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('JerrySimon', '21232f297a57a5a743894a0e4a801fc3')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('JoelStacy', '8afa847f50a716e64932d995c8e7435a')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('JohnSmith1', 'd0763edaa9d9bd2a9516280e9044d885')''')
c.execute('''INSERT INTO LOGIN (username, password)  values('JohnSmith2', 'd56b699830e77ba53855679cb1d252da')''')

conn.commit()


# Note that the syntax to create new tables should only be used once in the code (unless you dropped the table/s at the end of the code).
# The [generated_id] column is used to set an auto-increment ID for each record
# When creating a new table, you can add both the field names as well as the field formats (e.g., Text)

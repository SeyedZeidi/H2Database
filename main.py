import sqlite3
import requests
import json

url_raspberry_pi = ''
con = sqlite3.connect('result.db')

cur = con.cursor()
r = requests.get(url_raspberry_pi)
js = json.loads(r.text)

# Create table
cur.execute('''CREATE TABLE IF NOT EXISTS results (TA1 real, TA2 real, TA1_2 real, TAP real, TB1 real, TB2 real, TB1_2 real, TBP real, TC1 real, TC2 real, TC1_2 real, TCP real, TD1 real, TD2 real, TD1_2 real, TDP real,
#               flow_1 real, flow_2 real, flow_3 real, flow_H2)''')

# Insert a row of data
cur.execute("INSERT INTO results VALUES (:TA1, :TA2, :TA1_2, :TAP, :TB1, :TB2, :TB1_2, :TBP, :TC1, :TC2, :TC1_2, :TCP, :TD1, :TD2, :TD1_2, :TDP, :flow_1, :flow_2, :flow_3, :flow_H2)", js)

# Save (commit) the changes
con.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
con.close()